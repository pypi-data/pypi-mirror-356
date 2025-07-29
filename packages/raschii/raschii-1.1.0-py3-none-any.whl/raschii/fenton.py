import math
from numpy import (
    pi,
    cos,
    sin,
    zeros,
    arange,
    isfinite,
    newaxis,
    asarray,
    linspace,
    cosh,
    sinh,
    array,
    empty,
)
from numpy.linalg import solve
from numpy.fft import irfft
from .common import (
    NonConvergenceError,
    sinh_by_cosh,
    cosh_by_cosh,
    blend_air_and_wave_velocities,
    blend_air_and_wave_velocity_cpp,
    trapezoid_integration,
    np2py,
    RasciiError,
)
from .swd_tools import SwdShape1and2
from .base_classes import WaveModel


class FentonWave(WaveModel):
    required_input = {"height", "depth", "length", "N"}
    optional_input = {"air": None, "g": 9.81, "relax": 0.5}

    def __init__(
        self,
        height: float,
        depth: float,
        length: float | None = None,
        N: int = 5,
        period: float | None = None,
        air=None,
        g: float = 9.81,
        relax: float = 0.5,
    ):
        """
        Implement stream function waves based on the paper by Rienecker and
        Fenton (1981)

        * height: wave height above still water level
        * depth: still water distance from the flat sea bottom to the free surface
          in meters, but you can give -1.0 for infinite depth
        * length: the periodic length of the wave (optional, if not given then period is used)
        * N: the number of coefficients in the truncated Fourier series
        * period: the wave period (optional, if not given then length is used)
        """
        if length is None:
            if period is None:
                raise RasciiError("Either length or period must be given, both are None!")
            length = compute_length_from_period(
                height=height, depth=depth, period=period, N=N, g=g, relax=relax
            )

        self.height: float = height  #: The wave height
        self.depth: float = depth  #: The water depth
        self.length: float = length  #: The wave length
        self.order: int = N  #: The approximation order
        self.air = air  #: The optional air-phase model
        self.g: float = g  #: The acceleration of gravity
        self.relax: float = relax  #: The numerical relaxation in the optimization loop
        self.warnings: str = ""  #: Warnings raised when generating this wave

        # Find the coeffients through optimization
        data = fenton_coefficients(height, depth, length, N, g, relax=relax)
        self.set_data(data)

        # For evaluating velocities close to the free surface
        self.eta_eps: float = self.height / 1e5

        # Provide velocities also in the air phase
        if self.air is not None:
            self.air.set_wave(self)

    def set_data(self, data):
        """
        Update the coefficients defining this stream-function wave
        """
        self.data = data
        self.eta = data["eta"]  # Wave elevation at colocation points
        self.x = data["x"]  # Positions of colocation points
        self.k = data["k"]  # Wave number
        self.c = data["c"]  # Phase speed
        self.cs = self.c - data["Q"]  # Mean Stokes drift speed
        self.T = self.length / self.c  # Wave period
        self.omega = self.c * self.k  # Wave frequency

        # Cosine series coefficients for the elevation
        N = len(self.eta) - 1
        self.E = zeros(N + 1, float)
        J = arange(0, N + 1)
        self.E = trapezoid_integration(self.eta * cos(J * J[:, newaxis] * pi / N))

    def stream_function(self, x, z, t=0, frame="b"):
        """
        Compute the stream function at time t for position(s) x
        """
        if isinstance(x, (float, int)):
            x, z = [x], [z]
        x2 = asarray(x, dtype=float) - self.c * t
        z2 = asarray(z, dtype=float)
        x2, z2 = x2[:, newaxis], z2[:, newaxis]

        N = len(self.eta) - 1
        B = self.data["B"]
        k = self.k
        J = arange(1, N + 1)

        psi = (sinh(J * k * z2) / cosh(J * k * self.depth) * cos(J * k * x2)).dot(B[1:])

        if frame == "b":
            return B[0] * z + psi
        elif frame == "c":
            return psi

    def surface_elevation(self, x: float | list[float], t: float = 0.0, include_depth: bool = True):
        """
        Compute the surface elevation at time t for position(s) x
        """
        if isinstance(x, (float, int)):
            x = array([x], float)
        x = asarray(x)

        # Cosine transformation of the elevation
        N = len(self.eta) - 1
        J = arange(0, N + 1)
        k, c = self.k, self.c
        eta = 2 * trapezoid_integration(self.E * cos(J * k * (x[:, newaxis] - c * t))) / N

        if include_depth:
            if self.depth < 0:
                raise RasciiError("Cannot include depth in elevation for infinite depth")
            subtract = 0.0
        else:
            # Apply consistent water depth limitation with 'fenton_coefficients'
            subtract = 25 * self.length if self.depth < 0 else self.depth

        return eta - subtract

    def surface_slope(self, x, t=0):
        """
        Compute the x derivative of the surface elevation at time t
        """
        if isinstance(x, (float, int)):
            x = array([x], float)
        x = asarray(x)

        # Cosine transformation of the elevation
        N = len(self.eta) - 1
        J = arange(0, N + 1)
        k, c = self.k, self.c
        return -2 * trapezoid_integration(self.E * J * k * sin(J * k * (x[:, newaxis] - c * t))) / N

    def velocity(
        self,
        x: float | list[float],
        z: float | list[float],
        t: float = 0,
        all_points_wet: bool = False,
    ):
        """
        Compute the fluid velocity at time t for position(s) (x, z)
        where z is 0 at the bottom and equal to depth at the free surface
        """
        if self.depth < 0:
            raise RasciiError("Cannot currently compute velocity for infinite depth waves")
        if isinstance(x, (float, int)):
            x, z = [x], [z]
        x = asarray(x, dtype=float)
        z = asarray(z, dtype=float)

        N = len(self.eta) - 1
        B = self.data["B"]
        k = self.k
        c = self.c
        J = arange(1, N + 1)

        vel = zeros((x.size, 2), float)
        vel[:, 0] = k * (
            B[1:]
            * cos(J * k * (x[:, newaxis] - c * t))
            * cosh(J * k * z[:, newaxis])
            / cosh(J * k * self.depth)
        ).dot(J)
        vel[:, 1] = k * (
            B[1:]
            * sin(J * k * (x[:, newaxis] - c * t))
            * sinh(J * k * z[:, newaxis])
            / cosh(J * k * self.depth)
        ).dot(J)

        if not all_points_wet:
            blend_air_and_wave_velocities(x, z, t, self, self.air, vel, self.eta_eps)

        return vel

    def stream_function_cpp(self, frame="b"):
        """
        Return C++ code for evaluating the stream function of this specific
        wave. The positive traveling direction is x[0] and the vertical
        coordinate is x[2] which is zero at the bottom and equal to +depth at
        the mean water level.
        """
        if self.depth < 0:
            raise RasciiError("Cannot currently generate C++ code for infinite depth waves")
        N = len(self.eta) - 1
        J = arange(1, N + 1)
        B = self.data["B"]
        k = self.k

        Jk = J * k
        facs = B[1:] / cosh(Jk * self.depth)

        # Repr of np.float64(42.0) is "np.float64(42.0)" and not "42.0"
        # We use repr to make Python output a "smart" amount of digits
        c = np2py(self.c)
        Jk = np2py(Jk)
        facs = np2py(facs)

        cpp = " + ".join(
            f"{facs[i]!r} * cos({Jk[i]!r} * (x[0] - {c!r}* t)) * sinh({Jk[i]!r} * x[2])"
            for i in range(N)
        )

        if frame == "b":
            return f"{np2py(B[0])!r} * x[2] + {cpp}"
        elif frame == "c":
            return cpp

    def elevation_cpp(self):
        """
        Return C++ code for evaluating the elevation of this specific wave.
        The positive traveling direction is x[0]
        """
        if self.depth < 0:
            raise RasciiError("Cannot currently generate C++ code for infinite depth waves")
        N = self.E.size - 1
        facs = self.E * 2 / N
        facs[0] *= 0.5
        facs[-1] *= 0.5

        # Repr of np.float64(42.0) is "np.float64(42.0)" and not "42.0"
        # We use repr to make Python output a "smart" amount of digits
        k = np2py(self.k)
        c = np2py(self.c)
        facs = np2py(facs)

        code = " + ".join(
            f"{facs[j]!r} * cos({j:d} * {k!r} * (x[0] - {c!r} * t))" for j in range(0, N + 1)
        )
        return code

    def slope_cpp(self):
        """
        Return C++ code for evaluating the surface slope of this specific wave.
        The positive traveling direction is x[0]
        """
        if self.depth < 0:
            raise RasciiError("Cannot currently generate C++ code for infinite depth waves")
        N = self.E.size - 1
        facs = self.E * 2 / N * self.k * -1.0
        facs[0] *= 0.5
        facs[-1] *= 0.5

        # Repr of np.float64(42.0) is "np.float64(42.0)" and not "42.0"
        # We use repr to make Python output a "smart" amount of digits
        k = np2py(self.k)
        c = np2py(self.c)
        facs = np2py(facs)

        code = " + ".join(
            f"{facs[j]!r} * {j:d} * sin({j:d} * {k!r} * (x[0] - {c!r} * t))"
            for j in range(0, N + 1)
        )
        return code

    def velocity_cpp(self, all_points_wet=False):
        """
        Return C++ code for evaluating the particle velocities of this specific
        wave. Returns the x and z components only with z positive upwards. The
        positive traveling direction is x[0] and the vertical coordinate is x[2]
        which is zero at the bottom and equal to +depth at the mean water level.
        """
        if self.depth < 0:
            raise RasciiError("Cannot currently generate C++ code for infinite depth waves")
        N = len(self.eta) - 1
        J = arange(1, N + 1)
        B = self.data["B"]
        k = self.k
        c = self.c

        Jk = J * k
        facs = J * B[1:] * k / cosh(Jk * self.depth)

        # Repr of np.float64(42.0) is "np.float64(42.0)" and not "42.0"
        # We use repr to make Python output a "smart" amount of digits
        c = np2py(self.c)
        Jk = np2py(Jk)
        facs = np2py(facs)

        cpp_x = " + ".join(
            f"{facs[i]!r} * cos({Jk[i]!r} * (x[0] - {c!r} * t)) * cosh({Jk[i]!r} * x[2])"
            for i in range(N)
        )
        cpp_z = " + ".join(
            f"{facs[i]!r} * sin({Jk[i]!r} * (x[0] - {c!r} * t)) * sinh({Jk[i]!r} * x[2])"
            for i in range(N)
        )

        if all_points_wet:
            return cpp_x, cpp_z

        # Handle velocities above the free surface
        e_cpp = self.elevation_cpp()
        cpp_ax = cpp_az = None
        cpp_psiw = cpp_psia = cpp_slope = None
        if self.air is not None:
            cpp_ax, cpp_az = self.air.velocity_cpp()
            cpp_psiw = self.stream_function_cpp(frame="c")
            cpp_psia = self.air.stream_function_cpp(frame="c")
            cpp_slope = self.slope_cpp()

        cpp_x = blend_air_and_wave_velocity_cpp(
            cpp_x, cpp_ax, e_cpp, "x", self.eta_eps, self.air, cpp_psiw, cpp_psia, cpp_slope
        )
        cpp_z = blend_air_and_wave_velocity_cpp(
            cpp_z, cpp_az, e_cpp, "z", self.eta_eps, self.air, cpp_psiw, cpp_psia, cpp_slope
        )

        return cpp_x, cpp_z

    def write_swd(self, path, dt, tmax=None, nperiods=None):
        """
        Write a SWD-file of the wave field according to the file
        specification in the Github repository spectral-wave-data ....

        * path:     Full path of the new SWD file
        * dt:       The temporal sampling spacing in the SWD file
        * tmax:     The temporal sampling range in the SWD file is [0, tmax]
        * nperiods: Alternative specification: tmax = nperiods * wave_period
        """
        if tmax is None:
            assert nperiods is not None
            tmax = nperiods * self.T
        assert tmax > dt > 0.0

        # Apply consistent water depth limitation with 'fenton_coefficients'
        if self.depth < 0:
            depth = 25 * self.length
        else:
            depth = self.depth

        # The swd coordinate system is earth fixed with zswd=0 in the calm
        # surface. Hence:
        #   xswd = x + t * self.c    and    zswd = z - self.depth

        # In SWD we apply summation and not trapezoidal integration of surface
        # Fourier coefficients. We apply exact Discrete Fourier Transformations
        # assuming constant spaced collocation points...
        nc = len(self.eta)
        dx0 = abs(self.x[1] - self.x[0])
        assert [
            abs(abs(self.x[i + 2] - self.x[i + 1]) - abs(self.x[i + 1] - self.x[i])) < 1.0e-4 * dx0
            for i in range(nc - 2)
        ]
        # elevation on complete wave length...
        nc2 = 2 * nc - 1
        etas = array([self.eta[i] if i < nc else self.eta[nc2 - i - 1] for i in range(nc2)])
        res = irfft(etas)
        # zeta(x) = sum[ecs[j] * cos(j * self.k * x) for j in range(nc)]
        # res[:] other than Bias and Nyquist must be doubled. Skip zero sinusoidal coefficients...
        ecs = empty(nc)
        ecs[0] = (
            res[0].real - depth
        )  # Also shift zero to free surface. (Should be very close to zero)
        for j in range(1, nc - 1):
            ecs[j] = 2.0 * res[2 * j].real
        ecs[-1] = res[nc2 - 1].real

        # Note that ecs[j] * cos(j * self.k * x) == Re{h[j, t] * exp(-I * j * self.k * xswd)}
        # where h[j, t] = ecs[j] * exp(-I * j * self.k * (-self.c * t)),   j>=0, I=sqrt(-1)
        # Hence dh[j, t]/dt = I * j * self.k * self.c * h[j, t]

        # From particle velocities we construct the SWD velocity potential...

        # Note:  B[j] * cos(j * self.k * x) == Im{c[j, t] * exp(-I * j * self.k * xswd)}
        # where c[j, t] = I * B[j] * exp(-I * j * self.k * (-self.c * t)),     j>0
        # Hence dc[j, t]/dt = I * j * self.k * self.c * c[j, t]

        B = self.data["B"]
        vcs = empty(nc, complex)
        vcs[0] = 0.0
        for j in range(1, nc):
            vcs[j] = 1.0j * B[j]

        input_data = {
            "model": "Fenton",
            "T": self.T,
            "height": self.height,
            "depth": self.depth,
            "depth_actual": depth,
            "N": self.order,
            "air": self.air.__class__.__name__,
            "g": self.g,
            "c": self.c,
            "relax": self.relax,
        }

        swd = SwdShape1and2(
            self.T, self.length, self.depth, vcs, ecs, input_data, self.g, order_zpos=-1
        )
        swd.write(path, dt, tmax=tmax)


