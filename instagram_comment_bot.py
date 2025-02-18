from instagrapi import Client
import time
import json
import codecs
import re
import os

class InstagramCommentBot:
    def __init__(self):
        self.config = self._load_config()
        self.api = Client()
        
    def _extract_media_id(self, url):
        try:
            # URL'den post kodunu çıkar
            if 'instagram.com/p/' in url:
                code = url.split('/p/')[-1].split('/')[0]
                # Önce medyayı kodu kullanarak al
                media_info = self.api.media_pk_from_code(code)
                print(f"Media ID bulundu: {media_info}")
                return media_info
            else:
                print("Geçersiz Instagram URL'si")
                return None
        except Exception as e:
            print(f"Post ID çıkarma hatası: {e}")
            return None

    def _load_config(self):
        try:
            with codecs.open('config.json', 'r', 'utf-8') as f:
                config = json.load(f)
                # Şifreyi environment variable'dan al
                config["password"] = os.getenv('INSTAGRAM_PASSWORD', config["password"])
                return config
        except FileNotFoundError:
            return {
                "username": "",
                "password": "",
                "post_id": "",
                "reply_message": "Yorumunuz için teşekkürler! 🙏",
                "comment_reply": "Kodu DM üzerinden ilettim 💛",
                "trigger_word": ""
            }
    
    def login(self):
        try:
            # İki faktörlü doğrulama ve diğer güvenlik önlemleri için
            self.api.set_locale('tr_TR')
            self.api.set_country('TR')
            self.api.set_country_code(90)  # Türkiye
            self.api.set_device({
                'app_version': '203.0.0.29.118',
                'android_version': 26,
                'android_release': '8.0.0',
                'dpi': '480dpi',
                'resolution': '1080x1920',
                'manufacturer': 'Samsung',
                'device': 'SM-G950F',
                'model': 'G950F',
                'cpu': 'universal8895',
                'version_code': '314665256'
            })
            
            self.api.login(
                self.config["username"],
                self.config["password"]
            )
            print("Giriş başarılı!")
            
            # Session'ı kaydet
            self.api.dump_settings('session.json')
            
        except Exception as e:
            print(f"Giriş hatası: {e}")
            raise e
    
    def check_and_reply_comments(self):
        try:
            media_id = self._extract_media_id(self.config["post_id"])
            if not media_id:
                raise Exception("Geçersiz post ID")

            comments = self.api.media_comments(media_id)
            print(f"Toplam {len(comments)} yorum bulundu.")
            
            for comment in comments:
                user_id = comment.user.pk
                username = comment.user.username
                comment_id = comment.pk
                comment_text = comment.text.lower().strip()  # Yorumu küçük harfe çevirip boşlukları düzenliyoruz
                trigger = self.config["trigger_word"].lower().strip()  # Tetikleyici kelimeyi de düzenliyoruz
                
                print(f"Yorum kontrol ediliyor: '{comment_text}' - Aranan: '{trigger}'")
                
                # Belirlenen kelime yorumda var mı kontrol et
                if trigger in comment_text:
                    print(f"Tetikleyici kelime bulundu: {comment_text}")
                    if not self._has_replied_before(user_id):
                        print(f"İşlem yapılıyor: {username}")
                        try:
                            # Yoruma cevap ver - kullanıcıyı etiketleyerek
                            self.api.media_comment(
                                media_id=media_id,
                                text=f"@{username} {self.config['comment_reply']}", 
                                replied_to_comment_id=comment_id
                            )
                            print(f"Yorum yapıldı: {username}")

                            # DM gönder
                            self.api.direct_send(
                                text=self.config["reply_message"],
                                user_ids=[user_id]
                            )
                            self._save_replied_user(user_id)
                            print(f"DM gönderildi: {username}")
                            
                            time.sleep(5)
                        except Exception as e:
                            print(f"İşlem hatası ({username}): {e}")
                    else:
                        print(f"Bu kullanıcıya daha önce yanıt verilmiş: {username}")
                else:
                    print(f"Tetikleyici kelime bulunamadı: {comment_text}")
                
        except Exception as e:
            print(f"Hata oluştu: {e}")
    
    def _has_replied_before(self, user_id):
        try:
            with open('replied_users.txt', 'r') as f:
                replied_users = f.read().splitlines()
                return str(user_id) in replied_users
        except FileNotFoundError:
            return False
    
    def _save_replied_user(self, user_id):
        with open('replied_users.txt', 'a') as f:
            f.write(f"{user_id}\n")

    def run(self):
        self.login()
        print("Bot çalışıyor...")
        while True:
            try:
                self.check_and_reply_comments()
                print("Yorumlar kontrol edildi, 30 saniye bekleniyor...")
                time.sleep(60)  # Daha sık kontrol için 1 dakikaya düşürdük
            except Exception as e:
                print(f"Hata oluştu, yeniden başlatılıyor: {e}")
                time.sleep(60)
                self.login() 