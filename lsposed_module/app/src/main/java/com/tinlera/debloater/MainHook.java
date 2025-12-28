package com.tinlera.debloater;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.IXposedHookZygoteInit;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.XC_MethodReplacement;
import de.robv.android.xposed.XposedBridge;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;

import android.app.Activity;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.os.PowerManager;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * CN-Based ROM Debloater - LSPosed Module
 * 
 * Çin ROM'larındaki gereksiz servisleri, analytics'i ve
 * pil tüketen bileşenleri engeller.
 * 
 * @author Tinlera
 */
public class MainHook implements IXposedHookLoadPackage, IXposedHookZygoteInit {

    private static final String TAG = "CNDebloater";
    private static String MODULE_PATH = null;

    // ═══════════════════════════════════════════════════════════════════════════
    // BLOATWARE PAKETLERİ
    // ═══════════════════════════════════════════════════════════════════════════

    // Tamamen engellenecek paketler (hiç çalışmasın)
    private static final Set<String> BLOCKED_PACKAGES = new HashSet<>(Arrays.asList(
            // Xiaomi Analytics & Ads
            "com.miui.analytics",
            "com.miui.msa.global",
            "com.miui.systemAdSolution",

            // Xiaomi Telemetry
            "com.miui.bugreport",
            "com.xiaomi.joyose",
            "com.xiaomi.xmsf",

            // Xiaomi Bloatware
            "com.miui.hybrid",
            "com.miui.hybrid.accessory",
            "com.xiaomi.mipicks",
            "com.miui.yellowpage",
            "com.miui.personalassistant",

            // Çin Klavyeleri
            "com.sohu.inputmethod.sogou.xiaomi",
            "com.baidu.input_mi",
            "com.iflytek.inputmethod.miui",

            // Çin Oyun Servisleri
            "com.xiaomi.glgm",
            "com.xiaomi.gamecenter.sdk.service",

            // OPPO/Realme Bloatware
            "com.heytap.market",
            "com.heytap.browser",
            "com.nearme.gamecenter",

            // Vivo Bloatware
            "com.vivo.browser",
            "com.vivo.appstore",
            "com.bbk.iqoo.logsystem",

            // Huawei Bloatware
            "com.huawei.appmarket",
            "com.huawei.browser"));

    // Servis hook'lanacak paketler (servisler durdurulacak)
    private static final Set<String> SERVICE_HOOK_PACKAGES = new HashSet<>(Arrays.asList(
            "com.miui.daemon",
            "com.miui.powerkeeper",
            "com.miui.securitycenter",
            "com.xiaomi.xmsf",
            "com.miui.analytics",
            "com.miui.cloudservice"));

    // Wakelock engellenecek paketler
    private static final Set<String> WAKELOCK_BLOCK_PACKAGES = new HashSet<>(Arrays.asList(
            "com.miui.analytics",
            "com.xiaomi.xmsf",
            "com.miui.daemon",
            "com.miui.securitycenter",
            "com.miui.cloudservice",
            "com.xiaomi.joyose",
            "com.miui.hybrid"));

    // Analytics URL'leri engellenecek
    private static final Set<String> BLOCKED_ANALYTICS_HOSTS = new HashSet<>(Arrays.asList(
            "tracking.miui.com",
            "data.mistat.xiaomi.com",
            "api.ad.xiaomi.com",
            "sdkconfig.ad.xiaomi.com",
            "log.avlyun.com",
            "api.scanner.xiaomi.com",
            "resolver.msg.xiaomi.net",
            "abtest.mistat.xiaomi.com",
            "tracking.rus.miui.com",
            "data.mistat.intl.xiaomi.com",
            "globalapi.ad.xiaomi.com",
            "cnbj-tracking.miui.com",
            // Baidu
            "hm.baidu.com",
            "hmma.baidu.com",
            "mobads.baidu.com",
            // Tencent
            "pingma.qq.com",
            "report.qqmail.com",
            // Alibaba
            "log.alibaba.com",
            "alisdk.alibaba.com"));

