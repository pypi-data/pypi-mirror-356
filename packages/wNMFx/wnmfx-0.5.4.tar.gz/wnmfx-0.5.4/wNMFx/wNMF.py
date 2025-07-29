"""Weighted Non-negative matrix factorization (NMF).

See "Weighted Nonnegative Matrix Factorization and Face Feature Extraction", Blondel, Ho and Dooren 2007.

NMF decomposes a matrix X into two matrices U,V with a shared internal dimension, representing a reduced-dimension
latent space.

X = UV

Columns of U are the basis vectors for this latent space, and columns of V contain the set of coeffcients required
to represent each sample in A as a linear combination of the basis vectors in U.

Weighted NMF:
    Blondel, Ho and Dooren introduce a weight matrix W that pre-weights the importance of each feature (row) in
    each sample (column) of the data matrix X, such that W ⊗ X = UV, where ⊗ is the Hadamard product of W and X.
    To determine U and V, given W and X, the authors develop a variation of the Multiplicative Update algorithm
    proposed by (Lee, 1999) and (Lee, 2001) to minimize the Kubllback-Leibler divergence, or,
    alternatively the Frobenius Norm. Variants of algorithms to solve the weighted-NMF problem by minimizing both
    KL-divergence and the Frobenius Norm are provided. See, reference.

"""

from functools import partial

import jax
import jax.numpy as jnp
import numpy as np


def coerce(matrix: np.ndarray, epsmin: float):
    """Coerce a matrix like object to a numpy.ndarray.

    Used for converting X, W to suitable matrices.
    Throws an error from numpy if the object provided is not coercible. No guarantees
    are provided on what the coerced result looks like. Zeroes are also replaced with
    epsmin to prevent potential underflow.

    Params:
    -------
    matrix : a numpy.ndarray or any object that can be coerced to an array by numpy.ndarray
        An object that is or can be coerced to a numpy.ndarray

    Returns:
    -------
    matrix : numpy.ndarray
        A coerced verision of the provided matrix
    """
    # test if object is a numpy.ndarray / ndarray
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)

    # Convert 0 entries to epsmin to prevent underflow
    matrix[matrix == 0] = epsmin
    return matrix


def coerce_bool(matrix: np.ndarray):
    """Coerce a matrix like object to a numpy.ndarray.

    Used for converting R to suitable matrices.
    Throws an error from numpy if the object provided is not coercible. No guarantees
    are provided on what the coerced result looks like.

    Params:
    -------
    matrix : a numpy.ndarray or any object that can be coerced to an array by numpy.ndarray
        An object that is or can be coerced to a numpy.ndarray

    Returns:
    -------
    matrix : numpy.ndarray
        A coerced verision of the provided matrix
    """
    # test if object is a numpy.ndarray / ndarray
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    return matrix


@partial(jax.jit, static_argnames=["axis"])
def calculate_reconstruction_error_frobenius(
    X: np.ndarray,
    U: np.ndarray,
    V: np.ndarray,
    W: np.ndarray,
    epsmin: float,
    axis=None,
):
    """Calculate the reconstruction error of U, V to X, given W.

    Params:
    ------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized / compared to

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    Returns:
    ------
    err: the estimated error using the selected loss function
    """
    # Replace zeroes with epsmin to prevent divide by zero / log(0) errors
    U = jnp.where(U == 0.0, epsmin, U)
    V = jnp.where(V == 0.0, epsmin, V)

    # select loss function and calculate error
    rec = X - U @ V
    return 0.5 * jnp.sum(W * rec * rec, axis=axis)


@partial(jax.jit, static_argnames=["axis"])
def calculate_reconstruction_error_kullback_leibler(
    X: np.ndarray,
    U: np.ndarray,
    V: np.ndarray,
    W: np.ndarray,
    epsmin: float,
    axis=None,
):
    """Calculate the reconstruction error of U, V to X, given W.

    Params:
    ------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized / compared to

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    Returns:
    ------
    err: the estimated error using the selected loss function
    """
    # Replace zeroes with epsmin to prevent divide by zero / log(0) errors
    U = jnp.where(U == 0.0, epsmin, U)
    V = jnp.where(V == 0.0, epsmin, V)

    # select loss function and calculate error
    rec = U @ V
    return jnp.sum(W * (X * jnp.log(X / rec) - X + rec), axis=axis)


