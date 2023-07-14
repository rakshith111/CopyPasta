from PyQt6.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QTextEdit, QPushButton, QGridLayout, QDialog,QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import json
import os
import sys

from ui_generated.basic import Ui_CopyPasta
from add_widget import AddEditDialog
class MainWindow(QMainWindow, Ui_CopyPasta):
    '''
    Main window of the application.

    Args:
        QMainWindow (QMainWindow): Main window class.
        Ui_CopyPasta (Ui_CopyPasta): Generated UI class.
    '''    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_field.clicked.connect(self.show_add_dialog)
        self.basic_frame_template.hide()
        self.clipboard = QApplication.clipboard()
        self.data_dir = os.path.join('src','user_data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.data_file = os.path.normpath(os.path.join(self.data_dir, "data.json"))
        self.huge = 69
        self.frames = []
        self.load_data()
        self.label.setScaledContents(True)
        self.setWindowTitle("CopyPasta")
        self.resource_path()   

    def resource_path(self):
        '''
        Sets the path to the resource folder.
         return os.path.join(base_path, relative_path)
        '''
        if hasattr(sys, '_MEIPASS'):
        
            # Bundled with PyInstaller
            base_path = sys._MEIPASS
  
            self.label.setPixmap(QPixmap(os.path.join(base_path,"src","ui_files","icons","title.png")))
            self.setWindowIcon(QIcon(os.path.join(base_path,"src","ui_files","icons","icon.png")))

        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
            self.label.setPixmap(QPixmap(os.path.join("src","ui_files","icons","title.png")))
            self.setWindowIcon(QIcon(os.path.join("src","ui_files","icons","icon.png")))
       

    def show_add_dialog(self):
        '''
        Shows the add dialog.
        '''        
        dialog = AddEditDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item_name, field_value = dialog.get_item_data()
            if not item_name.strip() and not field_value.strip():
                QMessageBox.critical(self, "Invalid Input", "Item name and field value cannot be empty.")
                self.show_add_dialog()
            else:
                self.create_form_entry(item_name, field_value)
                self.save_data()

    def show_edit_dialog(self):
        '''
        Shows the edit dialog.
        '''        
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
                self.save_data()

    def create_form_entry(self, item_name: str, field_value: str)->None:
        '''
        Creates a new form entry.

        Args:
            item_name (str): Name of the item.
            field_value (str): Value of the item.
        '''        
        new_frame = QFrame(parent=self.scrollAreaWidgetContents)
        new_frame.setMinimumSize(self.basic_frame_template.minimumSize())
        new_frame.setMaximumSize(self.basic_frame_template.maximumSize())
        new_frame.setFrameShape(QFrame.Shape.StyledPanel)
        new_frame.setFrameShadow(QFrame.Shadow.Raised)
        new_frame.setObjectName(f'my_{self.huge}_frame')
        self.huge+=1
        self.frames.append(new_frame)
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
        '''
        Deletes the selected entry.
        '''        
        
        sender = self.sender()
        entry = sender.parent()
        if entry.objectName() == "basic_frame_template":
            # do not delete the template
            pass
        if entry.objectName().startswith("my_"):
            self.frames.remove(entry)
            entry.deleteLater()
            self.save_data()

    def copy_entry_to_clipboard(self):
        '''
        Copies the selected entry to the clipboard.
        '''        

        sender = self.sender()
        entry = sender.parent()
        item_info_text_edit = entry.findChild(QTextEdit, "item_info")
        self.clipboard.setText(item_info_text_edit.toPlainText())
        print("Copied to clipboard")

    def save_data(self):
        '''
        Saves the data to the data file.
        '''        
        data = []

        if len(self.frames)>=1:
            # iterate over all the frames
            for frame in self.frames:
                if frame.objectName() == "basic_frame_template":
                    continue
                elif frame.objectName().startswith("my_"):
                    item_name_label = frame.findChild(QLabel, "item_name")
                    item_info_text_edit = frame.findChild(QTextEdit, "item_info")
                    item_name = item_name_label.text()
                    item_info = item_info_text_edit.toPlainText()
                    data.append({"item_name": item_name, "item_info": item_info})
            with open(self.data_file, "w") as file:
                json.dump(data, file, indent=4)
        else:
            with open(self.data_file, "w") as file:
                json.dump(data, file, indent=4)

            
    def load_data(self):
        '''
        Loads the data from the data file.
        '''        
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                for item in data:
                    item_name = item["item_name"]
                    item_info = item["item_info"]
                    self.create_form_entry(item_name, item_info)
        except FileNotFoundError:
            if not os.path.exists(self.data_dir):
                os.mkdir(self.data_dir)
            with open(self.data_file, "w") as file:
                data={}
                json.dump(data, file, indent=4)
     

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.setStyle("Fusion")
    mainWindow.show()
    sys.exit(app.exec())
