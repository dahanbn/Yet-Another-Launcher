# Yet-Another-Launcher

Yet Another Launcher - a Sublime Text 3 launcher plugin

 A [Sublime Text](http://www.sublimetext.com/) plugin that is an easy launcher for local files, directories or urls.

## Installation

You only need to install this package:

-   [Using the Package Control plugin](https://packagecontrol.io/). (**has to be implemented, not yet**)
-   Manually, either download or checkout this repository and [install into your packages directory](http://docs.sublimetext.info/en/latest/extensibility/packages.html#package-installation).

## Usage

You can access Yet Another Launcher via the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows) by selecting "Yet Another Launcher". 

You can also find the Yet Another Launcher submenu in the menu `Tools`. You can also easily bind the launcher command to a key of your choice, e.g. `{"keys": ["f1"], "command": "yet_another_launcher"}`.

## Upcoming Features

The plugin is a rough first version. Over time I will try to add the following features:

+ testing it on Linux and making it work there (it should already work, but it isn't tested yet)
+ testing it on Mac and making it work there (it should already work, but it isn't tested yet)
+ implementing launcher category `file+subl` to open files in the current Sublime Text session
+ adding support for operating system dependend user settings
+ adding support for launching launchers by launcher names or category

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
        // it's okay to only define one launcher, e.g. "default"
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
The plugin is licensed under the GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007. In detail you can read the licensing terms in the file `LICENSE`.
