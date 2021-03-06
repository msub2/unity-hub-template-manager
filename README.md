# Unity Hub Template Manager

The Unity Hub Template Manager is intended to provide a more streamlined way of creating template projects to use in Unity Hub.

## Usage

To use the Unity Hub Template Manager, download the latest release for your system. Once downloaded, simply double-click to launch the GUI, or run it from a terminal like so:

`./UHTM.exe '/path/to/template/project'`

This will check the default location for Unity Hub editors and copy your template to the selected one at that location.
The default path to the Editors folder for each system is as follows:

Windows: `C:\Program Files\Unity\Hub\Editor`

Mac: `/Application/Unity/Hub/Editor`

Linux: `~/Unity/Hub/Editor`

You can also pass in a custom path to your Editor folder like so:

`./UHTM.exe '/path/to/template/project' '/path/to/Unity/Hub/Editors'`

Please note that in order for the template to be copied over to the ProjectTemplates folder, you will need write permissions for that folder. If it is unable to be copied,  the archive will remain in the local directory, where you can attempt to move it manually.
