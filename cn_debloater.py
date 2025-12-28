#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     CN-BASED ROM DEBLOATER v1.0                               ║
║                   Çin ROM'ları için Bloatware Temizleyici                     ║
║                                                                               ║
║  Desteklenen ROM'lar: MIUI, HyperOS, ColorOS, OriginOS, FlymeOS, EMUI        ║
║  Geliştirici: Tinlera (github.com/Tinlera)                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# RENK KODLARI
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def color_print(text: str, color: str = Colors.WHITE):
    print(f"{color}{text}{Colors.RESET}")

def success(text: str):
    color_print(f"✅ {text}", Colors.GREEN)

def warning(text: str):
    color_print(f"⚠️  {text}", Colors.YELLOW)

def error(text: str):
    color_print(f"❌ {text}", Colors.RED)

def info(text: str):
    color_print(f"ℹ️  {text}", Colors.CYAN)

# ═══════════════════════════════════════════════════════════════════════════════
# BLOATWARE VERİTABANI
# ═══════════════════════════════════════════════════════════════════════════════

class RiskLevel(Enum):
    SAFE = "safe"           # Güvenle kaldırılabilir
    MODERATE = "moderate"   # Dikkatli kaldırılmalı
    RISKY = "risky"         # Riskli - bazı özellikler bozulabilir

@dataclass
class Bloatware:
    package: str
    name: str
    category: str
    risk: RiskLevel
    description: str

