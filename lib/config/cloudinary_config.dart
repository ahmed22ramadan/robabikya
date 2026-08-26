/// بيانات حساب Cloudinary (تخزين صور مجاني بدون بطاقة).
///
/// إزاي تجيب القيم دي:
/// 1. اعمل حساب مجاني على https://cloudinary.com (بالإيميل أو جوجل، من غير بطاقة).
/// 2. من الـ Dashboard الرئيسي، انسخ "Cloud name" وحطه في cloudName.
/// 3. روح لـ Settings → Upload → Upload presets → Add upload preset.
///    - Signing Mode: اختار "Unsigned" (مهم جدًا).
///    - احفظ، وانسخ اسم الـ preset وحطه في uploadPreset.
class CloudinaryConfig {
  static const String cloudName = 'hlgpuhz7';
  static const String uploadPreset = 'llldq18y';
}
