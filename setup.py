# setuptools configuration file
from setuptools import find_packages , setup

def get_requirements(file_path:str) -> list:
    """
    This function will return the list of requirements
    """
    requirements = []
    HYPEM_REQ = '-e .' # editable install for local development
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements] # removing the new line character from each line
        if HYPEM_REQ in requirements: # if there is -e . in the requirements.txt file, we will remove it
            requirements.remove('-e .')
    return requirements

# metadata information about the project
setup(
    name = 'mlproject',
    version= '0.0.1',
    author = 'ajay',
    author_email = 'ajaysulya06@gmail.com',
    packages = find_packages(),
    
    # install_requires = ['numpy','pandas','scikit-learn','matplotlib','seaborn'], # if there is 100 packages , we can't add manually instead we can use 
    # this function will read the requirements.txt file and return the list of packages
    
)