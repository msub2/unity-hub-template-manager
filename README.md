# Unity Hub Template Manager

The Unity Hub Template Manager is intended to provide a more streamlined way of creating template projects to use in Unity Hub.
It is currently CLI only, but a GUI is planned soon.

## Usage

To use the Unity Hub Template Manager, download the latest release for your system (note: currently Windows only. Mac and Linux soon).
Once downloaded, it can be used as such:

`./unity_hub_template_manager.exe '/path/to/Unity/Hub/Editors' '/path/to/template/project'`

The default path to the Editors folder for each system is as follows:

Windows: `C:\Program Files\Unity\Hub\Editor`.
Mac: `/Application/Unity/Hub/Editor`.
Linux: `~/Unity/Hub/Editor`

Please note that in order for the template to be copied over to the ProjectTemplates folder, you will need write permissions for that folder. If it is unable to be copied,  the archive will remain in the local directory, where you can attempt to move it manually.
