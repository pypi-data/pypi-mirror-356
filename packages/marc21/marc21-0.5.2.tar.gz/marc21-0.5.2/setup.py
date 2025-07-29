from setuptools import setup, find_packages

setup(
    name='marc21',
    version='0.5.2',
    description='library to create bibliographic MARC21 records',
    url='https://github.com/jwvdvuurst/marc21.git',
    author='John van der Vuurst',
    author_email='jwvdvuurst@gmail.com',
    packages=find_packages(include=['marc21', 'marc21.*']),
    install_requires=[],
    python_requires='>=3.10',
)