'''
This script helps to create custom project templates for use in Unity Hub.

Example usage:
    $ python ./unity_hub_template_manager.py '/path/to/Unity/Hub/Editors' '/path/to/template/project'

TODO:
    * Identify user OS
    * Implement default paths based on OS
'''
__version__ = '0.2.0'

from ctypes import windll
from json import dumps
from os import chdir, listdir, makedirs, path, scandir, remove, rename
from pathlib import Path
from platform import system
from shutil import copyfile, copytree, make_archive, rmtree
from sys import argv, executable
from re import match


def verify_paths():
    '''
    Check that we have been given a path to the Editors folder and a path to the template project.
    If both are present and valid, return True. If not, inform the user and return False.
    '''
    if len(argv) != 3:
        print('Invalid number of arguments. Expecting path to Editor folder and path to template project.')
        return False

    # Check that these are valid paths
    global editors_path
    editors_path = Path(argv[1])
    global project_path
    project_path = Path(argv[2])
    if not path.isdir(editors_path):
        print('Editor path is not a valid path!')
        return False
    elif not path.isdir(project_path):
        print('Project path is not a valid path!')
        return False

    # Check that the paths contain what we expect them to
    global editors_list
    editors_list = [f for f in scandir(editors_path) if f.is_dir()]
    editor_name_pattern = r'^[0-9]+\.[0-9]+\.[0-9]+f[0-9]+'
    for f in editors_list:
        if match(editor_name_pattern, f.name) is None:
            print('These folders do not appear to follow Unity\'s versioning pattern. Please verify you have the correct path.')
            return False

    project_folders = [f.name for f in scandir(project_path) if f.is_dir()]
    if 'Assets' not in project_folders or 'ProjectSettings' not in project_folders:
        print('Folder is either not a valid Unity project or is missing its Assets/ProjectSettings folder(s). Please verify project is valid.')
        return False

    return True


def create_template(editor=None, name=None, displayname=None, version=None, description=None):
    '''Returns the full path to the chosen Editor's project templates folder, or None if given editor is invalid.'''
    if editor is None:
        # Prompt user for which version of Unity this template will be for
        choosing = True
        while choosing:
            print('Select Unity version template will be added to:')
            for editor in editors_list:
                print(editors_list.index(editor), '-', editor.name)

            choice = int(input())
            if choice >= len(editors_list) or choice < 0:
                print('Invalid choice.\n')
                continue
            choosing = False

        # Get path to Editor project templates
        unity_version = editors_list[choice].name
        templates_path = path.join(
            editors_list[choice].path, r'Editor\Data\Resources\PackageManager\ProjectTemplates')

    elif Path.is_dir(editor.path):
        unity_version = editor.name
        templates_path = path.join(
            editor.path, r'Editor\Data\Resources\PackageManager\ProjectTemplates')

    else:
        print('Invalid Editor!')
        return

    # Construct package.json for the template
    if not path.isdir('./tmp/package'):
        makedirs('./tmp/package')
    chdir('./tmp/package')
    package_json = {
        "name": "",
        "displayName": "",
        "version": "",
        "type": "template",
        "host": "hub",
        "unity": "",
        "description": "",
        "dependencies": {}
    }
    if name and displayname and version and description:
        package_json['name'] = name
        package_json['displayName'] = displayname
        package_json['version'] = version
        package_json['description'] = description
    elif not name and not displayname and not version and not description:
        package_json['name'] = input('Enter filename: ')
        package_json['displayName'] = input('Enter display name: ')
        package_json['version'] = input('Enter version number: ')
        package_json['description'] = input('Enter description: ')
    else:
        print('This function should only be called with 1 or 5 valid arguments. Stopping program.')
        print(name, displayname, version, description)
        quit()
    package_json['unity'] = unity_version

    # Dump package.json to file
    f = open('package.json', 'w')
    f.write(dumps(package_json, indent=4))
    f.close()

    # Construct ProjectData~ folder and copy project contents over
    copytree(path.join(project_path, 'Assets'), './Assets')
    copytree(path.join(project_path, 'Packages'), './Packages')
    copytree(path.join(project_path, 'ProjectSettings'), './ProjectSettings')

    # Unity will throw an error if this file is present in a template
    remove('./ProjectSettings/ProjectVersion.txt')

    # Create gzipped tarball
    chdir('../..')
    tar_gz2 = make_archive(package_json['name'], 'gztar', 'tmp', 'package')
    base = path.splitext(tar_gz2)[0].split('.')[0]
    rename(tar_gz2, base + '.tgz')
    rmtree('./tmp')

    # Copy new template to selected Editor project templates folder
    for file in listdir('.'):
        if file.endswith('.tgz'):
            try:
                copyfile(file, path.join(templates_path, file))
                print('File copied to templates folder successfully.')
                remove(file)
            except:
                print(
                    'File not copied. You may not have write permissions to templates folder.')
                print('You can still attempt to copy the archive over manually.')


if __name__ == "__main__":
    if verify_paths():
        create_template()
    else:
        print('Paths could not be verified.')
