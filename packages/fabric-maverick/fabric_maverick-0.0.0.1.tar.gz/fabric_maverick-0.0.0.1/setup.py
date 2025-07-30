from setuptools import setup, find_packages

setup(
    name='fabric_maverick',
    version='0.1.0',
    description='A Fabric Package for Semantic/Dataset level validation',
    author='Nisarg Patel',
    author_email='nisargp@maqsoftware.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'fuzzywuzzy',
        'python-Levenshtein', # often a dependency for fuzzywuzzy for better performance
        'sempy' 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

# python setup.py sdist
# twine upload dist/*

#python3 -m build 
#python3 -m  twine upload dist/* 