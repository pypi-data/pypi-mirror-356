# ExoRM

ExoRM is a model for the mass of an exoplanet given the radius

- HomePage: https://github.com/kzhu2099/ExoRM
- Issues: https://github.com/kzhu2099/ExoRM/issues

[![PyPI Downloads](https://static.pepy.tech/badge/ExoRM)](https://pepy.tech/projects/ExoRM)

Author: Kevin Zhu

## Features

- continuous radius-mass relationship
- smooth with lower residuals
- simple usage, log10 and linear
- method to create your own model
- prediction interval

## Installation

To install ExoRM, use pip: ```pip install ExoRM```.

However, many prefer to use a virtual environment (or any of their preferred choice).

macOS / Linux:

```sh
# make your desired directory
mkdir /path/to/your/directory
cd /path/to/your/directory

# setup the .venv (or whatever you want to name it)
pip install virtualenv
python3 -m venv .venv

# install ExoRM
source .venv/bin/activate
pip install ExoRM

deactivate # when you are completely done
```

Windows CMD:

```sh
# make your desired directory
mkdir C:path\to\your\directory
cd C:path\to\your\directory

# setup the .venv (or whatever you want to name it)
pip install virtualenv
python3 -m venv .venv

# install ExoRM
.venv\Scripts\activate
pip install ExoRM

deactivate # when you are completely done
```

## Usage

To first begin using ExoRM, the data and model must be initialized. This is due to the constant discovery of new exoplanets, adding to the data. You may also call these at any time to update the model.

Simply run `get_data()` and `initialize_model()`. Note: import those by using `from ExoRM.get_data import get_data()` and `from ExoRM.initialize_model() import initialize_model()`. A plot of the model will be shown for you to see. Both are stored in your OS's Application Data for ExoRM. ExoRM provides built in functions to retrieve from this folder.

To use the model, call `ExoRM.load_model()` which returns the model from the filepath. If you wish, you may use `model.save(...)` to save it to your own directory.

Note that all files saved are located in `/Users/<username>/Library/Application Support/ExoRM` for macOS and `C:\Users\<username>\AppData\Local\ExoRM\ExoRM` for windows.

The model supports log10 and linear scale in earth radii. When using the `model([...]), .__call__([...]), or .predict([...])`, the log10 scale is used. Linear predictions are used in `.predict_linear([...])`.

The high amount of uncertainty can be accessed from ExoRM. An exponential curve fit is used to estimate the squared errors, and square root of the model at any point is the RMSE (standard deviation of the errors). Generally, the log error increases as the log radius increases. Estimate the error by using `model.error([...])` and `model.linear_error([...])`, which returns the 2nd standard deviation, with a smooth transition to the 3rd during extrapolations.

An example is seen in the `example.ipynb`. Deep analysis is seen in `comparison.ipynb`, showing statistical results and a comparison with Forecaster.

## Additional notes

ExoRM has an implementation of Forecaster for according to the NASA Exoplanet Archive.

Forecaster: https://github.com/chenjj2/forecaster
NASA Exoplanet Archive implementation: https://exoplanetarchive.ipac.caltech.edu/docs/pscp_calc.html

## License

The License is an MIT License found in the LICENSE file.