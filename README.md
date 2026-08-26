# روبابيكيا (Robabikya)

تطبيق Flutter متصل بـ Firebase. النسخة الحالية فيها:
- تسجيل الدخول/إنشاء حساب (إيميل وباسورد + Google)
- شاشة رئيسية بقائمة "طلباتي" (متصلة بـ Firestore فعليًا)
- شاشة طلب تحصيل جديد بأربع خطوات (الفئة والكمية، العنوان والموبايل والخريطة، الميعاد، الصورة والملاحظات) — بتحفظ الطلب في Firestore وترفع الصورة على Firebase Storage

## ملاحظة مهمة
المشروع ده متبني بحيث GitHub Actions هو اللي "يخلق" مجلد الأندرويد ويبني الـ APK تلقائيًا — مش محتاج تنزّل Flutter ولا Android Studio على جهازك خالص عشان تجيب الـ APK.

---

## الخطوات قبل أول تشغيل

### 1. جهّز مشروع Firebase
- ادخل [Firebase Console](https://console.firebase.google.com) على نفس المشروع اللي عملته.
- من "Project settings" ضيف تطبيق أندرويد جديد، واستخدم بالظبط اسم الحزمة ده:
  ```
  com.robabikya.app
  ```
- حمّل ملف `google-services.json` اللي هيظهرلك، واستبدل بيه الملف الموجود في جذر المشروع (اللي فيه بيانات وهمية حاليًا).

### 2. فعّل طرق الدخول
من قسم **Authentication → Sign-in method** في Firebase، فعّل:
- Email/Password
- Google

### 3. لازم لدخول Google تحديدًا: أضف بصمة SHA-1
تسجيل الدخول بجوجل مش هيشتغل من غيرها. على جهازك، شغّل:

```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

(لو مش عندك `~/.android/debug.keystore`، شغّل أي أمر `flutter build` أو `flutter run` مرة واحدة الأول عشان يتولّد تلقائي، أو ثبّت Android Studio اللي بيعمله تلقائي.)

انسخ قيمة **SHA1** اللي هتظهر، وضيفها في Firebase Console: **Project settings → معلومات التطبيق (Android) → Add fingerprint**.

### 4. جهّز Firestore (لتخزين الطلبات)
من **Firestore Database** في Firebase، اعمل "Create database" (اختار "Start in test mode" مبدئيًا).

غيّر قواعد Firestore (تبويب Rules) عشان كل مستخدم يقدر يقرا/يكتب طلباته هو بس:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /orders/{orderId} {
      allow read, update, delete: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.userId;
    }
  }
}
```

### 5. جهّز Cloudinary (لتخزين صور الطلبات — مجاني بالكامل بدون بطاقة)
Firebase Storage بقى محتاج بطاقة (خطة Blaze)، فاستخدمنا بديل مجاني 100% منه.

1. اعمل حساب مجاني على [cloudinary.com](https://cloudinary.com) (بإيميل أو جوجل، من غير أي بطاقة).
2. من الـ Dashboard الرئيسي، انسخ قيمة **Cloud name**.
3. روح لـ **Settings → Upload → Upload presets → Add upload preset**، واختار **Signing Mode: Unsigned**، واحفظ، وانسخ اسم الـ preset.
4. افتح ملف `lib/config/cloudinary_config.dart` في المشروع، واستبدل القيمتين:
   ```dart
   static const String cloudName = 'hlgpuhz7';
   static const String uploadPreset = 'REPLACE_WITH_YOUR_UNSIGNED_PRESET';
   ```

### 6. أول مرة تفتح صفحة "طلباتي"
لو ظهرلك خطأ نصه بيتكلم عن "index" جوه التطبيق، ده طبيعي أول مرة — Firestore بيحتاج فهرس (index) عشان يرتب الطلبات. الخطأ نفسه بيجيب معاه رابط، افتحه في المتصفح ودوس "Create Index"، واستنى دقيقة أو اتنين، وبعدها هيشتغل عادي.

---

## إزاي تجيب الـ APK (مجانًا بالكامل)

1. اعمل حساب/repo جديد على [GitHub](https://github.com) لو معندكش.
2. من مجلد المشروع، شغّل:
   ```bash
   git init
   git add .
   git commit -m "أول نسخة من روبابيكيا"
   git branch -M main
   git remote add origin https://github.com/USERNAME/robabikya.git
   git push -u origin main
   ```
3. روح لتبويب **Actions** في الـ repo بتاعك على GitHub، هتلاقي "Build APK" شغالة تلقائيًا (بتاخد حوالي 5-10 دقايق أول مرة).
4. لما تخلص، دوس عليها، وهتلاقي في الأسفل ملف باسم **robabikya-apk** — حمّله (هيجيلك كـ zip فيه الـ APK جواه).
5. فك الضغط، وابعت ملف `app-release.apk` لموبايل أندرويد (واتساب/درايف/كابل)، وثبّته (لازم تفعّل "السماح بتثبيت من مصادر غير معروفة" من إعدادات الموبايل).

---

## لو البناء فشل على GitHub Actions
ابعتلي رسالة الخطأ اللي هتظهر في الـ Actions log، وهساعدك تصلّحها فورًا. أشهر مشكلة محتملة: لو ظهر خطأ متعلق بـ `minSdkVersion`، افتح `android/app/build.gradle` (بعد ما يتولّد) وغيّر السطر الخاص بيه لـ `minSdk 23`.

## ملاحظات تصميم
- لسه مفيش أيقونة Google الرسمية على زرار "الدخول بحساب Google" — استخدمت أيقونة عامة بديلة مؤقتًا. لو عايز الشعار الرسمي، ممكن تنزّله من [موارد Google الرسمية لعلامة Sign-In](https://developers.google.com/identity/branding-guidelines) وأضيفه كصورة.
- خط عربي مخصص (زي Cairo) هيضيف شكل أحلى لاحقًا — نقدر نضيفه بسهولة بعد كده.

## الخطوة الجاية
شاشة لوحة تحكم بسيطة (Admin) تشوف بيها الطلبات الواردة من كل العملاء وتغيّر حالتها (قيد الانتظار / تم القبول / تم التحصيل)، ولو حبيت، تحسينات زي: خط عربي مخصص، وربط رقم الموبايل بإشعارات فورية (Push Notifications) لما حد يقبل الطلب.
