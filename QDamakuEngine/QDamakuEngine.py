import os
import platform
import json
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
logging.basicConfig(filename="QDE.log",filemode="w",format="%(asctime)s-%(levelname)s-%(message)s",datefmt="%Y-%m-%d %H:%M:%S")
if os.path.exists("config.json")==False:
	with open(file="config.json",mode="w",encoding="utf-8") as default_conf_witer:
		default_conf_dic={"lang":"zh_CN"}
		json.dump(obj=default_conf_dic,fp=default_conf_witer,indent=4,sort_keys=True)
	logging.warning("No config file found, creating default config file...")
with open(file="config.json",mode="r",encoding="utf-8") as config_reader:
	conf_dic=json.load(config_reader)
lang_=str(conf_dic["lang"])
with open(file="lang/"+lang_+"/"+lang_+".json",mode="r",encoding="utf-8") as lang_loader:
	langdic=json.load(lang_loader)
logging.info(lang.info.loaded_conf)
# 读入语言数据
class lang:
	qt_widget_translation="lang/"+lang_+"/widgets_"+lang_+".qm"
	qt_main_translation="lang/"+lang_+"qt_"+lang_+".qm"
	class error:
		platform_error=langdic["error"]["platform_error"]
	class info:
		loaded_conf=langdic["info"]["loaded_conf"]
	class warning:
		platform_warning=langdic["warning"]["platform_warning"]
	class notification:
		title=langdic["ui"]["notification_title"]
		msg=langdic["ui"]["notification_msg"]

try:
	sys_ver=platform.win32_ver()[0]
except:
	logging.error(lang.error.platform_error)
	exit()
if sys_ver=="10":
	import win10toast
	is_win10=True
else:
	is_win10=False
	logging.warning(lang.warning.platform_warning)
class TrayIcon(QSystemTrayIcon):
	def __init__(self):
		super(TrayIcon,self).__init__()
		self.menu=QMenu()
if is_win10==True:
	toaster=win10toast.ToastNotifier()
	# 图标作者:https://github.com/nullice/NViconsLib_Silhouette
	toaster.show_toast(title=lang.notification.title,msg=lang.notification.msg,icon_path="resources/program.ico",duration=10,threaded=True)
else:



