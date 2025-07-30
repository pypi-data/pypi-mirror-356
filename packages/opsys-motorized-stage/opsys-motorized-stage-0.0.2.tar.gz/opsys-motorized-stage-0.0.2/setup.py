import setuptools
from pathlib import Path


def get_install_requirements():
    """
    Extract packages from requirements.txt file to list

    Returns:
        list: list of packages
    """
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setuptools.setup(name='opsys-motorized-stage',
                 version='0.0.2',
                 description='python package for motorized stage device control',
                 url='https://bitbucket.org/opsys_tech/opsys-motorized-stage/src/master/',
                 download_url='https://bitbucket.org/opsys_tech/opsys-motorized-stage/src/master/',
                 author='dmitry.borovensky',
                 install_requires=get_install_requirements(),
                 author_email='dmitry.borovensky@opsys-tech.com',
                 packages=setuptools.find_packages(exclude=("test",)),
                 package_data={'opsys_motorized_stage': ['nsc_a1/*.dll']},
                 include_package_data=True,
                 zip_safe=False)