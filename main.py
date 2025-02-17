from instagram_comment_bot import InstagramCommentBot
import json
from datetime import datetime
import os
import asyncio
from instagrapi import Client
import logging

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_interaction_history():
    """Etkileşim geçmişini yükle"""
    history = set()
    if os.path.exists('successful_interactions.txt'):
        with open('successful_interactions.txt', 'r', encoding='utf-8') as f:
            for line in f:
                username = line.split(',')[0].strip()
                history.add(username)
    return history

def log_interaction(username, status, content_type, message=None):
    """Etkileşimleri logla"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "success":
        log_file = "successful_interactions.txt"
        log_message = f"{username}, {timestamp}, {content_type}, Başarılı DM ve yorum gönderildi"
    else:
        log_file = "failed_interactions.txt"
        log_message = f"{username}, {timestamp}, {content_type}, HATA: {message}"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def check_previous_interaction(username):
    """Kullanıcıyla daha önce etkileşime geçilip geçilmediğini kontrol et"""
    interaction_history = load_interaction_history()
    return username in interaction_history

class InstagramBot(InstagramCommentBot):
    def __init__(self):
        super().__init__()
        self.cl = Client()
        self.comment_media_ids = {}
        self.user_ids = {}
        self.last_check_time = datetime.now()
        self.session_file = "session.json"
        
        # Proxy ayarlarını yükle
        config = load_config()
        if config['proxy']['enabled']:
            self.cl.set_proxy(config['proxy']['https'])
            logger.info("Proxy aktif edildi")
        
    async def login(self, username, password):
        """Instagram'a giriş yap"""
        try:
            # Güvenlik ayarlarını yapılandır
            self.cl.set_locale('tr_TR')
            self.cl.set_timezone_offset(3 * 60 * 60)
            self.cl.set_device({
                "app_version": "269.0.0.18.75",
                "android_version": 26,
                "android_release": "8.0.0",
                "dpi": "480dpi",
                "resolution": "1080x1920",
                "manufacturer": "OnePlus",
                "device": "ONEPLUS A3003",
                "model": "OnePlus3",
                "cpu": "qcom",
                "version_code": "314665256"
            })

            # Oturum dosyasını kontrol et
            if os.path.exists(self.session_file):
                try:
                    self.cl.load_settings(self.session_file)
                    logger.info("Önceki oturum yüklendi")
                    self.cl.get_timeline_feed()
                    return True
                except Exception as e:
                    logger.warning("Önceki oturum geçersiz, yeni giriş yapılacak")
                    os.remove(self.session_file)

            # Yeni giriş yap
            logger.info("Instagram'a giriş yapılıyor...")
            login_result = self.cl.login(username, password)
            
            if login_result:
                self.cl.dump_settings(self.session_file)
                logger.info(f"{username} hesabına başarıyla giriş yapıldı")
                return True
            
            logger.error("Giriş başarısız")
            return False
            
        except Exception as e:
            logger.error(f"Giriş yapılırken hata oluştu: {str(e)}")
            return False

    async def check_login(self, config):
        """Oturum durumunu kontrol et ve gerekirse yeniden giriş yap"""
        try:
            self.cl.get_timeline_feed()
            return True
        except Exception as e:
            logger.warning("Oturum geçersiz, yeniden giriş yapılıyor...")
            return await self.login(config['username'], config['password'])

    async def get_reels_comments(self, reels_url):
        """Reels yorumlarını al"""
        try:
            shortcode = reels_url.split("/reel/")[1].split("/")[0]
            
            try:
                media_pk = self.cl.media_pk_from_code(shortcode)
                logger.info(f"Media ID: {media_pk}")
                
                # Yorumları al ve tarihe göre filtrele
                all_comments = self.cl.media_comments(media_pk)
                
                # Sadece son kontrolden sonra yapılan yorumları al
                new_comments = []
                for comment in all_comments:
                    # Unix timestamp'i datetime'a çevir
                    try:
                        comment_time = datetime.fromtimestamp(int(comment.created_at))
                        if comment_time > self.last_check_time:
                            new_comments.append(comment)
                            # Comment ID ve user ID'leri sakla
                            self.comment_media_ids[comment.pk] = media_pk
                            if comment.user.username not in self.user_ids:
                                try:
                                    user_info = self.cl.user_info_by_username(comment.user.username)
                                    self.user_ids[comment.user.username] = user_info.pk
                                    logger.info(f"Yeni kullanıcı ID alındı: {comment.user.username}")
                                except Exception as e:
                                    logger.error(f"Kullanıcı ID'si alınamadı: {str(e)}")
                    except Exception as e:
                        logger.error(f"Yorum tarihi işlenirken hata: {str(e)}")
                        continue
                
                if new_comments:
                    logger.info(f"Toplam {len(new_comments)} yeni yorum bulundu")
                else:
                    logger.info("Yeni yorum bulunamadı")
                
                return new_comments
                
            except Exception as e:
                logger.error(f"Media bilgileri alınırken hata: {str(e)}")
                return []
            
        except Exception as e:
            logger.error(f"Reels yorumları alınırken hata oluştu: {str(e)}")
            return []

    async def process_comment(self, comment, content_type):
        """Yorumları işle"""
        try:
            username = comment.user.username
            user_id = self.user_ids.get(username)
            
            if not user_id:
                logger.error(f"'{username}' kullanıcısının ID'si bulunamadı.")
                return
            
            if check_previous_interaction(username):
                logger.info(f"{username} kullanıcısıyla daha önce etkileşime geçilmiş, atlıyorum.")
                return
            
            try:
                config = load_config()
                
                logger.info(f"'{username}' kullanıcısına DM gönderiliyor...")
                # DM gönder
                try:
                    self.cl.direct_send(
                        text=config['dm_message'],
                        user_ids=[user_id]
                    )
                    logger.info("DM başarıyla gönderildi!")
                except Exception as dm_error:
                    logger.error(f"DM gönderilirken hata: {str(dm_error)}")
                
                logger.info(f"'{username}' kullanıcısının yorumuna yanıt veriliyor...")
                # Yoruma yanıt ver
                try:
                    media_id = self.comment_media_ids.get(comment.pk)
                    if media_id:
                        # Yoruma yanıt olarak gönder
                        self.cl.media_comment_replies(
                            media_id=media_id,
                            comment_id=comment.pk,  # Yanıt verilecek yorumun ID'si
                            text=f"@{username} {config['comment_reply']}"
                        )
                        logger.info("Yorum yanıtı başarıyla gönderildi!")
                except Exception as comment_error:
                    logger.error(f"Yorum yanıtı gönderilirken hata: {str(comment_error)}")
                    # Yanıt gönderilemezse normal yorum olarak dene
                    try:
                        self.cl.media_comment(
                            media_id=media_id,
                            text=f"@{username} {config['comment_reply']}"
                        )
                        logger.info("Normal yorum olarak gönderildi!")
                    except Exception as e:
                        logger.error(f"Normal yorum da gönderilemedi: {str(e)}")
                
                # Başarılı etkileşimi logla
                log_interaction(username, "success", content_type)
                logger.info(f"'{username}' kullanıcısıyla etkileşim başarılı!")
                
            except Exception as e:
                logger.error(f"Etkileşim sırasında hata: {str(e)}")
                log_interaction(username, "failed", content_type, str(e))
                
        except Exception as e:
            logger.error(f"Hata oluştu: {str(e)}")

    async def run(self):
        """Bot çalıştırma metodu"""
        config = load_config()
        
        # İlk giriş
        login_success = await self.login(config['username'], config['password'])
        if not login_success:
            return

        logger.info("Bot başlatıldı, yorumlar kontrol ediliyor...")
        
        while True:
            try:
                # Her döngüde oturumu kontrol et
                if not await self.check_login(config):
                    logger.warning("Oturum yenilenemedi, bot duraklatılıyor...")
                    await asyncio.sleep(300)  # 5 dakika bekle
                    continue

                check_start_time = datetime.now()
                
                if config['targets']['post']['enabled']:
                    post_comments = await self.get_post_comments(config['targets']['post']['url'])
                    for comment in post_comments:
                        if config['trigger_word'].lower() in comment.text.lower():
                            await self.process_comment(comment, "post")
                
                if config['targets']['reels']['enabled']:
                    reels_comments = await self.get_reels_comments(config['targets']['reels']['url'])
                    for comment in reels_comments:
                        if config['trigger_word'].lower() in comment.text.lower():
                            await self.process_comment(comment, "reels")
                
                self.last_check_time = check_start_time
                logger.info(f"Kontrol tamamlandı. Sonraki kontrol için 30 saniye bekleniyor... ({datetime.now().strftime('%H:%M:%S')})")
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Hata oluştu: {str(e)}")
                await asyncio.sleep(30)

def load_config():
    """Yapılandırma dosyasını yükle"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Config dosyası yüklenirken hata: {str(e)}")
        return None

async def main():
    """Ana fonksiyon"""
    try:
        bot = InstagramBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Bot çalışırken hata oluştu: {str(e)}")

if __name__ == "__main__":
    logger.info("Bot başlatılıyor...")
    asyncio.run(main()) 