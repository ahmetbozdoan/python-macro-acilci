import os
import subprocess
import sys

def main():
    print("Acilci kurulumu başlatılıyor...")
    
    # PyInstaller kuruluyor
    print("PyInstaller kuruluyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Gerekli kütüphaneler kuruluyor
    print("Gerekli kütüphaneler kuruluyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # EXE dosyası oluşturuluyor
    print("EXE dosyası oluşturuluyor...")
    subprocess.check_call([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Acilci",
        "--icon", "NONE",
        "selling_macro.py"
    ])
    
    print("\nKurulum tamamlandı!")
    print("Oluşturulan EXE dosyası: dist/Acilci.exe")

if __name__ == "__main__":
    main() 