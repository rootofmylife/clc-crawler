from setuptools import setup, find_packages

setup(
    name='nomscript',
    version='1.0',
    packages=find_packages(),
    package_data={
        'tutorial': ['resources/*.txt']
    },
    entry_points={
        'scrapy': ['settings = tutorial.settings']
    },
    zip_safe=False,
)
