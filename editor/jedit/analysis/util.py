import numpy as np
from fractions import Fraction

def signchanges(array) -> list:
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

def prepare(array, decimal, concat=False):
    """
    Pripraví výsledné hodnoty, ktoré sa pošlú na výstup (textový/grafický).
    Pythonovské pole hodnôt zmení na numpy pole, zaokrúhli jeho hodnoty, odstráni duplikáty a zoradí hodnoty vzostupne.
    :param array: vstupné pole hodnôt (polí hodnôt)
    :param decimal: desatinné miesta pre zaokrúhľovanie
    :param concat: určuje, že vstupné pole obsahuje ďalšie polia hodnôt, ktoré treba spojiť do jedného
    :return:
    """
    if concat:
        return np.sort(np.unique(np.around(np.concatenate(array), decimal)))
    return np.sort(np.unique(np.around(np.asarray(array), decimal)))

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
