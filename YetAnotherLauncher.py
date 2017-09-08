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

DEFAULT_LOG_LEVEL = logging.WARNING
# DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_LEVEL_NAME = logging.getLevelName(DEFAULT_LOG_LEVEL)

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
        if "by_launcher" in args and args["by_launcher"]:
            l.debug("args[by_launcher] is true")
            pass
        # check if args contains a category element and if its
        # value is an valid category (self.item_categories)
        elif "category" in args:
            # generating panel_items only with items that are defined with
            # the category that is set in args["category"]
            # otherwise show an error message
            if args["category"] in self.item_categories:
                self.generate_panel_items(sorted(self.items_by_category[args["category"]]))
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
            else:
                sublime.message_dialog(
                    '"' + args["launcher"] + '"' +
                    " isn't a valid launcher!\n\n\n" +
                    "Either check the arguments for yet_another_lauchner or" +
                    "check your user configuration of Yet Another Launcher.")
        else:
            self.generate_panel_items(sorted(list(self.items.keys())))
        # showing the quick panel with content of panel_items
        if self.panel_items:
            self.window.show_quick_panel(self.panel_items, self.on_done_launch)

    def on_done_launch(self, choice):
        if choice >= 0:
            path = self.panel_items[choice][1]  # the path is currently the second element
            if path.startswith('http://') or path.startswith('https://'):
                webbrowser.open(path, 2, True)
                return
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
