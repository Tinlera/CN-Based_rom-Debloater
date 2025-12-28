package com.tinlera.debloater.ui;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.SearchView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * CN Debloater - Ana Aktivite
 * Bloatware tarama ve engelleme UI'ı
 */
public class MainActivity extends Activity {

    private static final String PREFS_NAME = "cn_debloater_prefs";
    private static final String KEY_BLOCKED_PACKAGES = "blocked_packages";
    private static final String KEY_MODULE_ENABLED = "module_enabled";

    private ListView listView;
    private ProgressBar progressBar;
    private TextView statusText;
    private TextView statsText;
    private Switch masterSwitch;
    private LinearLayout headerLayout;

    private BloatwareAdapter adapter;
    private List<BloatwareItem> allBloatware = new ArrayList<>();
    private List<BloatwareItem> filteredBloatware = new ArrayList<>();
    private SharedPreferences prefs;
    private Set<String> blockedPackages = new HashSet<>();

    // Bloatware kategorileri
    private static final Set<String> BLOATWARE_PACKAGES = new HashSet<>(Arrays.asList(
            // Analytics & Ads
            "com.miui.analytics",
            "com.miui.msa.global",
            "com.miui.systemAdSolution",
            "com.miui.bugreport",
            "com.xiaomi.joyose",

            // Xiaomi Services
            "com.xiaomi.xmsf",
            "com.miui.daemon",
            "com.miui.hybrid",
            "com.miui.hybrid.accessory",
            "com.miui.cloudservice",
            "com.miui.cloudbackup",

            // Xiaomi Apps
            "com.xiaomi.mipicks",
            "com.miui.yellowpage",
            "com.miui.personalassistant",
            "com.miui.voiceassist",
            "com.mi.globalbrowser",
            "com.miui.player",
            "com.miui.video",
            "com.miui.fm",
            "com.miui.weather2",
            "com.miui.notes",
            "com.miui.calculator",
            "com.miui.compass",
            "com.xiaomi.scanner",
            "com.xiaomi.midrop",

            // Çin Klavyeleri
            "com.sohu.inputmethod.sogou.xiaomi",
            "com.baidu.input_mi",
            "com.iflytek.inputmethod.miui",

            // Oyun Servisleri
            "com.xiaomi.glgm",
            "com.xiaomi.gamecenter.sdk.service",
            "com.nearme.gamecenter",

            // Ödeme
            "com.xiaomi.payment",
            "com.mipay.wallet.id",
            "com.mipay.wallet.in",

            // Pre-installed Bloatware
            "com.facebook.katana",
            "com.facebook.system",
            "com.facebook.appmanager",
            "com.facebook.services",
            "com.zhiliaoapp.musically",
            "com.netflix.mediaclient",
            "com.netflix.partner.activation",
            "com.alibaba.aliexpresshd",
            "com.amazon.appmanager",
            "com.ebay.mobile",
            "ru.yandex.searchplugin",
            "com.opera.browser",

            // OPPO/Realme
            "com.heytap.market",
            "com.heytap.browser",
            "com.heytap.music",
            "com.heytap.cloud",
            "com.coloros.gamespace",
            "com.coloros.weather2",
            "com.coloros.filemanager",

            // Vivo
            "com.vivo.browser",
            "com.vivo.appstore",
            "com.vivo.game",
            "com.vivo.weather",
            "com.vivo.music",
            "com.bbk.iqoo.logsystem",

            // Huawei
            "com.huawei.appmarket",
            "com.huawei.browser",
            "com.huawei.music",
            "com.huawei.videos",
            "com.huawei.gameassistant"));

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Koyu tema
        setTheme(android.R.style.Theme_Material);

        // UI oluştur
        createUI();

        // Preferences yükle
        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        loadBlockedPackages();

        // Master switch durumu
        boolean moduleEnabled = prefs.getBoolean(KEY_MODULE_ENABLED, true);
        masterSwitch.setChecked(moduleEnabled);

