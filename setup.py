from setuptools import find_packages, setup
from typing import List
HYPHEN = "-e ."

def get_requirements(filepath: str) -> List[str]:
    '''
        Input: requirements.txt filepath
        Output: List of required libraries to install
    '''
    req = []
    with open(filepath,'r') as file:
        req = file.readlines()
        req = [r.replace("\n","").strip() for r in req]
        
        if HYPHEN in req:
            req.remove(HYPHEN)
        return req

setup(
    name='IntershipPredictor', # Project Name
    version='0.0.1', # Project Version
    author="Akshat Agarwal", 
    author_email="akshatsoftware9829@gmail.com",
    packages=find_packages(), # Identifies what folders can act as packages having __init__ file in it 
    install_requires=get_requirements('requirements.txt') # Exctract All files that need to be downloaded from requirements.txt filepath
)