@jax.jit
def update_uv_batch_frobenius(A, U, V, W, R, epsmin):
    """Perform 10 weighted NMF iterations for a Frobenius metric.

    Params:
    ------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized / compared to

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    R : numpy.ndarray, bool (n_components, n_samples)
        Activity matrix true if component is active for a sample

    epsmin: float
        Smallest non-zero float value.

    Returns:
    ------
    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix
    """
    if R is not None:
        V = jnp.where(R, V, 0)

    WA = W * A

    # Compute row-wise reconstruction error
    def step_fn(carry, _):
        U, V = carry

        # Update V
        V_new = V * ((U.T @ WA) / (U.T @ (W * (U @ V))))

        # Update U
        U_new = U * ((WA @ V_new.T) / ((W * (U @ V_new)) @ V_new.T))
        return (U_new, V_new), None

    # Run 10 iterations of updates
    (U_out, V_out), _ = jax.lax.scan(step_fn, (U, V), None, length=10)

    if R is not None:
        V_out = jnp.where(R, V_out, 0)

    # Ensure strictly positive U, V to avoid division by zero
    U_out = jnp.where(U_out == 0.0, epsmin, U_out)
    V_out = jnp.where(V_out == 0.0, epsmin, V_out)

    norms = U_out.max(axis=0)
    assert norms.shape == (U_out.shape[1],)

    return U_out / norms.reshape((1, -1)), V_out * norms.reshape((-1, 1))


@jax.jit
def update_uv_batch_kullback_leibler(A, U, V, W, R, epsmin):
    """Perform 10 weighted NMF iterations for a euclidean metric.

    Params:
    ------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized / compared to

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    R : numpy.ndarray, bool (n_components, n_samples)
        Activity matrix true if component is active for a sample

    epsmin: float
        Smallest non-zero float value.

    Returns:
    ------
    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix
    """
    if R is not None:
        V = jnp.where(R, V, 0)

    WA = W * A

    def step_fn(carry, _):
        U, V = carry

        # Update V
        V_new = V * ((U.T @ WA) / (U.T @ (W * (U @ V))))

        # Update U
        U_new = U * ((WA @ V_new.T) / ((W * (U @ V_new)) @ V_new.T))

        return (U_new, V_new), None

    # Run 10 iterations of updates
    (U_out, V_out), _ = jax.lax.scan(step_fn, (U, V), None, length=10)

    if R is not None:
        V_out = jnp.where(R, V_out, 0)

    # Ensure strictly positive U, V to avoid division by zero
    U_out = jnp.where(U_out == 0.0, epsmin, U_out)
    V_out = jnp.where(V_out == 0.0, epsmin, V_out)

    norms = U_out.max(axis=0)
    assert norms.shape == (U_out.shape[1],)

    return U_out / norms.reshape((1, -1)), V_out * norms.reshape((-1, 1))


@jax.jit
def update_v_batch_frobenius(A, U, V, W, R, epsmin):
    """Perform 10 weighted NMF iterations for a Frobenius metric.

    Only V is updated.

    Params:
    ------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized / compared to

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    R : numpy.ndarray, bool (n_components, n_samples)
        Activity matrix true if component is active for a sample

    epsmin: float
        Smallest non-zero float value.

    Returns:
    ------
    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix
    """
    if R is not None:
        V = jnp.where(R, V, 0)

    nom = U.T @ (W * A)

    # Compute row-wise reconstruction error
    def step_fn(V, _):
        V_new = V * (nom / (U.T @ (W * (U @ V))))

        if R is not None:
            V_new = jnp.where(R, V_new, 0)

        return (V_new), None

    # Run 10 iterations of updates
    V_out, _ = jax.lax.scan(step_fn, V, None, length=10)

    # Ensure strictly positive U, V to avoid division by zero
    V_out = jnp.where(V_out == 0.0, epsmin, V_out)

    return U, V_out


@jax.jit
def update_v_batch_kullback_leibler(A, U, V, W, R, epsmin):
    """Perform 10 weighted NMF iterations for a euclidean metric.

    Only V is updated.

    Params:
    ------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized / compared to

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    epsmin: float
        Smallest non-zero float value.

    Returns:
    ------
    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix
    """
    if R is not None:
        V = jnp.where(R, V, 0)

    nom = U.T @ (W * A)

    def step_fn(V, _):
        V_new = V * (nom / (U.T @ (W * (U @ V))))

        if R is not None:
            V_new = jnp.where(R, V_new, 0)

        return V_new, None

    # Run 10 iterations of updates
    V_out, _ = jax.lax.scan(step_fn, V, None, length=10)
    V_out = jnp.where(V_out == 0.0, epsmin, V_out)
    return U, V_out


