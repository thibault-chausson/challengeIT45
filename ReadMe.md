# Projet IT45 SESSAD


## Installation
Une version de Python 3 sera installée si il n'y en a pas sur votre machine.
#### Windows
```bat
dir Projet\
.\install.bat
```
Fermez le terminal et ouvrez en un nouveau pour le reste de l'installation :
```bat
dir Projet\
.\install_librairies.bat
```

#### Linux
```sh
cd Projet/
./install.sh
```

## Exécution
Le flag ```--remplace``` est très utile dans le cas ou l'algorithme génétique ne trouve plus de solutions et se bloque.
Il est conseillé de le laisser, car il permet de débloquer mais ne change pas le résultat de l'algorithme s'il ne se bloque pas.

Voici quelques exemples d'éxecution :
#### Windows
```bat
py main.py --help
py main.py -g 10000 -p 150 -m 0.1 -e 0 -t cascade_fit -d 45-4 --remplace
py main.py -g 10000 -p 200 -m 0.1 -e 0 -t cascade -d 45-4 --remplace
py main.py -g 20000 -p 600 -m 0.1 -e 0 -t classique -f sessad -d 100-10 --remplace
py main.py -g 8000 -p 250 -m 0.1 -e 0 -t moyenne -d 96-6 --remplace
py main.py -g 8000 -p 250 -m 0.1 -e 0 -t moyenne_normalise -d 100-10
py main.py -g 8000 -p 250 -m 0.2 -e 0.1 -t cascade_fit -d 45-4 --remplace
```

#### Linux
```sh
python3 main.py --help
python3 main.py -g 10000 -p 150 -m 0.1 -e 0 -t cascade_fit -d 45-4 --remplace
python3 main.py -g 10000 -p 200 -m 0.1 -e 0 -t cascade -d 45-4 --remplace
python3 main.py -g 20000 -p 600 -m 0.1 -e 0 -t classique -f sessad -d 100-10 --remplace
python3 main.py -g 8000 -p 250 -m 0.1 -e 0 -t moyenne -d 96-6
python3 main.py -g 8000 -p 250 -m 0.1 -e 0 -t moyenne_normalise -d 100-10
python3 main.py -g 8000 -p 250 -m 0.2 -e 0.1 -t cascade_fit -d 45-4 --remplace
```

