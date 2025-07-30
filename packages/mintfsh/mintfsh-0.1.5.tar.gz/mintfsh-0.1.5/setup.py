from setuptools import setup, find_packages

setup(
    name='mintfsh',
    version='0.1.5',
    packages=find_packages(),
    py_modules=['mint.mint'],
    install_requires=[
        'flask>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'mint = mint.mint:main',
            'mint-host = mint.mint_host:cli'
        ],
    },
    author='giacomosm',
    author_email='giacomosm@proton.me',
    description='Mint is a terminal-based file sharing service, with support for custom mirrors, rich JSON config, and more.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license='BSD-2-Clause',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
