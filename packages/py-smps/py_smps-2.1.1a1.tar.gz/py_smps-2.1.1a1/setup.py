# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['smps']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.3,<2.0',
 'matplotlib>=3.4,!=3.6.1',
 'numpy>1.20,!=1.24.0',
 'pandas>=1.2',
 'requests>=2.0',
 'scipy>1.7',
 'seaborn>=0.12',
 'setuptools>48.0',
 'statsmodels>=0.13.0']

setup_kwargs = {
    'name': 'py-smps',
    'version': '2.1.1a1',
    'description': 'A simple python library to import and visualize data from particle sizing instruments',
    'long_description': "[![PyPI version](https://badge.fury.io/py/py-smps.svg)](https://badge.fury.io/py/py-smps)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Coverage Status](https://coveralls.io/repos/github/dhhagan/py-smps/badge.svg?branch=master)](https://coveralls.io/github/dhhagan/py-smps?branch=master)\n[![ci.tests](https://github.com/quant-aq/py-smps/actions/workflows/test-and-report.yml/badge.svg)](https://github.com/quant-aq/py-smps/actions/workflows/test-and-report.yml)\n\n\n# py-smps\n\npy-smps is a Python data analysis library built for analyzing size-resolved aerosol data from a variety of aerosol sizing instruments (e.g., Scanning Mobility Particle Sizer, Optical Particle Counters).\n\n\n**NOTE: As of `v1.2.0`, the library is compatible with Apple silicone (M1, M2 chips).**\n\n# Installation\n\nOfficial releases of `py-smps` can be installed from [PyPI](https://pypi.org/project/py-smps/):\n\n    $ pip install py-smps [--upgrade]\n\nIf you'd like the latest pre-release:\n\n    $ pip install py-smps --pre [--upgrade]\n\nTo install the edge release directly from GitHub:\n\n    pip install git+https://github.com/quant-aq/py-smps.git\n\n# Dependencies\n\n## Supported Python versions\n- Python 3.8+\n\n## Mandatory Dependencies\n\nThe full list of dependencies can be found in the [`pyproject.toml`](pyproject.toml) file.\n\n# Development\n\n## Testing\n\nTests can be run by issuing the following command from within the main repo:\n\n```sh\n$ poetry run pytest -s tests/ --ignore=tests/datafiles\n```\n\n## Contributing to Development\n\nWe welcome all contributions from the community in the form of issues reporting, feature requests, bug fixes, etc.\n\nIf there is a feature you would like to see or a bug you would like to report, please open an issue. We will try to get to things as promptly as possible. Otherwise, feel free to send PR's!\n\n### Contributors\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\n\n# Documentation\n\nDocumentation is available [here](https://quant-aq.github.io/py-smps/). To build locally, you must first install [pandoc](https://pandoc.org/). Docs are built using Sphinx and can be built locally by doing the following:\n\n```sh\n# Activate the virtualenv\n$ poetry shell\n\n# Build the docs\n$ cd docs/\n$ make clean\n$ make html\n$ cd ..\n```\n\nThen, you can navigate to your local directory at `docs/build/html/` and open up the `index.html` file in your preferred browser window.\n",
    'author': 'David H Hagan',
    'author_email': 'david.hagan@quant-aq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/quant-aq/py-smps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