# Xiaomi/MIUI/HyperOS Bloatware Listesi
XIAOMI_BLOATWARE = [
    # === SAFE - GÜVENLİ KALDIRILACAKLAR ===
    # Çin Uygulamaları
    Bloatware("com.miui.analytics", "Xiaomi Analytics", "Telemetri", RiskLevel.SAFE, "Kullanım verisi toplama"),
    Bloatware("com.xiaomi.mipicks", "Mi Picks / GetApps", "Bloatware", RiskLevel.SAFE, "Uygulama önerileri"),
    Bloatware("com.miui.msa.global", "MSA (MIUI System Ads)", "Reklam", RiskLevel.SAFE, "Sistem reklamları"),
    Bloatware("com.miui.hybrid", "Quick Apps", "Bloatware", RiskLevel.SAFE, "Hızlı uygulamalar"),
    Bloatware("com.miui.hybrid.accessory", "Quick Apps Accessory", "Bloatware", RiskLevel.SAFE, "Hızlı uygulama eklentisi"),
    Bloatware("com.miui.bugreport", "Bug Report", "Telemetri", RiskLevel.SAFE, "Hata raporlama"),
    Bloatware("com.miui.yellowpage", "Yellow Pages", "Bloatware", RiskLevel.SAFE, "Sarı sayfalar (Çin)"),
    Bloatware("com.xiaomi.payment", "Mi Pay", "Ödeme", RiskLevel.SAFE, "Xiaomi ödeme (Çin)"),
    Bloatware("com.mipay.wallet.id", "Mi Wallet ID", "Ödeme", RiskLevel.SAFE, "Mi cüzdan"),
    Bloatware("com.mipay.wallet.in", "Mi Wallet IN", "Ödeme", RiskLevel.SAFE, "Mi cüzdan Hindistan"),
    Bloatware("com.xiaomi.midrop", "Mi Drop / ShareMe", "Paylaşım", RiskLevel.SAFE, "Dosya paylaşım (alternatifler var)"),
    Bloatware("com.miui.player", "Mi Music", "Medya", RiskLevel.SAFE, "Xiaomi müzik çalar"),
    Bloatware("com.miui.video", "Mi Video", "Medya", RiskLevel.SAFE, "Xiaomi video çalar"),
    Bloatware("com.miui.videoplayer", "MIUI Video Player", "Medya", RiskLevel.SAFE, "Video oynatıcı"),
    Bloatware("com.miui.fm", "FM Radio", "Medya", RiskLevel.SAFE, "FM radyo"),
    Bloatware("com.miui.virtualsim", "Virtual SIM", "Telekom", RiskLevel.SAFE, "Sanal SIM (Çin)"),
    Bloatware("com.miui.antispam", "Antispam", "Güvenlik", RiskLevel.SAFE, "Spam engelleme (sorunlu)"),
    Bloatware("com.xiaomi.glgm", "Games", "Oyun", RiskLevel.SAFE, "Xiaomi oyun servisi"),
    Bloatware("com.xiaomi.gamecenter.sdk.service", "Game Center SDK", "Oyun", RiskLevel.SAFE, "Oyun merkezi"),
    Bloatware("com.sohu.inputmethod.sogou.xiaomi", "Sogou Keyboard", "Klavye", RiskLevel.SAFE, "Çin klavyesi"),
    Bloatware("com.baidu.input_mi", "Baidu Keyboard", "Klavye", RiskLevel.SAFE, "Baidu klavye"),
    Bloatware("com.iflytek.inputmethod.miui", "iFlytek Keyboard", "Klavye", RiskLevel.SAFE, "iFlytek klavye"),
    Bloatware("com.miui.userguide", "User Guide", "Bloatware", RiskLevel.SAFE, "Kullanım kılavuzu"),
    Bloatware("com.miui.miservice", "Mi Service", "Servis", RiskLevel.SAFE, "Xiaomi servis"),
    Bloatware("com.miui.cloudservice", "Mi Cloud (Çin)", "Bulut", RiskLevel.SAFE, "Çin Mi Cloud"),
    Bloatware("com.miui.cloudbackup", "Mi Cloud Backup", "Bulut", RiskLevel.SAFE, "Bulut yedekleme"),
    Bloatware("com.xiaomi.scanner", "Mi Scanner", "Araç", RiskLevel.SAFE, "Tarayıcı"),
    Bloatware("com.miui.compass", "Compass", "Araç", RiskLevel.SAFE, "Pusula"),
    Bloatware("com.miui.notes", "Notes", "Araç", RiskLevel.SAFE, "Notlar (Keep kullanılabilir)"),
    Bloatware("com.miui.calculator", "Calculator", "Araç", RiskLevel.SAFE, "Hesap makinesi"),
    Bloatware("com.miui.weather2", "Weather", "Araç", RiskLevel.SAFE, "Hava durumu"),
    Bloatware("com.miui.cleanmaster", "Cleaner", "Sistem", RiskLevel.SAFE, "Temizleyici"),
    Bloatware("com.miui.screenrecorder", "Screen Recorder", "Araç", RiskLevel.SAFE, "Ekran kaydedici"),
    
    # Çin Servisleri
    Bloatware("cn.wps.moffice_eng.xiaomi.lite", "WPS Office", "Ofis", RiskLevel.SAFE, "WPS ofis uygulaması"),
    Bloatware("com.duokan.reader", "Mi Reader", "Okuyucu", RiskLevel.SAFE, "E-kitap okuyucu"),
    Bloatware("com.mfashiongallery.emag", "Mi Wallpaper Carousel", "Bloatware", RiskLevel.SAFE, "Duvar kağıdı carousel"),
    Bloatware("com.mi.globalbrowser", "Mi Browser", "Tarayıcı", RiskLevel.SAFE, "Mi tarayıcı"),
    Bloatware("com.android.browser", "AOSP Browser", "Tarayıcı", RiskLevel.SAFE, "Varsayılan tarayıcı"),
    Bloatware("com.facebook.katana", "Facebook", "Sosyal", RiskLevel.SAFE, "Facebook uygulaması"),
    Bloatware("com.facebook.system", "Facebook System", "Sosyal", RiskLevel.SAFE, "Facebook sistem servisi"),
    Bloatware("com.facebook.appmanager", "Facebook App Manager", "Sosyal", RiskLevel.SAFE, "Facebook uygulama yöneticisi"),
    Bloatware("com.facebook.services", "Facebook Services", "Sosyal", RiskLevel.SAFE, "Facebook servisleri"),
    Bloatware("com.zhiliaoapp.musically", "TikTok", "Sosyal", RiskLevel.SAFE, "TikTok uygulaması"),
    Bloatware("com.ss.android.ugc.aweme", "Douyin (TikTok CN)", "Sosyal", RiskLevel.SAFE, "Çin TikTok"),
    Bloatware("com.netflix.mediaclient", "Netflix", "Medya", RiskLevel.SAFE, "Netflix (istemiyorsan)"),
    Bloatware("com.netflix.partner.activation", "Netflix Activation", "Medya", RiskLevel.SAFE, "Netflix aktivasyon"),
    Bloatware("com.alibaba.aliexpresshd", "AliExpress", "Alışveriş", RiskLevel.SAFE, "AliExpress"),
    Bloatware("com.amazon.appmanager", "Amazon App Manager", "Alışveriş", RiskLevel.SAFE, "Amazon yönetici"),
    Bloatware("com.amazon.mShop.android.shopping", "Amazon Shopping", "Alışveriş", RiskLevel.SAFE, "Amazon alışveriş"),
    Bloatware("com.ebay.mobile", "eBay", "Alışveriş", RiskLevel.SAFE, "eBay"),
    Bloatware("ru.yandex.searchplugin", "Yandex", "Arama", RiskLevel.SAFE, "Yandex"),
    Bloatware("com.opera.browser", "Opera Browser", "Tarayıcı", RiskLevel.SAFE, "Opera tarayıcı"),
    Bloatware("com.opera.mini.native", "Opera Mini", "Tarayıcı", RiskLevel.SAFE, "Opera Mini"),
    
    # Oyunlar
    Bloatware("com.gameloft.android.GloftA9HM", "Asphalt 9", "Oyun", RiskLevel.SAFE, "Asphalt oyunu"),
    Bloatware("com.kiloo.subwaysurf", "Subway Surfers", "Oyun", RiskLevel.SAFE, "Subway Surfers"),
    Bloatware("com.king.candycrushsaga", "Candy Crush", "Oyun", RiskLevel.SAFE, "Candy Crush"),
    
    # === MODERATE - DİKKATLİ KALDIRILABİLİR ===
    Bloatware("com.miui.gallery", "Mi Gallery", "Medya", RiskLevel.MODERATE, "Galeri (Google Photos kullanılabilir)"),
    Bloatware("com.miui.backup", "Mi Backup", "Yedekleme", RiskLevel.MODERATE, "Yedekleme (alternatif gerekebilir)"),
    Bloatware("com.xiaomi.discover", "Mi Discover", "Bloatware", RiskLevel.MODERATE, "Keşfet"),
    Bloatware("com.miui.voiceassist", "Mi AI", "Asistan", RiskLevel.MODERATE, "Sesli asistan"),
    Bloatware("com.miui.personalassistant", "Personal Assistant", "Asistan", RiskLevel.MODERATE, "Kişisel asistan"),
    Bloatware("com.xiaomi.xmsf", "Xiaomi Service Framework", "Servis", RiskLevel.MODERATE, "Xiaomi servis çerçevesi"),
    Bloatware("com.miui.daemon", "MIUI Daemon", "Sistem", RiskLevel.MODERATE, "MIUI arka plan servisi"),
    
    # === RISKY - SİSTEM BOZULMA RİSKİ ===
    Bloatware("com.miui.securitycenter", "Security Center", "Güvenlik", RiskLevel.RISKY, "Güvenlik merkezi - dikkatli ol!"),
    Bloatware("com.miui.powerkeeper", "Battery Saver", "Sistem", RiskLevel.RISKY, "Pil optimizasyonu - sorun çıkarabilir"),
]

