from PyQt6.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QTextEdit, QPushButton, QGridLayout, QDialog,QMessageBox

from ui_generated.basic import Ui_CopyPasta
from add_widget import AddEditDialog
class MainWindow(QMainWindow, Ui_CopyPasta):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_field.clicked.connect(self.show_add_dialog)
        self.edit.clicked.connect(self.show_edit_dialog)
        self.item_info.setReadOnly(True)
        self.delete.setDisabled(True)
        self.copy.clicked.connect(self.copy_entry_to_clipboard)
        self.clipboard = QApplication.clipboard()

    def show_add_dialog(self):
        dialog = AddEditDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item_name, field_value = dialog.get_item_data()
            self.create_form_entry(item_name, field_value)

    def show_edit_dialog(self):
        dialog = AddEditDialog(self)
        dialog.setWindowTitle("Edit Item")
        selected_frame = self.focusWidget().parent()
        item_name_label = selected_frame.findChild(QLabel, "item_name")
        item_info_text_edit = selected_frame.findChild(QTextEdit, "item_info")
        dialog.item_name_input.setText(item_name_label.text())
        dialog.field_value_input.setPlainText(item_info_text_edit.toPlainText())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item_name, field_value = dialog.get_item_data()

            if not item_name.strip() and not field_value.strip():
                QMessageBox.critical(self, "Invalid Input", "Item name and field value cannot be empty.")
                # reopens the dialog
                self.show_edit_dialog()
            else:
                item_name_label.setText(item_name)
                item_info_text_edit.setPlainText(field_value)


    def create_form_entry(self, item_name, field_value):
        new_frame = QFrame(parent=self.scrollAreaWidgetContents)
        new_frame.setMinimumSize(self.basic_frame_template.minimumSize())
        new_frame.setMaximumSize(self.basic_frame_template.maximumSize())
        new_frame.setFrameShape(QFrame.Shape.StyledPanel)
        new_frame.setFrameShadow(QFrame.Shadow.Raised)

        layout = QGridLayout(new_frame)

        item_name_label = QLabel(parent=new_frame)
        item_name_label.setMaximumSize(self.item_name.maximumSize())
        item_name_label.setObjectName("item_name")
        item_name_label.setText(item_name)
        layout.addWidget(item_name_label, 0, 0)

        item_info_text_edit = QTextEdit(parent=new_frame)
        item_info_text_edit.setMinimumSize(self.item_info.minimumSize())
        item_info_text_edit.setMaximumSize(self.item_info.maximumSize())
        item_info_text_edit.setObjectName("item_info")
        item_info_text_edit.setPlainText(field_value)
        item_info_text_edit.setReadOnly(True)
        layout.addWidget(item_info_text_edit, 1, 0)

        delete_button = QPushButton(parent=new_frame)
        delete_button.setMinimumSize(self.delete.minimumSize())
        delete_button.setMaximumSize(self.delete.maximumSize())
        delete_button.setObjectName("delete")
        delete_button.setText("delete")
        layout.addWidget(delete_button, 1, 1)


        edit_button = QPushButton(parent=new_frame)
        edit_button.setMinimumSize(self.edit.minimumSize())
        edit_button.setMaximumSize(self.edit.maximumSize())
        edit_button.setObjectName("edit")
        edit_button.setText("edit")
        edit_button.setEnabled(True)
        edit_button.clicked.connect(self.show_edit_dialog)
        layout.addWidget(edit_button, 1, 2)

        copy_button = QPushButton(parent=new_frame)
        copy_button.setMinimumSize(self.copy.minimumSize())
        copy_button.setMaximumSize(self.copy.maximumSize())
        copy_button.setObjectName("copy")
        copy_button.setText("copy")
        copy_button.clicked.connect(self.copy_entry_to_clipboard)
        layout.addWidget(copy_button, 1, 3)       

        delete_button.clicked.connect(self.delete_entry)

        self.scrollable.addWidget(new_frame)

    def delete_entry(self):
        
        sender = self.sender()
        entry = sender.parent()
        if entry.objectName() == "basic_frame_template":
            # do not delete the template
            return
        entry.deleteLater()

    def copy_entry_to_clipboard(self):

        sender = self.sender()
        entry = sender.parent()
        item_info_text_edit = entry.findChild(QTextEdit, "item_info")
        self.clipboard.setText(item_info_text_edit.toPlainText())
     

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
