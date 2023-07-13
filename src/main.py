from PyQt6.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QTextEdit, QPushButton, QGridLayout
from ui_generated.basic import Ui_CopyPasta

        
class MainWindow(QMainWindow, Ui_CopyPasta):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_field.clicked.connect(self.duplicate_form)
        self.clipboard = QApplication.clipboard()




    def duplicate_form(self):
        # Create a new form entry
        new_frame = QFrame(parent=self.scrollAreaWidgetContents)
        new_frame.setMinimumSize(self.basic_frame_template.minimumSize())
        new_frame.setMaximumSize(self.basic_frame_template.maximumSize())
        new_frame.setFrameShape(QFrame.Shape.StyledPanel)
        new_frame.setFrameShadow(QFrame.Shadow.Raised)

        layout = QGridLayout(new_frame)

        item_name = QLabel(parent=new_frame)
        item_name.setMaximumSize(self.item_name.maximumSize())
        item_name.setObjectName("item_name")
        item_name.setText("item_name")
        layout.addWidget(item_name, 0, 0)

        item_info = QTextEdit(parent=new_frame)
        item_info.setMinimumSize(self.item_info.minimumSize())
        item_info.setMaximumSize(self.item_info.maximumSize())
        item_info.setObjectName("item_info")
        item_info.isReadOnly(True)
        layout.addWidget(item_info, 1, 0)

        edit = QPushButton(parent=new_frame)
        edit.setMinimumSize(self.edit.minimumSize())
        edit.setMaximumSize(self.edit.maximumSize())
        edit.setObjectName("edit")
        edit.setText("edit")
        edit.setEnabled(True)
        edit.clicked.connect(self.edit_entry)
        layout.addWidget(edit, 1, 1)

        copy = QPushButton(parent=new_frame)
        copy.setMinimumSize(self.copy.minimumSize())
        copy.setMaximumSize(self.copy.maximumSize())
        copy.setObjectName("copy")
        copy.setText("copy")
        copy.clicked.connect(self.copy_entry_to_clipboard)
        layout.addWidget(copy, 1, 2)

        delete = QPushButton(parent=new_frame)
        delete.setMinimumSize(self.delete.minimumSize())
        delete.setMaximumSize(self.delete.maximumSize())
        delete.setObjectName("delete")
        delete.setText("delete")
        layout.addWidget(delete, 1, 3)
        delete.clicked.connect(self.delete_entry)

        self.scrollable.addWidget(new_frame)


    def delete_entry(self):
        sender = self.sender()
        entry = sender.parent()
        entry.deleteLater()

    def copy_entry_to_clipboard(self):

        sender = self.sender()
        entry = sender.parent()
        item_info = entry.findChild(QTextEdit, "item_info")
        self.clipboard.setText(item_info.toPlainText())
        print("copied")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
