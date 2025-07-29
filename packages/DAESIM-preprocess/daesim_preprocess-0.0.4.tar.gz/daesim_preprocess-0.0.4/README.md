# DAESIM_preprocess
Harvesting environmental forcing data for running the Dynamic Agro-Ecosystem Simulator (DAESIM)


# Setup locally
1. Download and install Miniconda from https://www.anaconda.com/download/success
2. Add the miniconda filepath to your ~/.zhrc, e.g. export PATH="/opt/miniconda3/bin:$PATH" 
3. brew install gdal
4. git clone https://github.com/ChristopherBradley/DAESIM_preprocess.git
5. cd DAESIM_preprocess
6. conda env create -f environment.yml
7. conda activate DAESIM_preprocess
8. pytest

- If in future there is an issue with dependency conflicts, then try creating a new python environment in 3.11 and using the requirements.txt which has fixed versions (instead of just using the latest version with pyproject.toml).
  - conda create --name DAESIM_preprocess_3.11 python=3.11
  - conda activate DAESIM_preprocess_3.11
  - pip install -r requirements.txt

# Uploading to pypi
1. python3 -m build
2. twine upload dist/*
3. Enter the API token
4. Check it out at https://pypi.org/project/DAESIM-preprocess