def fenton_coefficients(
    height, depth, length, N, g=9.8, maxiter=500, tolerance=1e-8, relax=1.0, num_steps=None
):
    """
    Find B, Q and R by Newton-Raphson following Rienecker and Fenton (1981)

    Using relaxation can help in some difficult cases, try a value less than 1
    to decrease convergence speed, but increase chances of converging.
    """
    if depth < 0:
        depth = 25 * length

    # Non dimensionalised input
    H = height / depth
    lam = length / depth
    k = 2 * pi / lam
    c = (math.tanh(k) / k) ** 0.5
    D = 1
    N_unknowns = 2 * (N + 1) + 2

    # Input data arrays
    J = arange(1, N + 1)
    M = arange(0, N + 1)
    x = M * lam / (2 * N)

    def initial_guess(H):
        """
        Initial guesses for the unknowns (linear wave)
        """
        B = zeros(N + 1, float)
        B[0] = c
        B[1] = -H / (4 * c * k)
        eta = 1 + H / 2 * cos(k * x)
        Q = c
        R = 1 + 0.5 * c**2
        return B, Q, R, eta

    def optimize(B, Q, R, eta, H):
        """
        Find B, Q and R by Newton iterations starting from the given initial
        guesses. According to Rienecker and Fenton (1981) a linear theory
        initial guess should work unless H close to breaking, then an initial
        guess from the optimization routine run with a slightly lower H should
        be used instead.
        """
        # Insert initial guesses into coefficient vector
        coeffs = zeros(N_unknowns, float)
        coeffs[: N + 1] = B
        coeffs[N + 1 : 2 * N + 2] = eta
        coeffs[2 * N + 2] = Q
        coeffs[2 * N + 3] = R
        f = func(coeffs, H, k, D, J, M)

        for it in range(1, maxiter + 1):
            jac = fprime(coeffs, H, k, D, J, M)
            delta = solve(jac, -f)
            coeffs += delta * relax
            f = func(coeffs, H, k, D, J, M)

            # Check the progress
            error = abs(f).max()
            eta_max = coeffs[N + 1 : 2 * N + 2].max()
            eta_min = coeffs[N + 1 : 2 * N + 2].min()
            if eta_max > 2:
                raise NonConvergenceError(
                    "Optimization did not converge. Got "
                    "max(eta)/depth = %r in iteration %d" % (eta_max, it)
                )
            elif eta_min < 0.1:
                raise NonConvergenceError(
                    "Optimization did not converge. Got "
                    "min(eta)/depth = %r in iteration %d" % (eta_min, it)
                )
            elif not isfinite(error):
                raise NonConvergenceError(
                    "Optimization did not converge. Got error %r in iteration %d" % (error, it)
                )
            elif error < tolerance:
                B = coeffs[: N + 1]
                eta = coeffs[N + 1 : 2 * N + 2]
                Q = coeffs[2 * N + 2]
                R = coeffs[2 * N + 3]
                return B, Q, R, eta, error, it
        raise NonConvergenceError(
            "Optimization did not converge after %d iterations, error = %r" % (it, error)
        )

    # Perform the optimization, optionally in steps gradually increasing H
    steps = wave_height_steps(num_steps, D, lam, H)
    B, Q, R, eta = initial_guess(steps[0])
    for Hi in steps:
        B, Q, R, eta, error, niter = optimize(B, Q, R, eta, Hi)

    # Scale back to physical space
    B[0] *= (g * depth) ** 0.5
    B[1:] *= (g * depth**3) ** 0.5
    return {
        "x": x * depth,
        "eta": eta * depth,
        "B": B,
        "Q": Q * (g * depth**3) ** 0.5,
        "R": R * g * depth,
        "k": k / depth,
        "c": B[0],
        "error": error,
        "niter": niter,
    }


