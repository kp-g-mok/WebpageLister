import os
import sys
from PyQt4 import QtCore, QtGui, uic

from file_database_api import Files
from gui_frame import Frame
from gui_select import Select

__author__ = 'KPGM'

form_main = uic.loadUiType('main.ui')[0]


class MainWindow(QtGui.QMainWindow, form_main):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.last_session = Files('last_open.json')
        try:
            if os.path.isdir(self.last_session.get_directory()):
                self.directory = self.last_session.get_directory()
            else:
                if getattr(sys, 'frozen', False):  # frozen
                    self.directory = os.path.dirname(os.path.realpath(sys.executable))
                else:  # unfrozen
                    self.directory = os.path.dirname(os.path.realpath(__file__))
                try:
                    self.last_session.set_directory(self.directory)
                except ValueError as ve:
                    error_message(ve)

            file_list = self.last_session.grab()
            sorted_names = sorted(file_list)
            for i, name in enumerate(sorted_names):
                if os.path.isfile(file_list[name]['File']):
                    new_tab = Frame(file_list[name]['File'],  file_list[name]['Delay'], self)
                    self.FileList.addTab(new_tab, name)
                else:
                    self.last_session.remove(name)
        except ValueError:
            if getattr(sys, 'frozen', False):  # frozen
                self.directory = os.path.dirname(os.path.realpath(sys.executable))
            else:  # unfrozen
                self.directory = os.path.dirname(os.path.realpath(__file__))
            try:
                self.last_session.set_directory(self.directory)
            except ValueError as ve:
                error_message(ve)

        self.connect_components()
        self.initialize_shortcuts()

    def connect_components(self):
        self.act_New.triggered.connect(self.act_new_triggered)
        self.act_Open.triggered.connect(self.act_open_triggered)
        self.act_Close_Tab.triggered.connect(self.act_close_tab_triggered)
        self.act_Exit.triggered.connect(self.act_exit_triggered)
        self.act_Move_Link.triggered.connect(self.act_move_link_triggered)
        self.act_Change_Database_Directory.triggered.connect(self.act_change_default_account_directory_triggered)
        self.FileList.currentChanged.connect(self.refresh)

    def initialize_shortcuts(self):
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Tab),
                        self, self.next_tab)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Tab),
                        self, self.previous_tab)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_V), self, self.skip)

    def next_tab(self):
        new_index = (self.FileList.currentIndex() + 1) % self.FileList.count()
        self.FileList.setCurrentIndex(new_index)

    def previous_tab(self):
        new_index = self.FileList.currentIndex() - 1
        if new_index == -1:
            new_index = self.FileList.count() - 1
        self.FileList.setCurrentIndex(new_index)

    def skip(self):
        tab = self.FileList.currentWidget()
        name = tab.lin_Out_Name.text()
        link = 'skip'+tab.lin_Out_Link.text()
        vol = tab.lin_Out_Last_Vol.text()
        chap = tab.lin_Out_Last_Chap.text()
        tab.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
        tab.btn_add_update_clicked()

    def act_new_triggered(self):
        '''
        Creates a new csv list and opens in a new tab
        :return:
        '''
        filename = QtGui.QFileDialog.getSaveFileName(QtGui.QFileDialog(), 'New file', self.directory, '*.json')
        if filename != '':
            base_filename = os.path.basename(filename)

            new_tab = Frame(filename, 2)
            new_tab.lin_FileLocation.setText(filename)
            self.FileList.addTab(new_tab, base_filename)
            self.FileList.setCurrentIndex(self.FileList.count() - 1)
            self.FileList.currentWidget().display_links()
            self.last_session.add_update(base_filename, filename, 2)

    def act_open_triggered(self):
        """
        Opens a file in current tab or new tab
        :return:
        """
        filename = QtGui.QFileDialog.getOpenFileName(QtGui.QFileDialog(), 'Open file', self.directory, '*.json')
        if filename != '':
            base_filename = os.path.basename(filename)

            for i in range(self.FileList.count()):
                text = str(self.FileList.tabText(i))
                if text == base_filename:
                    self.FileList.setCurrentIndex(i)
                    self.FileList.currentWidget().display_links()
                    break
            else:
                new_tab = Frame(filename, 2, self)
                self.FileList.addTab(new_tab, base_filename)
                self.FileList.setCurrentIndex(self.FileList.count() - 1)
                self.FileList.currentWidget().display_links()
                self.last_session.add_update(base_filename, filename, 2)

    def act_close_tab_triggered(self):
        current = self.FileList.currentIndex()
        self.last_session.remove(str(self.FileList.tabText(current)))
        self.FileList.removeTab(current)

    def act_change_default_account_directory_triggered(self):
        self.directory = QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), None,
                                                                'Choose Webpage Database Directory')
        self.last_session.set_directory(self.directory)

    def act_exit_triggered(self):
        self.close()

    def act_move_link_triggered(self):
        # create df of tabs
        current = self.FileList.currentIndex()
        tab = self.FileList.currentWidget()
        name = tab.lin_Out_Name.text()
        link = tab.lin_Out_Link.text()
        vol = tab.lin_Out_Last_Vol.text()
        chap = tab.lin_Out_Last_Chap.text()

        name_search = tab.data.get_name(name, link)

        if len(name_search) > 1:
            name, ok = Select.select_choice(name_search, False, self)
            data = tab.data.get_data(name)
            link = data['Link']
            vol = data['Vol']
            chap = data['Chap']

        filelist = sorted(self.last_session.grab().keys())
        filelist.remove(self.FileList.tabText(current))
        dfilename, ok = Select.select_choice(filelist, False, self)

        for i in range(self.FileList.count()):
            if dfilename == self.FileList.tabText(i):
                tab.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
                tab.btn_remove_clicked()
                self.FileList.setCurrentIndex(i)
                new_tab = self.FileList.currentWidget()
                new_tab.set_lin_edit({'Type': 'Both', 'Name': name, 'Link': link, 'Vol': vol, 'Chap': chap})
                new_tab.btn_add_update_clicked()
                self.FileList.setCurrentIndex(current)
                break

    def refresh(self):
        if self.FileList.currentWidget():
            self.FileList.currentWidget().display_links()

def error_message(err_msg):
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Critical)
    msg.setText("Error when running utility.")
    msg.setInformativeText(str(err_msg))
    msg.setWindowTitle("Error Message")
    msg.setStandardButtons(QtGui.QMessageBox.Ok)

    msg.exec_()

def main():
    app = QtGui.QApplication(sys.argv)
    myWindow = MainWindow(None)
    myWindow.show()
    myWindow.refresh()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()