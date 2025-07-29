# DAESIM_preprocess
Harvesting environmental forcing data for running the Dynamic Agro-Ecosystem Simulator (DAESIM). 

# Jupyter Notebook Examples
I've made some demo notebooks and these can all be run directly in Google Colab like this:  

Click [Google Colab](https://colab.google/) > Open Colab > Sign In (just requires a google account) > GitHub >   
search for 'ChristopherBradley' and select a notebook.
- [ozwald_daily.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/ozwald_daily.ipynb)
- [ozwald_8day.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/ozwald_8day.ipynb)
- [silo_daily.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/silo_daily.ipynb)
- [slga_soils.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/slga_soils.ipynb)
- [terrain_tiles.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/terrain_tiles.ipynb)
- [topography.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/topography.ipynb)
- [daesim_forcing.ipynb](https://github.com/ChristopherBradley/DAESIM_preprocess/blob/main/notebooks/daesim_forcing.ipynb)

Then uncomment the line '!pip install daesim-preprocess' and run each cell in sequence (or click 'Run all').

# Available Variables
**ozwald_8day.py** can download these variables modelled at 500m spatial and 8 day temporal resolution, from the Australian Water and Landscape Dynamics ([OzWALD](https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f9589_2733_2545_4343)).
- Alb: Albedo 
- BS: Bare Surface  
- EVI: Enhanced Vegetation Index  
- FMC: Fuel Moisture Content  
- GPP: Gross Primary Productivity  
- LAI: Leaf Area Index  
- NDVI: Normalised Difference Vegetation Index  
- NPV: Non Photosynthetic Vegetation  
- OW: Open Water  
- PV: Photosynthetic Vegetation  
- Qtot: Streamflow  
- SN: Snow  
- Ssoil: Soil profile moisture change  

**ozwald_daily.py** can download these climate variables modelled at varying spatial resolutions (500m-5km depending on the variable) and daily temporal resolution, also from OzWald. 
- Pg : Gross precipitation     
- Tmax : Maximum temperature       
- Tmin : Minimum temperature      
- Uavg : Average 24h windspeed     
- Ueff : Effective daytime windspeed  
- VPeff : Volume of effective rainfall 
- kTavg : Coefficient to calculate mean screen level temperature  
- kTeff : Coefficient to calculate effective screen level temperature

**silo_daily.py** can download these climate variables modelled at 5km resolution daily, from Scientific Information for LandOwners ([SILO](https://www.longpaddock.qld.gov.au/silo/)).
- daily_rain: Daily rainfall, mm  
- monthly_rain: Monthly rainfall, mm  
- max_temp: Maximum temperature, degrees Celsius  
- min_temp: Minimum temperature, degrees Celsius  
- vp: Vapour pressure, hPa  
- vp_deficit: Vapour pressure deficit, hPa  
- evap_pan: Class A pan evaporation, mm 
- evap_syn: Synthetic estimate, mm
- evap_morton_lake: Morton's shallow lake evaporation, mm  
- radiation: Solar radiation: Solar exposure, consisting of both direct and diffuse components, MJ/m2  
- rh_tmax: Relative humidity at the time of maximum temperature, %  
- rh_tmin: Relative humidity at the time of minimum temperature, %  
- et_short_crop: Evapotranspiration FAO564 short crop, mm  
- et_tall_crop: ASCE5 tall crop6, mm  
- et_morton_actual: Morton's areal actual evapotranspiration, mm  
- et_morton_potential: Morton's point potential evapotranspiration, mm  
- et_morton_wet: Morton's wet-environment areal potential evapotranspiration over land, mm  
- mslp: Mean sea level pressure Mean sea level pressure, hPa  

**slga_soils.py** can download these soil variables modelled at 90m resolution from the Soils and Landscape Grid of Australia ([SLGA](https://esoil.io/TERNLandscapes/Public/Pages/SLGA/index.html)).
- Clay  
- Silt  
- Sand  
- pH_CaCl2  
- Bulk_Density  
- Available_Water_Capacity  
- Effective_Cation_Exchange_Capacity  
- Total_Nitrogen  
- Total_Phosphorus  

**terrain_tiles.py** can download global elevation data from various sources at minimum 30m resolution, rescaled to 10m resolution by using tile level 14 ([Terrain Tiles](https://github.com/tilezen/joerd/blob/master/docs/data-sources.md)).
- elevation  

**topography.py** can download these derived topographic information mainly using ([pysheds](https://mattbartos.com/pysheds/)).
- slope  
- aspect  
- accumulation  
- topographic wetness index (TWI)  

# Available Parameters
The functions in this repo use mostly the same inputs for consistency. All parameters have default values to make the functions easier to use and help with debugging. 

| Function          | Parameters                                                                                          |
|-------------------|-----------------------------------------------------------------------------------------------------|
| **ozwald_8day**   | variables, lat, lon, buffer, start_year, end_year, outdir, stub, tmpdir, thredds, save_netcdf, plot |
| **ozwald_daily**  | variables, lat, lon, buffer, start_year, end_year, outdir, stub, tmpdir, thredds, save_netcdf, plot |
| **silo_daily**    | variables, lat, lon, buffer, start_year, end_year, outdir, stub, tmpdir, thredds, save_netcdf, plot |
| **slga_soils**    | variables, lat, lon, buffer, outdir, stub, tmpdir, depths                                           |
| **terrain_tiles** | lat, lon, buffer, outdir, stub, tmpdir, tile_level, interpolate                                     |
| **topography**    | outdir, stub, ds, smooth, sigma, savetifs, plot                                                     |
| **daesim_forcing**| outdir, stub                                                                                        |


# Parameter Descriptions
This is the meaning of each parameter.

| Parameter   | Default                 | Description   
|-------------|-------------------------|-------------------------------------------------------------|
| variables   | depends on the function | List of variables to download                               |
| lat         | -34.389                 | Latitude from google maps (EPSG:4326)                       |
| lon         | 148.469                 | Longitude from google maps (EPSG:4326)                      |
| buffer      | 0.01 or 0.1             | Buffer in degrees in each direction (so 0.01 ~= 2km x 2km)  |
| start_year  | 2020                    | Temporal data starts from Jan 1 of this year                |
| end_year    | 2021                    | Temporal data ends on Dec 31 of this year                   |
| outdir      | "." (current directory) | The directory for the final outputs                         |
| stub        | "TEST"                  | The name that gets prepended to each file                   |
| tmpdir      | "." (current directory) | The directory for temporary intermediate files              |
| thredds     | True                    | Boolean to use the public facing Thredds API                |
| save_netcdf | True                    | Boolean to save the final result to file                    |
| plot        | True                    | Boolean to generate output png images                       |

The extra parameters for slga_soils, terrain_tiles and topography are documented in the relevant python files.

# Return Types
Data is returned as an xarray DataSet and downloaded as NetCDF (.nc), tif, and/or png files. 

# Usage
This is the basic pattern for using each function. More comprehensive examples are in the notebooks and tests.
```
pip install DAESIM_preprocess  

from DAESIM_preprocess.ozwald_daily import ozwald_daily # (or another function)  
variables = [Tmax, Tmin]                                # (or other variables)  
lat, lon, buffer = -34.38, 148.46, 0.01                 # (or another location)  
ds = ozwald_daily(variables, lat, lon, buffer)  
```

# Running Locally
1. Download and install Miniconda from https://www.anaconda.com/download/success
2. Add the miniconda filepath to your ~/.zhrc, e.g. export PATH="/opt/miniconda3/bin:$PATH" 
3. `brew install gdal`
4. `git clone https://github.com/ChristopherBradley/DAESIM_preprocess.git`
5. `cd DAESIM_preprocess`
6. `conda env create -f environment.yml`
7. `conda activate DAESIM_preprocess`
8. `jupyter lab` (to run the example notebooks like on google colab)

# Running via Command Line
After completing steps 1-7 of running locally, you can run each of the scripts directly via the command line. For example: 
```
python ozwald_8day.py   --variable Ssoil    --lat -34.389 --lon 148.469 --buffer 0.01 --start_year 2020 --end_year 2021  # etc.
python ozwald_daily.py  --variable Tmin     --lat -34.389 --lon 148.469 --buffer 0.01 --start_year 2020 --end_year 2021  # etc.
python silo_daily.py    --variable min_temp --lat -34.389 --lon 148.469 --buffer 0.01 --start_year 2020 --end_year 2021  # etc.
python slga_soils.py    --variable Clay     --lat -34.389 --lon 148.469 --buffer 0.01  # etc.
python terrain_tiles.py --lat -34.389 --lon 148.469 --buffer 0.01  # etc.
python topography.py    --outdir '.'  --stub TEST  # etc.
```
The main differences when running from the command line are that you can only specify a single variable at a time, and the boolean default is False. This is documented in each python file, and you can also use `python ozwald_8day.py --help` to see info about the available parameters for each function from the command line.

# Testing
After completing steps 1-7 of running locally, you can check the setup is working correctly by running the tests. Currently the tests are run with `python tests/test_local.py`, but I'm about to change this to use pytest instead... Sometimes the API's can be a bit temperamental, especially the SLGA, so you may need to wait a while and try the test again.

# Uploading to PyPI
Just a note for myself when I need to republish the library.
1. python3 -m build
2. twine upload dist/*
3. Enter the API token
4. Check it out at https://pypi.org/project/DAESIM-preprocess

# References
Each data source is referenced in the source code, jupyter notebooks, and there is a complete list here:
...