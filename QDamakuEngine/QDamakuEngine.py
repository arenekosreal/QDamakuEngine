import os
import sys
import platform
import json
import logging
import socket
import random
import time
import ssl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
if sys.argv[1].upper()=="--DEBUG":
	is_debug=True
else:
	is_debug=False
if is_debug==False:
	logging.basicConfig(filename="QDE.log",filemode="w",format="%(asctime)s %(levelname)s:%(message)s",datefmt="%Y-%m-%d %H:%M:%S",level=logging.INFO)
else:
	logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s",datefmt="%Y-%m-%d %H:%M:%S",level=logging.DEBUG)
if os.path.exists("config.json")==False:
	with open(file="config.json",mode="w",encoding="utf-8") as default_conf_witer:
		default_conf_dic={"lang":"zh_CN","font": "Microsoft YaHei","font_size": 15,"font_speed": 100,"font_weight": 50,"font_italic": 0,"font_bold": 0,"color_alpha":1.0,"port": 2333,"address": "localhost","max_connection":5}
		json.dump(obj=default_conf_dic,fp=default_conf_witer,indent=4,sort_keys=True)
	logging.warning("No config file found, creating default config file...")
with open(file="config.json",mode="r",encoding="utf-8") as config_reader:
	conf_dic=json.load(config_reader)
class setting:
	lang_=str(conf_dic["lang"])
	font=str(conf_dic["font"])
	font_size=int(conf_dic["font_size"])
	font_weight=int(conf_dic["font_weight"])
	font_italic=bool(conf_dic["font_italic"])
	font_bold=bool(conf_dic["font_bold"])
	font_speed=int(conf_dic["font_speed"])
	color_alpha=float(conf_dic["color_alpha"])
	port=int(conf_dic["port"])
	address=str(conf_dic["address"])
	max_connection=int(conf_dic["max_connection"])
	damaku_font=QFont(font,pointSize=font_size,weight=font_weight,italic=font_italic)
	damaku_font.setBold(font_bold)
	def update_setting(self,conf_dic:dict):
		new_lang=str(conf_dic["lang"])
		new_font=str(conf_dic["font"])
		new_font_size=str(conf_dic["font_size"])
		new_font_speed=int(conf_dic["font_speed"])
		new_font_weight=int(conf_dic["font_weight"])
		new_font_italic=bool(conf_dic["font_italic"])
		new_font_bold=bool(conf_dic["font_bold"])
		setting.damaku_font=QFont(new_font,pointSize=new_font_size,weight=new_font_weight,italic=new_font_italic)
		setting.damaku_font.setBold(new_font_bold)
		qt_widget_translation="lang/"+setting.lang_+"/widgets_"+setting.lang_+".qm"
		qt_main_translation="lang/"+setting.lang_+"qt_"+setting.lang_+".qm"
		lang.widget_translator=QTranslator()
		lang.widget_translator.load(qt_widget_translation)
		lang.main_translator=QTranslator()
		lang.main_translator.load(qt_main_translation)
		QApplication.processEvents()
with open(file="lang/"+setting.lang_+"/"+setting.lang_+".json",mode="r",encoding="utf-8") as lang_loader:
	langdic=json.load(lang_loader)
