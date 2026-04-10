[app]
title = Zamil Ibrahim Al-Malsi
package.name = zamil_app
package.domain = org.alslbh
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0

# تم إضافة pillow وتحديد إصدارات مستقرة لتجنب تعارض التجميع
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, arabic_reshaper, python-bidi

presplash.filename = %(source.dir)s/avatar.png
icon.filename = %(source.dir)s/avatar.png

orientation = portrait
fullscreen = 0

# صلاحيات الوسائط لأندرويد 13 (API 33)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_AUDIO

android.api = 33
android.minapi = 21
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
