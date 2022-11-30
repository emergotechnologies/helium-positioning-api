# Helium Positioning API

[![PyPI](https://img.shields.io/pypi/v/helium-positioning-api.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/helium-positioning-api.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/helium-positioning-api)][python version]
[![License](https://img.shields.io/pypi/l/helium-positioning-api)][license]

[![Read the documentation at https://helium-positioning-api.readthedocs.io/](https://img.shields.io/readthedocs/helium-positioning-api-api-api-api-api-api/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/g4challenge/helium-positioning-api-api/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/g4challenge/helium-positioning-api/branch/main/graph/badge.svg)][codecov]

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

- TODO

## Requirements

- TODO

## Installation

You can install _Helium Positioning API_ via [pip] from [PyPI]:

```console
$ pip install helium-positioning-api
```

### Developer install

The following allows a user to create a developer install of the positioning.

You need to create a `.env` file for now and add the `API_KEY=XXX` from Helium Console to the file.

```console
pip install git+https://github.com/emergotechnologies/helium-api-wrapper
pip install .
# Test with Device
python -m helium_positioning_api predict --uuid 92f23793-6647-40aa-b255-fa1d4baec75d
```

## Usage

Please see the [Command-line Reference] for details.

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
