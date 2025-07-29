import os
from urllib.request import urlopen
import hashlib
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py


from setuptools import setup, find_packages

# Version will be read from your package's __init__.py
# Make sure __version__ is defined in imswitch/__init__.py
def get_version():
    version_file = 'ashlarUC2/__init__.py'
    with open(version_file, 'r') as file:
        for line in file:
            if line.startswith('__version__'):
                # Strip the line to remove whitespaces and newline characters,
                # then split the string by '=' and take the second part,
                # which is the version number. Finally, strip the quotes and any
                # additional whitespace or newline characters around the version number.
                version = line.strip().split('=')[1].strip().strip('\'"')
                return version
    raise RuntimeError("Version konnte nicht gefunden werden.")


requires = [
    'numpy>=1.18.1',
    'matplotlib>=3.1.2',
    'networkx>=2.4',
    'scipy>=1.4.1',
    'scikit-image>=0.19.2', # The v1.0 API promises breaking changes.<0.20
    'scikit-learn>=0.21.1',
    'tifffile>=2023.3.15',
    'zarr>=2.11.3',
    'blessed>=1.17' #'imagecodecs>=2021.6.8',
]

# get version from init file
VERSION =  get_version()
DESCRIPTION = ('Alignment by Simultaneous Harmonization of Layer/Adjacency '
               'Registration')
LONG_DESCRIPTION='''

ASHLAR: Alignment by Simultaneous Harmonization of Layer/Adjacency Registration

Ashlar implements efficient combined stitching and registration of multi-channel
image mosaics collected using the Tissue-CycIF microscopy protocol [1]_. Although
originally developed for CycIF, it may also be applicable to other tiled and/or
cyclic imaging approaches. The package offers both a command line script for the
most common use cases as well as an API for building more specialized tools.

.. [1] Tissue-CycIF is multi-round immunofluorescence microscopy on large fixed
   tissue samples. See https://doi.org/10.1101/151738 for details.

'''
AUTHOR = 'Jeremy Muhlich modified by Benedict Diederich'
AUTHOR_EMAIL = 'benedictdied@gmail.com'
LICENSE = 'MIT License'
HOMEPAGE = 'https://github.com/openuc2/ashlar'


class PreDevelop(develop):
    def run(self):
        develop.run(self)

class PreSdist(sdist):
    def run(self):
        sdist.run(self)

class PreBuildPy(build_py):
    def run(self):
        build_py.run(self)

cmdclass = {
    'develop': PreDevelop,
    'sdist': PreSdist,
    'build_py': PreBuildPy,
}

setup(
    name='ashlarUC2',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points={
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: %s' % LICENSE,
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=HOMEPAGE,
    download_url='%s/archive/v%s.tar.gz' % (HOMEPAGE, VERSION),
    keywords=['scripts', 'microscopy', 'registration', 'stitching'],
    zip_safe=False,
)
