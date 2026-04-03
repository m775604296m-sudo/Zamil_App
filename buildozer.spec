[app]

# (str) Title of your application
title = Zamil Ibrahim Al-Malsi

# (str) Package name
package.name = zamil_app

# (str) Package domain (needed for android/ios packaging)
package.domain = org.alslbh

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Application versioning (هذا السطر الذي كان ينقصك)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,arabic_reshaper,python-bidi

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/images/avatar.png

# (str) Icon of the application
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

# (int) Log level (2 لإظهار كافة التفاصيل)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
