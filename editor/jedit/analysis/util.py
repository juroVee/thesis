import numpy as np

from scipy.misc import derivative
from scipy.signal import argrelextrema
from fractions import Fraction

from ..settings import settings

def zero_crossings(array) -> list:
    """
    Pri hľadaní nulových hodnôt derivácií sa často stretávame s problémom, že tieto hodnoty
    sú nule len blízke, pričom samotné nuly sa v našich vypočítaných hodnotách ani nenachádzajú.
    To však nebráni správnemu odhadu "nuly", t.j. nájdeniu hodnôt najbližších nule.
    Najjednoduchší spôsob výberu hodnôt najbližsích nule, je nájsť medzi hodnotami indexy hodnôt,
    kde sa mení znamienko na opačné. Niekedy sa toto znamienko môže meniť v krajných bodoch intervalu, čo ignorujeme.
    :param array: Vstupné pole hodnôt, v ktorom hľadáme hodnoty najbližšie nule.
    :return: Zoznam dvojíc indexov hodnôt v poli, medzi ktorými sa mení znamienko na opačné
    """
    result = np.where((np.diff(np.sign(array)) != abs(0)) * 1)[0]
    if 0 in result:
        result = result[1:]
    if len(array) - 1 in result + 1:
        result = result[:-1]
    return list(zip(result, result + 1))

def approximate_zeros(array):
    atol = float(settings['editor']['zero_tolerance'])
    touching_zero_pos = argrelextrema(array, np.less)[0]
    touching_zero_neg = argrelextrema(array, np.greater)[0]
    if np.any(np.isclose(array[touching_zero_pos], 0, atol=atol)):
        array[touching_zero_pos] = 0.
    if np.any(np.isclose(array[touching_zero_neg], 0, atol=atol)):
        array[touching_zero_neg] = 0.
    crossings = [pair[np.abs(array[np.array(pair)]).argmin()] for pair in zero_crossings(array)]
    array[crossings] = 0.
    return array

def get_derivative(func, X, n):
    delta_x, order = np.diff(X)[0], n + 5 if n % 2 == 0 else n + 2
    return derivative(func, X, n=n, dx=delta_x, order=order)

def prepare(array, decimal):
    """
    Pripraví výsledné hodnoty, ktoré sa pošlú na výstup (textový/grafický).
    Pythonovské pole hodnôt zmení na numpy pole, zaokrúhli jeho hodnoty, odstráni duplikáty a zoradí hodnoty vzostupne.
    :param array: vstupné pole hodnôt (polí hodnôt)
    :param decimal: desatinné miesta pre zaokrúhľovanie
    :return:
    """
    return np.sort(np.unique(np.around(np.asarray(list(array)), decimal)))

def init_subplot(ax):
    """
    Author: J. Komara
    """

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