def wave_height_steps(num_steps, D, lam, H):
    """
    Compute the breaking height and use this to select how many steps take when
    gradually increasing the wave height to improve convergence on high waves
    """
    # Breaking height
    Hb = 0.142 * math.tanh(2 * pi * D / lam) * lam

    # Try with progressively higher waves to get better initial conditions
    if num_steps is not None:
        pass
    if H > 0.75 * Hb:
        num_steps = 10
    elif H > 0.65 * Hb:
        num_steps = 5
    else:
        num_steps = 3

    if num_steps == 1:
        return [H]
    else:
        return linspace(H / num_steps, H, num_steps)


def func(coeffs, H, k, D, J, M):
    "The function to minimize"
    N_unknowns = coeffs.size
    N = J.size

    B0 = coeffs[0]
    B = coeffs[1 : N + 1]
    eta = coeffs[N + 1 : 2 * N + 2]
    Q = coeffs[2 * N + 2]
    R = coeffs[2 * N + 3]

    # The function to me minimized
    f = zeros(N_unknowns, float)

    # Loop over the N + 1 points along the half wave
    for m in M:
        S1 = sinh_by_cosh(J * k * eta[m], J * k * D)
        C1 = cosh_by_cosh(J * k * eta[m], J * k * D)
        S2 = sin(J * m * pi / N)
        C2 = cos(J * m * pi / N)

        # Velocity at the free surface
        # The sign of B0 is swapped from what is in the paper
        um = -B0 + k * J.dot(B * C1 * C2)
        vm = 0 + k * J.dot(B * S1 * S2)

        # Enforce a streamline along the free surface
        # The sign of B0 is swapped from what is in the paper
        f[m] = -B0 * eta[m] + B.dot(S1 * C2) + Q

        # Enforce the dynamic free surface boundary condition
        f[N + 1 + m] = (um**2 + vm**2) / 2 + eta[m] - R

    # Enforce mean(eta) = D
    f[-2] = trapezoid_integration(eta) / N - 1

    # Enforce eta_0 - eta_N = H, the wave height criterion
    f[-1] = eta[0] - eta[-1] - H

    return f


