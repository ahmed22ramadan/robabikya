"""
يتنفذ تلقائيًا أثناء GitHub Actions بعد أمر `flutter create`.
بيعدّل مشروع أندرويد المُولَّد عشان:
1. يضيف صلاحيات الإنترنت والكاميرا والموقع.
2. يخلي اسم التطبيق "روبابيكيا" بالعربي.
3. يضيف Google Services Gradle plugin عشان Firebase يشتغل.
"""
import re
import pathlib

# 1) AndroidManifest.xml: الصلاحيات + الاسم بالعربي
manifest_path = pathlib.Path("android/app/src/main/AndroidManifest.xml")
manifest = manifest_path.read_text(encoding="utf-8")

extra_permissions = (
    '\n    <uses-permission android:name="android.permission.INTERNET"/>'
    '\n    <uses-permission android:name="android.permission.CAMERA"/>'
    '\n    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>'
    '\n    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>'
    '\n    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>'
    '\n    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32"/>'
)
if "android.permission.INTERNET" not in manifest:
    manifest = re.sub(r"(<manifest[^>]*>)", r"\1" + extra_permissions, manifest, count=1)

manifest = re.sub(r'android:label="[^"]*"', 'android:label="روبابيكيا"', manifest)
manifest_path.write_text(manifest, encoding="utf-8")

# 2) android/app/build.gradle: إضافة Google Services plugin
app_gradle_path = pathlib.Path("android/app/build.gradle")
app_gradle = app_gradle_path.read_text(encoding="utf-8")
if "com.google.gms.google-services" not in app_gradle:
    app_gradle = app_gradle.replace(
        'id "kotlin-android"',
        'id "kotlin-android"\n    id "com.google.gms.google-services"',
        1,
    )
app_gradle_path.write_text(app_gradle, encoding="utf-8")

# 3) android/settings.gradle: تسجيل نسخة الـ plugin
settings_path = pathlib.Path("android/settings.gradle")
settings = settings_path.read_text(encoding="utf-8")
if "com.google.gms.google-services" not in settings:
    settings = re.sub(
        r'(id "com\.android\.application" version "[^"]+" apply false)',
        r'\1\n    id "com.google.gms.google-services" version "4.4.2" apply false',
        settings,
        count=1,
    )
settings_path.write_text(settings, encoding="utf-8")

print("تم تعديل مشروع أندرويد بنجاح.")
