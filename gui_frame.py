import os
import random
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from webpage_database_api import WebPages
from file_database_api import Files
from gui_select import Select

__author__ = 'KPGM'
form_frame = uic.loadUiType('frame.ui')[0]

class Frame(QtWidgets.QWidget, form_frame):
    def __init__(self, filename, delay, parent=None):
        self.filename = filename
        self.delay = delay
        self.data = WebPages(filename)
        self.current = ''
        self.items = {}  # dictionary between Webpage names and QTableWidgetItems

        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.connect_components()
        self.initialize_shortcuts()
        self.initialize_components()

    def connect_components(self):
        self.btn_OpenLinks.clicked.connect(self.btn_open_links_clicked)
        self.btn_AddUpdate.clicked.connect(self.btn_add_update_clicked)
        self.btn_Remove.clicked.connect(self.btn_remove_clicked)
        self.btn_Copy_All.clicked.connect(self.btn_copy_all_clicked)
        self.btn_Copy_Name.clicked.connect(self.btn_copy_name_clicked)
        self.btn_Copy_Link.clicked.connect(self.btn_copy_link_clicked)
        self.btn_Copy_Last.clicked.connect(self.btn_copy_last_clicked)

        self.tbv_LinkView.cellClicked.connect(self.cell_clicked)
        self.tbv_LinkView.cellChanged.connect(self.cell_changed)
        self.tbv_LinkView.itemSelectionChanged.connect(self.selection_changed)
        self.tbv_LinkView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.lin_In_Delay.textChanged.connect(self.delay_changed)

    def initialize_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R), self, self.display_links)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_C), self, self.btn_copy_link_clicked)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S), self, self.btn_add_update_clicked)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_C),
                        self, self.clear)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_R),
                        self, self.btn_remove_clicked)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_F), self, self.find_item)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_A), self, self.increment_chapter)

    def initialize_components(self):
        self.lin_FileLocation.setText(self.filename)
        self.lin_In_Delay.blockSignals(True)
        self.lin_In_Delay.setText(str(self.delay))
        self.lin_In_Delay.blockSignals(False)
        self.display_links()

    def resize_table(self):
        self.tbv_LinkView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        size = 0
        for i in range(5):
            size += self.tbv_LinkView.horizontalHeader().sectionSize(i)

        self.tbv_LinkView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.tbv_LinkView.horizontalHeader().resizeSection(0, int(size * .4))
        self.tbv_LinkView.horizontalHeader().resizeSection(1, int(size * .3))
        self.tbv_LinkView.horizontalHeader().resizeSection(2, int(size * .1))
        self.tbv_LinkView.horizontalHeader().resizeSection(3, int(size * .1))
        self.tbv_LinkView.horizontalHeader().resizeSection(4, int(size * .1))

        self.tbv_LinkView.resizeRowsToContents()

    def display_links(self):
        self.tbv_LinkView.blockSignals(True)
        self.data.read()

        headers = ['Name', 'Link', 'Vol', 'Chap', 'Date']
        names = sorted(self.data.grab_names())

        current_rows = self.tbv_LinkView.rowCount()
        needed_rows = len(names)
        if current_rows != needed_rows:
            if current_rows < needed_rows:
                for i in range(needed_rows - current_rows):
                    if self.tbv_LinkView.rowCount() == 0:
                        self.tbv_LinkView.insertRow(self.tbv_LinkView.rowCount())
                    else:
                        self.tbv_LinkView.insertRow(self.tbv_LinkView.rowCount() - 1)
            else:
                for i in range(current_rows - needed_rows):
                    self.tbv_LinkView.removeRow(0)

        for row, name in enumerate(names):
            data = self.data.get_data(name)
            self.items[name] = QtWidgets.QTableWidgetItem(name)
            new_items = [self.items[name],
                         QtWidgets.QTableWidgetItem(str(data['Link'])),
                         QtWidgets.QTableWidgetItem(str(data['Vol'])),
                         QtWidgets.QTableWidgetItem(str(data['Chap'])),
                         QtWidgets.QTableWidgetItem(str(data['Date']))]
            for col in range(len(new_items)):
                self.tbv_LinkView.setItem(row, col, new_items[col])

        self.tbv_LinkView.setHorizontalHeaderLabels(headers)
        self.resize_table()
        self.tbv_LinkView.blockSignals(False)

    def set_lin_edit(self, input_dict):
        if input_dict['Type'] == 'In':
            self.lin_In_Name.setText(input_dict['Name'])
            self.lin_In_Link.setText(input_dict['Link'])
            self.lin_In_Last_Vol.setText(input_dict['Vol'])
            self.lin_In_Last_Chap.setText(input_dict['Chap'])
        elif input_dict['Type'] == 'Out':
            self.lin_Out_Name.setText(input_dict['Name'])
            self.lin_Out_Link.setText(input_dict['Link'])
            self.lin_Out_Last_Vol.setText(input_dict['Vol'])
            self.lin_Out_Last_Chap.setText(input_dict['Chap'])
        elif input_dict['Type'] == 'Both':
            self.lin_In_Name.setText(input_dict['Name'])
            self.lin_In_Link.setText(input_dict['Link'])
            self.lin_In_Last_Vol.setText(input_dict['Vol'])
            self.lin_In_Last_Chap.setText(input_dict['Chap'])
            self.lin_Out_Name.setText(input_dict['Name'])
            self.lin_Out_Link.setText(input_dict['Link'])
            self.lin_Out_Last_Vol.setText(input_dict['Vol'])
            self.lin_Out_Last_Chap.setText(input_dict['Chap'])

    def clear(self):
        self.set_lin_edit({'Type': 'In', 'Name': '', 'Link': '', 'Vol': '', 'Chap': ''})
        self.tbv_LinkView.clearSelection()

    def find_item(self):
        self.tbv_LinkView.clearSelection()
        name, ok = Select.select_choice(self.data.grab_names(), True, self)
        if ok and name:
            search = self.data.get_name(name)
            if len(search) == 1:
                name = search[0]
                item = self.items[name]
                self.tbv_LinkView.scrollToItem(item, 3)
                self.tbv_LinkView.setItemSelected(item, True)
            elif len(search) > 1:
                name, ok = Select.select_choice(search, False, self)
                if ok or name:
                    item = self.items[name]
                    self.tbv_LinkView.scrollToItem(item, 3)
                    self.tbv_LinkView.setItemSelected(item, True)
            self.tbv_LinkView.setFocus()

    def increment_chapter(self):
        if self.lin_In_Last_Chap.text():
            self.lin_In_Last_Chap.setText(str(int(self.lin_In_Last_Chap.text().strip()) + 1))
            self.btn_add_update_clicked()


    def btn_open_links_clicked(self):
        """
        Opens all the links in the file
        :return:
        """
        self.data.open_links(float(self.lin_In_Delay.text()))
        self.display_links()

    def btn_add_update_clicked(self):
        name = str(self.lin_In_Name.text()).strip()
        link = str(self.lin_In_Link.text()).strip()
        vol = str(self.lin_In_Last_Vol.text()).strip()
        chap = str(self.lin_In_Last_Chap.text()).strip()
        now = datetime.datetime.now()
        new_data = {'Link': link,
                    'Vol': vol,
                    'Chap': chap,
                    'Date': str(now.month) + '/' + str(now.day) + '/' + str(now.year)
                    }

        if not name:  # no name exists
            name = '_Update Name' + str(hash(random.random()))
        if not link:  # no link exists
            new_data['Link'] = '_Update Link' + str(hash(random.random()))

        name_search = self.data.get_name(name)  # Search for name with a name or link
        link_search = self.data.get_name(None, link)

        if len(name_search) > 0:  # Name found
            if len(name_search) > 1:
                name, ok = Select.select_choice(name_search, False, self)
                if ok or name:
                    data = self.data.get_data(name)
                    self.set_lin_edit({'Type': 'Both', 'Name': name,
                                       'Link': data['Link'],
                                       'Vol': data['Vol'],
                                       'Chap': data['Chap']})
            else:
                name = name_search[0]
                self.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
                if len(link_search) > 0:  # Link is found in database
                    if name != link_search[0]:  # There is a link with a different name
                        return
                self.data.add_update(name, None, None, new_data)
        else:  # Name not found
            if len(link_search) > 0:  # Link found
                old_name = link_search[0]
                self.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
                self.data.add_update(old_name, None, name, new_data)
            else:  # Completley new
                self.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
                self.data.add_update(name, None, None, new_data)

        self.display_links()

    def btn_remove_clicked(self):
        """
        Remove the item specified
        :return:
        """
        name = str(self.lin_In_Name.text()).strip()
        link = str(self.lin_In_Link.text()).strip()

        name_search = self.data.get_name(name)  # Search for name with a name or link
        link_search = self.data.get_name(None, link)

        if len(name_search) > 0:  # Name found
            ok = False
            if len(name_search) > 1:
                name, ok = Select.select_choice(name_search, False, self)
            else:
                name = name_search[0]
            if ok or name:
                data = self.data.get_data(name)
                self.set_lin_edit({'Type': 'Both', 'Name': name,
                                   'Link': data['Link'],
                                   'Vol': data['Vol'],
                                   'Chap': data['Chap']})
                self.data.remove(name, None, data)
        else:  # Name not found
            if len(link_search) > 0:  # Link found
                name = link_search[0]
                data = self.data.get_data(name)
                self.set_lin_edit({'Type': 'Both', 'Name': name,
                                   'Link': data['Link'],
                                   'Vol': data['Vol'],
                                   'Chap': data['Chap']})
                self.data.remove(name, None, data)

        self.display_links()

    def btn_copy_all_clicked(self):
        name = self.lin_Out_Name.text()
        link = self.lin_Out_Link.text()
        vol = 'v' + self.lin_Out_Last_Vol.text()
        chap = 'c' + self.lin_Out_Last_Chap.text()

        full = '\"{0}\"'.format('", "'.join([name, link, vol, chap]))
        self.lin_Out_Name.setText(full)
        self.btn_Copy_Name_clicked()
        self.lin_Out_Name.setText(name)

    def btn_copy_name_clicked(self):
        self.lin_Out_Name.selectAll()
        self.lin_Out_Name.copy()
        self.lin_Out_Name.deselect()

    def btn_copy_link_clicked(self):
        self.lin_Out_Link.selectAll()
        self.lin_Out_Link.copy()
        self.lin_Out_Link.deselect()

    def btn_copy_last_clicked(self):
        name = self.lin_Out_Name.text()
        vol = self.lin_Out_Last_Vol.text()
        chap = self.lin_Out_Last_Chap.text()

        full = 'v' + vol + ' c' + chap
        self.lin_Out_Name.setText(full)
        self.btn_Copy_Name_clicked()
        self.lin_Out_Name.setText(name)

    def cell_clicked(self, row, column):
        name = self.tbv_LinkView.item(row, 0)
        link = self.tbv_LinkView.item(row, 1)
        vol = self.tbv_LinkView.item(row, 2)
        chap = self.tbv_LinkView.item(row, 3)

        self.set_lin_edit({'Type': 'Both',
                           'Name': name.text(),
                           'Link': link.text(),
                           'Vol': vol.text(),
                           'Chap': chap.text()})

        self.current = str(self.tbv_LinkView.item(row, column).text())

    def cell_changed(self, row, column):
        name, link, vol, chap = [str(self.tbv_LinkView.item(row, 0).text()),
                                 str(self.tbv_LinkView.item(row, 1).text()),
                                 str(self.tbv_LinkView.item(row, 2).text()),
                                 str(self.tbv_LinkView.item(row, 3).text())]

        now = datetime.datetime.now()
        date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
        if column == 0:  # Name [self.current contains the previous name]
            self.data.add_update(self.current, None, name, {'Link': link, 'Vol': vol, 'Chap': chap, 'Date': date})
        elif column == 1:  # Link [self.current contains the previous link]
            self.data.add_update(name, self.current , None, {'Link': link, 'Vol': vol, 'Chap': chap, 'Date': date})
        elif column == 2 or column == 3:  # Vol or Chapter [self.current contains the previous volume or chapter #]
            self.data.add_update(name, link, None, {'Link': link, 'Vol': vol, 'Chap': chap, 'Date': date})

        self.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
        self.display_links()

    def selection_changed(self):
        for index in self.tbv_LinkView.selectedIndexes():
            row = index.row()
            name = self.tbv_LinkView.item(row, 0).text()
            data = self.data.get_data(name)
            self.set_lin_edit({'Type': 'Both', 'Name': name,
                               'Link': data['Link'],
                               'Vol': data['Vol'],
                               'Chap': data['Chap']})
            self.current = str(self.tbv_LinkView.item(row, index.column()).text())

    def delay_changed(self, delay):
        last_session = Files('last_open.json')
        last_session.add_update(os.path.basename(self.filename), self.filename, int(delay))
