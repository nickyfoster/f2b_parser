from setuptools import find_packages
import os

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

dir_path = os.path.dirname(os.path.realpath(__file__))


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)


setup(
    name='f2b_parser',
    url='https://github.com/nickyfoster/f2b_parser',
    description='Fail2Ban Parser',
    keywords='fail2ban python parser',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "redis==3.3.8",
        "ipwhois==1.1.0"
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
