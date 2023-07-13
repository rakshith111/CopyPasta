from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDialogButtonBox

class AddEditDialog(QDialog):
    def __init__(self, parent=None):
        '''
        Simple dialog to add or edit an item in the list.
        Args:
            parent (_type_, optional):  Defaults to None.
        '''        
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Item")
        self.layout = QVBoxLayout(self)
        self.item_name_label = QLabel("Item Name:", self)
        self.item_name_input = QLineEdit(self)
        self.field_value_label = QLabel("Field Value:", self)
        self.field_value_input = QTextEdit(self)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        self.layout.addWidget(self.item_name_label)
        self.layout.addWidget(self.item_name_input)
        self.layout.addWidget(self.field_value_label)
        self.layout.addWidget(self.field_value_input)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_item_data(self):
        item_name = self.item_name_input.text()
        field_value = self.field_value_input.toPlainText()
        return item_name, field_value