        // Bloatware tara
        scanBloatware();
    }

    private void createUI() {
        LinearLayout mainLayout = new LinearLayout(this);
        mainLayout.setOrientation(LinearLayout.VERTICAL);
        mainLayout.setBackgroundColor(Color.parseColor("#121212"));

        // Header
        headerLayout = new LinearLayout(this);
        headerLayout.setOrientation(LinearLayout.VERTICAL);
        headerLayout.setPadding(32, 32, 32, 16);
        headerLayout.setBackgroundColor(Color.parseColor("#1E1E1E"));

        // Başlık
        TextView titleText = new TextView(this);
        titleText.setText("🧹 CN Debloater");
        titleText.setTextSize(24);
        titleText.setTextColor(Color.parseColor("#FF6B6B"));
        headerLayout.addView(titleText);

        // Alt başlık
        TextView subtitleText = new TextView(this);
        subtitleText.setText("Çin ROM Bloatware Engelleyici");
        subtitleText.setTextSize(14);
        subtitleText.setTextColor(Color.parseColor("#888888"));
        subtitleText.setPadding(0, 8, 0, 16);
        headerLayout.addView(subtitleText);

        // Master switch
        LinearLayout switchLayout = new LinearLayout(this);
        switchLayout.setOrientation(LinearLayout.HORIZONTAL);
        switchLayout.setPadding(0, 16, 0, 16);

        TextView switchLabel = new TextView(this);
        switchLabel.setText("Modül Aktif");
        switchLabel.setTextSize(16);
        switchLabel.setTextColor(Color.WHITE);
        switchLabel.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1));
        switchLayout.addView(switchLabel);

        masterSwitch = new Switch(this);
        masterSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            prefs.edit().putBoolean(KEY_MODULE_ENABLED, isChecked).apply();
            updateUIState();
            String msg = isChecked ? "Modül aktif edildi" : "Modül devre dışı bırakıldı";
            Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
        });
        switchLayout.addView(masterSwitch);

        headerLayout.addView(switchLayout);

        // Stats
        statsText = new TextView(this);
        statsText.setTextSize(12);
        statsText.setTextColor(Color.parseColor("#4CAF50"));
        statsText.setPadding(0, 8, 0, 0);
        headerLayout.addView(statsText);

        mainLayout.addView(headerLayout);

        // Progress bar
        progressBar = new ProgressBar(this);
        progressBar.setIndeterminate(true);
        progressBar.setPadding(0, 32, 0, 32);
        mainLayout.addView(progressBar);

        // Status text
        statusText = new TextView(this);
        statusText.setText("Taranıyor...");
        statusText.setTextColor(Color.parseColor("#888888"));
        statusText.setTextSize(14);
        statusText.setPadding(32, 0, 32, 16);
        statusText.setVisibility(View.VISIBLE);
        mainLayout.addView(statusText);

        // ListView
        listView = new ListView(this);
        listView.setBackgroundColor(Color.parseColor("#121212"));
        listView.setDivider(null);
        listView.setDividerHeight(0);
        listView.setPadding(16, 0, 16, 0);
        mainLayout.addView(listView);

        setContentView(mainLayout);
    }

    private void loadBlockedPackages() {
        Set<String> saved = prefs.getStringSet(KEY_BLOCKED_PACKAGES, new HashSet<>());
        blockedPackages.clear();
        blockedPackages.addAll(saved);
    }

    private void saveBlockedPackages() {
        prefs.edit().putStringSet(KEY_BLOCKED_PACKAGES, blockedPackages).apply();
    }

    private void scanBloatware() {
        new AsyncTask<Void, Void, List<BloatwareItem>>() {
            @Override
            protected List<BloatwareItem> doInBackground(Void... voids) {
                List<BloatwareItem> items = new ArrayList<>();
                PackageManager pm = getPackageManager();

                for (String packageName : BLOATWARE_PACKAGES) {
                    try {
                        PackageInfo info = pm.getPackageInfo(packageName, 0);
                        ApplicationInfo appInfo = info.applicationInfo;

                        BloatwareItem item = new BloatwareItem();
                        item.packageName = packageName;
                        item.appName = pm.getApplicationLabel(appInfo).toString();
                        item.icon = appInfo.loadIcon(pm);
                        item.isSystem = (appInfo.flags & ApplicationInfo.FLAG_SYSTEM) != 0;
                        item.isBlocked = blockedPackages.contains(packageName);
                        item.category = categorizePackage(packageName);

                        items.add(item);
                    } catch (PackageManager.NameNotFoundException ignored) {
                        // Paket yüklü değil, atla
                    }
                }

                // Kategoriye göre sırala
                items.sort((a, b) -> a.category.compareTo(b.category));

                return items;
            }

            @Override
            protected void onPostExecute(List<BloatwareItem> items) {
                allBloatware.clear();
                allBloatware.addAll(items);
                filteredBloatware.clear();
                filteredBloatware.addAll(items);

                adapter = new BloatwareAdapter();
                listView.setAdapter(adapter);

                progressBar.setVisibility(View.GONE);
                statusText.setVisibility(View.GONE);

                updateStats();
            }
        }.execute();
    }

    private String categorizePackage(String packageName) {
        if (packageName.contains("analytics") || packageName.contains("msa") ||
                packageName.contains("bugreport") || packageName.contains("joyose")) {
            return "📊 Telemetri";
        } else if (packageName.contains("input") || packageName.contains("keyboard")) {
            return "⌨️ Klavye";
        } else if (packageName.contains("game")) {
            return "🎮 Oyun";
        } else if (packageName.contains("payment") || packageName.contains("wallet")) {
            return "💰 Ödeme";
        } else if (packageName.contains("facebook") || packageName.contains("netflix") ||
                packageName.contains("tiktok") || packageName.contains("amazon")) {
            return "📱 Pre-installed";
        } else if (packageName.contains("browser")) {
            return "🌐 Tarayıcı";
        } else if (packageName.contains("music") || packageName.contains("video") ||
                packageName.contains("player")) {
            return "🎵 Medya";
        } else {
            return "📦 Diğer";
        }
    }

    private void updateStats() {
        int total = allBloatware.size();
        int blocked = (int) allBloatware.stream().filter(b -> b.isBlocked).count();
        statsText.setText(String.format("📊 %d bloatware tespit edildi | 🚫 %d engellendi", total, blocked));
    }

    private void updateUIState() {
        boolean enabled = masterSwitch.isChecked();
        listView.setEnabled(enabled);
        listView.setAlpha(enabled ? 1.0f : 0.5f);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Tümünü engelle
        MenuItem blockAll = menu.add("Tümünü Engelle");
        blockAll.setOnMenuItemClickListener(item -> {
            for (BloatwareItem b : allBloatware) {
                b.isBlocked = true;
                blockedPackages.add(b.packageName);
            }
            saveBlockedPackages();
            adapter.notifyDataSetChanged();
            updateStats();
            Toast.makeText(this, "Tüm bloatware engellendi", Toast.LENGTH_SHORT).show();
            return true;
        });

        // Tümünü aç
        MenuItem unblockAll = menu.add("Tümünü Aç");
        unblockAll.setOnMenuItemClickListener(item -> {
            for (BloatwareItem b : allBloatware) {
                b.isBlocked = false;
                blockedPackages.remove(b.packageName);
            }
            saveBlockedPackages();
            adapter.notifyDataSetChanged();
            updateStats();
            Toast.makeText(this, "Tüm engeller kaldırıldı", Toast.LENGTH_SHORT).show();
            return true;
        });

        // Sadece telemetri
        MenuItem blockTelemetry = menu.add("Sadece Telemetri");
        blockTelemetry.setOnMenuItemClickListener(item -> {
            for (BloatwareItem b : allBloatware) {
                if (b.category.contains("Telemetri")) {
                    b.isBlocked = true;
                    blockedPackages.add(b.packageName);
                }
            }
            saveBlockedPackages();
            adapter.notifyDataSetChanged();
            updateStats();
            Toast.makeText(this, "Telemetri uygulamaları engellendi", Toast.LENGTH_SHORT).show();
            return true;
        });

        // Yeniden tara
        MenuItem rescan = menu.add("Yeniden Tara");
        rescan.setOnMenuItemClickListener(item -> {
            progressBar.setVisibility(View.VISIBLE);
            statusText.setVisibility(View.VISIBLE);
            statusText.setText("Yeniden taranıyor...");
            scanBloatware();
            return true;
        });

        return true;
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // ADAPTER
    // ═══════════════════════════════════════════════════════════════════════════

    private class BloatwareAdapter extends BaseAdapter {

        @Override
        public int getCount() {
            return filteredBloatware.size();
        }

        @Override
        public BloatwareItem getItem(int position) {
            return filteredBloatware.get(position);
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            BloatwareItem item = getItem(position);

            LinearLayout layout = new LinearLayout(MainActivity.this);
            layout.setOrientation(LinearLayout.HORIZONTAL);
            layout.setPadding(16, 16, 16, 16);
            layout.setBackgroundColor(Color.parseColor("#1E1E1E"));

            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT);
            params.setMargins(0, 8, 0, 8);
            layout.setLayoutParams(params);

            // Icon
            ImageView iconView = new ImageView(MainActivity.this);
            iconView.setImageDrawable(item.icon);
            LinearLayout.LayoutParams iconParams = new LinearLayout.LayoutParams(96, 96);
            iconParams.setMargins(0, 0, 16, 0);
            iconView.setLayoutParams(iconParams);
            layout.addView(iconView);

            // Info
            LinearLayout infoLayout = new LinearLayout(MainActivity.this);
            infoLayout.setOrientation(LinearLayout.VERTICAL);
            infoLayout.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1));

            TextView nameText = new TextView(MainActivity.this);
            nameText.setText(item.appName);
            nameText.setTextColor(Color.WHITE);
            nameText.setTextSize(16);
            infoLayout.addView(nameText);

            TextView packageText = new TextView(MainActivity.this);
            packageText.setText(item.packageName);
            packageText.setTextColor(Color.parseColor("#888888"));
            packageText.setTextSize(12);
            infoLayout.addView(packageText);

            TextView categoryText = new TextView(MainActivity.this);
            categoryText.setText(item.category + (item.isSystem ? " | Sistem" : ""));
            categoryText.setTextColor(Color.parseColor("#FF6B6B"));
            categoryText.setTextSize(11);
            infoLayout.addView(categoryText);

            layout.addView(infoLayout);

            // Checkbox
            CheckBox checkBox = new CheckBox(MainActivity.this);
            checkBox.setChecked(item.isBlocked);
            checkBox.setOnCheckedChangeListener((buttonView, isChecked) -> {
                item.isBlocked = isChecked;
                if (isChecked) {
                    blockedPackages.add(item.packageName);
                } else {
                    blockedPackages.remove(item.packageName);
                }
                saveBlockedPackages();
                updateStats();
            });
            layout.addView(checkBox);

            return layout;
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // DATA CLASS
    // ═══════════════════════════════════════════════════════════════════════════

    private static class BloatwareItem {
        String packageName;
        String appName;
        android.graphics.drawable.Drawable icon;
        boolean isSystem;
        boolean isBlocked;
        String category;
    }
}
