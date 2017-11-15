from collections import OrderedDict
import datetime
import webpage_database_api

__author__ = 'KPGM'

now = datetime.datetime.now()
date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)

filepath = input('Filename: ')
while filepath != 'q':
    filepath = 'D:\\drive\\AA - Collective\\Links\\' + filepath + '.json'
    change = webpage_database_api.WebPages(filepath)
    change.read()
    key = list(change.data.keys())
    values = change.data.values()
    for value in values:
        value['Date'] = date
    change.write()
    filepath = input('Filename: ')