# Yet Another Launcher (YAL) - a Sublime Text 3 launcher plugin

[![GitHub license](https://img.shields.io/badge/license-AGPL-blue.svg)](https://raw.githubusercontent.com/dahanbn/Yet-Another-Launcher/master/LICENSE) [![Downloads](https://img.shields.io/packagecontrol/dt/Yet%20Another%20Launcher.svg?style=flat-square)](https://packagecontrol.io/packages/Yet%20Another%20Launcher) [![Author](https://img.shields.io/badge/twitter-%40dahanbn-blue.svg?style=flat-square)](https://twitter.com/dahanbn)

A [Sublime Text](http://www.sublimetext.com/) plugin that is an easy launcher for local files, directories or urls.
 
You will find all release notes in [RELEASES.md](RELEASES.md). For a quick overview follows the latest two release notes below.
 
## v1.0.4 - added infos about releases
- added release notes to repo and README.md

## v1.0.3 - bug fix
- fixed a bug that generated wrong urls for items

## Installation

You only need to install this package:

-   [Using the Package Control plugin](https://packagecontrol.io/) - you will find it [here](https://packagecontrol.io/packages/Yet%20Another%20Launcher).
-   Manually, either download or checkout this repository and [install into your packages directory](http://docs.sublimetext.info/en/latest/extensibility/packages.html#package-installation).

## Usage

### Via Command Palette or Tools menu

You can access Yet Another Launcher via the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows) by selecting "Yet Another Launcher". 

You can also find the Yet Another Launcher submenu in the menu `Tools`. 

### Via keybindings

You can also easily bind the launcher command to a key of your choice, e.g. `{"keys": ["f1"], "command": "yet_another_launcher"}`. If you want to launch the default launcher only you can bind it with the following code: `{"keys": ["shift+f1"], "command": "yet_another_launcher","args": {"launcher": "default"}},`. 

*Notice:* YAL doesn't set any keybindings per default. You have to set them yourself if you want to use it.

### Via directly calling the command

The plugin defines one `Sublime.WindowCommand` with the name `yet_another_launcher`. You can run it on various places in Sublime Text, e.g. in the console via `window.run_command("yet_another_launcher")` or `window.run_command("yet_another_launcher", {"launcher": "default"})`.

You can see the various command arguments used in [Main.sublime-menu](Main.sublime-menu). 

## Implemented Features

+ [X] initial release (v1.0.0)
+ [X] make the package available on [PackageControl](https://packagecontrol.io/) (v1.0.0)
+ [X] adding support for launching launchers by launcher names or category (v1.0.1)

## Upcoming Features

Over time I will try to add the following features:

+ [ ] launching launchers are able to select an existing launchers
+ [ ] testing it on Linux and making it work there (it should already work, but it isn't tested yet)
+ [ ] testing it on Mac and making it work there (it should already work, but it isn't tested yet)
+ [ ] implementing launcher category `file+subl` to open files in the current Sublime Text session
+ [ ] adding support for operating system dependend user settings

## Configuration

You configure your launcher and launchable items via the [plugin settings file](http://docs.sublimetext.info/en/latest/customization/settings.html). Via the application menu, go to `"Preferences" -> "Package Settings" -> "Yet Another Launcher" -> "Settings - User"`.

# Example configuration

The configuration is written in [JSON](https://en.wikipedia.org/wiki/JSON) as usual for Sublime Text settings.

You need a top level JSON-object called `launchers`. Under it you have to create different launcher objects. In the example you see a launcher called `default`.

```js
{
    //
    // the "launchers" object is needed and contains all launchers
    //
    "launchers": { 
        //
        // under "launchers" you can create at least one named launcher,
        // at least you have to define one launcher with the name "default"
        // 
        // "default" is used if you launch YAL's default launcher
        //
        "default": {
            // 
            // in launchers you can create three different objects:
            // 
            // "url"       - for urls that will be opened in your default browser
            // "file+sys"  - for files or directories that will be opened with the
            //               default application of your operating system
            // "file+subl" - for files or directories that will be opened in your
            //               current Sublime Text session
            "url": {
                "Sublime Text 3 - Api Reference": "http://www.sublimetext.com/docs/3/api_reference.html",
                "Sublime Text Forum": "https://forum.sublimetext.com",
            },
    }
}
```

## License
The plugin is licensed under the GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007. In detail you can read the licensing terms in the file `[LICENSE](LICENSE)`.
