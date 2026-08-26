import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../config/cloudinary_config.dart';

/// رفع صورة على Cloudinary (مجاني بدون بطاقة) وإرجاع رابطها النهائي.
/// بيرجع null لو فشل الرفع، عشان الشاشة تقدر تكمل حفظ الطلب من غير صورة
/// بدل ما توقف العميل بالكامل.
class CloudinaryService {
  static Future<String?> uploadImage(File imageFile) async {
    try {
      final uri = Uri.parse(
        'https://api.cloudinary.com/v1_1/${CloudinaryConfig.cloudName}/image/upload',
      );
      final request = http.MultipartRequest('POST', uri)
        ..fields['upload_preset'] = CloudinaryConfig.uploadPreset
        ..files.add(await http.MultipartFile.fromPath('file', imageFile.path));

      final response = await request.send();
      if (response.statusCode != 200) return null;

      final body = await response.stream.bytesToString();
      final data = jsonDecode(body) as Map<String, dynamic>;
      return data['secure_url'] as String?;
    } catch (_) {
      return null;
    }
  }
}