def fprime_num(coeffs, H, k, D, J, M):
    "The Jacobian of the function to minimize (numerical version)"
    N_unknowns = coeffs.size
    dc = 1e-10
    jac = zeros((N_unknowns, N_unknowns), float)
    f0 = func(coeffs, H, k, D, J, M)
    for i in range(N_unknowns):
        incr = zeros(N_unknowns, float)
        incr[i] = dc
        f1 = func(coeffs + incr, H, k, D, J, M)
        jac[:, i] = (f1 - f0) / dc
    return jac


def fprime(coeffs, H, k, D, J, M):
    "The Jacobian of the function to minimize"
    N_unknowns = coeffs.size
    N = J.size

    jac = zeros((N_unknowns, N_unknowns), float)
    B0 = coeffs[0]
    B = coeffs[1 : N + 1]
    eta = coeffs[N + 1 : 2 * N + 2]

    for m in range(N + 1):
        S1 = sinh_by_cosh(J * k * eta[m], J * k * D)
        C1 = cosh_by_cosh(J * k * eta[m], J * k * D)
        S2 = sin(J * m * pi / N)
        C2 = cos(J * m * pi / N)

        SC = S1 * C2
        SS = S1 * S2
        CC = C1 * C2
        CS = C1 * S2

        # Velocity at the free surface
        um = -B0 + k * J.dot(B * CC)
        vm = 0 + k * J.dot(B * SS)

        # Derivatives of the eq. for the streamline along the free surface
        jac[m, N + 1 + m] = um
        jac[0 : N + 1, 0] = -eta
        jac[m, 1 : N + 1] = SC
        jac[m, -2] = 1

        # Derivatives of the dynamic free surface boundary condition
        jac[N + 1 + m, N + 1 + m] = 1 + (
            um * k**2 * B.dot(J**2 * SC) + vm * k**2 * B.dot(J**2 * CS)
        )
        jac[N + 1 + m, -1] = -1
        jac[N + 1 + m, 0] = -um
        jac[N + 1 + m, 1 : N + 1] = k * um * J * CC + k * vm * J * SS

    # Derivative of mean(eta) = 1
    jac[-2, N + 1 : 2 * N + 2] = M * 0 + 1 / N
    jac[-2, N + 1] = 1 / (2 * N)
    jac[-2, 2 * N + 1] = 1 / (2 * N)

    # Derivative of the wave height criterion
    jac[-1, N + 1] = 1
    jac[-1, 2 * N + 1] = -1

    return jac


