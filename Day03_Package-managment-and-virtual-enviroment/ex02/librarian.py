import sys
import subprocess

import os
from zipp import zipfile



#-------------------------------#
#   Install packages functions  #
#-------------------------------#

def is_in_venv() -> bool:
    """Check is program executed in venv
    Returns:
        bool: true is venv is set, false otherwise
    """
    return sys.prefix != sys.base_prefix


def install_packages(packages: list, output_file='requirements.txt') -> str:
    """Install packages to running virtual enviroment.
    Printing installed packages list to output file and stdout.

    Args:
        packages (list): list of packages to install
        output_file (str, optional): output file for requirements. Defaults to 'requirements.txt'.

    Raises:
        RuntimeError: raises if script was runned not inside venv

    Returns:
        str: _description_
    """
    # check env
    if not is_in_venv():
        raise RuntimeError('Virtual enviroment is not running!')

    # install
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages])

    # freeze
    installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = installed_packages.decode('utf-8')
    print(installed_packages)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(installed_packages)



#-------------------------------#
#       Zip venv functions      #
#-------------------------------#

def zipdir(path: str, ziph) -> None:
    """Zip all files in directory to archive
    Args:
        path (str): path to zip
        ziph (_type_): zipfile handler
    """
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def create_current_venv_archive(archive_name: str) -> None:
    """ Create an archive of current virtual enviroment

    Args:
        archive_name (str): name of resulting archive
    """
    with zipfile.ZipFile(archive_name, 'w') as myzip:
        zipdir(sys.prefix, myzip)



#-------------------------------#
#             Main              #
#-------------------------------#

if __name__ == '__main__':
    try:
        install_packages(['beautifulsoup4', 'pytest'])
        create_current_venv_archive('venv.zip')
    except RuntimeError as err:
        print(f'Runtime error: {err.args[0]}')
