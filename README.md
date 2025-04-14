# Acilci

Bu uygulama, otomatik mesaj göndermek için tasarlanmış bir yardımcı programdır.

## Özellikler

- ENTER tuşuna basıp istediğiniz mesajı yazarak tekrar ENTER tuşuna basar
- Her mesajdan sonra boş satır bırakır
- Özelleştirilebilir mesaj alanı (varsayılan olarak "ACİL İTEMLERİNİZ ALINIR")
- İşlem yaklaşık her 1-1.5 saniyede bir tekrarlanır (doğal görünüm için)
- Basit ve kullanıcı dostu arayüze sahiptir
- ESC tuşu ile acil durumda durdurulabilir

## Kurulum

1. Python yüklü değilse [python.org](https://www.python.org/downloads/) adresinden Python 3.7 veya üstünü indirip kurun.
2. Bu projeyi bilgisayarınıza indirin.
3. Komut satırında proje dizinine gidin.
4. Aşağıdaki komutu çalıştırarak EXE dosyasını oluşturun:

```
python setup.py
```

5. Oluşturulan `dist/Acilci.exe` dosyasını kullanabilirsiniz.

## Kullanım

1. `Acilci.exe` dosyasını çift tıklayarak uygulamayı başlatın.
2. İsterseniz mesaj kutusuna göndermek istediğiniz özel mesajı yazın.
3. Mesaj göndermek istediğiniz uygulamayı açın.
4. Uygulamadaki "Başlat" düğmesine tıklayın.
5. İşlemi durdurmak için "Durdur" düğmesine tıklayın veya ESC tuşuna basın.
6. İşlemi duraklatıp mesajı değiştirebilir, sonra tekrar devam ettirebilirsiniz.

## Dikkat

- Bu program eğitim amaçlı yapılmıştır.
- Kullanımdan doğabilecek sorunlar kullanıcının sorumluluğundadır.

## Geliştirme

Geliştirme ortamını ayarlamak için:

```
pip install -r requirements.txt
```

komutunu çalıştırın. 