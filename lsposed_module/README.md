# 🧹 CN-Debloater LSPosed Module

## LSPosed/Xposed Modülü

Çin ROM'larındaki bloatware'leri, analytics'i ve pil tüketen servisleri **sistem seviyesinde** engelleyen LSPosed modülü.

### ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| **🚫 Paket Engelleme** | Bloatware paketlerinin yüklenmesini tamamen engeller |
| **⚡ Servis Hook** | Gereksiz servisleri durdurur |
| **🔋 Wakelock Blocker** | Pil tüketen wakelock'ları engeller |
| **📊 Analytics Blocker** | Telemetri ve tracking isteklerini engeller |
| **⏰ Alarm Blocker** | Gereksiz arka plan alarm'larını engeller |
| **📱 İnteraktif UI** | Kolay kullanımlı engelleme arayüzü |

### 📦 Kurulum

1. **LSPosed** veya **EdXposed** kurulu olmalı
2. `CN-Debloater.apk` dosyasını yükleyin
3. LSPosed Manager'dan modülü aktif edin
4. Scope olarak "System Framework" ve hedef uygulamaları seçin
5. Cihazı yeniden başlatın

### 🎯 Engellenen Kategoriler

- **Telemetri**: Analytics, tracking, usage stats
- **Reklamlar**: MSA, AdSolution
- **Servisler**: Push, sync, background services
- **Wakelock'lar**: Gereksiz CPU uyandırmaları
- **Network**: Çin sunucularına bağlantılar

### 🔧 Derleme

```bash
cd lsposed_module
./gradlew assembleRelease
```

APK dosyası: `app/build/outputs/apk/release/app-release.apk`

### 📋 Gereksinimler

- Android 8.0+ (SDK 26+)
- LSPosed veya EdXposed
- Root erişimi

### ⚠️ Uyarı

Bu modül sistem uygulamalarını etkiler. Yanlış yapılandırma cihazınızda sorunlara yol açabilir. Risk size aittir.
