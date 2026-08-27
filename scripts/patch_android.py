"""
يتنفذ تلقائيًا أثناء GitHub Actions بعد أمر `flutter create`.
بيعدّل مشروع أندرويد المُولَّد عشان:
1. يضيف صلاحيات الإنترنت والكاميرا والموقع.
2. يخلي اسم التطبيق "روبابيكيا" بالعربي.
3. يضيف Google Services Gradle plugin عشان Firebase يشتغل.

ملحوظة: من Flutter 3.29 وبعدها، ملفات Gradle بقت افتراضيًا بصيغة
Kotlin DSL (.gradle.kts) بدل الصيغة القديمة (.gradle). السكريبت ده
بيتعرف تلقائيًا على أي صيغة موجودة ويتعامل معاها صح.
"""
import re
import pathlib

# 1) AndroidManifest.xml: الصلاحيات + الاسم بالعربي (XML، مش بيتأثر بصيغة Gradle)
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

# 2) android/app/build.gradle(.kts): إضافة Google Services plugin — يدعم الصيغتين
app_gradle_kts = pathlib.Path("android/app/build.gradle.kts")
app_gradle_groovy = pathlib.Path("android/app/build.gradle")

if app_gradle_kts.exists():
    content = app_gradle_kts.read_text(encoding="utf-8")
    if "com.google.gms.google-services" not in content:
        content = content.replace(
            'id("kotlin-android")',
            'id("kotlin-android")\n    id("com.google.gms.google-services")',
            1,
        )
    app_gradle_kts.write_text(content, encoding="utf-8")
elif app_gradle_groovy.exists():
    content = app_gradle_groovy.read_text(encoding="utf-8")
    if "com.google.gms.google-services" not in content:
        content = content.replace(
            'id "kotlin-android"',
            'id "kotlin-android"\n    id "com.google.gms.google-services"',
            1,
        )
    app_gradle_groovy.write_text(content, encoding="utf-8")
else:
    raise FileNotFoundError(
        "مفيش android/app/build.gradle ولا build.gradle.kts — يبدو إن أمر flutter create فشل قبل الخطوة دي."
    )

# 3) android/settings.gradle(.kts): تسجيل نسخة الـ plugin — يدعم الصيغتين
settings_kts = pathlib.Path("android/settings.gradle.kts")
settings_groovy = pathlib.Path("android/settings.gradle")

if settings_kts.exists():
    content = settings_kts.read_text(encoding="utf-8")
    if "com.google.gms.google-services" not in content:
        content = re.sub(
            r'(id\("com\.android\.application"\)\s+version\s+"[^"]+"\s+apply\s+false)',
            r'\1\n    id("com.google.gms.google-services") version "4.4.2" apply false',
            content,
            count=1,
        )
    settings_kts.write_text(content, encoding="utf-8")
elif settings_groovy.exists():
    content = settings_groovy.read_text(encoding="utf-8")
    if "com.google.gms.google-services" not in content:
        content = re.sub(
            r'(id "com\.android\.application" version "[^"]+" apply false)',
            r'\1\n    id "com.google.gms.google-services" version "4.4.2" apply false',
            content,
            count=1,
        )
    settings_groovy.write_text(content, encoding="utf-8")
else:
    raise FileNotFoundError("مفيش android/settings.gradle ولا settings.gradle.kts.")

print("تم تعديل مشروع أندرويد بنجاح.")
