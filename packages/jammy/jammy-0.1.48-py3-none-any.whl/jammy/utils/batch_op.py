__all__ = ["batch_add", "batch_mul", "batch_sub", "batch_div"]


def common_broadcast(x, y):
    ndims1 = x.ndim
    ndims2 = y.ndim

    common_ndims = min(ndims1, ndims2)
    for axis in range(common_ndims):
        assert x.shape[axis] == y.shape[axis], "Dimensions not equal at axis {}".format(
            axis
        )

    if ndims1 < ndims2:
        x = x.reshape(x.shape + (1,) * (ndims2 - ndims1))
    elif ndims2 < ndims1:
        y = y.reshape(y.shape + (1,) * (ndims1 - ndims2))

    return x, y


def batch_add(x, y):
    x, y = common_broadcast(x, y)
    return x + y


def batch_mul(x, y):
    x, y = common_broadcast(x, y)
    return x * y


def batch_sub(x, y):
    x, y = common_broadcast(x, y)
    return x - y


def batch_div(x, y):
    x, y = common_broadcast(x, y)
    return x / y
