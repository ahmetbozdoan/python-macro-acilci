import sys
import time
import random
import threading
import pyautogui
import keyboard
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QWidget, QLabel, QCheckBox, QHBoxLayout, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class MacroSignals(QObject):
    # Sinyal tanımı
    status_update = pyqtSignal(str)

class Macro(threading.Thread):
    def __init__(self, message="ACİL İTEMLERİNİZ ALINIR", interval_seconds=1.0):
        super().__init__()
        self.running = False
        self.paused = False
        self.signals = MacroSignals()
        self.daemon = True  # Ana program kapandığında thread'in de kapanması için
        self.message = message
        self.interval_seconds = interval_seconds
    
    def run(self):
        self.running = True
        self.signals.status_update.emit("Çalışıyor...")
        
        while self.running:
            if not self.paused:
                try:
                    # ENTER tuşuna bas
                    keyboard.press_and_release('enter')
                    
                    # Kısa bir bekleme ekleyelim
                    time.sleep(random.uniform(0.2, 0.3))
                    
                    # Mesajı yaz
                    keyboard.write(self.message)
                    
                    # Kısa bir bekleme ekleyelim
                    time.sleep(random.uniform(0.2, 0.3))
                    
                    # Tekrar ENTER tuşuna bas
                    keyboard.press_and_release('enter')
                    
                    # Bir kez daha ENTER tuşuna bas (boş satır için)
                    time.sleep(random.uniform(0.1, 0.2))
                    keyboard.press_and_release('enter')
                    
                    # Kullanıcının belirlediği saniye aralığında bekleme
                    wait_time = random.uniform(self.interval_seconds, self.interval_seconds + 0.5)
                    self.signals.status_update.emit(f"Sonraki mesaja {wait_time:.1f} saniye...")
                    time.sleep(wait_time)
                    
                except Exception as e:
                    self.signals.status_update.emit(f"Hata: {str(e)}")
                    time.sleep(1)
            else:
                time.sleep(0.1)  # Duraklatıldığında CPU kullanımını azaltmak için
    
    def stop(self):
        self.running = False
        self.signals.status_update.emit("Durduruldu.")
    
    def pause(self):
        self.paused = True
        self.signals.status_update.emit("Duraklatıldı.")
    
    def resume(self):
        self.paused = False
        self.signals.status_update.emit("Devam ediyor...")
    
    def set_message(self, message):
        self.message = message
    
    def set_interval(self, interval_seconds):
        self.interval_seconds = interval_seconds

class MacroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.macro = Macro()
        self.init_ui()
        
    def init_ui(self):
        # Ana pencere ayarları
        self.setWindowTitle("Acilci")
        self.setGeometry(100, 100, 400, 300)  # Yeni input alanı için daha yüksek pencere
        
        # Widget'lar
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Acilci")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px; color: #FF5733;")
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Otomatik Mesaj Uygulaması")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(subtitle_label)
        
        info_label = QLabel("Bu uygulama ENTER tuşuna basıp aşağıdaki mesajı yazıp\n"
                           "tekrar ENTER'e basar ve her mesajdan sonra boş satır bırakır.\n"
                           "Mesaj gönderme aralığını kendiniz ayarlayabilirsiniz.")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # Mesaj giriş alanı
        message_layout = QHBoxLayout()
        message_label = QLabel("Mesaj:")
        self.message_input = QLineEdit("ACİL İTEMLERİNİZ ALINIR")
        self.message_input.setToolTip("Göndermek istediğiniz mesajı buraya yazın")
        message_layout.addWidget(message_label)
        message_layout.addWidget(self.message_input)
        layout.addLayout(message_layout)
        
        # Saniye aralığı giriş alanı
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Mesaj Aralığı (saniye):")
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(60)
        self.interval_spinbox.setValue(1)
        self.interval_spinbox.setToolTip("Mesajlar arasındaki bekleme süresi (1-60 saniye)")
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_spinbox)
        layout.addLayout(interval_layout)
        
        # Butonlar için ayrı bir layout oluştur
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Başlat")
        self.start_button.clicked.connect(self.start_macro)
        button_layout.addWidget(self.start_button)
        
        self.pause_button = QPushButton("Duraklat")
        self.pause_button.clicked.connect(self.pause_macro)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)
        
        self.stop_button = QPushButton("Durdur")
        self.stop_button.clicked.connect(self.stop_macro)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        # Acil durum durdurma tuşu açıklaması
        esc_info = QLabel("Acil durumlarda uygulamayı durdurmak için 'ESC' tuşuna basın.")
        esc_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(esc_info)
        
        # Durum bildirimi
        self.status_label = QLabel("Hazır")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: blue;")
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
        
        # ESC tuşu ile acil durdurma
        keyboard.add_hotkey('esc', self.emergency_stop)
        
        # Sinyal bağlantıları
        self.macro.signals.status_update.connect(self.update_status)
    
    def start_macro(self):
        message = self.message_input.text()
        if not message:
            self.update_status("Hata: Mesaj boş olamaz!")
            return
            
        # Mesajı ve saniye aralığını güncelle
        self.macro.set_message(message)
        self.macro.set_interval(self.interval_spinbox.value())
        
        if not self.macro.running:
            self.macro.start()
        elif self.macro.paused:
            self.macro.resume()
        
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.message_input.setEnabled(False)  # Çalışırken mesaj değiştirilemesin
        self.interval_spinbox.setEnabled(False)  # Çalışırken aralık değiştirilemesin
    
    def pause_macro(self):
        if self.macro.running and not self.macro.paused:
            self.macro.pause()
            self.pause_button.setText("Devam Et")
            self.message_input.setEnabled(True)  # Duraklattığında mesaj değiştirilebilsin
            self.interval_spinbox.setEnabled(True)  # Duraklattığında aralık değiştirilebilsin
        else:
            self.macro.resume()
            self.pause_button.setText("Duraklat")
            self.message_input.setEnabled(False)  # Devam ettiğinde mesaj değiştirilemesin
            self.interval_spinbox.setEnabled(False)  # Devam ettiğinde aralık değiştirilemesin
    
    def stop_macro(self):
        if self.macro.running:
            self.macro.stop()
            # Yeni bir nesne oluştur
            self.macro = Macro(self.message_input.text(), self.interval_spinbox.value())
            self.macro.signals.status_update.connect(self.update_status)
            
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.pause_button.setText("Duraklat")
            self.stop_button.setEnabled(False)
            self.message_input.setEnabled(True)  # Durdurduğunda mesaj değiştirilebilsin
            self.interval_spinbox.setEnabled(True)  # Durdurduğunda aralık değiştirilebilsin
    
    def emergency_stop(self):
        self.stop_macro()
        self.update_status("Acil durdurma: ESC tuşuna basıldı!")
    
    def update_status(self, message):
        self.status_label.setText(message)
    
    def closeEvent(self, event):
        # Uygulama kapatıldığında durdur
        if self.macro.running:
            self.macro.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MacroApp()
    window.show()
    sys.exit(app.exec_()) 