# OPPO/Realme/OnePlus (ColorOS) Bloatware
OPPO_BLOATWARE = [
    Bloatware("com.coloros.gamespace", "Game Space", "Oyun", RiskLevel.SAFE, "Oyun modu"),
    Bloatware("com.heytap.browser", "HeyTap Browser", "Tarayıcı", RiskLevel.SAFE, "HeyTap tarayıcı"),
    Bloatware("com.heytap.market", "HeyTap Market", "Mağaza", RiskLevel.SAFE, "Uygulama mağazası"),
    Bloatware("com.heytap.music", "HeyTap Music", "Medya", RiskLevel.SAFE, "Müzik uygulaması"),
    Bloatware("com.heytap.cloud", "HeyTap Cloud", "Bulut", RiskLevel.SAFE, "Bulut depolama"),
    Bloatware("com.coloros.weather2", "Weather", "Araç", RiskLevel.SAFE, "Hava durumu"),
    Bloatware("com.coloros.compass2", "Compass", "Araç", RiskLevel.SAFE, "Pusula"),
    Bloatware("com.coloros.floatassistant", "Float Assistant", "Sistem", RiskLevel.SAFE, "Yüzen asistan"),
    Bloatware("com.oppo.music", "OPPO Music", "Medya", RiskLevel.SAFE, "OPPO müzik"),
    Bloatware("com.nearme.gamecenter", "Game Center", "Oyun", RiskLevel.SAFE, "Oyun merkezi"),
    Bloatware("com.coloros.oshare", "O Share", "Paylaşım", RiskLevel.SAFE, "Dosya paylaşım"),
    Bloatware("com.coloros.filemanager", "File Manager", "Araç", RiskLevel.SAFE, "Dosya yöneticisi"),
]

