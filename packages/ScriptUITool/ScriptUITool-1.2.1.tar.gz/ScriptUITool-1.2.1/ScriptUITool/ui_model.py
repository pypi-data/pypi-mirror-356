import os
import json
import sys
from PySide2.QtWidgets import QApplication     # pip install pyside2 -i  https://pypi.tuna.tsinghua.edu.cn/simple
from PySide2.QtUiTools import QUiLoader        # pip install pyside2
from PySide2.QtCore import QFile
import copy
import threading
from pathlib import Path
import requests
import FileKit
from create_thread import *
t = None       # 主线程
ls_names = []
window = None
""" pyinstaller -F start_script.py --hidden-import PySide2.QtXml """


class MainWindow:
    def __init__(self, s_xml, ui_file_name='Main-Window.ui', ls_checkbox=[], ls_line_edit=[], ls_plain_edit=[]):
        """    从文本中加载UI定义    """
        self.UI_PATH = ui_file_name
        self.UI_USER_PATH = r"ui/Main-Window-config.txt"
        self.config = {}
        for i in range(3):
            my_file = Path("ui")
            if my_file.is_dir():
                break
            os.makedirs(my_file)
        else:
            # input("异常终止,代号 ui1001")
            exit()
        for i in range(3):
            if not os.path.exists(self.UI_PATH):
                if s_xml:
                    with open(self.UI_PATH, mode='w', encoding='utf-8') as f:
                        f.write(s_xml)
                else:
                    print("没有界面")
            else:
                pass
        file_stats = QFile(self.UI_PATH)
        file_stats.open(QFile.ReadOnly)
        file_stats.close()
        self.ui = QUiLoader().load(file_stats)   # 加载界面
        self.ls_checkBox_name = copy.copy(ls_checkbox)
        self.ls_Edit_name = copy.copy(ls_line_edit)
        self.ls_plainEdit_name = copy.copy(ls_plain_edit)
        self.loads_config()  # 读取界面配置
        self.s = ''

    def loads_config(self):
        """  尝试读取配置文件，如果读取成功就把配置文件里面的内容设置到界面
             根据读取出来的配置设置界面控件状态
        """
        try:
            with open(self.UI_USER_PATH, "r") as f:
                s = f.read()
                if s:
                    self.config = json.loads(s)
                else:
                    return -1
        except Exception as e:
            # print(e)
            return -1
        ls_data = []
        try:
            for name in self.ls_checkBox_name:
                ls_data.append(self.checkbox_loads(name))
            for name in self.ls_Edit_name:
                ls_data.append(self.edit_loads(name))
            for name in self.ls_plainEdit_name:
                ls_data.append(self.plain_edit_loads(name))
            exec('\n'.join(ls_data))
        except Exception as e:
            print(e)
        return 0

    def save_config(self):
        """
           获取界面所有 用户设置控件的 值。 文本框使用text()方法， 选择框1 使用 isChecked() 方法
           然后转换成json字符串。保存到本地配置文件。
            self.config["Edit__Excl_Path"] = self.ui.Edit__Excl_Path.text()
            self.config["checkBox__CAIJI_BUBAOHAN"] = self.ui.checkBox__CAIJI_BUBAOHAN.isChecked()
        """
        ls_data = []
        for name in self.ls_checkBox_name:
            ls_data.append(self.checkbox_save(name))
        for name in self.ls_Edit_name:
            ls_data.append(self.edit_save(name))
        for name in self.ls_plainEdit_name:
            ls_data.append(self.plain_edit_save(name))
        try:
            exec('\n'.join(ls_data))
        except Exception as e:
            print("错误", e)

        with open(self.UI_USER_PATH, "w") as f:
            self.s = json.dumps(self.config)
            f.write(self.s)

    def checkbox_loads(self, name):
        return f"self.ui.{name}.setChecked(self.config.get('{name}', False))"

    def edit_loads(self, name):
        return f"self.ui.{name}.setText(self.config.get('{name}', ''))"

    def plain_edit_loads(self, name):
        return f"self.ui.{name}.setPlainText(self.config.get('{name}', ''))"

    def checkbox_save(self, name):
        return f"self.config['{name}'] = self.ui.{name}.isChecked()"

    def edit_save(self, name):
        return f"self.config['{name}'] = self.ui.{name}.text()"

    def plain_edit_save(self, name):
        return f"self.config['{name}'] = self.ui.{name}.toPlainText()"


if __name__ == "__main__":

    app = QApplication([])

    window = MainWindow("", ui_file_name=os.path.join('ui', 'StartUI.ui'), ls_checkbox=[], ls_line_edit=[],
                        ls_plain_edit=[])

    gl.window = window
    window.ui.show()
    sys.exit(app.exec_())
