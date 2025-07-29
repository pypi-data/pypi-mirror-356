<div align="center">
<a href='https://moonpies.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/moonpies/badge/?version=latest'
    alt='Moonpies Documentation' />
</a>
<a href="https://zenodo.org/badge/latestdoi/399214580">
    <img src="https://zenodo.org/badge/399214580.svg" 
    alt="DOI">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg"
    alt="Code Style: Black" />
</a>
</div>

# MoonPIES: Moon Polar Ice and Ejecta Stratigraphy

Welcome to the *Moon Polar Ice and Ejecta Stratigraphy* (MoonPIES) model.

Please direct bug reports or code feedback to the GitHub [issues board](https://github.com/cjtu/moonpies/issues) or general inquiries to Christian at [cjtu@nau.edu](mailto:cjtu@nau.edu).

## Motivation

MoonPIES models ice and ejecta at depth below lunar polar cold traps. With the imminent return of humans to the Moon through the NASA Artemis program, models like ours will inform future exploration for water ice and other lunar resources.

## Installing MoonPIES

The easiest way to get MoonPIES is with pip:

```python
pip install moonpies
```

It is currently tested on Python version 3.8+ for Windows, OS X and Linux.

To install for development, you will require [Poetry](https://python-poetry.org/). Fork this repository and then from the main moonpies folder, install the dev environment with:

```python
poetry install
```

The environment can then be activated in the shell with `poetry shell` (see [poetry docs](https://python-poetry.org/docs/cli/) for more info).

## Running the model

The MoonPIES model can be run directly from the terminal / command line with the `moonpies` command. Run `moonpies --help` for options.


### Random seeds

MoonPIES is designed to be reproducable when given the same random seed and input parameters (on a compatible version). By default, MoonPIES will choose a random seed in [1, 99999]. Specify a particular seed with:

```bash
moonpies 1958
```

### Configuring a run

MoonPIES functionality is easy to tweak by specifying any of its large list of input parameters. A configuration file can be specified as a `.py` file containing a single Python dictionary. For example, to change the output directory of a run, create a file called `myconfig.py` containing:

```python
{
    'out_path': '~/Downloads/'
}
```

And supply the config file when running the model:

```bash
moonpies --cfg myconfig.py
```

See the [documentation](https://moonpies.readthedocs.io) for a full list of parameters that can be supplied in a `config.py` file.

### Using MoonPIES in Python code

MoonPIES can be run directly from Python by importing the `moonpies` module and calling the `main()` function:

```Python
import moonpies
model_out = moonpies.main()
```

To specify custom configuration options, create a custom `Cfg` object provided by `config.py` and pass it to `moonpies.main()`. Any parameter in `config.Cfg()` can be set as an argument like so:

```Python
import config
custom_cfg = config.Cfg(solar_wind_ice=False, out_path='~/Downloads')
cannon_model_out = moonpies.main(custom_cfg)
```

Unspecified arguments will retain their defaults. Consult the full API documentation for a description of all model parameters.

### Outputs

MoonPIES outputs are saved by today's date, the run name, and the random seed (e.g. `out/yymmdd/run/#####/`, where `#####` is the 5-digit random seed used. For example, a seed of 1958 will produce:

```bash
out/
|- yymmdd/
|  |- moonpies_version/
|  |  |- 01958/
|  |  |  |- ej_columns_mpies.csv
|  |  |  |- ice_columns_mpies.csv
|  |  |  |- config_mpies.py
|  |  |  |- strat_Amundsen.csv
|  |  |  |- strat_Cabeus B.csv
|  |  |  |- strat_Cabeus.csv
|  |  |  |- ...
```

The output directory will contain a `config_<run_name>.py` file which will reproduce the outputs if supplied as a config file to MoonPIES. Resulting stratigraphy columns for each cold trap are contained within the `strat_...` CSV files. Two additional CSVs with ejecta and ice columns over time show the raw model output (before outputs are collapsed into stratigraphic sequences).

**Note:** Runs with the same run name, date and random seed will overwrite one another. When tweaking config parameters, remember to specify a descriptive `run_name` to ensure a unique output directory.

### Note on versioning

As a Monte Carlo model, MoonPIES deals with random variation but is designed to be reproducible such that a particular random seed will produce the same set of random outcomes in the model. MoonPIES uses semantic versioning (e.g. major.minor.patch). Major version changes can include API-breaking changes, minor version changes will not break the API (but may break random seed reproducibility), while patch version change should preserve both the API and random seed reproducibility.

## Monte Carlo method

MoonPIES is a Monte Carlo model, meaning outputs can vary significantly from run to run. Therefore, no single MoonPIES result should be thought of as the true stratigraphy of a polar cold trap. Rather, the model should be run many times (with many random seeds) to build statistical confidence in the distribution of ice below polar cold traps.

### Running with gnuparallel (Linux/Mac/WSL only)

To quickly process many MoonPIES runs in parallel, one can use [GNU parallel](https://www.gnu.org/software/parallel/) which is available from many UNIX package managers, e.g.:

```bash
apt install parallel  # Ubuntu / WSL
brew install parallel  # MacOS
```

**Note:** Not tested on Windows. On MacOS, requires homebrew first (see [brew.sh](https://brew.sh/)).

Now, many iterations of the model may be run in parallel. To spawn 100 runs:

`seq 100 | parallel -P-1 moonpies`

This example will start 100 runs of MoonPIES, with random seeds 1-100. To configure your `parallel` runs:

- The number of runs is given by the `seq N` parameter (for help see [seq](https://www.unix.com/man-page/osx/1/seq/)).
- By default, `parallel` will use all available cores on your system. Specifying `-P-1` instructs GNU parallel to use all cores except one (`P-2` would use all cores except 2, etc).

## Plotting outputs

Some functions are provided to help visualize model outputs

*Coming soon!*

## Authors

This model was produced by C. J. Tai Udovicic, K. Frizzell, K. Luchsinger, A. Madera, and T. Paladino with input from M. Kopp, M. Meier, R. Patterson, F. Wroblewski, G. Kodikara, and D. Kring.

## License and Referencing

This code is made available under the [MIT license](https://choosealicense.com/licenses/mit/) which allows warranty-free use with proper citation. The model can be cited as:

> Tai Udovicic et al. (2022). Moonpies (vX.Y.Z). Zenodo. doi: 10.5281/zenodo.7055800

See [CITATION.cff](https://github.com/cjtu/moonpies/blob/main/CITATION.cff) or [MoonPIES on zenodo](https://doi.org/10.5281/zenodo.7055799) for easy import to any reference manager.

## Acknowledgements

This model was produced during the 2021 LPI Exploration Science Summer Intern Program which was supported by funding from the Lunar and Planetary Institute ([LPI](https://lpi.usra.edu)) and the Center for Lunar Science and Exploration ([CLSE](https://sservi.nasa.gov/?team=center-lunar-science-and-exploration)) node of the NASA Solar System Exploration Research Virtual Institute ([SSERVI](https://sservi.nasa.gov/)).
