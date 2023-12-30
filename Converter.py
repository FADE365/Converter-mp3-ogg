import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressBar, QPushButton, QLabel
from pydub import AudioSegment

# Устанавливаем переменные среды для ffmpeg и ffprobe
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

# Функция для конвертации mp3 в ogg
def convert_mp3_to_ogg(source_folder, target_folder):
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.mp3'):
                mp3_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(mp3_path, source_folder)
                ogg_relative_path = os.path.splitext(relative_path)[0] + '.ogg'
                ogg_path = os.path.join(target_folder, ogg_relative_path)

                os.makedirs(os.path.dirname(ogg_path), exist_ok=True)

                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(ogg_path, format='ogg', bitrate='192k')

# Функция для конвертации ogg в mp3
def convert_ogg_to_mp3(source_folder, target_folder):
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.ogg'):
                ogg_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(ogg_path, source_folder)
                mp3_relative_path = os.path.splitext(relative_path)[0] + '.mp3'
                mp3_path = os.path.join(target_folder, mp3_relative_path)

                os.makedirs(os.path.dirname(mp3_path), exist_ok=True)

                audio = AudioSegment.from_ogg(ogg_path)
                audio.export(mp3_path, format='mp3', bitrate='192k')

# Класс основного окна приложения
# Класс основного окна приложения
# Класс основного окна приложения
class AudioConverterApp(QMainWindow):
    def __init__(self):
        super(AudioConverterApp, self).__init__()
        self.initUI()
        self.moving = False

    def initUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle('Audio Converter')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;  # Фон черный
                border: 5px solid green;
                border-radius: 15px;
            }
            QPushButton {
                border: 3px solid green;
                border-radius: 10px;
                background-color: #333333;
                color: white;  # Текст белый
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QLabel, QComboBox, QProgressBar {
                color: white;
            }
        """)

        # Кнопка выбора исходной папки
        self.sourceButton = QPushButton('Source Folder', self)
        self.sourceButton.setGeometry(QtCore.QRect(50, 50, 100, 40))
        self.sourceButton.setStyleSheet("QPushButton { border: 3px solid green; border-radius: 10px; }")

        # Кнопка выбора папки для экспорта
        self.targetButton = QPushButton('Extract Folder', self)
        self.targetButton.setGeometry(QtCore.QRect(250, 50, 100, 40))
        self.targetButton.setStyleSheet("QPushButton { border: 3px solid green; border-radius: 10px; }")

        # Переключатель формата конвертации
        self.toggleConversion = QtWidgets.QComboBox(self)
        self.toggleConversion.setGeometry(QtCore.QRect(150, 120, 100, 40))
        self.toggleConversion.addItems(['MP3 to OGG', 'OGG to MP3'])

        # Линия загрузки
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(50, 200, 340, 25)

        # Окошко сообщений
        self.messageBox = QLabel(self)
        self.messageBox.setGeometry(50, 240, 300, 50)
        self.messageBox.setStyleSheet("QLabel { border: 1px solid black; border-radius: 5px; }")
        self.messageBox.setAlignment(QtCore.Qt.AlignCenter)

        # Обработка закрытия приложения
        exitButton = QPushButton('X', self)
        exitButton.setFont(QtGui.QFont('Arial', 11, QtGui.QFont.Bold))
        exitButton.setStyleSheet("QPushButton { background-color: red; border-radius: 10px; }")
        exitButton.clicked.connect(self.close)
        exitButton.setGeometry(360, 10, 30, 30)

        # Кнопка для запуска конвертации
        self.convertButton = QPushButton('Convert', self)
        self.convertButton.setGeometry(QtCore.QRect(150, 160, 100, 40))
        self.convertButton.clicked.connect(self.start_conversion)

        # Сигналы
        self.sourceButton.clicked.connect(self.select_source_folder)
        self.targetButton.clicked.connect(self.select_target_folder)

    def select_source_folder(self):
        self.source_folder = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if self.source_folder:
            self.messageBox.setText("Selected source folder: " + self.source_folder)

    def select_target_folder(self):
        self.target_folder = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if self.target_folder:
            self.messageBox.setText("Selected target folder: " + self.target_folder)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.moving = True
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.moving:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.moving = False

    def start_conversion(self):
        # Вызываем соответствующую функцию конвертации в зависимости от выбранного варианта
        conversion_type = self.toggleConversion.currentText()
        if conversion_type == 'MP3 to OGG':
            convert_mp3_to_ogg(self.source_folder, self.target_folder)
        else:
            convert_ogg_to_mp3(self.source_folder, self.target_folder)
        self.progressBar.setValue(100)
        QMessageBox.information(self, "Conversion Complete", "Your files have been converted.")


# Главный блок
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = AudioConverterApp()
    mainWin.show()
    sys.exit(app.exec_())
