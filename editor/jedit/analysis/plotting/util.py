from fractions import Fraction

def init_subplot(ax):
    """Author: J. Komara"""

    # Hide the top and right spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # Only show ticks on the bottom and left spines
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))


def smart_ticklabel(n, unit, d):
    """
    Author: J. Komara
    Returns normalized fraction n/d of the unit in latex represenation.
    Example: smart_ticklabel(3, r"\pi", 2) == "$\\\\dfrac{3\\\\pi}{2}$"
    """

    def smart_sign(n):
        if n < 0:
            return "-"
        else:
            return ""

    def smart_nat(n):
        if n == 1:
            return ""
        else:
            return str(n)

    n1, d1 = Fraction(n, d).numerator, Fraction(n, d).denominator
    if n1 == 0:
        return "$0$"
    elif d1 == 1:
        return "$" + smart_sign(n1) + smart_nat(abs(n1)) + unit + "$"
    else:
        return "$" + smart_sign(n1) + r"\dfrac{" + smart_nat(abs(n1)) + unit + "}{" + str(d1) + "}$"
