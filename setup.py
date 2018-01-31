import setuptools

setuptools.setup(
    name="MoneyPy",
    version="0.0",
    url="https://github.com/learn-and-code/MoneyPy",

    author="learnandcode.it",

    description="A python framework to build custom budget-analysis workflows and applications",
    
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "test*"]),

    license='MIT',

    install_requires=[],

    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
) 