    // ═══════════════════════════════════════════════════════════════════════════
    // XPOSED HOOK BAŞLANGIÇ
    // ═══════════════════════════════════════════════════════════════════════════

    @Override
    public void initZygote(StartupParam startupParam) throws Throwable {
        MODULE_PATH = startupParam.modulePath;
        XposedBridge.log(TAG + ": Module initialized at " + MODULE_PATH);
    }

    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        String packageName = lpparam.packageName;

        // Engellenmiş paketler - hiç yüklenmesin
        if (BLOCKED_PACKAGES.contains(packageName)) {
            XposedBridge.log(TAG + ": BLOCKED package: " + packageName);
            killPackageOnLoad(lpparam);
            return;
        }

        // Servis hook'lama
        if (SERVICE_HOOK_PACKAGES.contains(packageName)) {
            hookServices(lpparam);
        }

        // Wakelock engelleme
        if (WAKELOCK_BLOCK_PACKAGES.contains(packageName)) {
            hookWakelocks(lpparam);
        }

        // Analytics engelleme (tüm paketlerde)
        hookAnalytics(lpparam);

        // Alarm engelleme
        hookAlarms(lpparam);

        // System apps için ek hook'lar
        if (packageName.startsWith("com.miui.") ||
                packageName.startsWith("com.xiaomi.") ||
                packageName.startsWith("com.coloros.") ||
                packageName.startsWith("com.heytap.") ||
                packageName.startsWith("com.vivo.") ||
                packageName.startsWith("com.huawei.")) {

            hookChinaSystemApps(lpparam);
        }

        // Android sistem hook'ları
        if (packageName.equals("android")) {
            hookAndroidSystem(lpparam);
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // HOOK FONKSİYONLARI
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Paket yüklendiğinde hemen öldür
     */
    private void killPackageOnLoad(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            // Application onCreate - hiçbir şey yapmasın
            XposedHelpers.findAndHookMethod(
                    "android.app.Application",
                    lpparam.classLoader,
                    "onCreate",
                    XC_MethodReplacement.DO_NOTHING);

            // Activity onCreate - hemen kapat
            XposedHelpers.findAndHookMethod(
                    "android.app.Activity",
                    lpparam.classLoader,
                    "onCreate",
                    android.os.Bundle.class,
                    new XC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) {
                            Activity activity = (Activity) param.thisObject;
                            activity.finish();
                        }
                    });

