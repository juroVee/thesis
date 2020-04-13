import numpy as np

def transform_title(title: str) -> str:
    if title == '':
        return ''
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    return result

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
    print(result)
    if 0 in result:
        result = result[1:]
    if len(array) - 1 in result + 1:
        result = result[:-1]
    return list(zip(result, result + 1))

def around(array, dec='undefined'):
    if dec == 'undefined':
        return array
    return np.around(array, dec)