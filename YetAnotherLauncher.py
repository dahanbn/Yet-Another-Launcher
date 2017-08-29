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

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)
logger.debug("YAL has been loaded")


class YetAnotherLauncherCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
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

    def run(self):
        # items = sorted(list(self.items.keys()))
        # items = sorted(self.items_by_launchers["@work"])
        panel_items = []
        for item in sorted(list(self.items.keys())):
            panel_items.append(self.items[item]["panel_name"])
        self.window.show_quick_panel(panel_items, self.on_done)

    def on_done(self, choice):
        if choice >= 0:
            items = sorted(list(self.items.keys()))
            # items = sorted(self.items_by_launchers["@work"])
            path = self.items[items[choice]]["url"]
            if path.startswith('http://') or path.startswith('https://'):
                webbrowser.open(path, 2, True)
                return
            if not os.path.exists(path):
                sublime.message_dialog(
                    '"' + path + '"' +
                    "isn't a valid path and can't be opened!")
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
