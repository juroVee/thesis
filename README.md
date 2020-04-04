# Repozitár k bakalárskej práci

## Spustenie editora

### Inštalácia Jupyter

V prvom rade je potrebné mať nainštalovaný Jupyter Notebook (ideálne v distribúcii `Anaconda`).

Alternatívne:

```
pip3 install --upgrade pip
pip3 install jupyter
```

### Spustenie prostredia Jupyter Notebook:

```
jupyter notebook
```

V zvolenom pracovnom priečinku vytvorte nový dokument `.ipynb`.

### (Predbežná) inštalácia a import editora v Jupyter Notebook:

Nakopírujte priečinok `jedit`, ktorý sa nachádza v priečinku `editor` tohto repozitára do vyššie zvoleného pracovného priečinka. Potom:

```
import matplotlib.pyplot as plt
%matplotlib notebook
from jedit import editor
```

### Nakreslenie grafu užívateľom pomocou knižnice Matplotlib:

```
...
X = ...
def f(x) = ...
fig, ax = plt.subplots()
...
```

### Spustenie editora po nakreslení grafu:

Samotný editor sa spúšťa zavolaním funkcie ```editor()```, ktorá vyžaduje tzv. keyworded argumenty ```**params```.

```
``editor(figure=fig, axes=ax, function=f, intervals=[X1, ..., Xn], primes=[p1, ..., pn], asymptotes=[a1, ..., an])``
```
kde ```figure, axes, intervals``` sú povinné argumenty a ```primes, asymptotes``` nepovinné a znamenajú užívateľom definované funkcie derivácií (zadané poradie zároveň definuje ich stupeň), resp. užívateľom zadané asymptoty (taktiež ich funkcie).

Hodnoty pre kľúče ```intervals, primes, asymptotes``` treba zadávať v zoznamoch (list), aj keď užívateľ definuje len jednu hodnotu.

Editor je možné spustiť aj v tzv. ```default``` móde s vopred definovanými funkciami, a to bez parametrov:
```
editor()
```
