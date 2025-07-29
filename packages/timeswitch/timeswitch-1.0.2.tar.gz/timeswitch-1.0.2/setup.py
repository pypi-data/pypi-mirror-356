import os

from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


def long_description(readme_path='README.md'):
    try:
        import pypandoc
        return pypandoc.convert(readme_path, 'rst')
    except (OSError, IOError, ImportError):
        return read(readme_path)


setup(

    name='timeswitch',
    version='1.0.2',

    description='Test date/time against a time period expressed in a simple grammar',
    long_description=long_description('README.md'),

    url='https://bitbucket.org/rocketboots/timeswitch/',
    author='RocketBoots Pty Ltd',
    author_email='support@rocketboots.com',

    packages=find_packages(exclude=['test*']),
    include_package_data=True,

    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords='date time range period expression language',

    install_requires=[
        'pyparsing~=3.2; python_version>="3.9"',
        'pyparsing~=2.1; python_version<"3.9"',
        'enum34~=1.0'
    ],

    extras_require={
        'test': [
            'coverage',
            'mock',
            'nose2',
            'testfixtures'
        ]
    },

    entry_points={
        'console_scripts': [
            'timeswitch=timeswitch.__main__:main',
        ]
    }

)
