from setuptools import setup

setup(
    name="pubmed-bib",
    version='0.1',
    py_modules=['pubmed_bib'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        pubmed-bib=pubmed_bib:pubMed2BibTex
    '''
)
