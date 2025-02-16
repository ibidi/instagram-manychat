# Instagram Comment Bot 🤖

> Instagram gönderilerinizde belirli anahtar kelimeleri içeren yorumları otomatik olarak yanıtlayan ve kullanıcılara özel mesaj gönderen bir Python botu.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Özellikler ✨

* Belirli kelime/kelime gruplarını içeren yorumları otomatik tespit
* Yorumlara kullanıcıyı etiketleyerek otomatik yanıt
* Yorum yapan kullanıcılara otomatik DM gönderme
* Daha önce yanıt verilen kullanıcıları takip etme
* Instagram spam politikalarına uyumlu güvenlik önlemleri
* Türkçe karakter desteği

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

3. `config.json` dosyasını oluşturun:

```json
{
    "username": "instagram_username",
    "password": "instagram_password",
    "post_id": "https://instagram.com/p/ORNEK12345",
    "reply_message": "Yorumunuz için teşekkürler! Daha detaylı bilgi için DM'den ulaşabilirsiniz 🙏",
    "comment_reply": "Kodu DM üzerinden ilettim 💛",
    "trigger_word": "yapay zeka"
}
```

4. Botu çalıştırın:

```bash
python main.py
```

## Kullanım 📝

```bash
python main.py
```

2. Bot otomatik olarak:
   * Gönderideki yorumları kontrol eder
   * Tetikleyici kelimeyi içeren yorumları bulur
   * Yorumu yapan kullanıcıyı etiketleyerek yanıt verir
   * Kullanıcıya DM gönderir

## Örnek Yapılandırma 📝

```json
{
    "username": "hesabiniz",
    "post_id": "https://instagram.com/p/POSTID",
    "reply_message": "Detaylı bilgileri gönderdim 🙏",
    "comment_reply": "Bilgileri DM'den ilettim 💛",
    "trigger_word": "yapay zeka"
}
```

## Güvenlik Önerileri ⚠️

* Instagram şifrenizi environment variable olarak saklayın
* İki faktörlü doğrulamayı aktif tutun
* Test hesabıyla deneme yapın
* Instagram kullanım koşullarına uyun
* Spam limitlerini aşmamaya dikkat edin

## Özelleştirme 🛠️

* `trigger_word`: İstediğiniz kelime veya kelime grubunu ayarlayabilirsiniz
* `reply_message`: DM mesajını özelleştirebilirsiniz
* `comment_reply`: Yorum yanıtını özelleştirebilirsiniz
* Kontrol sıklığını `time.sleep()` değerini değiştirerek ayarlayabilirsiniz

## Katkıda Bulunma 🤝

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## Önemli Notlar 📌

* Instagram'ın API politikaları değişebilir
* Aşırı kullanım hesabınızın kısıtlanmasına neden olabilir
* Her zaman güncel Instagram politikalarını takip edin
* Spam yapmaktan kaçının

## Lisans 📄

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim 📞

Sorularınız veya önerileriniz için Issues bölümünü kullanabilirsiniz.

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
