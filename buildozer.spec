[app]

# (str) Title of your application
title = Zamil Ibrahim Al-Malsi

# (str) Package name
package.name = zamilapp

# (str) Package domain
package.domain = org.alslbh

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (تم إضافة mp3 هنا)
source.include_exts = py,png,jpg,kv,atlas,ttf,json,mp3

# (str) Application versioning
version = 0.1

# (list) Application requirements (تم إضافة pillow و تحديد إصدار Cython لاحقاً)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,arabic_reshaper,python-bidi,pillow

# (str) Presplash and Icon
# تأكد أن المسارات مطابقة لما هو موجود في مجلد assets لديك
presplash.filename = %(source.dir)s/assets/images/avatar.png
icon.filename = %(source.dir)s/assets/images/avatar.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API support
android.minapi = 21

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) automatically accept SDK license
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
