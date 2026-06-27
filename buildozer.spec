[app]
title = Zamil App
package.name = zamilapp
package.domain = org.test.zamil
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3
version = 0.1
requirements = python3,kivy,kivymd,arabic-reshaper,python-bidi,pillow
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
