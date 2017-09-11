# -*- coding: utf8 -*-

# Copyright (C) 2017 - Daniel Hannaske <d.hannaske@gmail.com>
# This program is Free Software see LICENSE file for details

"""
Yet Another Launcher is a plugin for Sublime Text
that allows to launch arbitrary user defined files & urls
- urls
    will be opened in the default browser
- files
    either in Sublime Text ("file+subl") or
    with the operating system default application / file manager
"""


import sublime
import sublime_plugin
import os
import subprocess
import sys
import webbrowser
import logging
# setting logging base-level,
# in production it will be set to logging.WARNING by commenting it out

# TODO: find more out about logging
DEFAULT_LOG_LEVEL = logging.WARNING
# DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_LEVEL_NAME = logging.getLevelName(DEFAULT_LOG_LEVEL)
EVENT_LEVEL = logging.INFO
# EVENT_LEVEL = logging.INFO

pl = logging.getLogger(__package__)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="[{name}] {levelname}: {message}", style='{')
handler.setFormatter(formatter)
pl.addHandler(handler)
pl.setLevel(DEFAULT_LOG_LEVEL)

l = logging.getLogger(__name__)
l.debug("YetAnotherLauncher.py is being loaded")


class YetAnotherLauncherCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        l.debug("__init__")
        # each launcher can have the following item_categories
        # url, file+sys, file+subl
        self.item_categories = ("url", "file+sys", "file+subl")
        # launchers contains the name of the defined launchers
        self.launchers = []
        # items has the following data structure containing dicts
        # {'name_of_launchable_item': {
        #       'url': 'url or path to launchable item',
        #       'launcher': 'name_of_user_defined_launcher',
        #       'category': 'category of the launchable item, url, file+sys,...
        # }
        self.items = {}
        self.panel_items = []  # will contain the formatted panel item for the quick panel
        self.panel_items_info = ""  # will contain either "by_launcher", "by_category" or "launchable_item"
        self.items_by_launchers = {}
        self.items_by_category = {}
        for category in self.item_categories:
            # initialing list items_by_category
            self.items_by_category[category] = []
        self.settings = sublime.load_settings("YetAnotherLauncher.sublime-settings")
        self.process_settings()
        sublime_plugin.WindowCommand.__init__(self, window)

    def process_settings(self):
        # each setting file should contain "yal_launchers"
        if self.settings.has("launchers"):
            data = self.settings.get("launchers")
            for launcher in self.settings.get("launchers"):
                # adding launcher name to a list called launchers
                self.launchers.append(launcher)
                # initialing list items_by_launchers
                self.items_by_launchers[launcher] = []
                for category in data[launcher].keys():
                    if category in self.item_categories:
                        for item in data[launcher][category]:
                            # filling the data structure of the launchable item
                            self.items[item] = {
                                "url": data[launcher][category][item],
                                "category": category,
                                "launcher": launcher,
                                "panel_name": [
                                    item,
                                    data[launcher][category][item],
                                    # launcher
                                    ]}
                            # adding the item name to the corresponding
                            # list of items per launcher
                            self.items_by_launchers[launcher].append(item)
                            # adding the item name to the corresponding
                            # list of items per category
                            self.items_by_category[category].append(item)

    def run(self, **args):
        """run(self, **args) - runs the launcher dialog.

           without arguments it runs the launcher with all items

           **args is optional, possible args are:
                "by_launcher": True
                    - launcher let you select which launcher to launch
                "category": "url" or "file+sys" or "file+subl"
                    - launcher shows only items from that category
                "launcher": "name of the launcher, e.g. default"
                    - launcher shows only items from the given launcher
        """
        l.debug("run with the following args")
        l.debug(args)
        # check if args contains an "by_launcher" element and
        # if it is true
        # emptying panel_items
        self.panel_items = []
        # emptying panel_items_info, it will contain the type of panel_items_info
        self.panel_items_info = ""
        # first check two special cases that needs another logic
        # by_launcher & by_category
        # both need two launchers,
        #      first to select launcher or category
        #      second to launch that
        # self.panel_items_info will contain "by_category" or "by_launcher"
        # to check later, what is exactly in self.panel_items
        if ("by_launcher" in args and args["by_launcher"]) or ("by_category" in args and args["by_category"]):
            # check if args contains an "by_launcher" element and
            # if it is true
            if "by_launcher" in args and args["by_launcher"]:
                l.debug("args[by_launcher] is true")
                self.panel_items = sorted(self.launchers)
                self.panel_items_info = "by_launcher"
            # check if args contains an "by_category" element and
            # if it is true
            elif "by_category" in args and args["by_category"]:
                l.debug("args[by_category] is true")
                self.panel_items = sorted(self.item_categories)
                self.panel_items_info = "by_category"
        # check if args contains a category element and if its
        # value is an valid category (self.item_categories)
        elif "category" in args:
            # generating panel_items only with items that are defined with
            # the category that is set in args["category"]
            # otherwise show an error message
            if args["category"] in self.item_categories:
                self.generate_panel_items(sorted(self.items_by_category[args["category"]]))
                self.panel_items_info = "launchable_item"
            else:
                # first generating a string representation of the
                # tuple (self.item_categories) for the error message
                allowed_categories = ""
                for category in self.item_categories:
                    allowed_categories += '"' + category + '", '
                # removing last comma and whitespace from string
                allowed_categories = allowed_categories.rstrip(", ")
                sublime.message_dialog(
                    '"' + args["category"] + '"' +
                    " isn't a valid category!\n\n\n" +
                    "Please check the arguments for yet_another_lauchner.\n" +
                    "Allowed categories are: " + allowed_categories)
        # check if args contains an launcher element and if its
        # value is an user defined launcher (self.launchers)
        elif "launcher" in args:
            # generating panel_items only with items that are defined with
            # the launcher that is set in args["launcher"]
            # otherwise show an error message
            if args["launcher"] in self.launchers:
                self.generate_panel_items((self.items_by_launchers[args["launcher"]]))
                self.panel_items_info = "launchable_item"
            else:
                sublime.message_dialog(
                    '"' + args["launcher"] + '"' +
                    " isn't a valid launcher!\n\n\n" +
                    "Either check the arguments for yet_another_lauchner or" +
                    "check your user configuration of Yet Another Launcher.")
        else:
            self.generate_panel_items(sorted(list(self.items.keys())))
            self.panel_items_info = "launchable_item"
        # showing the quick panel with content of panel_items
        if self.panel_items:
            self.window.show_quick_panel(self.panel_items, self.on_done_launch)

    def on_done_launch(self, choice):
        """on_done_launch(self, choice) - launches the choice

            choice can either be launchable_items or
                                 another quickpanel (by_category/by_launcher

            what choice means depends on the value of self.panel_items_info

                self.panel_items_info = 'by_category'
                self.panel_items_info = 'by_launcher'

                        will launch a second quickpanel by selected category/launcher

                self.panel_items_info = 'launchable_item'

                        will launch the launchable_item"""
        if choice >= 0:
            # test, what panel_items contains
            if self.panel_items_info == "by_category":
                sublime.active_window().run_command("yet_another_launcher", {"category": self.panel_items[choice]})
            elif self.panel_items_info == "by_launcher":
                sublime.active_window().run_command("yet_another_launcher", {"launcher": self.panel_items[choice]})
            elif self.panel_items_info == "launchable_item":
                path = self.items[self.panel_items[choice][0]]['url']
                category = self.items[self.panel_items[choice][0]]['category']
                if category == "url":
                    if path.startswith('http://') or \
                            path.startswith('https://') or \
                            path.startswith('ftp://') or \
                            path.startswith('ftps://'):
                        webbrowser.open(path, 2, True)
                        return
                elif category == "file+sys" or category == "file+subl":
                    # preprocessing path if it isn't absolute
                    if not os.path.isabs(path):
                        # expanding unix style user names,
                        # works on Windows as well
                        if path.startswith("~"):
                            path = os.path.expanduser(path)
                        # expanding Windows Environment variables,
                        # currently only the following  
                        elif os.name == "nt" and \
                                (path.startswith("%USERPROFILE%") or
                                    path.startswith("%APPDATA%") or
                                    path.startswith("%LOCALAPPDATA%") or
                                    path.startswith("%PUBLIC%") or
                                    path.startswith("%WINDIR%") or
                                    path.startswith("%SYSTEMROOT%") or
                                    path.startswith("%TEMP%") or
                                    path.startswith("%TMP%") or
                                    "%USERNAME%" in path):
                            path = os.path.expandvars(path)
                    if not os.path.exists(path):
                        sublime.message_dialog(
                            '"' + path + '"' +
                            " isn't a valid path and can't be opened!")
                        return False
                    # Windows
                    if os.name == "nt":
                        os.startfile(path)
                    # Macintosh - not tested yet
                    elif sys.platform == "darwin":
                        subprocess.call(['open', path])
                    # Generisches Unix (X11) - not tested yet
                    else:
                        subprocess.call(['xdg-open', path])

    def generate_panel_items(self, items):
        for item in items:
            self.panel_items.append(self.items[item]["panel_name"])
