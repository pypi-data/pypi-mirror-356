![package_python_tuto](https://github.com/user-attachments/assets/93d342ad-742d-41dd-9597-77fc701b5a0b)

# cr_package_installable

## Introduction

Un package Python est une collection organisée de modules qui facilitent la réutilisation du code. Les packages permettent de structurer un projet de manière modulaire, ce qui améliore la maintenabilité, la lisibilité et le partage de code. Pour les développeurs, et en particulier en **Data Science**, créer et utiliser des packages permet de réutiliser des fonctionnalités complexes, de les organiser et de les partager facilement. Cela contribue également à la productivité en regroupant des fonctions spécifiques à un domaine ou à une tâche dans un ensemble cohérent.

Dans ce tutoriel, nous allons découvrir comment créer un package Python à travers l'exemple de **cr_package_installable**, un package simple qui permet de convertir des unités impériales de longueur et de poids.

## Explication de la structure du répertoire de travail

Un package Python n'est rien d'autre qu'un dossier qui contient un fichier spécial appelé `__init__.py`. Ce fichier indique à Python que le dossier doit être traité comme un package. Un package peut également contenir des sous-packages, qui sont simplement des sous-dossiers avec leur propre fichier `__init__.py`.

### Structure hiérarchique

Voici la structure du répertoire de travail pour le projet **cr_package_installable** :

```
cr_package_installable/
│
├── LICENSE
├── MANIFEST.in
├── README.md
├── requirements-dev.txt
├── setup.py
├── example_script.py
├── cr_package_installable/
    ├── __init__.py
    ├── utils.py
    ├── length/
    │   ├── __init__.py
    │   ├── core.py
    │   ├── api.py
    ├── weight/
        ├── __init__.py
        ├── core.py
        ├── api.py
```

#### Explication des éléments :

- **cr_package_installable/** : Le répertoire principal de travail, qui contient le package ainsi que d'autres fichiers liés à la configuration du projet.
  
- **LICENSE** : Ce fichier contient la licence du projet qui définit les termes sous lesquels le code peut être utilisé et distribué.
  
- **MANIFEST.in** : Ce fichier permet de spécifier quels fichiers doivent être inclus lors de la distribution du package.
  
- **README.md** : Le fichier que vous êtes en train de lire. Il décrit le projet, ses fonctionnalités et son utilisation.
  
- **requirements-dev.txt** : Un fichier listant les dépendances nécessaires pour le développement du projet, par exemple pour les tests ou la documentation.
  
- **setup.py** : Le script de configuration qui permet de packager et de distribuer le projet via des outils comme PyPI (Python Package Index).
  
- **example_script.py** : Un script d'exemple utilisé pour tester l'utilisation du package **cr_package_installable**.

- **cr_package_installable/** : Le dossier qui contient le code source du package. Ce dossier représente le cœur du projet.

  - **__init__.py** : Ce fichier fait de **cr_package_installable** un package Python. Il peut contenir des importations qui exposent des sous-packages ou des modules.
  
  - **utils.py** : Un module contenant des fonctions utilitaires qui peuvent être utilisées à travers le package.
  
  - **length/** et **weight/** : Ces deux dossiers représentent des sous-packages du package **cr_package_installable**. Chaque sous-package contient :
    
    - **__init__.py** : Ce fichier fait de chaque dossier un sous-package et peut être utilisé pour importer des fonctions ou modules spécifiques.
    
    - **core.py** : Contient les fonctions de conversion principales pour les unités de longueur ou de poids.
    
    - **api.py** : Fournit une interface utilisateur plus simple et plus intuitive pour appeler les fonctions du module `core.py`.

## Description du package cr_package_installable

**cr_package_installable** est un package permettant de convertir des unités impériales de longueur et de poids. Ce package a été créé dans le cadre du cours [DataCamp](https://www.datacamp.com) "Developing Python Packages".

### Fonctionnalités

- Convertir des longueurs entre miles, yards, pieds et pouces.
- Convertir des poids entre cental, stones, livres et onces.

### Utilisation

Voici comment utiliser le package **cr_package_installable** dans un script Python :

```python
import cr_package_installable

# Convertir 500 yards en pieds
result = cr_package_installable.length.convert_unit(500, from_unit='yd', to_unit='ft')  # renvoie 1500.0
print(result)

# Convertir 100 onces en livres
result = cr_package_installable.weight.convert_unit(100, from_unit='oz', to_unit='lb')  # renvoie 6.25
print(result)
```


## Place à la démo

Dans cette section, nous allons parcourir les étapes pour démarrer le développement de votre package **cr_package_installable**.

### 1. Création d'un répertoire GitHub

- Rendez-vous sur [GitHub](https://github.com/) et créez un nouveau dépôt nommé **cr_package_installable**. Ce dépôt contiendra tout le code de votre package.

### 2. Cloner le répertoire en local

- Une fois le dépôt créé, clonez-le en local sur votre machine à l'aide de la commande suivante dans votre terminal :

  ```bash
  git clone https://github.com/username/cr_package_installable.git
  ```

  Remplacez `username` par votre nom d'utilisateur GitHub.

### 3. Créer un environnement virtuel

- Une bonne pratique pour les projets Python est de travailler dans un environnement virtuel afin d'isoler les dépendances. Pour créer un environnement virtuel dans votre répertoire de travail, utilisez la commande suivante sous Linux :

  ```bash
  python3 -m venv .venv
  ```

### 4. Activer l'environnement virtuel

- Activez l'environnement virtuel avec la commande suivante (toujours sous Linux) :

  ```bash
  source .venv/bin/activate
  ```

  Cela vous permet de travailler avec des versions spécifiques de bibliothèques et de maintenir votre environnement de développement propre.

### 5. Ouvrir VSCode

- Lancez Visual Studio Code (VSCode) et ouvrez le répertoire **cr_package_installable** que vous avez cloné.

  ```bash
  code .
  ```

  Cela ouvrira le projet dans VSCode, où vous pouvez commencer à développer.

### 6. Créer la structure du package

- Créez tous les fichiers et dossiers nécessaires en suivant la structure décrite dans la section précédente du README. Assurez-vous que chaque fichier et sous-dossier est correctement positionné.

### 7. Développer le package

- Vous êtes maintenant prêt à commencer à coder ! Suivez les instructions ou la vidéo de démo pour développer les modules du package **cr_package_installable**.


## Commandes Linux pour démarrer

Voici les commandes Linux pour créer la structure hiérarchique du projet **cr_package_installable** en étant dans le répertoire principal de travail :

```bash
# Créer le dossier du package principal
mkdir cr_package_installable

# Créer les sous-dossiers "length" et "weight"
mkdir -p cr_package_installable/length
mkdir -p cr_package_installable/weight

# Créer les fichiers initiaux
touch cr_package_installable/__init__.py
touch cr_package_installable/utils.py
touch cr_package_installable/length/__init__.py
touch cr_package_installable/length/core.py
touch cr_package_installable/length/api.py
touch cr_package_installable/weight/__init__.py
touch cr_package_installable/weight/core.py
touch cr_package_installable/weight/api.py

# Créer les fichiers dans le répertoire principal
touch LICENSE # Il est préférable de générer ce fichier pendant la création du répertoire GitHub. J'ai choisi la licence MIT
touch MANIFEST.in
touch README.md # Il est préférable de générer ce fichier pendant la création du répertoire GitHub.
touch setup.py
touch example_script.py
```

