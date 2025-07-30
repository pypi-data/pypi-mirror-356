import os
from PySide6.QtWidgets import QComboBox, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class QComboBoxCmap(QComboBox):
    def __init__(self):
        super().__init__()

        colormap_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'combo_selector','resources', 'colormaps'))

        if os.path.isdir(colormap_directory):
            for file in os.listdir(colormap_directory):
                filename = os.fsdecode(file)
                if filename.endswith(".png"):
                    cmapIcon = QIcon(os.path.join(colormap_directory, filename))
                    self.addItem(cmapIcon, os.path.splitext(filename)[0])
        size = QSize(70, 20)
        self.setCurrentText('Spectral')
        self.setIconSize(size)
        self.adjustSize()

def main():
    import sys
    app = QApplication(sys.argv)
    cmap = QComboBoxCmap()
    cmap.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()