from setuptools import setup, find_packages

setup(
    name='mintfsh',
    version='0.1.2',
    packages=find_packages(),
    py_modules=['mint.mint'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mint = mint.mint:main',
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
