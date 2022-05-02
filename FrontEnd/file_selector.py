import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 800, 200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options = ('Get File Name', 'Get Folder Dir')

        self.combo = QComboBox()
        self.combo.addItems(self.options)
        layout.addWidget(self.combo)

        btn = QPushButton('Launch')
        btn.clicked.connect(self.launchDialog)
        layout.addWidget(btn)

    def launchDialog(self):
        option = self.options.index(self.combo.currentText())

        if option == 0:
            response = self.getFileName()
        elif option == 1:
            response = self.getDirectory()
        else:
            print('Got Nothing')

    def getFileName(self):
        file_filter = 'Text File (*.txt)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Text File (*.txt)'
        )
        print(response[0])
        return response[0]

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        return response


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
