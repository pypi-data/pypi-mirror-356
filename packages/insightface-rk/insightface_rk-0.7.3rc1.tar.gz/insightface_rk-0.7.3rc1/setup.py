#!/usr/bin/env python
import os
import io
import glob
import numpy
import re
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

def read(*names, **kwargs):
    with io.open(os.path.join(os.path.dirname(__file__), *names),
                 encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

short_description = 'Enhanced face analysis package with frontal face detection and filtering largest face / small faces'
try:
    long_description = open('README.md').read()
except:
    long_description = short_description

requirements = [
    'numpy>=2.3.0',
    'onnx>=1.18.0',
    'onnxruntime>=1.22.0',
    'tqdm>=4.67.1',
    'requests>=2.32.3',
    'matplotlib>=3.10.3',
    'opencv-python>=4.11.0.86',
    'scikit-image>=0.25.2',
    'easydict',
    'cython>=3.1.2',
    'albumentations>=2.0.8',
    'prettytable',
]

extensions = [
    Extension(
        'insightface.thirdparty.face3d.mesh.cython.mesh_core_cython',
        ['insightface/thirdparty/face3d/mesh/cython/mesh_core_cython.pyx',
         'insightface/thirdparty/face3d/mesh/cython/mesh_core.cpp'],
        include_dirs=[numpy.get_include()],
        language='c++'
    )
]

data_images = list(glob.glob('insightface/data/images/*.jpg'))
data_images += list(glob.glob('insightface/data/images/*.png'))

data_mesh = list(glob.glob('insightface/thirdparty/face3d/mesh/cython/*.h'))
data_mesh += list(glob.glob('insightface/thirdparty/face3d/mesh/cython/*.c'))
data_mesh += list(glob.glob('insightface/thirdparty/face3d/mesh/cython/*.py*'))

data_objects = list(glob.glob('insightface/data/objects/*.pkl'))

data_files = [
    ('insightface/data/images', data_images),
    ('insightface/data/objects', data_objects),
    ('insightface/thirdparty/face3d/mesh/cython', data_mesh)
]

package_data = {
    'insightface': [
        'data/images/*.jpg',
        'data/images/*.png',
        'data/objects/*.pkl'
    ]
}

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='insightface-rk',
    version=find_version('insightface', '__init__.py'),
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rikkeisoft - MinhNTT3, Rikkeisoft - LinhPD2',
    author_email='minhntt3@rikkeisoft.com, linhpd2@rikkeisoft.com',
    url='https://github.com/minhntt3-rikkei/insightface-rk',
    license='MIT',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    package_data=package_data,
    cmdclass={'build_ext': build_ext},
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=classifiers,
    keywords='face detection recognition insightface computer-vision machine-learning',
    data_files=data_files,
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()],
    zip_safe=True,
    include_package_data=True,
)