def iterate_UV(
    A: np.ndarray, U: np.ndarray, V: np.ndarray, W: np.ndarray,
    R,
    epsmin: float, max_iter: int, tol: float,
    verbose: int, track_error: bool,
    calculate_reconstruction_error_func,
    update_uv_batch_func
):
    """Minimize the objective iteratively.

    Params:
    -------
    A : numpy.ndarray, values > 0, (n_features, n_samples)
        Data matrix to be factorized, referred to as X in the main code body, referred to as A here to make it easier to
        read the update steps because the authors Blondel, Ho, Ngoc-Diep and Dooren use A.

    U : numpy.ndarray, values > 0, (n_features,n_components)
        U matrix, randomly initialized entries.

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        V matrix, randomly initialized entries.

    W : numpy.ndarray, values > 0 (n_features, n_samples)
        Weight matrix, weighting importance of each feature in each sample, for all samples in X

    R : numpy.ndarray, bool (n_components, n_samples)
        Activity matrix true if component is active for a sample


    Returns:
    ------
    U : numpy.ndarray, values > 0, (n_features,n_components)
        Optimized version of the U-matrix

    V : numpy.ndarray, values > 0 (n_components, n_samples)
        Optimized version of the V-matrix

    i : int
        The iteration at which the minimization procedure terminated

    err : float
        The final error between the reconstruction UV and the actual values of W ⊗ X

    err_stored : numpy.ndarray
        A numpy vector containing the estimated reconstruction error at each minimization step
        if self.track_error is True, otherwise an empty array of zeroes.

    """
    err_stored = np.zeros(max_iter)
    prev_err = None
    if tol > 0:
        init_err = calculate_reconstruction_error_func(
            A, U, V, W, epsmin=epsmin
        )
    # Begin iterations until max_iter
    for i in range(0, int(np.ceil(max_iter / 10))):
        if track_error or tol > 0:
            curr_err = calculate_reconstruction_error_func(
                A, U, V, W, epsmin=epsmin
            )
            if verbose > 1:
                print(f"|--- iteration {i * 10}: err={curr_err:.2e}")
            if track_error:
                err_stored[i * 10:] = curr_err
            if tol > 0 and prev_err is not None and (prev_err - curr_err) / init_err < tol:
                print(f'|--- Convergence reached at iteration {i}')
                break
            del prev_err
            prev_err = curr_err
        else:
            if verbose > 1:
                print(f"|--- iteration {i * 10}")

        U, V = update_uv_batch_func(A, U, V, W, R=R, epsmin=epsmin)

    # Calculate final reconstruction error
    err = calculate_reconstruction_error_func(A, U, V, W, epsmin=epsmin)
    return U, V, i, err, err_stored


