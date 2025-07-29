# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rdp']
install_requires = \
['cython==3.0.12', 'numpy==1.21.1', 'wheel==0.41.0']

setup_kwargs = {
    'name': 'rdp-package',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