def compute_length_from_period(
    height: float,
    depth: float,
    period: float,
    N: int = 5,
    g: float = 9.81,
    relax: float = 0.5,
):
    """
    Compute the wave length from the wave period using the Fenton wave theory

    This would be much faster if we had an implementation of the Fenton wave
    theory dispersion relation for arbitrary order N
    """
    from .airy import compute_length_from_period as airy_compute_length_from_period

    # Initial guess is based on the linear dispersion relation for deep water waves
    length = airy_compute_length_from_period(depth=depth, period=period, g=g)

    # Find the length by Newton iterations
    wave1 = FentonWave(height=height, depth=depth, length=length * 0.95, N=N, g=g, relax=relax)
    wave2 = FentonWave(height=height, depth=depth, length=length * 1.05, N=N, g=g, relax=relax)

    length_N = 0.0
    iter = 0
    while abs(length_N - length) > 1e-4:
        # Store the previous length
        length = length_N

        # New guess for the wave length by interpolation
        f = (period - wave1.T) / (wave2.T - wave1.T)
        length_N = wave1.length + (wave2.length - wave1.length) * f

        # Resulting wave period for the new length from the dispersion relation
        waveN = FentonWave(height=height, depth=depth, length=length_N, N=N, g=g, relax=relax)

        # Update the two points used for the interpolation in the next iteration
        if waveN.T < period:
            wave1 = waveN
        else:
            wave2 = waveN

        iter += 1
        if iter > 100:
            raise NonConvergenceError(
                "Failed to converge when computing wave length from period for Fenton waves"
            )

    return length_N
