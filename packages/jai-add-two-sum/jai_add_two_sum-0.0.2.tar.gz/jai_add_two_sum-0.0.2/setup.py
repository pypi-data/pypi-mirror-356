from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # add your dependencies
    entry_points={
        'console_scripts': [
            'my-command = jai_add_two_sum.main:add_two_sum',  # format: cli-name = module:function
        ],
    },
)