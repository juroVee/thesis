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

### Import editora v Jupyter Notebook:

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
