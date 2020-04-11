import os
import sys

from setuptools import setup


def main():
    """The main entry point."""
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
        readme = f.read()
    skw = dict(
        name='asht',
        description='Abstract Shell Tree'
        long_description=readme,
        long_description_content_type='text/markdown',
        license='BSD',
        version='0.0.0',
        author='Anthony Scopatz',
        maintainer='Anthony Scopatz',
        author_email='scopatz@gmail.com',
        url='https://github.com/regro/asht',
        platforms='Cross Platform',
        classifiers=['Programming Language :: Python :: 3'],
        packages=['asht'],
        package_dir={'asht': 'asht'},
        package_data={'asht': ['*.xsh']},
        install_requires=[],
        python_requires=">=2.7",
        zip_safe=False,
        )
    setup(**skw)


if __name__ == '__main__':
    main()
