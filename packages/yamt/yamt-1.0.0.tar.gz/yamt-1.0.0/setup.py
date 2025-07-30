# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yamt',
    'version': '1.0.0',
    'description': 'yet another monkey toolkit',
    'long_description': '# yamt (yet another monkey toolkit)\n[![PyPI version](https://badge.fury.io/py/yamt.svg)](https://badge.fury.io/py/yamt)\n![PyPI downloads per mounth](https://img.shields.io/pypi/dm/yamt)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/UT1C/yamt)\n\n## Installation\n```\npip install yamt\n```\n',
    'author': 'lightmanLP',
    'author_email': 'liteman1000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