# 读入语言数据
class lang:
	qt_widget_translation="lang/"+setting.lang_+"/widgets_"+setting.lang_+".qm"
	qt_main_translation="lang/"+setting.lang_+"qt_"+setting.lang_+".qm"
	widget_translator=QTranslator()
	widget_translator.load(qt_widget_translation)
	main_translator=QTranslator()
	main_translator.load(qt_main_translation)
	class error:
		platform_error=str(langdic["error"]["platform_error"])
		failed_start_thread=str(langdic["error"]["failed_start_thread"])
		failed_listen_port=str(langdic["error"]["failed_listen_port"])
		timeout=str(langdic["error"]["timeout"])
		recived_close_connection=str(langdic["error"]["recived_close_connection"])
		io_error=str(langdic["error"]["io_error"])
	class info:
		loaded_conf=str(langdic["info"]["loaded_conf"])
		current_sys=str(langdic["info"]["current_sys"])
		sended_notification=str(langdic["info"]["sended_notification"])
		shown_tray=str(langdic["info"]["shown_tray"])
		shown_window=str(langdic["info"]["shown_window"])
		shown_damaku=str(langdic["info"]["shown_damaku"])
		closed_tray=str(langdic["info"]["closed_tray"])
		successfully_start_thread=str(langdic["info"]["successfully_start_thread"])
		started_thread=str(langdic["info"]["started_thread"])
		finished_thread=str(langdic["info"]["finished_thread"])
		successfully_listen_port=str(langdic["info"]["successfully_listen_port"])
		close_connection=str(langdic["info"]["close_connection"])
		loaded_cert=str(langdic["info"]["loaded_cert"])
		connected_client=str(langdic["info"]["connected_client"])
		started_sock_thread=str(langdic["info"]["started_sock_thread"])
		generated_orig_label=str(langdic["info"]["generated_orig_label"])
		generated_final_label=str(langdic["info"]["generated_final_label"])
		recived_data=str(langdic["info"]["recived_data"])
	class warning:
		platform_warning=str(langdic["warning"]["platform_warning"])
		aborted_connection=str(langdic["warning"]["aborted_connection"])
	class debug:
		created_action=str(langdic["debug"]["created_action"])
		finished_creating_menu=str(langdic["debug"]["created_menu"])
		enabled_toast=str(langdic["debug"]["enabled_toast"])
		used_color=str(langdic["debug"]["used_color"])
	class notification:
		title=str(langdic["ui"]["notification_title"])
		msg=str(langdic["ui"]["notification_msg"])
		exit_menu=str(langdic["ui"]["exit_menu"])
		setting_menu=str(langdic["ui"]["setting_menu"])
		tooltip=str(langdic["ui"]["tooltip"])
	class setting_ui:
		yes=str(langdic["ui"]["yes"])
		no=str(langdic["ui"]["no"])
		save=str(langdic["ui"]["save"])
		cancel=str(langdic["ui"]["cancel"])
		restore=str(langdic["ui"]["restore"])
		title=str(langdic["ui"]["setting_title"])
		lang_label=str(langdic["ui"]["setting_lang_label"])
		font_label=str(langdic["ui"]["setting_font_label"])
		font_size=str(langdic["ui"]["setting_font_size"])
		font_speed=str(langdic["ui"]["setting_font_speed"])
		font_weight=str(langdic["ui"]["setting_font_weight"])
		font_italic=str(langdic["ui"]["setting_font_italic"])
		font_bold=str(langdic["ui"]["setting_font_bold"])
		address_label=str(langdic["ui"]["setting_address"])
		port_label=str(langdic["ui"]["setting_port"])
		max_connection=str(langdic["ui"]["setting_max_connection"])
		alpha_label=str(langdic["ui"]["alpha_label"])
logging.info(lang.info.loaded_conf)

try:
	sys_ver=platform.win32_ver()[0]
except:
	logging.error(lang.error.platform_error)
	exit()
if sys_ver=="10" or sys_ver=="8":
	import win10toast
	is_win10=True
	logging.debug(lang.debug.enabled_toast)
else:
	is_win10=False
	logging.warning(lang.warning.platform_warning)