            // Service onCreate - hemen durdur
            XposedHelpers.findAndHookMethod(
                    "android.app.Service",
                    lpparam.classLoader,
                    "onCreate",
                    new XC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) {
                            Service service = (Service) param.thisObject;
                            service.stopSelf();
                        }
                    });

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error killing package: " + t.getMessage());
        }
    }

    /**
     * Servisleri hook'la ve durdur
     */
    private void hookServices(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            // Service.startService - engelle
            XposedHelpers.findAndHookMethod(
                    "android.app.Service",
                    lpparam.classLoader,
                    "onStartCommand",
                    Intent.class,
                    int.class,
                    int.class,
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            Service service = (Service) param.thisObject;
                            String serviceName = service.getClass().getName();

                            // Blocker servisleri
                            if (shouldBlockService(serviceName)) {
                                XposedBridge.log(TAG + ": BLOCKED service: " + serviceName);
                                service.stopSelf();
                                param.setResult(Service.START_NOT_STICKY);
                            }
                        }
                    });

            XposedBridge.log(TAG + ": Service hooks installed for: " + lpparam.packageName);

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error hooking services: " + t.getMessage());
        }
    }

    /**
     * Wakelock'ları engelle
     */
    private void hookWakelocks(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            XposedHelpers.findAndHookMethod(
                    PowerManager.WakeLock.class,
                    "acquire",
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            XposedBridge.log(TAG + ": BLOCKED wakelock acquire in: " + lpparam.packageName);
                            param.setResult(null);
                        }
                    });

            XposedHelpers.findAndHookMethod(
                    PowerManager.WakeLock.class,
                    "acquire",
                    long.class,
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            XposedBridge.log(TAG + ": BLOCKED timed wakelock in: " + lpparam.packageName);
                            param.setResult(null);
                        }
                    });

            XposedBridge.log(TAG + ": Wakelock hooks installed for: " + lpparam.packageName);

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error hooking wakelocks: " + t.getMessage());
        }
    }

    /**
     * Analytics ve tracking isteklerini engelle
     */
    private void hookAnalytics(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            // URL.openConnection hook
            XposedHelpers.findAndHookMethod(
                    "java.net.URL",
                    lpparam.classLoader,
                    "openConnection",
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            java.net.URL url = (java.net.URL) param.thisObject;
                            String host = url.getHost();

                            if (host != null && shouldBlockHost(host)) {
                                XposedBridge.log(TAG + ": BLOCKED analytics URL: " + host);
                                param.setThrowable(new java.io.IOException("Blocked by CN Debloater"));
                            }
                        }
                    });

            // HttpURLConnection hook
            try {
                Class<?> httpUrlConnectionClass = XposedHelpers.findClass(
                        "com.android.okhttp.internal.huc.HttpURLConnectionImpl",
                        lpparam.classLoader);

                XposedHelpers.findAndHookMethod(
                        httpUrlConnectionClass,
                        "connect",
                        new XC_MethodHook() {
                            @Override
                            protected void beforeHookedMethod(MethodHookParam param) {
                                try {
                                    java.net.URL url = (java.net.URL) XposedHelpers.callMethod(param.thisObject,
                                            "getURL");
                                    String host = url.getHost();

                                    if (host != null && shouldBlockHost(host)) {
                                        XposedBridge.log(TAG + ": BLOCKED HTTP connection: " + host);
                                        param.setThrowable(new java.io.IOException("Blocked by CN Debloater"));
                                    }
                                } catch (Throwable ignored) {
                                }
                            }
                        });
            } catch (Throwable ignored) {
            }

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error hooking analytics: " + t.getMessage());
        }
    }

    /**
     * Alarm'ları engelle (gereksiz arka plan çalışmalarını)
     */
    private void hookAlarms(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            // Sadece bloatware paketleri için
            if (!isBlockedOrHookedPackage(lpparam.packageName)) {
                return;
            }

            XposedHelpers.findAndHookMethod(
                    "android.app.AlarmManager",
                    lpparam.classLoader,
                    "setExact",
                    int.class,
                    long.class,
                    android.app.PendingIntent.class,
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            XposedBridge.log(TAG + ": BLOCKED alarm setExact in: " + lpparam.packageName);
                            param.setResult(null);
                        }
                    });

            XposedHelpers.findAndHookMethod(
                    "android.app.AlarmManager",
                    lpparam.classLoader,
                    "setRepeating",
                    int.class,
                    long.class,
                    long.class,
                    android.app.PendingIntent.class,
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            XposedBridge.log(TAG + ": BLOCKED repeating alarm in: " + lpparam.packageName);
                            param.setResult(null);
                        }
                    });

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error hooking alarms: " + t.getMessage());
        }
    }

    /**
     * Çin sistem uygulamalarını hook'la
     */
    private void hookChinaSystemApps(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            // JobScheduler engelleme
            XposedHelpers.findAndHookMethod(
                    "android.app.job.JobScheduler",
                    lpparam.classLoader,
                    "schedule",
                    android.app.job.JobInfo.class,
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            XposedBridge.log(TAG + ": BLOCKED job schedule in: " + lpparam.packageName);
                            param.setResult(android.app.job.JobScheduler.RESULT_FAILURE);
                        }
                    });

            // WorkManager engelleme
            try {
                Class<?> workManagerClass = XposedHelpers.findClass(
                        "androidx.work.WorkManager",
                        lpparam.classLoader);

                XposedHelpers.findAndHookMethod(
                        workManagerClass,
                        "enqueue",
                        XposedHelpers.findClass("androidx.work.WorkRequest", lpparam.classLoader),
                        new XC_MethodHook() {
                            @Override
                            protected void beforeHookedMethod(MethodHookParam param) {
                                XposedBridge.log(TAG + ": BLOCKED WorkManager enqueue in: " + lpparam.packageName);
                                param.setResult(null);
                            }
                        });
            } catch (Throwable ignored) {
            }

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error hooking China system apps: " + t.getMessage());
        }
    }

    /**
     * Android sistem hook'ları (ActivityManager, PackageManager vs.)
     */
    private void hookAndroidSystem(XC_LoadPackage.LoadPackageParam lpparam) {
        try {
            // Broadcast engelleme - bloatware paketlerinden gelen broadcast'ler
            XposedHelpers.findAndHookMethod(
                    "com.android.server.am.ActivityManagerService",
                    lpparam.classLoader,
                    "broadcastIntent",
                    new XC_MethodHook() {
                        @Override
                        protected void beforeHookedMethod(MethodHookParam param) {
                            // İlk parametre genellikle caller app
                            try {
                                Object callerApp = param.args[0];
                                if (callerApp != null) {
                                    String callerPackage = (String) XposedHelpers.getObjectField(callerApp,
                                            "info.packageName");
                                    if (callerPackage != null && BLOCKED_PACKAGES.contains(callerPackage)) {
                                        XposedBridge.log(TAG + ": BLOCKED broadcast from: " + callerPackage);
                                        param.setResult(0);
                                    }
                                }
                            } catch (Throwable ignored) {
                            }
                        }
                    });

            XposedBridge.log(TAG + ": Android system hooks installed");

        } catch (Throwable t) {
            XposedBridge.log(TAG + ": Error hooking Android system: " + t.getMessage());
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // YARDIMCI FONKSİYONLAR
    // ═══════════════════════════════════════════════════════════════════════════

    private boolean shouldBlockService(String serviceName) {
        // Bilinen zararlı servisler
        String[] blockedServices = {
                "AnalyticsService",
                "TrackingService",
                "PushService",
                "AdService",
                "ReportService",
                "LogService",
                "UploadService",
                "SyncService",
                "DataCollectorService",
                "UsageStatsService",
                // Xiaomi specific
                "MiPushService",
                "XMPushService",
                "PushMessageHandler",
                "AnalyticService",
                "StatService"
        };

        for (String blocked : blockedServices) {
            if (serviceName.contains(blocked)) {
                return true;
            }
        }

        return false;
    }

    private boolean shouldBlockHost(String host) {
        if (host == null)
            return false;

        // Direkt eşleşme
        if (BLOCKED_ANALYTICS_HOSTS.contains(host)) {
            return true;
        }

        // Subdomain kontrolü
        for (String blockedHost : BLOCKED_ANALYTICS_HOSTS) {
            if (host.endsWith("." + blockedHost) || host.equals(blockedHost)) {
                return true;
            }
        }

        // Genel analytics/tracking keyword'leri
        String[] blockKeywords = {
                "analytics", "tracking", "telemetry", "report",
                "stat.", "stats.", "log.", "logs.", "metric",
                "adservice", "adsdk", "msa.", "mipush"
        };

        for (String keyword : blockKeywords) {
            if (host.contains(keyword)) {
                return true;
            }
        }

        return false;
    }

    private boolean isBlockedOrHookedPackage(String packageName) {
        return BLOCKED_PACKAGES.contains(packageName) ||
                SERVICE_HOOK_PACKAGES.contains(packageName) ||
                WAKELOCK_BLOCK_PACKAGES.contains(packageName);
    }
}
