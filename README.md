# Helium Positioning API

[![PyPI](https://img.shields.io/pypi/v/helium-positioning-api.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/helium-positioning-api.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/helium-positioning-api)][python version]
[![License](https://img.shields.io/pypi/l/helium-positioning-api)][license]

[![Read the documentation at https://helium-positioning-api.readthedocs.io/](https://img.shields.io/readthedocs/helium-positioning-api-api-api-api-api-api/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/emergotechnologies/helium-positioning-api/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/emergotechnologies/helium-positioning-api/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/helium-positioning-api/
[status]: https://pypi.org/project/helium-positioning-api/
[python version]: https://pypi.org/project/helium-positioning-api
[read the docs]: https://helium-positioning-api.readthedocs.io/
[tests]: https://github.com/emergotechnologies/helium-positioning-api/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/emergotechnologies/helium-positioning-api
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

Prediction of the location of devices belonging to an organization in the [Helium Console](https://console.helium.com/). 
Several different methods and models are available.

## Installation

### Developer install

The following allows a user to create a developer install of the positioning api.

```console
pip install -r requirements.txt
poetry install
poetry shell
pip install git+https://github.com/emergotechnologies/helium-api-wrapper
```

## Prerequisites

Before use, ensure that there is an `.env` file in the root directory of the repository where the `API_KEY` variable is entered (see `.env.sample`). You can generate and copy the `API_KEY` at https://console.helium.com/profile.

## Usage

The service allows usage via **command line interface** or locally hosted **REST interface**.

### CLI

**Get Device Position**

```
python -m helium_positioning_api predict --uuid 92f23793-6647-40aa-b255-fa1d4baec75d
```

Currently defaults to the "nearest_neighbor" model.

**Advanced Requests**

The location prediction command is

```
python -m helium_positioning_api predict --uuid 'your uuid' --model 'your model selection'
```

See the table below for a list of currently available models.

| **model**       | **position estimation explanation**                                   |
| ----------------- | ------------------------------------------------------------------- |
| nearest_neighbor  | location of hotspot with the best signal                            |
| midpoint          | point of equal distance from the two hotspots with the best signals |
| linear_regression | trilateration with an linear regression distance estimator          |
| gradient_boosting | trilateration with a gradient boosted regression distance estimator |

### REST-API

1. Start local REST-API (default)
   ```
   python -m helium_positioning_api serve
   ```
2. Open Browser and navigate to `127.0.0.1:8000/docs`
3. Click on `predict_tf` path to drop down the endpoint details
4. Click on the `Try it out` button.
5. Fill in the `uuid` of your device and click on the button `Execute` to get an estimation using the `nearest_neighbor` model
6. You can see the location prediction response in the `Responses` section below.

The mapping of available models to paths can be seen in the table below.

| **model**         | **path**                                                            |
| ----------------- | ------------------------------------------------------------------- |
| nearest_neighbor  | predict_tf                                                          |
| midpoint          | predict_mp                                                          |
| linear_regression | predict_tl_lin                                                      |
| gradient_boosting | predict_tl_grad                                                     |

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Helium Positioning API_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/emergotechnologies/helium-positioning-api/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/emergotechnologies/helium-positioning-api/blob/main/LICENSE
[contributor guide]: https://github.com/emergotechnologies/helium-positioning-api/blob/main/CONTRIBUTING.md
[command-line reference]: https://helium-positioning-api.readthedocs.io/en/latest/usage.html