logging.info(lang.info.current_sys+sys_ver)
class SettingDialog(QDialog):
	def __init__(self):
		super(SettingDialog,self).__init__()
		font=QFont("Microsoft YaHei",15)
		self.setWindowIcon(QIcon("resources/program.ico"))
		self.setWindowTitle("")
		self.setWindowOpacity(0.95)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlag(Qt.FramelessWindowHint)
		setting_title_label=QLabel(lang.setting_ui.title)
		setting_title_label.setFont(font)
		setting_title_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		setting_title_label.setAlignment(Qt.AlignCenter)
		lang_label=QLabel(lang.setting_ui.lang_label)
		lang_label.setFont(font)
		lang_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.lang_chooser=QComboBox()
		lang_list,lang_files=self.get_lang()
		self.lang_chooser.setFont(font)
		self.lang_chooser.setStyleSheet("QComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.lang_chooser.addItems(lang_list)
		self.lang_chooser.setCurrentIndex(self.lang_code_list.index(setting.lang_))
		font_label=QLabel(lang.setting_ui.font_label)
		font_label.setFont(font)
		font_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_chooser=QFontComboBox()
		self.font_chooser.setFont(font)
		self.font_chooser.setStyleSheet("QFontComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QFontComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QFontComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QFontComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.font_chooser.setFontFilters(QFontComboBox.AllFonts)
		self.font_chooser.setCurrentFont(setting.damaku_font)
		font_size_label=QLabel(lang.setting_ui.font_size)
		font_size_label.setFont(font)
		font_size_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_size_text=QLineEdit(str(setting.font_size))
		self.font_size_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		self.font_size_text.setAlignment(Qt.AlignCenter)
		self.font_size_text.setFont(font)
		font_weight_label=QLabel(lang.setting_ui.font_weight)
		font_weight_label.setFont(font)
		font_weight_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_weight_text=QLineEdit(str(setting.font_weight))
		self.font_weight_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		self.font_weight_text.setAlignment(Qt.AlignCenter)
		self.font_weight_text.setFont(font)
		font_speed_label=QLabel(lang.setting_ui.font_speed)
		font_speed_label.setFont(font)
		font_speed_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_speed_text=QLineEdit(str(setting.font_speed))
		self.font_speed_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		self.font_speed_text.setAlignment(Qt.AlignCenter)
		self.font_speed_text.setFont(font)
		font_italic_label=QLabel(lang.setting_ui.font_italic)
		font_italic_label.setFont(font)
		font_italic_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_italic_text=QComboBox()
		self.font_italic_text.setStyleSheet("QComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.font_italic_text.addItems([lang.setting_ui.yes,lang.setting_ui.no])
		if setting.font_italic==True:
			self.font_italic_text.setCurrentIndex(0)
		else:
			self.font_italic_text.setCurrentIndex(1)
		self.font_italic_text.setFont(font)
		font_bold_label=QLabel(lang.setting_ui.font_bold)
		font_bold_label.setFont(font)
		font_bold_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.font_bold_text=QComboBox()
		self.font_bold_text.setStyleSheet("QComboBox{border:1px solid gray;width:60px;border-radius:10px;padding:2px 4px;background:#00CED1;}QComboBox:drop-down{subcontrol-origin:padding;subcontrol-position:top right;border-top-right-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-bottom-left-radius:10px;}QComboBox:down-arrow{image:url(resources/downarrow.png);width:15px;height:15px;}QComboBox:down-arrow:on{image:url(resources/uparrow.png);}")
		self.font_bold_text.addItems([lang.setting_ui.yes,lang.setting_ui.no])
		if setting.font_bold==True:
			self.font_bold_text.setCurrentIndex(0)
		else:
			self.font_bold_text.setCurrentIndex(1)
		self.font_bold_text.setFont(font)
		address_label=QLabel(lang.setting_ui.address_label)
		address_label.setFont(font)
		address_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.address_text=QLineEdit(str(setting.address))
		self.address_text.setFont(font)
		self.address_text.setAlignment(Qt.AlignCenter)
		self.address_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		port_label=QLabel(lang.setting_ui.port_label)
		port_label.setFont(font)
		port_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.port_text=QLineEdit(str(setting.port))
		self.port_text.setFont(font)
		self.port_text.setAlignment(Qt.AlignCenter)
		self.port_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		max_connection_label=QLabel(lang.setting_ui.max_connection)
		max_connection_label.setFont(font)
		max_connection_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.max_connection_text=QLineEdit(str(setting.max_connection))
		self.max_connection_text.setFont(font)
		self.max_connection_text.setAlignment(Qt.AlignCenter)
		self.max_connection_text.setStyleSheet("QLineEdit{border:1px solid gray;width:30px;border-radius:10px;padding:2px 4px;}")
		alpha_label=QLabel(lang.setting_ui.alpha_label)
		alpha_label.setFont(font)
		alpha_label.setStyleSheet("QLabel{border:1px solid gray;width:15px;border-radius:10px;padding:2px 4px;background:#00CED1;}")
		self.alpha_text=EnhancedSlider()
		self.alpha_text.setOrientation(Qt.Horizontal)
		self.alpha_text.setFont(font)
		self.alpha_text.setStyleSheet("QSlider{background-color:transparent;border:1px solid gray;width:5px;border-radius:10px;padding:2px 4px;}QSlider::handle:horizontal{border:1px;border-image:url(resources/slider.png);width:30px;}QSlider::add-page:horizontal{background:#00CED1;}QSlider::sub-page:horizontal{background:white;}")
		self.alpha_text.setMinimum(0)
		self.alpha_text.setMaximum(100)
		self.alpha_text.setValue(int(setting.color_alpha*100))
		self.alpha_text.setSingleStep(10)
		self.alpha_text.setTickPosition(QSlider.TicksAbove)
		save_button=QPushButton(lang.setting_ui.save)
		save_button.setFont(font)
		save_button.setStyleSheet("QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}")
		save_button.clicked.connect(self.save_setting)
		cancel_button=QPushButton(lang.setting_ui.cancel)
		cancel_button.setFont(font)
		cancel_button.setStyleSheet("QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}")
		cancel_button.clicked.connect(self.close)
		restore_button=QPushButton(lang.setting_ui.restore)
		restore_button.setFont(font)
		restore_button.setStyleSheet("QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}")
		restore_button.clicked.connect(self.restore_settings)
		lang_layout=QHBoxLayout()
		font_layout=QHBoxLayout()
		font_size_layout=QHBoxLayout()
		font_weight_layout=QHBoxLayout()
		font_speed_layout=QHBoxLayout()
		font_italic_layout=QHBoxLayout()
		font_bold_layout=QHBoxLayout()
		address_layout=QHBoxLayout()
		port_layout=QHBoxLayout()
		max_connection_layout=QHBoxLayout()
		alpha_layout=QHBoxLayout()
		button_layout=QHBoxLayout()
		dialog_layout=QVBoxLayout()
		lang_layout.addWidget(lang_label)
		lang_layout.addWidget(self.lang_chooser)
		font_layout.addWidget(font_label)
		font_layout.addWidget(self.font_chooser)
		font_size_layout.addWidget(font_size_label)
		font_size_layout.addWidget(self.font_size_text)
		font_weight_layout.addWidget(font_weight_label)
		font_weight_layout.addWidget(self.font_weight_text)
		font_speed_layout.addWidget(font_speed_label)
		font_speed_layout.addWidget(self.font_speed_text)
		font_italic_layout.addWidget(font_italic_label)
		font_italic_layout.addWidget(self.font_italic_text)
		font_bold_layout.addWidget(font_bold_label)
		font_bold_layout.addWidget(self.font_bold_text)
		address_layout.addWidget(address_label)
		address_layout.addWidget(self.address_text)
		port_layout.addWidget(port_label)
		port_layout.addWidget(self.port_text)
		max_connection_layout.addWidget(max_connection_label)
		max_connection_layout.addWidget(self.max_connection_text)
		alpha_layout.addWidget(alpha_label)
		alpha_layout.addWidget(self.alpha_text)
		button_layout.addWidget(save_button)
		button_layout.addWidget(cancel_button)
		button_layout.addWidget(restore_button)
		dialog_layout.addWidget(setting_title_label)
		dialog_layout.addLayout(lang_layout)
		dialog_layout.addLayout(font_layout)
		dialog_layout.addLayout(font_size_layout)
		dialog_layout.addLayout(font_weight_layout)
		dialog_layout.addLayout(font_italic_layout)
		dialog_layout.addLayout(font_bold_layout)
		dialog_layout.addLayout(font_speed_layout)
		dialog_layout.addLayout(address_layout)
		dialog_layout.addLayout(port_layout)
		dialog_layout.addLayout(max_connection_layout)
		dialog_layout.addLayout(alpha_layout)
		dialog_layout.addLayout(button_layout)
		self.setLayout(dialog_layout)
	def get_lang(self):
		lang_list=[]
		lang_files=[]
		self.lang_code_list=[]
		for root,dirs,files in os.walk("lang"):
			for name in files:
				with open(file=os.path.join(root,name),mode="r",encoding="utf-8") as lang_reader:
					if name.endswith(".json"):
						lang_dict=json.load(lang_reader)
						lang_list.append(str(lang_dict["name"]))
						lang_files.append(str(os.path.join(root,name)))
						self.lang_code_list.append(str(lang_dict["code"]))
		return lang_list,lang_files
	def get_fixed_value(self,index:int):
		if index==0:
			return 1
		elif index==1:
			return 0
		else:
			raise ValueError
	def save_setting(self):
		new_conf_dic={"lang":str(self.lang_code_list.index(self.lang_chooser.currentIndex())),"font":str(self.font_chooser.currentFont.family()),"font_size":int(self.font_size_text.text()),"font_speed":int(self.font_speed_text.text()),"font_weight":int(self.font_weight_text.text()),"font_italic":int(self.get_fixed_value(self.font_italic_text.currentIndex())),"font_bold":int(self.get_fixed_value(self.font_bold_text.currentIndex())),"color_alpha":self.alpha_text.value()/100,"port":int(self.port_text.text()),"address":str(self.address_text.text()),"max_connection":int(self.max_connection_text.text())}
		with open(file="config.json",mode="w",encoding="utf-8") as new_conf_writer:
			json.dump(obj=new_conf_dic,fp=new_conf_writer,indent=4,sort_keys=True)
	def restore_settings(self):
		with open(file="config.json",mode="w",encoding="utf-8") as default_conf_witer:
			default_conf_dic={"lang":"zh_CN","font": "Microsoft YaHei","font_size": 15,"font_speed": 100,"font_weight": 50,"font_italic": 0,"font_bold": 0,"color_alpha":1.0,"port": 2333,"address": "localhost","max_connection":5}
			json.dump(default_conf_dic,default_conf_writer,indent=4,sort_keys=True)
class TrayIcon(QSystemTrayIcon):
	def __init__(self):
		super(TrayIcon,self).__init__()
		self.tray_menu=QMenu()
		action_exit=QAction(QIcon("resources/exit.png"),lang.notification.exit_menu,self)
		action_exit.triggered.connect(self.quit_program)
		logging.debug(lang.debug.created_action)
		action_setting=QAction(QIcon("resources/setting.png"),lang.notification.setting_menu,self)
		action_setting.triggered.connect(self.show_setting_ui)
		logging.debug(lang.debug.created_action)
		self.tray_menu.addAction(action_setting)
		self.tray_menu.addAction(action_exit)
		self.setContextMenu(self.tray_menu)
		self.setToolTip(lang.notification.tooltip)
		self.setIcon(QIcon("resources/program.ico"))
		self.setVisible(True)
		logging.debug(lang.debug.finished_creating_menu)
	def quit_program(self):
		self.setVisible(False)
		logging.info(lang.info.closed_tray)
		qApp.quit()
		self.deleteLater()
		sys.exit()
	def show_setting_ui(self):
		setting_dialog=SettingDialog()
		setting_dialog.exec_()
class main_window(QMainWindow):
	update_signal=pyqtSignal(str)
	def __init__(self):
		super(main_window,self).__init__()
		central_widget=QWidget()
		self.setCentralWidget(central_widget)
		self.setWindowOpacity(0.95)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setWindowFlag(Qt.Tool)
		self.screen=QApplication.desktop().availableGeometry()
		self.screen_size=QSize(self.screen.width(),self.screen.height())
		self.setGeometry(0,0,self.screen.width(),self.screen.height())
		self.update_signal.connect(self.show_damaku)
	def show_damaku(self,text:str):
		damaku_act=damaku(text)
		try:
			damaku_act.show()
		except RuntimeError:
			logging.error(lang.error.recived_close_connection)
		else:
			logging.info(lang.info.shown_damaku)
class damaku(QLabel):
	def __init__(self,text:str):
		if text=="":
			return None
		super(damaku,self).__init__()
		self.setFont(setting.damaku_font)
		self.setText(text)
		self.adjustSize()
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setWindowFlag(Qt.Tool)
		color=str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(setting.color_alpha)
		style="QLabel{color:rgba("+color+");background-color:transparent;}"
		logging.debug(lang.debug.used_color+"rgba("+color+")")
		self.setStyleSheet(style)
		self.raise_()
		logging.info(lang.info.generated_orig_label)
		self.anim2=QPropertyAnimation(self,bytes("pos","utf-8"))
		self.anim2.setDuration(int(10000*(setting.font_speed/100)))
		self.screen=QApplication.desktop().availableGeometry()
		self.screen_x=int(self.screen.width())
		self.screen_y=int(self.screen.height())
		self.font_y=setting.damaku_font.pointSize()
		pos_y=random.randint(0,self.screen_y-self.font_y)
		self.anim2.setStartValue(QPoint(self.screen_x,pos_y))
		self.anim2.setEndValue(QPoint(0,pos_y))
		self.anim2.setEasingCurve(QEasingCurve.Linear)
		self.anim2.finished.connect(self.finish_play)
		self.anim2.start(QAbstractAnimation.DeleteWhenStopped)
		logging.info(lang.info.generated_final_label)
	def finish_play(self):
		self.deleteLater()
class EnhancedSlider(QSlider):
	def __init__(self):
		super(EnhancedSlider,self).__init__()
		self.value_label=QLabel(self)
		self.value_label.setFixedSize(QSize(25,25))
		self.value_label.setAutoFillBackground(True)
		self.value_label.setAlignment(Qt.AlignCenter)
		self.value_label.setVisible(False)
		self.value_label.move(0,0)
		self.value_label.setWindowFlag(Qt.FramelessWindowHint)
		self.value_label.setWindowFlag(Qt.Tool)
		self.value_label.setAttribute(Qt.WA_TranslucentBackground)
		self.value_label.adjustSize()
		self.value_label.setStyleSheet("QLabel{border:1px solid gray;width:25px;border-radius:10px;padding:2px 4px;}")
	def mousePressEvent(self, QMouseEvent):
		if self.value_label.isVisible()==False:
			self.value_label.setVisible(True)
		self.value_label.setText(str(self.value()))
		QSlider.mousePressEvent(self,QMouseEvent)
	def mouseReleaseEvent(self,QMouseEvent):
		if self.value_label.isVisible()==True:
			self.value_label.setVisible(False)
		QSlider.mouseReleaseEvent(self,QMouseEvent)
	def mouseMoveEvent(self,QMouseEvent):
		self.value_label.setText(str(self.value()))
		self.value_label.move(int(self.pos().x()+self.parent().x()+(self.width()-self.value_label.width())*self.value()/(self.maximum()-self.minimum())),self.pos().y()+self.parent().y()-8)
		QSlider.mouseMoveEvent(self,QMouseEvent)
app=QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
tray_icon=TrayIcon()
if is_win10==True:
	toaster=win10toast.ToastNotifier()
	# 图标作者:https://github.com/nullice/NViconsLib_Silhouette
	toaster.show_toast(title=lang.notification.title,msg=lang.notification.msg,icon_path="resources/program.ico",duration=5,threaded=True)
else:
	tray_icon.showMessage(lang.notification.title,lang.notification.msg,QIcon("resources/program.ico"),5000)
logging.info(lang.info.sended_notification)
tray_icon.show()
logging.info(lang.info.shown_tray)
tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_socket.bind((setting.address,setting.port))
tcp_socket.listen(setting.max_connection)
logging.info(lang.info.successfully_listen_port)
class process_work(QObject):
	def __init__(self,tcp_socket):
		super(process_work,self).__init__()
		context=ssl.SSLContext()
		context.load_cert_chain(keyfile="cert/key.pem",certfile="cert/cert.pem")
		self.tcp_socket=tcp_socket
		self.tcp_socket=context.wrap_socket(sock=self.tcp_socket,server_side=True)
		logging.info(lang.info.loaded_cert)
	def connection_process(self):
		while True:
			connect,address=self.tcp_socket.accept()
			while True:
				try:
					data=connect.recv(1024).decode("utf-8")
				except ConnectionResetError:
					logging.info(lang.info.close_connection)
					break
				except ConnectionAbortedError:
					logging.warning(lang.warning.aborted_connection)
					break
				except IOError:
					logging.error(lang.error.io_error)
					break
				else:
					if data=="":
						connect.close()
					w.update_signal.emit(data)
					logging.info(lang.info.connected_client+str(address))
					connect.send(("{\"status\":\"accepted\",\"code\":1,\"data\":"+data+"}").encode("utf-8"))
					logging.info(lang.info.recived_data+str(data))
			connect.close()
process=process_work(tcp_socket)
process_socket_thread=QThread()
process.moveToThread(process_socket_thread)
process_socket_thread.started.connect(process.connection_process)
process_socket_thread.start()
logging.info(lang.info.started_sock_thread)
w=main_window()
w.show()
logging.info(lang.info.shown_window)
sys.exit(app.exec_())