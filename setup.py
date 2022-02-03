from setuptools import setup, find_packages


setup(
    name='kenda',
    version="0.0.1",
    packages=find_packages(),
    author="ipooters",
    author_email="ipooters@gmail.com",
    install_requires=["termcolor","colorama"],
    description="Check online service provider for account presence.",
    include_package_data=True,
    url='http://github.com/3ev0/kenda',
    entry_points = {'console_scripts': ['kenda = kenda.main:main']},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)