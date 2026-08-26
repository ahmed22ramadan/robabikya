import 'package:flutter/material.dart';

/// فئة من فئات المخلفات القابلة لإعادة التدوير.
/// unit: 'weight' (بالكيلو) أو 'count' (بالعدد).
class ScrapCategory {
  final String id;
  final String nameAr;
  final String nameEn;
  final String unit;
  final IconData icon;

  const ScrapCategory({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    required this.unit,
    required this.icon,
  });
}

const List<ScrapCategory> scrapCategories = [
  ScrapCategory(id: 'cans', nameAr: 'عبوات الكانز', nameEn: 'Drink cans', unit: 'count', icon: Icons.local_drink),
  ScrapCategory(id: 'aluminum_scrap', nameAr: 'ألومنيوم اسكراب', nameEn: 'Aluminum scrap', unit: 'weight', icon: Icons.recycling),
  ScrapCategory(id: 'foil', nameAr: 'ورق فويل', nameEn: 'Foil paper', unit: 'weight', icon: Icons.layers),
  ScrapCategory(id: 'aluminum_trays', nameAr: 'أطباق ألومنيوم', nameEn: 'Aluminum trays', unit: 'count', icon: Icons.album),
  ScrapCategory(id: 'plastic', nameAr: 'بلاستيك', nameEn: 'Plastic', unit: 'weight', icon: Icons.shopping_bag),
  ScrapCategory(id: 'tires', nameAr: 'كاوتش العربية', nameEn: 'Car tires', unit: 'count', icon: Icons.directions_car),
  ScrapCategory(id: 'iron_scrap', nameAr: 'خردة حديد', nameEn: 'Iron scrap', unit: 'weight', icon: Icons.build),
];
