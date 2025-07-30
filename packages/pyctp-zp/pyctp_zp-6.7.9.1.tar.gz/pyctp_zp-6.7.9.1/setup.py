from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            relpath = os.path.relpath(os.path.join(path, filename), 'pyctp_zp')
            paths.append(relpath)
    return paths

cppyctp_files = package_files('pyctp_zp/CPPyCTP')
pyctp_files = package_files('pyctp_zp/PyCTP')

setup(
    name='pyctp-zp',
    version='6.7.9.1',
    author='luochenyeling',
    author_email='zhaokehan86@163.com',
    description='CTP Python接口，支持行情和交易，兼容PyCTP和CPPyCTP',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'pyctp_zp': cppyctp_files + pyctp_files,
    },
    include_package_data=True,
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    url='https://pypi.org/project/pyctp-zp/',
) 