class wNMF:
    """Weighted Non-negative Matrix Factorization.

    Methods
    -------
    A set of methods that reflect the SKlearn model API (fit, fit_transform) are implemented.

    fit(X, W):
        description: Fits an NMF model for the data X, and the weight matrix W
        requires: X, W
        returns: self - the wNMF object with access to all the return variables listed above

    fit_transform(X, W):
        description: Fits an NMF model for the data X, weight matrix W, and returns the coefficient matrix V.
        requires: X, W
        returns: self.coefficients_  - specifically the best version of V (lowest self.err) identified in n_run's

    transform(X, W):
        description: Given a fitted NMF model, determines the coefficient matrix V.
        requires: X, W
        returns: self.coefficients_  - specifically the best version of V (lowest self.err)

    Examples
    --------
    >>> import numpy as np
    >>> X = np.array([[1,1], [2, 1], [3, 1.2], [4, 1], [5, 0.8], [6, 1]])
    >>> W = np.array([0.8,0.4],[0.1,0.1],[1,1],[0.7,0.3],[0.9,1],[0.01,0.04])
    >>> from weighted-nmf import wNMF
    >>> model = wNMF(n_components=3).fit(X,W)
    >>> V = model.V
    >>> V = model.coefficients_
    >>> U = model.U
    >>> U = model.components_
    >>> iterations_to_convergence = model.n_iters_
    >>> final_error = model.reconst_err_
    >>> # Accessing all matrices in n_run runs
    >>> V_all = model.V_all
    >>> V_all = model.coefficients_all_
    >>> U_all = model.U_all
    >>> U_all = model.components_all_

    References
    ----------
    Blondel, Vincent & Ho, Ngoc-Diep & Van Dooren, Paul. (2007).
    Weighted Nonnegative Matrix Factorization and Face Feature Extraction.
    Image and Vision Computing - IVC.

    Params
    ------

    n_components : int
        The rank of the decomposition of X, alternatively the reduced dimension of the factorization.

    init : str --> ("random" , None) default "random"
        The initialization strategy for matrices U and V. Defaults to "random" if no value is provided

    beta_loss : string --> ("frobenius", "kullback-leibler") default "frobenius"
        The error to be minimized between W ⊗ X, and UV, using the approrite multiplicative update variant.

    max_iter : int
        The maximum number of minimization iterations to perform before stopping.

    tol : float, default 1e-4
        If the relative error is found to change less than this amount after 20 iterations, or alternativley increase
        then minimization is completed.

    random_state : int default 12345
        Specifies a seed value to initilaize the numpy random number generator. Defaults to 12345

    rescale : bool, default False
        Controls whether to normalize the resulting U matrix columns such that each basis vector can be interpreted
        as a categorical probability distribution over the features in X. Useful for Signature Extraction, but invalidates
        the coefficients in V.

    track_error : bool, default False
        Controls whether to track the error of each wNMF fitting run, and store the result as a vector of length max_iter.
        One vector is generated per run and tracks the performace of that fitting run over time. By default this is false
        as it can slow down the overall fitting, and is primarily useful for diagnostics

    verbose : integer --> (0, 1, 2) default 1
        The level of verbosity. If 1 is provided, reports n_features, n_samples, and n_components, as well as the current
        error every 100 iterations. verbose=2 gives output at each iteration.

    n_run : int
        The number of times to repeat the wNMF fitting process.
        Each attempt utilizes a unique random initialization.
        The best solution is then selected.
    """

    def __init__(
        self,
        n_components: int,
        init: str = "random",
        beta_loss: str = "frobenius",
        max_iter: int = 1000,
        tol: float = 1e-4,
        random_state: int = 12345,
        rescale: bool = False,
        track_error: bool = False,
        verbose: int = 1,
        n_run: int = 1,
    ):
        # init variables
        self.n_components = n_components
        self.init = init
        self.beta_loss = beta_loss
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.rescale = rescale
        self.track_error = track_error
        self.verbose = verbose

        # Return Variables
        self.X = None

        # Components / U
        self.components_ = None
        self.U = None
        self.components_all_ = tuple()
        self.U_all = tuple()

        # coefficients / V
        self.coefficients_ = None
        self.V = None
        self.coefficients_all_ = tuple()
        self.V_all = tuple()

        # Reconstruction error / reconst_err_
        self.reconstruction_err_ = None
        self.err = None
        self.reconstruction_err_all_ = tuple()
        self.err_all = tuple()

        self.err_stored = list()

        # n_iters
        self.n_run = n_run
        self.n_iter_ = None
        self.n_iter_all_ = tuple()
        self.n_iter = None
        self.n_iter_all = tuple()

        # run check
        self._check_init()

    def __repr__(self):
        """Get string representation."""
        return f"wNMF model with {self.n_components} components"

    def _check_init(self):
        """Check the parameters supplied during initialization.

        Parameters checked : expected values
            n_components  : int, greater than 0
                    init  : string, 'random' | no other initialization strategies allowed at present
                beta_loss : string, ('kullback-leibler','frobenius')
                 max_iter : int, greater than 0
                      tol : float, greater than 0
             random_state : int greater than or equal to zero
                  rescale : boolean
              track_error : boolean
                  verbose : int, (0, 1)

        """
        # check n_components is int > 0
        if not isinstance(self.n_components, int) or self.n_components <= 0:
            raise ValueError(
                f"Number of components must be a positive integer greater than zero; got '{self.n_components}', of type {type(self.n_components)}"
            )

        # check init is random
        if self.init not in ("random", "PCA", "logAR1", "sample"):
            raise ValueError(
                f"Only random, PCA, logAR1 initialization is supported; got '{self.init}' of type {type(self.init)}"
            )

        # check beta_loss is frobenius or kullback-leiblier
        if self.beta_loss not in ["kullback-leibler", "frobenius"]:
            raise ValueError(
                f"Selected loss must be either 'frobenius' or 'kullback-leibler'; got '{self.beta_loss}'"
            )

        # check max_iter is int > 0
        if not isinstance(self.max_iter, int) or self.max_iter <= 0:
            raise ValueError(
                f"Number of iterations must be a positive integer greater than zero; got '{self.max_iter}', of type {type(self.max_iter)}"
            )

        # check tol is numeric > 0
        if not isinstance(self.tol, float) or self.tol <= 0:
            raise ValueError(
                f"Error convergence criteria must be a positive float greater than zero; got '{self.tol}', of type {type(self.tol)}"
            )

        # check random_state is int > 0
        if not isinstance(self.random_state, int) or self.random_state < 0:
            raise ValueError(
                f"Random state seed must be a positive integer, or zero; got '{self.random_state}', of type {type(self.random_state)}"
            )

        # check rescale is boolean
        if not isinstance(self.rescale, bool):
            raise ValueError(
                f"rescale must be a boolean; got '{self.rescale}', of type {type(self.rescale)}"
            )

        # check track_error is boolean
        if not isinstance(self.track_error, bool):
            raise ValueError(
                f"rescale must be a boolean; got '{self.track_error}', of type {type(self.track_error)}"
            )

        # check verbose is int
        if self.verbose not in (0, 1, 2):
            raise ValueError(
                f"Verbosity is specified with an it, 0 or 1 or 2; got '{self.verbose}', of type {type(self.verbose)}"
            )

    def fit(self, X: np.ndarray, W: np.ndarray, R: np.ndarray = None):
        """Fit a wNMF model.

        Fitting is a modified
        multiplicative update algorithm (see reference), and is repeated n_run times. It is recommended to repeat
        the fitting procedure multiple times (at least 100) and take the best solution (with the lowest error), or
        alternatively to cluster multiple runs together.

        The algorithm is roughly as follows:
        1) Initialize matrices U (n_features,n_components) and V(n_components,n_samples) with random entries
            scaled approximately to the mean of X divded by n_components
        2) For each iteration, successively update U, then V using the aformentioned multiplicative update steps
        3) Terminate the iterations of the number exceeds max_iter, or if error does not change within tol
        4) Repeat 1-3 n_run times and select the best run, but store all runs.

        Attributes
        ----------
        U : numpy.ndarray, shape (n_features, n_components)
            The basis matrix for the reduced dimension latent space. Columns of U are basis vectors that can be
            added with different weights to yield a sample from X (columns).

        V : numpy.ndarray, shape (n_components, n_samples)
            The coefficient matrix for the reduced dimension latent space. Columns of V are the reduced representation of
            each sample in X, decomposed into a linear combination of the basis vectors in U. Samples in X can be 'reconstructed'
            by multiplying a column of U by V.

        reconstruction_error : float
            The reconstruction error between X, and W ⊗ UV, using the approriate error function specified in beta_loss

        n_iter : int
            The number of iterations at which the minimization terminated, maximal value is max_iter.


        Scikit-learn-like API
        ---------------------
        This information can be accessed from the following variables, to mimic the SKlearn API

            U : self.components_
            |   The matrix U from the best run, with dimensions (n_features, n_components)
            |
            | : self.components_all_
            |    A tuple of length n_runs, with each entry containing a matrix U from a single run.


            V : self.coefficients_
            |    The matrix V from the best  run, with dimensions (n_components, n_samples)
            |
            | : self.coefficients_all_
            |    A tuple of length n_runs, with each entry containing a matrix V from a single run.

            reconstruction_error : self.reconstruction_err_
                            |       The reconstruction error from the best run, a float.
                            |
                            |    : self.reconstruction_err_all_
                            |         A tuple of length n_runs, with each entry containing a the reconstruction error from a single run

            n_iter : self.n_iter_
               |      The number of iterations at which the minimization terminated for the best fitting run
               |
               |   : self.n_iter_all_
               |      A tuple of length n_runs, with each entry containing the number of iterations at which minimization terminated for a single run


        But can also be accessed more directly using what you would expect the variables to be named

            U : self.U
            |   The matrix U from the best run, with dimensions (n_features, n_components)
            |
            | : self.U_all
            |    A tuple of length n_runs, with each entry containing a matrix U from a single run.


            V : self.V
            |    The matrix V from the best  run, with dimensions (n_features, n_components)
            |
            | : self.V_all
            |    A tuple of length n_runs, with each entry containing a matrix V from a single run.

            reconstruction_error : self.err
                            |       The reconstruction error from the best run, a float.
                            |
                            |    : self.err_all
                            |         A tuple of length n_runs, with each entry containing a the reconstruction error from a single run

            n_iter : self.n_iter
               |      The number of iterations at which the minimization terminated for the best fitting run
               |
               |   : self.n_iter_all
               |      A tuple of length n_runs, with each entry containing the number of iterations at which minimization terminated for a single run


        SKLearn response API variables:
            self.components_,
            self.coefficients_,
            self.n_iters_,
            self.reconst_err_

        Normal variables:
            self.U
            self.V
            self.n_iters
            self.err

        And lists containing all values for all runs
            self.components_all_  / self.U_all
            self.coefficients_all_ / self.V_all
            self.n_iters_all_     / self.n_iters_all
            self.reconst_err_all_ / self.err_all

        And the error tracker, if enabled
            self.error_tracker


        Params
        ------
        X : numpy.ndarray or coercible array-like object
            A data matrix to be factorized, with dimensions (n_samples, n_features).

        W : numpy.ndarray or coercible array-like object
            A weight matrix of same dimension as X, which weights each entry in X. Generally expected
            to be values ranging from 0 to 1, but can contain any non-negative entries.
            If you have measurement errors, set W to the inverse variance.

        R : None or numpy.ndarray or coercible array-like object
            A boolean activity matrix of dimension (n_samples, n_components),
            which is true if a component is allowed to be active for the sample,
            and false if a component is disallowed.
            Intended for semi-supervised learning with sample class information.

        Returns
        -------
        self: object
            fit object, with added variables
        """
        # Set the minimal value (that masks 0's) to be the smallest
        # step size for the data-type in matrix X.
        self.epsmin = np.finfo(type(X[0, 0])).eps

        # Try to coerce X and W to numpy arrays
        X = coerce(X, self.epsmin).T
        W = coerce(W, self.epsmin).T
        R = None if R is None else coerce_bool(R).T

        # Check X and W are suitable for NMF
        self._check_x_w(X, W, R)

        # If passes, initialize random number generator using random_state
        rng = self.init_random_generator()

        # Extract relevant information from X
        n_features, n_samples = X.shape
        mean = np.mean(X)

        # Initialize result storage
        result = list()

        # Begin Runs...
        for r in range(0, self.n_run):
            if self.verbose >= 1:
                print(f"Beginning Run {r + 1}...")

            # Generate random initializatoins of U,V using random number generator
            if self.verbose >= 1:
                print("|--- Initializing U,V")
            U, V = self.initialize_u_v(rng, n_features, n_samples, mean, X)

            # Factorize X into U,V given W
            if self.verbose >= 1:
                print("|--- Running wNMF")

            if self.beta_loss == "frobenius":
                calculate_reconstruction_error_func = calculate_reconstruction_error_frobenius
                update_uv_batch_func = update_uv_batch_frobenius
            elif self.beta_loss == "kullback-leibler":
                calculate_reconstruction_error_func = calculate_reconstruction_error_kullback_leibler
                update_uv_batch_func = update_uv_batch_kullback_leibler

            factorized = iterate_UV(
                X, U, V, W, R=R,
                epsmin=self.epsmin, max_iter=self.max_iter,
                tol=self.tol, verbose=self.verbose, track_error=self.track_error,
                calculate_reconstruction_error_func=calculate_reconstruction_error_func,
                update_uv_batch_func=update_uv_batch_func,
            )

            # Rescale the columns of U (basis vectors) if needed
            if self.rescale:
                if self.verbose >= 1:
                    print("|--- Rescaling U basis vectors")

                factorized[0] = factorized[0] / jnp.sum(factorized[0], axis=0)

            # append the result and store it
            result.append(factorized)

            if self.verbose >= 1:
                print("|--- Completed")

        # transform the result from a list of tuples to a set of lists, each with multiple individual entries
        result = list(zip(*result))

        # Implementing the SKLearn model response API
        self.U_all = result[0]
        self.V_all = result[1]
        self.n_iter_all = result[2]
        self.err_all = result[3]

        # if tracking errors, set variable to store tracked errors
        if self.track_error:
            self.error_tracker = result[4]

        # setting up lists
        self.components_all_ = self.U_all
        self.coefficients_all_ = self.V_all
        self.n_iter_all_ = self.n_iter_all
        self.reconstruction_err_all_ = self.err_all

        # finding best result
        best_result = np.argmin(self.err_all)

        # Index out the best result, and set variables
        self.U = self.U_all[best_result]
        self.components_ = self.U

        self.V = self.V_all[best_result]
        self.coefficients_ = self.V

        self.n_iter = self.n_iter_all[best_result]
        self.n_iter_ = self.n_iter

        self.err = self.err_all[best_result]
        self.reconstruction_err_ = self.err

        # return entire wNMF object
        return self

    def transform(self, X: np.ndarray, W: np.ndarray, R: np.ndarray = None):
        """Transform with a fitted wNMF model.

        Same as fit(), but only update V.

        Params
        ------
        X : numpy.ndarray or coercible array-like object
            A data matrix to be factorized, with dimensions (n_samples, n_features).

        W : numpy.ndarray or coercible array-like object
            A weight matrix of same dimension as X, which weights each entry in X. Generally expected
            to be values ranging from 0 to 1, but can contain any non-negative entries.
            If you have measurement errors, set W to the inverse variance.

        R : None or numpy.ndarray or coercible array-like object
            A boolean activity matrix of dimension (n_samples, n_components),
            which is true if a component is allowed to be active for the sample,
            and false if a component is disallowed.
            Intended for semi-supervised learning with sample class information.

        Returns
        -------
        V: array
            non-negative coefficients, of shape (n_samples, n_components)
        """
        # Set the minimal value (that masks 0's) to be the smallest
        # step size for the data-type in matrix X.
        self.epsmin = np.finfo(type(X[0, 0])).eps

        # Try to coerce X and W to numpy arrays
        X = coerce(X, self.epsmin).T
        W = coerce(W, self.epsmin).T
        R = None if R is None else coerce_bool(R).T

        # Check X and W are suitable for NMF
        self._check_x_w(X, W, R)

        # If passes, initialize random number generator using random_state
        rng = self.init_random_generator()

        # Extract relevant information from X
        n_features, n_samples = X.shape
        mean = np.mean(X)
        U = self.U

        if self.verbose >= 1:
            print("Beginning transform...")

        # Generate random initializatoins of U,V using random number generator
        if self.verbose >= 1:
            print("|--- Initializing V")
        V = self.initialize_v(rng, n_features, n_samples, mean)

        # Factorize X into U,V given W
        if self.verbose >= 1:
            print("|--- Running wNMF")

        if self.beta_loss == "frobenius":
            calculate_reconstruction_error_func = calculate_reconstruction_error_frobenius
            update_uv_batch_func = update_v_batch_frobenius
        elif self.beta_loss == "kullback-leibler":
            calculate_reconstruction_error_func = calculate_reconstruction_error_kullback_leibler
            update_uv_batch_func = update_v_batch_kullback_leibler

        factorized = iterate_UV(
            X, U, V, W, R=R,
            epsmin=self.epsmin, max_iter=self.max_iter,
            tol=self.tol, verbose=self.verbose, track_error=self.track_error,
            calculate_reconstruction_error_func=calculate_reconstruction_error_func,
            update_uv_batch_func=update_uv_batch_func,
        )

        if self.verbose >= 1:
            print("|--- Completed")

        # factorized[0] is U, which has not changed
        self.coefficients_ = self.V = factorized[1]
        self.n_iter = factorized[2]
        self.err = factorized[3]
        return self.coefficients_.T

    def fit_transform(self, X: np.ndarray, W: np.ndarray):
        """Fit and transform data.

        Implements the fit_transform functionality from the SKlearn model API. Fits an NMF model to the
        data matrix X, and weight matrix W. Determines the best solution U,V over n_run's. The data-matrix
        is then "transformed" into its latent space coefficients given by the matrix V, or coefficients_.

        Params:
        ------
        X : numpy.ndarray or coercible array-like object
            A data matrix to be factorized, with dimensions (n_features, n_samples).

        W : numpy.ndarray or coercible array-like object
            A weight matrix of same dimension as X, which weights each entry in X. Generally expected
            to be values ranging from 0 to 1, but can contain any non-negative entries.

        Returns:
        ------
        f.coefficients : numpy.ndarray
            The best fit matrix V, or coefficients_ in SKlearn API language
        """
        f = self.fit(X, W)

        return f.coefficients_

    def _check_x_w(self, X: np.ndarray, W: np.ndarray, R=None):
        """Check whether supplied X and W are suitable for NMF.

           Conditions checked : expected values
            X.shape, W.shape  : shapes / dimensions should be equal
                entries in X  : greater than or equal to 0, no NaNs
                entries in W  : greater than or equal to 0, no NaNs
        X.shape, n_components : n_components < n_samples in X
        """
        # check X and W are the same shape
        if X.shape != W.shape:
            raise ValueError("Dimensions of X and weight matrix W must be the same")

        # check if entries of X and W are greater than 0
        if not np.all(X >= 0):
            raise ValueError("Entries of X must be positive or zero")

        if not np.all(W >= 0):
            raise ValueError("Entries of W must be positive or zero")

        # Check for Nans / and halt if there are any
        if np.any(np.isnan(X)):
            raise ValueError(
                "Entries of X must not contain NaN / NA, or missing entries"
            )

        if np.any(np.isnan(W)):
            raise ValueError(
                "Entries of W must not contain NaN / NA, or missing entries"
            )

        # check to ensure n_components < n_samples
        if X.shape[1] < self.n_components:
            raise ValueError(
                "Number of components cannot be greater than the number of samples (columns) in X"
            )
        if R is not None:
            n_samples = X.shape[1]
            if not R.shape == (self.n_components, n_samples):
                raise ValueError(
                    "Activity matrix R must be of shape (n_samples, n_components)"
                )
            if R.dtype != bool:
                raise ValueError(
                    "Activity matrix R must be boolean"
                )

    def init_random_generator(self):
        """Initialize pseudo-random number generator.

        Params:
        -------
        seed : random_seed, int, greater than 0
            A random seed to initialize the random number generator. Default is 12345

        Returns:
        -------
        rng : numpy.random.RandomState
            A numpy random number generator
        """
        # initialize the numpy random generator with random seed
        rng = np.random.RandomState(self.random_state)
        return rng

    def initialize_u_v(
        self,
        random_number_generator: np.random.mtrand.RandomState,
        n_features: int,
        n_samples: int,
        mean: float,
        X: np.ndarray,
    ):
        """Initialize U and V.

        U and V are initialized randomly but scaled to the mean
        of X divided by n_components.

        Params:
        -------
        random_number_generator : numpyp.random.RandomState
            An initialized numpy random number generator with a set seed.

        n_features : int
            The number of features in X, or rows of X

        n_samples : int
            The number of samples in X, or columns of X

        mean : float
            Estimated mean over the entire data-set X, used for scaling initilization to approximately
            similar range

        X : numpy.ndarray, values > 0, (n_features, n_samples)
            Data matrix to be factorized, referred to as X in the main code body, referred to as A here to make it easier to
            read the update steps because the authors Blondel, Ho, Ngoc-Diep and Dooren use A.

        Returns:
        -------
        U : numpy.ndarray
            The matrix U, with randomly initialized entries

        V : numpy.ndarray
            The matrix V, with randomly initialized entries

        """
        # estimate density by partitioning mean across components
        est = np.sqrt(mean / self.n_components)

        # generate entries of U/V using randn, scale by est
        if self.init == "random":
            U = est * random_number_generator.randn(n_features, self.n_components)
            V = est * random_number_generator.randn(self.n_components, n_samples)
        elif self.init == "PCA":
            from sklearn.decomposition import PCA

            pca = PCA(self.n_components)
            V = pca.fit_transform(X.T).T
            # any negative values? move the component up to make them zero
            low = np.clip(pca.components_.min(axis=1, keepdims=True), None, 0)
            U = (pca.components_ - low).T
            norms = U.max(axis=0)
            U /= norms
            V *= norms.reshape((-1, 1))
            assert np.clip(pca.components_.min(axis=1), None, 0).shape == (
                self.n_components,
            )
            assert U.shape == (n_features, self.n_components), (
                U.shape,
                (n_features, self.n_components),
            )
            assert V.shape == (self.n_components, n_samples), (
                V.shape,
                (self.n_components, n_samples),
            )
        elif self.init == "logAR1":
            phi = 0.99
            U = random_number_generator.randn(n_features, self.n_components)
            for i in range(n_features - 1):
                U[i + 1] = U[i] * phi + U[i + 1]
            U = np.exp(U)
            U = U * (est / U.mean())
            V = est * random_number_generator.randn(self.n_components, n_samples)
        elif self.init == "sample":
            while True:
                # directly pick data samples as components
                i = random_number_generator.choice(
                    n_samples, size=self.n_components, replace=False
                )
                U = np.clip(X[:, i], 0, None)
                mask = np.any(U > 0, axis=0)
                assert mask.shape == (self.n_components,), (
                    mask.shape,
                    n_samples,
                    n_features,
                    self.n_components,
                )
                if mask.all():
                    break
            V = random_number_generator.randn(self.n_components, n_samples)
        # mutate in-place absolute value
        np.abs(U, U)
        np.abs(V, V)

        # set all zeroes (if there are any) to epsmin
        V[V == 0] = self.epsmin
        U[U == 0] = self.epsmin

        return jnp.array(U), jnp.array(V)

    def initialize_v(
        self,
        random_number_generator: np.random.mtrand.RandomState,
        n_features: int,
        n_samples: int,
        mean: float,
    ):
        """Initialize V.

        V is initialized randomly but scaled to the mean
        of X divided by n_components.

        Params:
        -------
        random_number_generator : numpyp.random.RandomState
            An initialized numpy random number generator with a set seed.

        n_features : int
            The number of features in X, or rows of X

        n_samples : int
            The number of samples in X, or columns of X

        mean : float
            Estimated mean over the entire data-set X, used for scaling initilization to approximately
            similar range

        Returns:
        -------
        U : numpy.ndarray
            The matrix U, with randomly initialized entries

        """
        # estimate density by partitioning mean across components
        est = np.sqrt(mean / self.n_components)

        # generate entries of U/V using randn, scale by est
        V = est * random_number_generator.randn(self.n_components, n_samples)
        np.abs(V, V)
        V[V == 0] = self.epsmin
        return jnp.array(V)
