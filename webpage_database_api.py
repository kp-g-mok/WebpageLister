import json

from collections import OrderedDict
import webbrowser
from time import sleep

__author__ = 'KPGM'

class WebPages:
    def __init__(self, file):
        """
        Headers are Name, Link, Vol, Chap
        :param file:
        :return:
        """
        self.webdrivers = []

        self.file = file
        self.data = {}
        try:
            self.read()
        except FileNotFoundError:
            self.write()

    def new(self):
        with open(self.file, 'w') as outfile:
            json.dump({}, outfile, indent=4)
        self.read()

    def read(self):
        with open(self.file, 'r') as readfile:
            data = json.load(readfile, object_pairs_hook=OrderedDict)
            self.data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

    def write(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        self.read()

    def get_name(self, name=None, link=None):
        if name:
            return [key for key, value in self.data.items() if name.lower() in key.lower()]
        elif link:
            return [key for key, value in self.data.items() if link.lower() in value['Link'].lower()]

    def get_data(self, name):
        if name in self.data.keys():
            return self.data[name]
        return {}

    def add_update(self, name=None, link=None, new_name=None, new_info=None):
        self.read()
        if not new_name and not new_info:
            return False  # Nothing to update with
        check = self.get_name(name, link)
        if check:  # Found a result
            name = check[0]
            if not new_name and new_info:  # No new_name but new_info
                self.data[name] = new_info  # Update old name with new info
            else:
                if new_info:
                    self.data[new_name] = new_info  # Add or update with new item
                else:
                    self.data[new_name] = self.data[name]  # Update old info with new name
                if new_name != name:
                    del self.data[name]  # Remove old name
            self.write()
            return True
        else:  # New item
            self.data[name] = new_info
            self.write()
            return True

    def remove(self, name=None, link=None, verify=None):
        self.read()
        check = self.get_name(name, link)
        if len(check) > 0:
            if len(check) == 1:
                del self.data[check[0]]  # TODO delete multiple?
            else:
                if verify:
                    for name in check:
                        if self.data[name]['Link'] == verify['Link']:
                            del self.data[name]
            self.write()
            return True
        return False

    def grab_names(self):
        return [key for key, value in self.data.items()]

    def open_links(self, delay):
        self.read()
        key = list(self.data.keys())
        values = self.data.values()
        for i, item in enumerate(values):
            if item['Link'][:4] == 'skip':
                self.data[key[i]]['Link'] = item['Link'][4:]
                continue
            webbrowser.open_new_tab(item['Link'])  # open link in new tab
            sleep(delay)
        self.write()

    def empty(self):
        return len(self.data) > 0
