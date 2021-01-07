'''
This script helps to create custom project templates for use in Unity Hub.

Example usage: 
    $ python ./unity_hub_template_manager.py '/path/to/Unity/Hub/Editors' '/path/to/template/project'

TODO:
    * Separate out into modules
    * Identify user OS
    * Implement default paths based on OS
    * Request elevated privileges on Windows to resolve copy permissions issues
'''
__version__ = '0.1.0'

from json import dumps
from os import chdir, listdir, makedirs, path, scandir, remove, rename
from pathlib import Path
from shutil import copy, copytree, make_archive, rmtree
from sys import argv
from re import match

# Check that we have been given a path to the Editors folder and a path to the template project.
# If not, inform the user and exit.
if len(argv) != 3:
    print('Invalid number of arguments. Expecting path to Editor folder and path to template project.')
    quit()

# Check that these are valid paths
editors_path = Path(argv[1])
project_path = Path(argv[2])
if not path.isdir(editors_path):
    print('Editor path is not a valid path!')
    quit()
elif not path.isdir(project_path):
    print('Project path is not a valid path!')
    quit()

# Check that the paths contain what we expect them to
editors_list = [f for f in scandir(editors_path) if f.is_dir()]
editor_name_pattern = '^[0-9]+\.[0-9]+\.[0-9]+f[0-9]+'
for f in editors_list:
    if match(editor_name_pattern, f.name) is None:
        print('These folders do not appear to follow Unity\'s versioning pattern. Please verify you have the correct path.')
        quit()
print('Editor folder looks good.')

project_folders = [f.name for f in scandir(project_path) if f.is_dir()]
if 'Assets' not in project_folders or 'ProjectSettings' not in project_folders:
    print('Folder is either not a valid Unity project or is missing its Assets/ProjectSettings folder(s). Please verify project is valid.')
    quit()
print('Project folder looks good.')

# Prompt user for which version of Unity this template will be for
print('Select version template will be added to:')
for editor in editors_list:
    print(editors_list.index(editor), '-', editor.name)
choice = int(input())

# Get path to Editor project templates
templates_path = path.join(
    editors_list[choice].path, 'Editor\Data\Resources\PackageManager\ProjectTemplates')

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
package_json['name'] = input('Enter filename: ')
package_json['displayName'] = input('Enter display name: ')
package_json['version'] = input('Enter version number: ')
package_json['unity'] = editors_list[choice].name
package_json['description'] = input('Enter description: ')

# Dump package.json to file
f = open('package.json', 'w')
f.write(dumps(package_json, indent=4))
f.close()

# Construct ProjectData~ folder and copy project contents over
copytree(path.join(project_path, 'Assets'), './Assets')
copytree(path.join(project_path, 'Packages'), './Packages')
copytree(path.join(project_path, 'ProjectSettings'), './ProjectSettings')

# Unity will throw an error if this is present in a template
remove('./ProjectSettings/ProjectVersion.txt')

# Create gzipped tarball
chdir('../..')
tar_gz2 = make_archive(package_json['name'], 'gztar', 'tmp', 'package')
base = path.splitext(tar_gz2)[0].split('.')[0]
rename(tar_gz2, base + '.tgz')
rmtree('./tmp')

# TEMP
print('Template created. Copy it to your ProjectTemplates directory:')
print(templates_path)
# TEMP

# See TODO(4)
# Copy new template to selected Editor project templates folder
# for file in listdir('.'):
#    if file.endswith('.tgz'):
#        copy(file, templates_path)
