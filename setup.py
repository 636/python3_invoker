# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="invoker",
    version="1.0.2",
    author='636',
    author_email='zx6r.636a1@gmail.com',
    description='Invoker utility for DI(Injector) and context configuration.',
    url='https://github.com/636/python3_invoker',
    packages=find_packages(),
    install_requires=["injector==0.14.1", "pyyaml>=4.2b1"],
    extras_require={
        "develop": ["autopep8", "pep8"]
    },
    entry_points={
        "console_scripts": [
            "invoker = invoker.cmd:execute"
        ],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6'
    ],
)
