import numpy
from numba import njit, float64, int64, boolean
from interpg.interp_data import interp_data


def interp_2d_line(x: numpy.array, y: numpy.array, f: numpy.ndarray, c_i: numpy.ndarray, z: numpy.array=None, ax_int: float=None,
                   nearest: bool=False, z_nearest: bool=False) -> tuple:

    """
    Performs 2D interpolation from a grid along a line.
    args...
        f is the interpolant, a 2D or 3D Numpy array with corresponding 1D axes arrays x and y along which interpolation is performed.
        x and y can be non-uniform but must be ordered, either increasing or decreasing.
        If f is a 3D array, its dimensions are (N, x.size, y.size), otherwise they are (x.size, y.size).
        c_i is a 2D Numpy array of interpolation coordinates, size M by 2 where M is the number of points.
        First column is x coordinates, second is y coordinates.
        Both columns of c_i can be non-uniform but must be ordered in the same sense as x and y respectively for optimum speed.
        If not, the interpolation will still work but will be slower.
    kwargs...
        z is the 1D axis array for the first dimension of f. If z is None or f is 2D, interpolation over z will not be performed.
        ax_int is the interval for interpolation over z. If equal to None, the minimum interval in z will be used for interpolation.
        nearest: on True use nearest-neighbour interpolation in x and y (the default is linear).
        z_nearest: on True use nearest-neighbour interpolation in z (the default is linear).
    returns...
        f_i: Numpy 2D array with dimensions (I, M) if f is a 3D array, otherwise 1D array, length M. I = N if ax_int is None.
        z_i: Numpy array with new (or unchanged) z axis values.
    """

    #  Check inputs

    nx = x.size
    ny = y.size
    nc = c_i.shape[0]

    fdims = f.shape
    is3d = False
    if len(fdims) == 3:
        is3d = True
        if (z is not None) and (z.size != fdims[0]):
            raise ValueError('Length of z not equal to length of first dimension in f')
        nz = fdims[0]
        check_dims = fdims[1:]
        out_dims = (nz, nc)
    else:
        check_dims = fdims
        out_dims = nc

    if (nx, ny) != check_dims:
        raise ValueError('Input dimensions are not consistent')

    if x[1] > x[0]:
        xinc = True
    else:
        xinc = False
    if y[1] > y[0]:
        yinc = True
    else:
        yinc = False

    xal = True
    yal = True
    if nc > 1:
        if xinc:
            if c_i[1, 0] < c_i[0, 0]:
                xal = False
        else:
            if c_i[1, 0] > c_i[0, 0]:
                xal = False
        if yinc:
            if c_i[1, 1] < c_i[0, 1]:
                yal = False
        else:
            if c_i[1, 1] > c_i[0, 1]:
                yal = False

    # Interpolate

    if is3d:
        f_i = _interp3D(out_dims[0], out_dims[1], nc, c_i, xal, yal, xinc, nx, x.__array__().astype(float), yinc, ny, y.__array__().astype(float),
                        f.__array__().astype(float), nearest)
    else:
        f_i = _interp2D(out_dims, nc, c_i, xal, yal, xinc, nx, x.__array__().astype(float), yinc, ny, y.__array__().astype(float),
                        f.__array__().astype(float), nearest)

    if is3d and (z is not None):
        _, z_i, f_i, _, _ = interp_data(numpy.arange(nc), z, f_i, ax_int=ax_int, nearest=z_nearest)
    else:
        z_i = z

    return f_i, z_i


