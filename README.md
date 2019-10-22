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
fig, ax = plt.subplots()
...
```

### Spustenie editora po nakreslení grafu:

```
editor.run(fig, ax)
```
