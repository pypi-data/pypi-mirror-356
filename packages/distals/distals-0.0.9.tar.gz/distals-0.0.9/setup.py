from setuptools import setup, find_packages

with open('README.md') as f:
    description = f.read()

setup(
    name='distals',
    version='0.0.9',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'newick',
        'scipy',
        'scikit-learn',
        'pandas', 
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'distals = distals:main'
        ]
    },
    long_description=description,
    long_description_content_type='text/markdown',
)

