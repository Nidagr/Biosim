from setuptools import setup
import codecs
import os


def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
    # Basic information
    name='biosim',

    # Packages to include
    packages=['biosim'],

    # Metadata
    description='Simulation of the Rossumøya island',
    long_description=read_readme(),
    authors ='Nida Grønbekk and Yuliia Dzihora',
    authors_emails ='nida.gronbekk@nmbu.no and yuliia.dzihora@nmbu.no',
    url='https://gitlab.com/nmbu.no/emner/inf200/h2020/januaryblock/dga2/g06_dzihora_gronbekk',
    keywords='island simulation',
    license='MIT Licence',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Science :: Stochastic processes',
        'License :: OSI Approved :: MIT Licence',
        'Programming Language :: Python :: 3.8',
    ]
)