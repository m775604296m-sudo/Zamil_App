[app]
# (str) Title of your application
title = Zamil App

# (str) Package name
package.name = zamilapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test.zamil

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let include_exts be empty if you want all)
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3

# (str) Application versioning
version = 0.1

# (list) Application requirements
# تمت إضافة كافة المكتبات المستخدمة في ملفاتك (home_screen.py, main.py, splash_screen.py)
requirements = python3,kivy,kivymd,arabic-reshaper,python-bidi,pillow

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android NDK API to use
android.ndk_api = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) Android archs
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
