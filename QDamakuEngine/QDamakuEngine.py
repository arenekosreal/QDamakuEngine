import os
import platform
import json
import logging
logging.basicConfig(filename="QDE.log",filemode="w",format="%(asctime)s-%(levelname)s-%(message)s",datefmt="%Y-%m-%d %H:%M:%S")
if os.path.exists("config.json")==False:
	with open(file="config.json",mode="w",encoding="utf-8") as default_conf_witer:
		default_conf_dic={"lang":"zh_CN"}
		json.dump(obj=default_conf_dic,fp=default_conf_witer,indent=4,sort_keys=True)
	logging.warning("No config file found, creating default config file...")
with open(file="config.json",mode="r",encoding="utf-8") as config_reader:
	conf_dic=json.load(config_reader)
lang=str(conf_dic["lang"])
with open(file="lang/"+lang+"/"+lang+".json",mode="r",encoding="utf-8") as lang_loader:
	langdic=json.load(lang_loader)
class lang:
	class error:
		platform_error=langdic["platform_error"]

try:
	sys_ver=platform.win32_ver()[0]
except:
	logging.error(lang.error.platform_error)
	exit()
if sys_ver=="10":
	import win10toast

