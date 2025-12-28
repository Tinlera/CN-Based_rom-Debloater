# 🧹 CN-Based ROM Debloater

<div align="center">

![CN Debloater](https://img.shields.io/badge/CN_Debloater-v1.0-ff6b6b?style=for-the-badge&logo=android&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Çin ROM'ları için Güçlü Bloatware Temizleme Aracı**

*MIUI • HyperOS • ColorOS • OriginOS • FlymeOS • EMUI*

</div>

---

## 📋 Açıklama

**CN-Based ROM Debloater**, Çin menşeli Android ROM'larında bulunan gereksiz uygulamaları (bloatware), reklam servislerini ve telemetri bileşenlerini güvenli bir şekilde kaldırmanızı sağlayan Python tabanlı bir araçtır.

### ✨ Özellikler

- 🔍 **Otomatik Tarama**: ROM'unuzdaki tüm bloatware'leri otomatik tespit eder
- 🛡️ **Risk Sınıflandırması**: Uygulamaları güvenlik seviyesine göre gruplandırır
- 📊 **Servis Analizi**: Çalışan Çin servislerini listeler
- 💾 **Veri Koruma**: Kaldırırken kullanıcı verilerini korur
- ♻️ **Geri Yükleme**: Kaldırılan uygulamaları geri yükleyebilirsiniz
- 📄 **Raporlama**: JSON formatında detaylı rapor oluşturur

### 🔧 İki Yöntem

| Yöntem | Açıklama | Gereksinim |
|--------|----------|------------|
| **Python Script** | ADB üzerinden bloatware kaldırma | Python + ADB |
| **LSPosed Modülü** | Sistem seviyesinde engelleme | Root + LSPosed |

---

## 🎯 Desteklenen ROM'lar

| Marka | ROM | Durum |
|-------|-----|-------|
| **Xiaomi/Poco/Redmi** | MIUI, HyperOS | ✅ Tam Destek |
| **OPPO/Realme/OnePlus** | ColorOS | ✅ Tam Destek |
| **Vivo/iQOO** | OriginOS, FuntouchOS | ✅ Tam Destek |
| **Huawei/Honor** | EMUI, HarmonyOS | ✅ Tam Destek |
| **Meizu** | FlymeOS | ✅ Tam Destek |

---

## 📦 Kurulum

### Gereksinimler

- Python 3.7 veya üzeri
- ADB (Android Debug Bridge)
- USB Debugging aktif Android cihaz

### ADB Kurulumu

```bash
# Ubuntu/Debian
sudo apt install adb

# Arch Linux
sudo pacman -S android-tools

# macOS (Homebrew)
brew install android-platform-tools

# Windows
# https://developer.android.com/studio/releases/platform-tools adresinden indirin
```

### Script Kurulumu

```bash
# Repoyu klonla
git clone https://github.com/Tinlera/CN-Based_rom-Debloater.git
cd CN-Based_rom-Debloater

# Çalıştır
python3 cn_debloater.py
```

---

## 🚀 Kullanım

### 1. Telefonu Hazırla

1. **USB Debugging** aktif et: `Ayarlar → Geliştirici Seçenekleri → USB Hata Ayıklama`
2. Telefonu USB kablosuyla bilgisayara bağla
3. Telefonda bağlantıyı **onayla**

### 2. Script'i Çalıştır

```bash
python3 cn_debloater.py
```

### 3. Ana Menü

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     CN-BASED ROM DEBLOATER v1.0                               ║
║                   Çin ROM'ları için Bloatware Temizleyici                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📋 ANA MENÜ
══════════════════════════════════════════════════

  1. 🔍 Bloatware ve Servisleri Tara
  2. 🗑️  Bloatware Kaldır
  3. 📱 Cihaz Bilgilerini Göster
  4. ♻️  Paket Geri Yükle
  5. 📄 Rapor Dışa Aktar
  0. 🚪 Çıkış
```

---

## 🛡️ Risk Seviyeleri

| Seviye | Renk | Açıklama |
|--------|------|----------|
| **SAFE** | 🟢 Yeşil | Güvenle kaldırılabilir, sistem etkilenmez |
| **MODERATE** | 🟡 Sarı | Dikkatli kaldırılmalı, bazı özellikler etkilenebilir |
| **RISKY** | 🔴 Kırmızı | Önerilmez, sistem kararsızlığına yol açabilir |

---

## 📝 Kaldırılan Bloatware Kategorileri

### 🚫 Reklam & Telemetri
- `com.miui.analytics` - Xiaomi Analytics
- `com.miui.msa.global` - MIUI System Ads
- `com.miui.bugreport` - Bug Report

### ⌨️ Çin Klavyeleri
- `com.sohu.inputmethod.sogou.xiaomi` - Sogou Keyboard
- `com.baidu.input_mi` - Baidu Keyboard
- `com.iflytek.inputmethod.miui` - iFlytek Keyboard

### 📱 Çin Uygulamaları
- `com.xiaomi.mipicks` - Mi Picks / GetApps
- `com.miui.yellowpage` - Yellow Pages
- `com.miui.hybrid` - Quick Apps
- `com.mi.globalbrowser` - Mi Browser

### 💰 Ödeme Servisleri
- `com.xiaomi.payment` - Mi Pay
- `com.mipay.wallet.id` - Mi Wallet

### 🎮 Oyun Servisleri
- `com.xiaomi.glgm` - Games
- `com.xiaomi.gamecenter.sdk.service` - Game Center SDK

### 📲 Pre-installed Apps
- Facebook, Netflix, TikTok, AliExpress, Amazon, eBay, Yandex, Opera...

---

## ⚠️ Uyarılar

> **DİKKAT**: Bu araç sistem uygulamalarını kaldırır. Yanlış kullanım cihazınızda sorunlara yol açabilir.

- 🔴 **Yedek alın**: İşlem öncesi önemli verilerinizi yedekleyin
- 🔴 **Root gerekmiyor**: Standard ADB kullanır, root şart değil
- 🔴 **Geri dönüş**: Kaldırılan uygulamalar fabrika ayarlarına dönüşle geri gelir
- 🔴 **Test edin**: Kaldırma sonrası cihazınızı test edin

---

## 🔧 Sorun Giderme

### Cihaz görünmüyor
```bash
# ADB server'ı yeniden başlat
adb kill-server
adb start-server
adb devices
```

### Kaldırma başarısız
```bash
# Manuel kaldırma
adb shell pm uninstall -k --user 0 <paket_adı>
```

### Uygulama geri yükleme
```bash
adb shell cmd package install-existing <paket_adı>
```

---

## 📊 Örnek Çıktı

```
🔍 TARAMA SONUÇLARI
═══════════════════════════════════════════════════════════════════

✅ GÜVENLİ KALDIRILACAKLAR (23 adet):
   • Xiaomi Analytics              [Telemetri]
   • MSA (MIUI System Ads)         [Reklam]
   • Sogou Keyboard                [Klavye]
   • Mi Browser                    [Tarayıcı]
   ...

⚠️  DİKKATLİ KALDIRILABİLİR (5 adet):
   • Mi Gallery                    [Medya] - Google Photos kullanılabilir
   • Mi Backup                     [Yedekleme] - alternatif gerekebilir
   ...

🔄 ÇİN SERVİSLERİ (12 adet):
   • com.xiaomi.xmsf
   • com.miui.daemon
   ...

═══════════════════════════════════════════════════════════════════
TOPLAM: 28 bloatware, 12 Çin servisi tespit edildi
```

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/new-bloatware`)
3. Yeni bloatware ekleyin (`ALL_BLOATWARE` listesine)
4. Commit yapın (`git commit -m 'Add new bloatware package'`)
5. Push edin (`git push origin feature/new-bloatware`)
6. Pull Request açın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

<div align="center">

**CN-Based ROM Debloater** - *Çin bloatware'lerinden kurtulun!* 🧹

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐

</div>
