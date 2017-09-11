# Yet Another Launcher - Release notes

For more infos about Yet Another Launcher (YAL) see [README](README.md). Before reporting issues Please check that [PackageControl YAL site](https://packagecontrol.io/packages/Yet%20Another%20Launcher) lists the latest version of YAL and that that version is also installed.

## v1.0.5
- adding support for launching YAL with the arguments:
    - "by_launcher" - opens quickpanel and allows to select a launcher
    - "by_category" - opens quickpanel and allows to select an item category (url, file+sys, file+subl)
- added "by_category" to menu and command palette ("by_launcher" was already there)
- added support for expanding elements in path names (~, ~user, %USERPROFILE%, %APPDATA%, %LOCALAPPDATA%, %PUBLIC%, %WINDIR%, %SYSTEMROOT%, %TEMP%, %TMP%, %USERNAME% - ~/~user works on Windows as well)
- switched to a [development branch on Github](https://github.com/dahanbn/Yet-Another-Launcher/tree/development) for developing new features

## v1.0.4 - added infos about releases
- added release notes to repo and README.md

## v1.0.3 - bug fix
- fixed a bug that generated wrong urls for items

## v1.0.2 - bug fix
- fixed a bug that after each call the item list would contain the old items as well

## v1.0.1 - added various option to yet\_another\_launcher command
- you can launch now single launchers or launcher by category for examples see [README](README.md)

## v1.0.0 - initial release
- basic implementation

