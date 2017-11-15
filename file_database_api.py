import json
import os

__author__ = 'Gareth Mok'


class Files:
    def __init__(self, filepath):
        """
        Keys are Account Names and Values is a dictionary with {'Filepath': str, 'Delay': int}
        :type filepath: str
        :param filepath: filepath path location
        :return:
        """
        assert isinstance(filepath, str)

        self.filepath = filepath
        self.data = {'Directory': ''}

        if os.path.isfile(filepath):
            self.read()
        else:
            self.write()

    def new(self):
        with open(self.filepath, 'w') as outfile:
            json.dump({}, outfile, indent=4)
        self.read()

    def read(self):
        with open(self.filepath, 'r') as readfile:
            self.data = json.load(readfile)

    def write(self):
        with open(self.filepath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        self.read()

    def add_update(self, name, file_location, delay):
        """
        Add an item to the database, rewrites if an item exists
        :type name: str
        :type file_location: str
        :type delay: int
        :param name: name of the file when opened as a tab
        :param file_location: the full file location
        :param delay: the delay between opening webpages
        :return:
        """
        assert isinstance(name, str)
        assert isinstance(file_location, str)
        assert isinstance(delay, int)

        if name != 'Directory' and not os.path.isfile(file_location):
            raise FileNotFoundError('Given file location not a valid file')
        if name not in self.data.keys():
            for names in self.data:
                if names != 'Directory':
                    if file_location == self.data[names]['File'] and name != names:
                        self.data[name] = {'File': file_location, 'Delay': self.data[names]['Delay']}
                        del self.data[names]

        self.read()
        self.data[name] = {'File': file_location, 'Delay': delay}
        self.write()

    def remove(self, name):
        """
        Remove the file from the database
        :type name: str
        :param name: name of the file in the database
        :return:
        """
        assert isinstance(name, str)

        self.read()
        if name in self.data.keys():
            self.data.pop(name)
        self.write()

    def get_directory(self):
        """
        Grab the directory for the databases
        :return: string that holds the directory path
        """
        self.read()
        return self.data['Directory']

    def set_directory(self, directory):
        """
        Set the directory for the databases
        :type directory: str
        :param directory: new directory location
        """
        assert isinstance(directory, str)
        if not os.path.isdir(directory):
            raise ValueError('Given directory is invalid')

        self.read()
        self.data['Directory'] = directory
        self.write()

    def grab(self):
        """
        Grab the data
        :return: dictionary with a str: str format with the name as key and file location as value
        """
        self.read()
        return {key: value for key, value in self.data.items() if key != 'Directory'}

    def empty(self):
        """
        Check if the database is empty. 'Directory' and 'Delay' nodes are always expected
        :return: True if empty, False if not
        """
        return len(self.data) == 1
