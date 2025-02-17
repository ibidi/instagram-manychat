# Instagram Manychat Bot 🤖

> Instagram reels ve gönderilerinizde belirli anahtar kelimeleri içeren yorumları otomatik olarak yanıtlayan ve kullanıcılara özel mesaj gönderen bir Python botu.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Özellikler ✨

* Reels ve post yorumlarını otomatik takip
* Belirli kelime/kelime gruplarını içeren yorumları tespit
* Yorumlara kullanıcıyı etiketleyerek otomatik yanıt
* Yorum yapan kullanıcılara otomatik DM gönderme
* Daha önce yanıt verilen kullanıcıları takip etme
* Oturum yönetimi ve otomatik yeniden bağlanma
* Detaylı log sistemi
* Proxy desteği
* Instagram spam politikalarına uyumlu güvenlik önlemleri

## Gereksinimler 📋

* Python 3.6+
* instagrapi

## Kurulum 🔧

1. Gerekli Python paketini yükleyin:

```bash
pip install instagrapi
```

2. Projeyi klonlayın:

```bash
git clone https://github.com/ibidi/instagram-manychat.git
```

3. `config.json` dosyasını düzenleyin:

```json
{
    "username": "instagram_username",
    "password": "instagram_password",
    "targets": {
        "post": {
            "url": "https://instagram.com/p/ORNEK12345",
            "enabled": false
        },
        "reels": {
            "url": "https://www.instagram.com/reel/ORNEK67890",
            "enabled": true
        }
    },
    "reply_message": "Yorumunuz için teşekkürler!",
    "comment_reply": "DM üzerinden ilettim 💛",
    "trigger_word": "yapay zeka",
    "dm_message": "Mesajınız için teşekkürler...",
    "log_files": {
        "success_log": "successful_interactions.txt",
        "failed_log": "failed_interactions.txt"
    }
}
```

4. Botu çalıştırın:

```bash
python main.py
```

## Özellikler ve Kullanım 📝

* **Reels ve Post Desteği**: Hem reels hem de normal gönderiler için çalışır
* **Akıllı Oturum Yönetimi**: Oturum sorunlarını otomatik çözer
* **Yeni Yorum Takibi**: Sadece yeni yorumları kontrol eder
* **Güvenli Etkileşim**: Spam limitlerini aşmaz
* **Log Sistemi**: Başarılı ve başarısız etkileşimleri kaydeder

## Güvenlik Önerileri ⚠️

* Instagram şifrenizi environment variable olarak saklayın
* İki faktörlü doğrulamayı aktif tutun
* Test hesabıyla deneme yapın
* Instagram kullanım koşullarına uyun
* Spam limitlerini aşmamaya dikkat edin

## Özelleştirme 🛠️

* `trigger_word`: Tetikleyici kelimeyi ayarlayın
* `reply_message`: DM mesajını özelleştirin
* `comment_reply`: Yorum yanıtını özelleştirin
* Kontrol sıklığını ayarlayın
* Proxy kullanımını aktifleştirin

## Katkıda Bulunma 🤝

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## Lisans 📄

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim 📞

* GitHub Issues üzerinden bildirim oluşturabilirsiniz
* Pull Request gönderebilirsiniz
* Önerilerinizi Issues bölümünde paylaşabilirsiniz

## Teşekkürler 🙏

* [instagrapi](https://github.com/adw0rd/instagrapi) kütüphanesine
* Tüm katkıda bulunanlara

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

MIT License

Copyright (c) 2025 ibidi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.