# Vivo/iQOO (OriginOS/FuntouchOS) Bloatware  
VIVO_BLOATWARE = [
    Bloatware("com.vivo.browser", "Vivo Browser", "Tarayıcı", RiskLevel.SAFE, "Vivo tarayıcı"),
    Bloatware("com.vivo.appstore", "Vivo App Store", "Mağaza", RiskLevel.SAFE, "Uygulama mağazası"),
    Bloatware("com.vivo.game", "Vivo Game Center", "Oyun", RiskLevel.SAFE, "Oyun merkezi"),
    Bloatware("com.vivo.weather", "Weather", "Araç", RiskLevel.SAFE, "Hava durumu"),
    Bloatware("com.vivo.music", "Vivo Music", "Medya", RiskLevel.SAFE, "Müzik çalar"),
    Bloatware("com.vivo.easyshare", "Easy Share", "Paylaşım", RiskLevel.SAFE, "Dosya paylaşım"),
    Bloatware("com.bbk.iqoo.logsystem", "iQOO Log System", "Telemetri", RiskLevel.SAFE, "Log sistemi"),
]

# Huawei (EMUI/HarmonyOS) Bloatware
HUAWEI_BLOATWARE = [
    Bloatware("com.huawei.appmarket", "Huawei AppGallery", "Mağaza", RiskLevel.SAFE, "Uygulama mağazası"),
    Bloatware("com.huawei.browser", "Huawei Browser", "Tarayıcı", RiskLevel.SAFE, "Huawei tarayıcı"),
    Bloatware("com.huawei.music", "Huawei Music", "Medya", RiskLevel.SAFE, "Müzik çalar"),
    Bloatware("com.huawei.videos", "Huawei Video", "Medya", RiskLevel.SAFE, "Video çalar"),
    Bloatware("com.huawei.gameassistant", "Game Assistant", "Oyun", RiskLevel.SAFE, "Oyun asistanı"),
    Bloatware("com.huawei.hwread", "Huawei Books", "Okuyucu", RiskLevel.SAFE, "E-kitap"),
    Bloatware("com.huawei.himovie", "Huawei Movies", "Medya", RiskLevel.SAFE, "Film uygulaması"),
    Bloatware("com.huawei.health", "Huawei Health", "Sağlık", RiskLevel.SAFE, "Sağlık uygulaması"),
    Bloatware("com.huawei.wallet", "Huawei Wallet", "Ödeme", RiskLevel.SAFE, "Cüzdan"),
]

# Meizu (FlymeOS) Bloatware
MEIZU_BLOATWARE = [
    Bloatware("com.meizu.mstore", "Meizu Store", "Mağaza", RiskLevel.SAFE, "Uygulama mağazası"),
    Bloatware("com.meizu.media.music", "Meizu Music", "Medya", RiskLevel.SAFE, "Müzik çalar"),
    Bloatware("com.meizu.media.video", "Meizu Video", "Medya", RiskLevel.SAFE, "Video çalar"),
    Bloatware("com.meizu.flyme.gamecenter", "Game Center", "Oyun", RiskLevel.SAFE, "Oyun merkezi"),
    Bloatware("com.meizu.net.pedometer", "Pedometer", "Sağlık", RiskLevel.SAFE, "Adım sayar"),
]

# Tüm bloatware'leri birleştir
ALL_BLOATWARE = XIAOMI_BLOATWARE + OPPO_BLOATWARE + VIVO_BLOATWARE + HUAWEI_BLOATWARE + MEIZU_BLOATWARE

# ═══════════════════════════════════════════════════════════════════════════════
# ADB FONKSIYONLARI
# ═══════════════════════════════════════════════════════════════════════════════

