import os.path
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *


class PlayerError(Exception):
    """Базовый класс для ошибок плеера."""
    pass

class FileLoadError(PlayerError):
    """Ошибка загрузки файла."""
    pass

class PlaybackError(PlayerError):
    """Ошибка воспроизведения."""
    pass



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(429, 572)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        

        #иконка окна
        icon.addPixmap(QtGui.QPixmap("icon2.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        #пуск
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 410, 75, 81))
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pusk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(45, 45))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pause_and_unpause)

        #кнопка назад
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 410, 81, 81))
        self.pushButton_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.stop_song)
        
        #кнопка вперёд
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 410, 81, 81))
        self.pushButton_3.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.next_song)
        #кнопка паузы
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 410, 81, 81))
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.hide()
        self.pushButton_4.clicked.connect(self.pause_and_unpause)
        # громкость
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(30, 390, 20, 101))
        self.verticalSlider.setSizeIncrement(QtCore.QSize(0, 0))
        self.verticalSlider.setMouseTracking(False)
        self.verticalSlider.setTabletTracking(False)
        self.verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalSlider.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.verticalSlider.setStatusTip("")
        self.verticalSlider.setAutoFillBackground(True)
        self.verticalSlider.setSingleStep(1)
        self.verticalSlider.setProperty("value", 50)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setInvertedAppearance(False)
        self.verticalSlider.setInvertedControls(False)
        self.verticalSlider.setObjectName("verticalSlider")
        self.verticalSlider.sliderMoved[int].connect(lambda: self.volume_changed())
        # дорожка трека 
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(70, 380, 291, 15))
        self.horizontalSlider.setMouseTracking(False)
        self.horizontalSlider.setAutoFillBackground(True)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.horizontalSlider.value()))
        #название трека 
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 340, 291, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        #обложка 
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 50, 281, 271))
        self.label_2.setStyleSheet("")
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setLineWidth(2)
        self.label_2.setMidLineWidth(10)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("cat.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        # кнопка загрузки 
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(370, 345, 40, 40))
        self.pushButton_5.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon5)
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton_5.clicked.connect(self.add_songs)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Inits
        # создание списка с треками 
        self.current_songs = []
        # устанавливаем уровень громкости
        self.current_volume = 50
        # таймер для бегущей строки
        self.marquee_timer = QTimer()
        self.marquee_timer.timeout.connect(self.marquee)
        self.marquee_timer.start(400)  # Интервал в полсекунды

        self.current_songs_index = 0

    

        global stopped
        stopped = False

        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(self.current_volume)

        # Slider Timer
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)

    def move_slider(self):
        if stopped:
            return
        else:
            # Update the slider
            if self.player.state() == QMediaPlayer.PlayingState:
                self.horizontalSlider.setMinimum(0)
                self.horizontalSlider.setMaximum(self.player.duration())
                slider_position = self.player.position()
                self.horizontalSlider.setValue(slider_position)
   



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MP3 Player"))
        self.label.setText(_translate("MainWindow", ""))

    #загрузка трека    
    def add_songs(self):
        try:
            files, _ = QtWidgets.QFileDialog.getOpenFileNames(
                None, "Выберите аудиофайлы", "", "Audio Files (*.mp3 *.wav *.ogg)")

            if files:
                for file in files:
                    if file not in self.current_songs:
                        self.current_songs.append(file)
                        print(f"Добавлен трек: {os.path.basename(file)}")

            if self.current_songs:
                self.play_song()
        except Exception as e:
            raise FileLoadError(f"Ошибка при добавлении песен: {e}")

    def play_song(self):
        try:
            self.pushButton.hide()
            self.pushButton_4.show()
            if self.current_songs:  # проверка, что список песен не пуст
                current_song = self.current_songs[self.current_songs_index]  # выбор текущей песни из списка

                song_url = QMediaContent(QUrl.fromLocalFile(current_song))
                self.player.setMedia(song_url)
                if self.player.state() == QMediaPlayer.PlayingState:

                    self.pushButton_4.hide()
                    self.pushButton.show()
                    # Если песня уже играет, то сохраняем текущую позицию и продолжаем воспроизведение
                    current_position = self.player.position()
                    
                    self.player.pause()  # Останавливаем воспроизведение
                    self.player.setPosition(current_position)  # Восстанавливаем позицию после паузы
            
            
                else:
                    self.player.play()
                    self.move_slider()
                    self.pushButton.hide()
                    self.pushButton_4.show()
          
       
            # Добавить название песни
            self.label.setText(os.path.basename(current_song))
            self.label.setToolTip(os.path.basename(current_song))  # Показывает полное название при наведении
            # Начать бегущую строку
            self.marquee_pos = 0
            self.marquee()

            if not self.current_songs:
                raise PlaybackError("Плейлист пуст.")
        except Exception as e:
            raise PlaybackError(f"Ошибка воспроизведения: {e}")

    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:

            self.pushButton_4.hide()
            self.pushButton.show()
            # Если песня уже играет, то сохраняем текущую позицию и продолжаем воспроизведение
            current_position = self.player.position()
            
            self.player.pause()  # Останавливаем воспроизведение
            self.player.setPosition(current_position)  # Восстанавливаем позицию после паузы
            
            
        else:
            self.player.play()
            self.pushButton.hide()
            self.pushButton_4.show()

    #следующая песня 
    def next_song(self):
        try:
            current_selection = self.current_songs_index  # используем сохраненный индекс

            if current_selection + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection + 1

            current_song = self.current_songs[next_index]
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()

            self.update_song_title(current_song)
            self.marquee_pos = 0
            self.marquee()

            self.current_songs_index = next_index  # сохраняем новый индекс
        except Exception as e:
            #print(f"Next song error: {e}")
            raise e 
    def update_song_title(self, song_path):
        # Обновляем название песни
        self.label.setText(os.path.basename(song_path))
        self.label.setToolTip(os.path.basename(song_path))

    def stop_song(self):
        self.player.stop()
        self.horizontalSlider.setValue(0)
        self.pushButton.show()
        self.pushButton_4.hide()

    def volume_changed(self):
        self.current_volume = self.verticalSlider.value()
        self.player.setVolume(self.current_volume)

    def marquee(self):
        # Бегущая строка
        text = self.label.text()
        if len(text) > 10:  # Если название песни длиннее 10 символов
            self.marquee_pos = (self.marquee_pos + 1) % len(text)
            self.label.setText(text[self.marquee_pos:]  + text[:self.marquee_pos])

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
