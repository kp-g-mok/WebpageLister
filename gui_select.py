from PyQt5 import QtCore, QtGui, QtWidgets, uic

__author__ = 'Gareth Mok'
form_import = uic.loadUiType('select.ui')[0]

class Select(QtWidgets.QDialog, form_import):
    def __init__(self, choices, editable, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.choice = ''

        self.clearFocus()
        self.combo_Choices.setFocus()
        for choice in choices:
            self.combo_Choices.addItem(choice)
        if editable:
            self.combo_Choices.setEditable(True)
            self.combo_Choices.clearEditText()
        else:
            self.combo_Choices.setEditable(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.btn_accepted_clicked)

    def btn_accepted_clicked(self):
        self.choice = self.combo_Choices.currentText()

    @staticmethod
    def select_choice(choices, editable=False, parent=None):
        """
        ok, name, link, last = Select.select_result()
        :param parent:
        :return:
        """
        dialog = Select(choices, editable, parent)
        result = dialog.exec_()

        return dialog.choice, result == QtWidgets.QDialog.Accepted
