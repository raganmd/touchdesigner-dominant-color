import os
import subprocess


def Check_dep(debug: bool = False) -> None:
    '''
    Check for dependencies and project path.

    This method checks to see if the path for the project is included in sys.path.
    This will ensure that the python modules used in the project will 
    be respected by the Touch.
    '''

    # our path for all non-standard python modules
    dep_path = '{}/dep/python/'.format(project.folder)

    # if our path is already present we can skip this step
    if dep_path in sys.path:
        pass

    # insert the python path into our sys.path
    else:
        sys.path.insert(0, dep_path)

    # print each path in sys.path if debug is true:
    if debug:
        for each in sys.path:
            print(each)
    else:
        pass

    pass


def Install_python_external() -> None:
    '''
    Check and install any external modules.

    This method will go through all the necessary steps to ensure
    that our external modules are loaded into our project specific
    location. This approach assumes that external libraries should be 
    housed with the project, rather than with the standalone python
    installation, or with the Touch Installation. This ensures a more consistent, 
    reliable, and portable approach when working with non-standard python
    modules. 
    '''

    dep_path = f'{project.folder}/dep'
    python_path = f'{project.folder}/dep/python'
    python_exe = app.pythonExecutable
    requirements = f'{dep_path}/requirements.txt'
    reqs_dat = op('reqs')

    required_paths = [dep_path, python_path]

    # check for all required paths, create them if they don't exist
    for each_path in required_paths:
        if os.path.isdir(each_path):
            pass
        else:
            os.mkdir(each_path)

    # check to see if the requirements txt is in place
    if os.path.isfile(requirements):
        pass
    else:
        with open(requirements, "w") as reqs_file:
            reqs_file.write(reqs_dat.text)

    run_subprocess_install(python_exe=python_exe, reqs_file_path=requirements,
                           target_installation_path=python_path)


def run_subprocess_install(python_exe: str, reqs_file_path: str, target_installation_path: str) -> None:
    ''' 
    Install python libraries.

        Using the python that ships with TouchDesigner we can pip install the libraries
        that are specified by our requirements file 
    '''
    popen_args = [python_exe, "-m", "pip", "install", "-r",
                  f"{reqs_file_path}", "--target", f"{target_installation_path}"]

    print(popen_args)
    # run installation as subprocess call
    subprocess.Popen(popen_args, shell=False)