class ADBManager:
    def __init__(self):
        self.device = None
        
    def check_adb(self) -> bool:
        """ADB kurulu mu kontrol et"""
        try:
            result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_devices(self) -> List[str]:
        """Bağlı cihazları listele"""
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # İlk satır başlık
        devices = []
        for line in lines:
            if '\tdevice' in line:
                devices.append(line.split('\t')[0])
        return devices
    
    def select_device(self, device_id: str):
        """Cihaz seç"""
        self.device = device_id
        
    def run_command(self, command: List[str]) -> Tuple[bool, str]:
        """ADB komutu çalıştır"""
        try:
            if self.device:
                full_cmd = ['adb', '-s', self.device] + command
            else:
                full_cmd = ['adb'] + command
            result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)
    
    def get_installed_packages(self) -> List[str]:
        """Yüklü paketleri listele"""
        success, output = self.run_command(['shell', 'pm', 'list', 'packages'])
        if success:
            packages = []
            for line in output.strip().split('\n'):
                if line.startswith('package:'):
                    packages.append(line.replace('package:', '').strip())
            return packages
        return []
    
    def get_system_packages(self) -> List[str]:
        """Sistem paketlerini listele"""
        success, output = self.run_command(['shell', 'pm', 'list', 'packages', '-s'])
        if success:
            packages = []
            for line in output.strip().split('\n'):
                if line.startswith('package:'):
                    packages.append(line.replace('package:', '').strip())
            return packages
        return []
    
    def get_running_services(self) -> List[str]:
        """Çalışan servisleri listele"""
        success, output = self.run_command(['shell', 'dumpsys', 'activity', 'services'])
        if success:
            services = []
            for line in output.split('\n'):
                if 'ServiceRecord{' in line:
                    # Servis adını çıkar
                    try:
                        service = line.split('{')[1].split('}')[0].split(' ')[-1]
                        services.append(service)
                    except:
                        pass
            return list(set(services))
        return []
    
    def uninstall_package(self, package: str, keep_data: bool = False) -> Tuple[bool, str]:
        """Paketi kaldır (kullanıcı için)"""
        cmd = ['shell', 'pm', 'uninstall', '-k', '--user', '0', package]
        return self.run_command(cmd)
    
    def disable_package(self, package: str) -> Tuple[bool, str]:
        """Paketi devre dışı bırak"""
        return self.run_command(['shell', 'pm', 'disable-user', '--user', '0', package])
    
    def enable_package(self, package: str) -> Tuple[bool, str]:
        """Paketi etkinleştir"""
        return self.run_command(['shell', 'pm', 'enable', package])
    
    def get_device_info(self) -> Dict[str, str]:
        """Cihaz bilgilerini al"""
        info = {}
        props = [
            ('ro.product.brand', 'Marka'),
            ('ro.product.model', 'Model'),
            ('ro.product.device', 'Cihaz Kodu'),
            ('ro.build.version.release', 'Android Sürümü'),
            ('ro.build.version.sdk', 'SDK'),
            ('ro.miui.ui.version.name', 'MIUI Sürümü'),
            ('ro.build.version.incremental', 'Build'),
        ]
        
        for prop, name in props:
            success, output = self.run_command(['shell', 'getprop', prop])
            if success and output.strip():
                info[name] = output.strip()
        
        return info

# ═══════════════════════════════════════════════════════════════════════════════
# ANA UYGULAMA
# ═══════════════════════════════════════════════════════════════════════════════

class CNDebloater:
    def __init__(self):
        self.adb = ADBManager()
        self.removed_packages = []
        self.log_file = f"debloat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
    def print_banner(self):
        """Banner yazdır"""
        banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║{Colors.MAGENTA}                     CN-BASED ROM DEBLOATER v1.0                               {Colors.CYAN}║
