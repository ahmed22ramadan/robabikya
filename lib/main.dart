import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';

import 'theme/app_theme.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const RobabikyaApp());
}

class RobabikyaApp extends StatefulWidget {
  const RobabikyaApp({super.key});

  @override
  State<RobabikyaApp> createState() => _RobabikyaAppState();
}

class _RobabikyaAppState extends State<RobabikyaApp> {
  // اللغة الافتراضية عربي؛ العميل يقدر يغيّرها من الزرار في شاشة الدخول/الرئيسية.
  String _lang = 'ar';

  void _toggleLang() {
    setState(() => _lang = _lang == 'ar' ? 'en' : 'ar');
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: _lang == 'ar' ? TextDirection.rtl : TextDirection.ltr,
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'روبابيكيا',
        theme: AppTheme.lightTheme,
        home: StreamBuilder<User?>(
          stream: FirebaseAuth.instance.authStateChanges(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Scaffold(body: Center(child: CircularProgressIndicator()));
            }
            if (snapshot.hasData) {
              return HomeScreen(lang: _lang, onToggleLang: _toggleLang);
            }
            return LoginScreen(lang: _lang, onToggleLang: _toggleLang);
          },
        ),
      ),
    );
  }
}
