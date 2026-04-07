[app]
title = Security Monitor
package.name = securitymonitor
package.domain = com.aryanchauhan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 0.1
requirements = python3,flask,kivy,werkzeug,jinja2,markupsafe,itsdangerous,click,blinker
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET, READ_LOGS
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 0
