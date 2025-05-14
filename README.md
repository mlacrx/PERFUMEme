<img width="700" alt="logo" src="https://github.com/mlacrx/PERFUMEme/blob/main/assets/banner.png">

[![GitHub](https://img.shields.io/badge/github-%2395c5c6.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mlacrx/PERFUMEme)
[![](https://img.shields.io/badge/Python-%23fcd2de?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/badge/Jupyter-%23b39eb5.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/)

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


## 🧑‍💻 Installation 

Create a new environment, you can give an other name to this new environment. Then activate this environment
```bash
conda create -n fragrance python=3.10
```
```bash
conda activate fragrance
```
As the PERFUMEme package is dedicated for usage in a Jupyter Lab, you should install Jupyter Lab by executing the following command.
```bash
pip install jupyter lab
```

[![](https://img.shields.io/badge/pypi-%23FAC898?style=for-the-badge&logo=pypi&logoColor=black)](https://pypi.org/project/perfumeme/)

PERFUMEme can be then installed using pip as
```bash
pip install perfumeme
```
[![GitHub](https://img.shields.io/badge/github-%2395c5c6.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mlacrx/PERFUMEme)

As an alternative, the package can be installed directly from the GitHub repository by executing the following pip command in your terminal
```bash
pip install git+https://github.com/mlacrx/PERFUMEme
```

![](https://img.shields.io/badge/GIT-%23C6E5B1?style=for-the-badge&logo=git&logoColor=black)

The package can also be installed from source by executing the following steps:
First, clone the repository from GitHub and navigate into the project directory
```bash
git clone https://github.com/mlacrx/PERFUMEme.git
cd path/to/perfumeme
```
Then, install the package in editable mode using:
```bash
pip install -e .
```

## 📖 Requirements

The PERFUMEme package runs on python 3.10. 
Its correct use requires several other packages.
```bash
rdkit
pandas
numpy
matplotlib
requests
```

If the installation completes successfully, all those required packages should be installed automatically.
To verify that everything is correctly set up in your environment, you can list the installed packages by running the following command in your terminal:
```bash
conda list
```

If you don't see them, install them by running the following commands. You have to make sure they are installed, otherwise the package will not run.
```bash
pip install rdkit
pip install pandas
pip install numpy
pip install matplotlib
pip install requests
```

## 🔥 Usage

As you may have gathered, the PERFUMEme package is destinated for usage in Jupyter Lab. 
After installing the package and opening a Jupyter Notebook, you can use PERFUMEme to evaluate the olfactory and physicochemical profile of a molecule using its SMILES representation or its name.

This includes:

- Odor detectability
- Skin toxicity
- Evaporation modeling (vapor pressure, boiling point, vaporization enthalpy)
- Evaporation curve plot
- Perfume compatibility (note type)
- Perfumes in which the molecule appears

An example on how to make our key functions (usable_in_perfume and perfume_molecule) work is shown below for linalool. 

```bash
import perfumeme as pm

mol = "Linalool"

summary, plot_path = pm.usable_in_perfume(mol)
print (summary)

display(Image(filename=plot_path))
```

The output of this first command will be : 

<img width=400  alt = "linalool usable in perfume"  src = "https://github.com/mlacrx/perfumeme/blob/main/assets/linalool.png">

Now you can find out the presence of your molecule in famous fragrances and extract olfactory information.

```bash
import perfumeme as pm

mol = "Linalool"

pm.combination(mol)
```

The output of this second command will be : 


Now if you just want to obtain simple properties of the molecule (smell, toxic, vapor pressure, vapor pressure temperature, boiling point, enthalpy of vaporisation), you can use our small functions : has_a_smell, is_toxic_skin and evaporation_trace. 

To have information on smell :

```bash
import perfumeme as pm

mol = "Linalool"

pm.has_a_smell(mol)
```

The output of this command will be: True.

Information on toxicity : 

```bash
import perfumeme as pm

mol = "Linalool"

pm.is_toxic_skin(mol)
```

The output will be: True.

Informations on physical properties : 

```bash

from perfumeme.main_functions import evaporation_trace

molecule = "linalool"

vapor_pressure, boiling_point, vp_temp, enthalpy, image_path = evaporation_trace(molecule)

print(f"💨 Vapor Pressure: {vapor_pressure} mmHg")
print(f"🔥 Boiling Point: {boiling_point} °C")
print(f"🌡️ Vapor Pressure Measured at: {vp_temp} °C")
print(f"⚡ Enthalpy of Vaporization: {enthalpy} J/mol")
```

The output will be : 

💨 Vapor Pressure: 0.16 mmHg
🔥 Boiling Point: 194°C
🌡️ Vapor Pressure Measured at: 23.5 °C
⚡ Enthalpy of Vaporization: 51400 J/mol

## 🔧 Fixing issues

If you encounter an issue with the package’s functions, start by ensuring that you are using the latest version. You can do this by running the following command in your terminal:

```bash
pip show perfumeme
```

You can then compare your installed version with the latest available version listed on the PyPI page, https://pypi.org/project/perfumeme/

If your installed version is outdated, update it by running the following command in your terminal:

```bash
pip install perfumeme -U
```

## 🚀 Start 

Open a Jupyter Notebook and discover more about your favourite molecules ! 
Try it out and maybe… find your next signature scent!
