from collections import namedtuple

Vector = namedtuple('Vector', 'x y')


def reflect(v, n):
    """Calculate reflection vector.

    Using the formula: Vnew = V-2*(V dot N)*N

    Arguments:
        v {Vector} -- Original vector
        n {Vector} -- Normal vector

    Returns:
        new_vector {Vector} -- Vector result of reflection formula

    """
    dot = (v.x * n.x) + (v.y * n.y)
    z = Vector(x=2 * dot * n.x, y=2 * dot * n.y)
    v_new = Vector(x=v.x - z.x, y=v.y - z.y)
    return v_new