║{Colors.WHITE}                   Çin ROM'ları için Bloatware Temizleyici                     {Colors.CYAN}║
║                                                                               ║
║  {Colors.GREEN}Desteklenen ROM'lar:{Colors.WHITE} MIUI, HyperOS, ColorOS, OriginOS, FlymeOS, EMUI        {Colors.CYAN}║
║  {Colors.YELLOW}Geliştirici:{Colors.WHITE} Tinlera (github.com/Tinlera)                                   {Colors.CYAN}║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)
    
    def log(self, message: str):
        """Log dosyasına yaz"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    
    def check_requirements(self) -> bool:
        """Gereksinimleri kontrol et"""
        info("ADB kontrol ediliyor...")
        
        if not self.adb.check_adb():
            error("ADB bulunamadı! Lütfen ADB kurulumunu yapın.")
            print("\nKurulum:")
            print("  Ubuntu/Debian: sudo apt install adb")
            print("  Arch Linux: sudo pacman -S android-tools")
            print("  Windows: https://developer.android.com/studio/releases/platform-tools")
            return False
        
        success("ADB bulundu!")
        
        devices = self.adb.get_devices()
        if not devices:
            error("Bağlı cihaz bulunamadı!")
            print("\nKontrol edin:")
            print("  1. USB Debugging aktif mi?")
            print("  2. USB kablosu bağlı mı?")
            print("  3. Telefonda bağlantıyı onayladınız mı?")
            return False
        
        if len(devices) == 1:
            self.adb.select_device(devices[0])
            success(f"Cihaz seçildi: {devices[0]}")
        else:
            print("\nBirden fazla cihaz bulundu:")
            for i, device in enumerate(devices, 1):
                print(f"  {i}. {device}")
            
            while True:
                try:
                    choice = int(input("\nCihaz seçin (numara): "))
                    if 1 <= choice <= len(devices):
                        self.adb.select_device(devices[choice - 1])
                        success(f"Cihaz seçildi: {devices[choice - 1]}")
                        break
                except ValueError:
                    pass
                error("Geçersiz seçim!")
        
        return True
    
    def show_device_info(self):
        """Cihaz bilgilerini göster"""
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}📱 CİHAZ BİLGİLERİ{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        info_dict = self.adb.get_device_info()
        for key, value in info_dict.items():
            print(f"  {Colors.YELLOW}{key}:{Colors.RESET} {value}")
        
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}\n")
    
    def scan_bloatware(self) -> Dict[str, List[Bloatware]]:
        """Bloatware tara"""
        info("Yüklü paketler taranıyor...")
        installed = set(self.adb.get_installed_packages())
        
        found = {
            'safe': [],
            'moderate': [],
            'risky': []
        }
        
        for bloat in ALL_BLOATWARE:
            if bloat.package in installed:
                if bloat.risk == RiskLevel.SAFE:
                    found['safe'].append(bloat)
                elif bloat.risk == RiskLevel.MODERATE:
                    found['moderate'].append(bloat)
                else:
                    found['risky'].append(bloat)
        
        return found
    
    def scan_services(self) -> List[str]:
        """Çin servislerini tara"""
        info("Çalışan servisler taranıyor...")
        services = self.adb.get_running_services()
        
        china_keywords = [
            'xiaomi', 'miui', 'mipay', 'baidu', 'alibaba', 'tencent', 'qq',
            'wechat', 'weibo', 'huawei', 'oppo', 'vivo', 'meizu', 'sogou',
            'iflytek', 'kuaishou', 'bytedance', 'douyin', 'heytap', 'coloros'
        ]
        
        china_services = []
        for service in services:
            for keyword in china_keywords:
                if keyword in service.lower():
                    china_services.append(service)
                    break
        
        return china_services
    
    def display_scan_results(self, bloatware: Dict[str, List[Bloatware]], services: List[str]):
        """Tarama sonuçlarını göster"""
        total = len(bloatware['safe']) + len(bloatware['moderate']) + len(bloatware['risky'])
        
        print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}🔍 TARAMA SONUÇLARI{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}✅ GÜVENLİ KALDIRILACAKLAR ({len(bloatware['safe'])} adet):{Colors.RESET}")
        if bloatware['safe']:
            for b in bloatware['safe']:
                print(f"   • {b.name:<30} [{b.category}]")
        else:
            print("   (Bulunamadı)")
        
        print(f"\n{Colors.YELLOW}⚠️  DİKKATLİ KALDIRILABİLİR ({len(bloatware['moderate'])} adet):{Colors.RESET}")
        if bloatware['moderate']:
            for b in bloatware['moderate']:
                print(f"   • {b.name:<30} [{b.category}] - {b.description}")
        else:
            print("   (Bulunamadı)")
        
        print(f"\n{Colors.RED}🚫 RİSKLİ - ÖNERİLMEZ ({len(bloatware['risky'])} adet):{Colors.RESET}")
        if bloatware['risky']:
            for b in bloatware['risky']:
                print(f"   • {b.name:<30} [{b.category}] - {b.description}")
        else:
            print("   (Bulunamadı)")
        
        print(f"\n{Colors.MAGENTA}🔄 ÇİN SERVİSLERİ ({len(services)} adet):{Colors.RESET}")
        if services:
            for s in services[:10]:  # İlk 10'u göster
                print(f"   • {s}")
            if len(services) > 10:
                print(f"   ... ve {len(services) - 10} adet daha")
        else:
            print("   (Bulunamadı)")
        
        print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}TOPLAM: {total} bloatware, {len(services)} Çin servisi tespit edildi{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}\n")
    
    def interactive_remove(self, bloatware: Dict[str, List[Bloatware]]):
        """İnteraktif kaldırma menüsü"""
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}🗑️  KALDIRMA MENÜSÜ{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        print("\nSeçenekler:")
        print(f"  {Colors.GREEN}1.{Colors.RESET} Tüm GÜVENLİ bloatware'leri kaldır ({len(bloatware['safe'])} adet)")
        print(f"  {Colors.YELLOW}2.{Colors.RESET} Güvenli + DİKKATLİ olanları kaldır ({len(bloatware['safe']) + len(bloatware['moderate'])} adet)")
        print(f"  {Colors.MAGENTA}3.{Colors.RESET} Tek tek seç ve kaldır")
        print(f"  {Colors.BLUE}4.{Colors.RESET} Paket adı ile manuel kaldır")
        print(f"  {Colors.RED}0.{Colors.RESET} Geri dön")
        
        choice = input("\nSeçiminiz: ").strip()
        
        if choice == '1':
            self.remove_packages([b.package for b in bloatware['safe']])
        elif choice == '2':
            packages = [b.package for b in bloatware['safe']] + [b.package for b in bloatware['moderate']]
            self.remove_packages(packages)
        elif choice == '3':
            self.select_and_remove(bloatware)
        elif choice == '4':
            package = input("Paket adı girin: ").strip()
            if package:
                self.remove_packages([package])
        elif choice == '0':
            return
        else:
            error("Geçersiz seçim!")
    
    def select_and_remove(self, bloatware: Dict[str, List[Bloatware]]):
        """Tek tek seç ve kaldır"""
        all_bloat = bloatware['safe'] + bloatware['moderate']
        
        if not all_bloat:
            warning("Kaldırılacak bloatware bulunamadı!")
            return
        
        print("\nKaldırmak istediklerinizin numaralarını girin (virgülle ayırın):")
        print("Örnek: 1,3,5,7\n")
        
        for i, b in enumerate(all_bloat, 1):
            risk_color = Colors.GREEN if b.risk == RiskLevel.SAFE else Colors.YELLOW
            print(f"  {i:2}. {risk_color}{b.name:<30}{Colors.RESET} [{b.category}]")
        
        selection = input("\nSeçiminiz: ").strip()
        
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            packages = []
            for idx in indices:
                if 1 <= idx <= len(all_bloat):
                    packages.append(all_bloat[idx - 1].package)
            
            if packages:
                self.remove_packages(packages)
            else:
                warning("Geçerli seçim yapılmadı!")
        except ValueError:
            error("Geçersiz format!")
    
    def remove_packages(self, packages: List[str]):
        """Paketleri kaldır"""
        if not packages:
            return
        
        print(f"\n{Colors.YELLOW}⚠️  {len(packages)} paket kaldırılacak!{Colors.RESET}")
        confirm = input("Devam etmek istiyor musunuz? (e/h): ").strip().lower()
        
        if confirm != 'e':
            warning("İşlem iptal edildi.")
            return
        
        print()
        success_count = 0
        fail_count = 0
        
        for package in packages:
            print(f"  Kaldırılıyor: {package}...", end=" ")
            ok, output = self.adb.uninstall_package(package)
            
            if ok and 'Success' in output:
                print(f"{Colors.GREEN}✓{Colors.RESET}")
                self.removed_packages.append(package)
                self.log(f"REMOVED: {package}")
                success_count += 1
            else:
                print(f"{Colors.RED}✗{Colors.RESET} ({output.strip()})")
                self.log(f"FAILED: {package} - {output.strip()}")
                fail_count += 1
        
        print()
        success(f"{success_count} paket başarıyla kaldırıldı!")
        if fail_count > 0:
            warning(f"{fail_count} paket kaldırılamadı.")
        
        self.log(f"SUMMARY: {success_count} removed, {fail_count} failed")
    
    def restore_package(self):
        """Kaldırılan paketi geri yükle"""
        print(f"\n{Colors.CYAN}♻️  PAKET GERİ YÜKLEME{Colors.RESET}")
        print("\nPaket yeniden yüklemek için şu komutu kullanabilirsiniz:")
        print(f"{Colors.YELLOW}adb shell cmd package install-existing <paket_adı>{Colors.RESET}")
        
        package = input("\nGeri yüklenecek paket adı (veya boş bırakın): ").strip()
        
        if package:
            ok, output = self.adb.run_command(['shell', 'cmd', 'package', 'install-existing', package])
            if ok:
                success(f"Paket geri yüklendi: {package}")
            else:
                error(f"Geri yükleme başarısız: {output}")
    
    def export_report(self, bloatware: Dict[str, List[Bloatware]], services: List[str]):
        """Rapor dışa aktar"""
        filename = f"cn_debloater_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'device_info': self.adb.get_device_info(),
            'bloatware': {
                'safe': [{'package': b.package, 'name': b.name, 'category': b.category} for b in bloatware['safe']],
                'moderate': [{'package': b.package, 'name': b.name, 'category': b.category} for b in bloatware['moderate']],
                'risky': [{'package': b.package, 'name': b.name, 'category': b.category} for b in bloatware['risky']],
            },
            'china_services': services,
            'removed_packages': self.removed_packages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        success(f"Rapor kaydedildi: {filename}")
    
    def main_menu(self):
        """Ana menü"""
        bloatware = None
        services = None
        
        while True:
            print(f"\n{Colors.CYAN}{'═' * 50}{Colors.RESET}")
            print(f"{Colors.BOLD}📋 ANA MENÜ{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 50}{Colors.RESET}")
            
            print(f"\n  {Colors.GREEN}1.{Colors.RESET} 🔍 Bloatware ve Servisleri Tara")
            print(f"  {Colors.GREEN}2.{Colors.RESET} 🗑️  Bloatware Kaldır")
            print(f"  {Colors.GREEN}3.{Colors.RESET} 📱 Cihaz Bilgilerini Göster")
            print(f"  {Colors.GREEN}4.{Colors.RESET} ♻️  Paket Geri Yükle")
            print(f"  {Colors.GREEN}5.{Colors.RESET} 📄 Rapor Dışa Aktar")
            print(f"  {Colors.RED}0.{Colors.RESET} 🚪 Çıkış")
            
            choice = input("\nSeçiminiz: ").strip()
            
            if choice == '1':
                bloatware = self.scan_bloatware()
                services = self.scan_services()
                self.display_scan_results(bloatware, services)
                
            elif choice == '2':
                if bloatware is None:
                    warning("Önce tarama yapmalısınız!")
                    bloatware = self.scan_bloatware()
                    services = self.scan_services()
                    self.display_scan_results(bloatware, services)
                self.interactive_remove(bloatware)
                
            elif choice == '3':
                self.show_device_info()
                
            elif choice == '4':
                self.restore_package()
                
            elif choice == '5':
                if bloatware is None:
                    bloatware = self.scan_bloatware()
                    services = self.scan_services()
                self.export_report(bloatware, services)
                
            elif choice == '0':
                print(f"\n{Colors.CYAN}Güle güle! 👋{Colors.RESET}\n")
                break
            else:
                error("Geçersiz seçim!")
    
    def run(self):
        """Uygulamayı başlat"""
        self.print_banner()
        
        if not self.check_requirements():
            sys.exit(1)
        
        self.show_device_info()
        self.main_menu()

# ═══════════════════════════════════════════════════════════════════════════════
# BAŞLATICI
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    try:
        app = CNDebloater()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}İşlem kullanıcı tarafından iptal edildi.{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Beklenmeyen hata: {e}{Colors.RESET}\n")
        sys.exit(1)