@njit(float64[:](int64, int64, float64[:, :], boolean, boolean, boolean, int64, float64[:], boolean, int64, float64[:], float64[:, :], boolean))
def _interp2D(out_dim, nc, c_i, xal, yal, xinc, nx, x, yinc, ny, y, f, nearest):

    f_i = numpy.ones(out_dim) * numpy.nan

    xn = yn = cn = 0

    while cn < nc:

        xc, yc = c_i[cn]

        if not xal:
            xn = 0
        if not yal:
            yn = 0

        if xinc:
            while (xn < nx) and (x[xn] < xc):
                xn += 1
            if xn > 0:
                xn -= 1
        else:
            while (xn < nx) and (x[xn] > xc):
                xn += 1
            if xn > 0:
                xn -= 1

        if yinc:
            while (yn < ny) and (y[yn] < yc):
                yn += 1
            if yn > 0:
                yn -= 1
        else:
            while (yn < ny) and (y[yn] > yc):
                yn += 1
            if yn > 0:
                yn -= 1

        if (xn < nx - 1) and (yn < ny - 1):

            if xinc:
                x0, x1 = xn, xn + 1
            else:
                x0, x1 = xn + 1, xn
            if yinc:
                y0, y1 = yn, yn + 1
            else:
                y0, y1 = yn + 1, yn

            if (x[x0] <= xc <= x[x1]) and (y[y0] <= yc <= y[y1]):

                if nearest:

                    xi = x0 if xc - x[x0] <= x[x1] - xc else x1
                    yi = y0 if yc - y[y0] <= y[y1] - yc else y1
                    fy = f[xi, yi]

                else:

                    xfact = (xc - x[xn]) / (x[xn + 1] - x[xn])
                    yfact = (yc - y[yn]) / (y[yn + 1] - y[yn])

                    f00 = f[xn, yn]
                    f01 = f[xn, yn + 1]
                    f10 = f[xn + 1, yn]
                    f11 = f[xn + 1, yn + 1]

                    fx0 = f00 + xfact * (f10 - f00)
                    fx1 = f01 + xfact * (f11 - f01)
                    fy = fx0 + yfact * (fx1 - fx0)

                f_i[cn] = fy

        cn += 1

    return f_i


@njit(float64[:, :](int64, int64, int64, float64[:, :], boolean, boolean, boolean, int64, float64[:], boolean, int64, float64[:], float64[:, :, :],
                    boolean))
def _interp3D(outdim1, outdim2, nc, c_i, xal, yal, xinc, nx, x, yinc, ny, y, f, nearest):

    f_i = numpy.ones((outdim1, outdim2)) * numpy.nan

    xn = yn = cn = 0

    while cn < nc:

        xc, yc = c_i[cn]

        if not xal:
            xn = 0
        if not yal:
            yn = 0

        if xinc:
            while (xn < nx) and (x[xn] < xc):
                xn += 1
            if xn > 0:
                xn -= 1
        else:
            while (xn < nx) and (x[xn] > xc):
                xn += 1
            if xn > 0:
                xn -= 1

        if yinc:
            while (yn < ny) and (y[yn] < yc):
                yn += 1
            if yn > 0:
                yn -= 1
        else:
            while (yn < ny) and (y[yn] > yc):
                yn += 1
            if yn > 0:
                yn -= 1

        if (xn < nx - 1) and (yn < ny - 1):

            if xinc:
                x0, x1 = xn, xn + 1
            else:
                x0, x1 = xn + 1, xn
            if yinc:
                y0, y1 = yn, yn + 1
            else:
                y0, y1 = yn + 1, yn

            if (x[x0] <= xc <= x[x1]) and (y[y0] <= yc <= y[y1]):

                if nearest:

                    xi = x0 if xc - x[x0] <= x[x1] - xc else x1
                    yi = y0 if yc - y[y0] <= y[y1] - yc else y1
                    fy = f[:, xi, yi]

                else:

                    xfact = (xc - x[xn]) / (x[xn + 1] - x[xn])
                    yfact = (yc - y[yn]) / (y[yn + 1] - y[yn])

                    f00 = f[:, xn, yn]
                    f01 = f[:, xn, yn + 1]
                    f10 = f[:, xn + 1, yn]
                    f11 = f[:, xn + 1, yn + 1]

                    fx0 = f00 + xfact * (f10 - f00)
                    fx1 = f01 + xfact * (f11 - f01)
                    fy = fx0 + yfact * (fx1 - fx0)

                f_i[:, cn] = fy

        cn += 1

    return f_i
