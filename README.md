<img width="830" alt="logo" src="https://github.com/mlacrx/PERFUMEme/blob/main/assets/banner.png">

[![GitHub](https://img.shields.io/badge/github-%2395c5c6.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mlacrx/PERFUMEme)
[![Python](https://img.shields.io/badge/Python-%23fcd2de?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-%23b39eb5.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)] (https://jupyter.org/)

# -         PERFUMEme      - 

[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=blue)](https://www.python.org)
[![](https://img.shields.io/badge/Contributors-3-purple.svg)](https://github.com/mlacrx/PERFUMEme/graphs/contributors)
[![](https://img.shields.io/badge/License-MIT-pink.svg)](https://github.com/mlacrx/PERFUMEme/blob/main/LICENSE)

 - Python Package for analysis of odorous molecules giving main properties

## ⚛️  Package description

PERFUMEme is a Python package designed to evaluate the suitability of molecules for use in perfumes. Combining cheminformatics, volatility modeling, and cosmetic safety criteria, it helps determine whether a compound has an odor, is safe for skin contact, and evaporates at a rate consistent with fragrance formulation (top, heart, or base note). It also tells in which famous perfumes the molecule is present.

Whether you're a fragrance formulator, a cosmetic chemist, or simply curious about scent molecules, PERFUMEme brings together data from PubChem and evaporation theory to support informed and creative olfactory design.

Creators : 
- Marie Lacroix, student in chemistry at EPFL [![jhc github](https://img.shields.io/badge/GitHub-mlacrx-181717.svg?style=flat&logo=github&logoColor=pink)](https://github.com/mlacrx) 
- Lilia Cretegny, student in chemistry at EPFL [![jhc github](https://img.shields.io/badge/GitHub-lilia--crtny-181717.svg?style=flat&logo=github&logoColor=pink)](https://github.com/lilia-crtny) 
- Coline Lepers, student in chemistry at EPFL  [![jhc github](https://img.shields.io/badge/GitHub-clepers-181717.svg?style=flat&logo=github&logoColor=pink)](https://github.com/clepers) 



## ⚒️ Installation 



## 🔥 Usage

```python
from mypackage import main_func

# One line to rule them all
result = main_func(data)
```

This usage example shows how to quickly leverage the package's main functionality with just one line of code (or a few lines of code). 
After importing the `main_func` (to be renamed by you), you simply pass in your `data` and get the `result` (this is just an example, your package might have other inputs and outputs). 
Short and sweet, but the real power lies in the detailed documentation.

## 👩‍💻 Installation

Create a new environment, you may also give the environment a different name. 

```
conda create -n perfume_package python=3.10 
```

```
conda activate perfume_package
(conda_env) $ pip install .
```

If you need jupyter lab, install it 

```
(perfume_package) $ pip install jupyterlab
```


## 🛠️ Development installation

Initialize Git (only for the first time). 

Note: You should have create an empty repository on `https://github.com:mlacrx/perfume-package`.

```
git init
git add * 
git add .*
git commit -m "Initial commit" 
git branch -M main
git remote add origin git@github.com:mlacrx/perfume-package.git 
git push -u origin main
```

Then add and commit changes as usual. 

To install the package, run

```
(perfume_package) $ pip install -e ".[test,doc]"
```

### Run tests and coverage

```
(conda_env) $ pip install tox
(conda_env) $ tox
```



