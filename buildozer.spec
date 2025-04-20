[app]
title = GroceryApp
package.name = groceryapp
package.domain = org.grocery.app
source.dir = .
source.include_exts = py,json
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
osx.kivy_version = 2.1.0

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
presplash = 
icon.filename = 
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 23b
android.arch = armeabi-v7a
android.gradle_dependencies = 
android.gradle_plugins = 

[app.android.ndk]
# Optional: speeds up builds after first one
# android.ndk_path = /home/YOUR_USERNAME/.buildozer/android/platform/android-ndk-r23b

[app.android.keystore]
# Leave blank for debug mode
