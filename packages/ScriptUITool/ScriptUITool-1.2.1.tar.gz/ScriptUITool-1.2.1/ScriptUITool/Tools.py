import re
import FileKit
import os
import sys
import shutil
import ast
import time
file_name_ui = 'ui\\StartUI.ui'
path_create_thread = 'create_thread.py'
path_start_ui = 'start_ui.py'
path_button_click_handler = 'button_click_handler.py'


class QtButton:
    def __init__(self, button_name):
        self.name = button_name
        self.create_thread_function = self.name.replace('pushButton', 'create_thread')
        self.button_click_handler_function = self.name.replace('pushButton', 'clicked')
        self.thread_id = self.name.replace('pushButton', 'thread')

    def make_clicked_connect_code(self):
        code = f'window.ui.{self.name}.clicked.connect({self.create_thread_function})'
        return code

    def add_sj_function_code(self):
        code_first_line = f'{self.button_click_handler_function}'
        all_now_code = FileKit.read(path_button_click_handler)

        if code_first_line not in all_now_code:
            code = \
f'''def {self.button_click_handler_function}():
    """这里添加功能"""


'''
            if self.name == 'pushButton_center':
                code = \
'''def clicked_center(td_run_id):
    ThreadManage.stop_all()
    print('已经停止操作')

'''
            FileKit.write_append(path_button_click_handler, code)

    def add_create_thread_code(self):
        if self.name == 'pushButton_center':
            code = \
f"""def {self.create_thread_function}():
    global running_task
    ThreadEx(target=clicked_center)
    running_task = None


"""
        else:
            code = \
f"""def {self.create_thread_function}():
    global {self.thread_id}, running_task
    if (not running_task) or (running_task == {self.thread_id} and running_task.status == 'stopped'):
        {self.thread_id} = ThreadManage.create_thread(target={self.button_click_handler_function})
        running_task = {self.thread_id}
    elif running_task == {self.thread_id}:
        print('{self.thread_id} 功能已经在运行')
    else:
        print(f'其他 功能已经在运行')


"""

        list_code = FileKit.read_lines(path_create_thread)
        print('list_code=', list_code)
        for index in range(5, len(list_code)):
            # if list_code[index]:
            #     print('退出循环：', list_code[index])
            #     break
            if list_code[index] == '\n':
                print('追加： ', list_code[index])
                list_code.insert(index, f'{self.thread_id}=None\n')
                break
        print(' list_code2 = ',  list_code)
        FileKit.write(path_create_thread, ''.join(list_code) + code)
        # FileKit.write_append(path_create_thread, code)

    def insert_code_to_start_ui(self):
        list_code = FileKit.read_lines(path_start_ui)
        new_code = self.make_clicked_connect_code()
        for index in range(len(list_code)):
            if new_code == list_code[index].strip():
                break
            if 'window.ui.show()' in list_code[index]:
                list_code.insert(index-1, f'    {new_code}\n')
                break
        else:
            raise Exception('start_ui.py 中 没有找到 代码 window.ui.show()')
        FileKit.write(path_start_ui, ''.join(list_code))

    def is_function_defined_ast(self, path, function_name):
        all_code = FileKit.read(path)
        result = self._is_function_defined_ast( all_code, function_name)
        return result

    def _is_function_defined_ast(self, code, function_name):
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return True
        except Exception as e:
            pass
        return False




def create_tow_code_file():


    code = \
"""from NewThread import ThreadManage, ThreadEx
from button_click_handler import *
from gl import gl

running_task = None
    


"""


    code_on_click=\
'''from NewThread import ThreadManage, ThreadEx
from gl import gl



'''

    # 创建两个文件：
    FileKit.write(path_create_thread, code)
    FileKit.write(path_button_click_handler, code_on_click)


def update_gl_value(argv_file_name_ui, argv_path_create_thread, argv_path_start_ui, argv_path_button_click_handler):
    global file_name_ui, path_create_thread, path_start_ui, path_button_click_handler
    file_name_ui = argv_file_name_ui
    path_create_thread = argv_path_create_thread
    path_start_ui = argv_path_start_ui
    path_button_click_handler = argv_path_button_click_handler


def run(action='', code=0,
        argv_file_name_ui = 'ui\\StartUI.ui',
        argv_path_create_thread = 'create_thread.py',
        argv_path_start_ui = 'start_ui.py',
        argv_path_button_click_handler = 'button_click_handler.py'):
    update_gl_value(argv_file_name_ui, argv_path_create_thread, argv_path_start_ui, argv_path_button_click_handler)

    if code == 0 and action == '':
        code = eval(input("1 新建项目\n2 更新UI界面\n"))
    if action == 'create' or code == 1:
        try:
            current_file_path = os.path.abspath(__file__)
            current_file_path = current_file_path.replace('Tools.py', 'start_ui.py')
            shutil.copy(current_file_path, os.path.join(os.getcwd(), path_start_ui))
            current_file_path = current_file_path.replace('start_ui.py', 'gl.py')
            shutil.copy(current_file_path, os.path.join(os.getcwd(), 'gl.py'))
            time.sleep(0.1)
            # input('继续吗')
        except Exception as e:
            pass

        create_tow_code_file()
        list_button_name = get_names_by_class(file_name_ui, 'QPushButton')
        # ls_sj_code = []
        for button_name in list_button_name:
            print(f'创建按钮对象： button_name= [{button_name}]')
            button = QtButton(button_name=button_name)
            button.add_create_thread_code()
            button.add_sj_function_code()
            button.insert_code_to_start_ui()
            # sj_code = button.make_clicked_connect_code()
            # ls_sj_code.append(sj_code)

        update_window_el_name(os.path.join(os.getcwd(), path_start_ui), file_name_ui)

    elif action == 'update' or code == 2:
        list_button_name = get_names_by_class(file_name_ui, 'QPushButton')
        # ls_sj_code = []
        is_add = False
        print('为您更新界面按钮时间和函数:\n')
        clear_connect_code(os.path.join(os.getcwd(), path_start_ui))
        for button_name in list_button_name:

            button = QtButton(button_name=button_name)
            if not button.is_function_defined_ast(path_create_thread, button.create_thread_function):
                print(f'在 {path_create_thread} 文件中  为按钮 {button_name} 新增函数 {button.create_thread_function}')
                button.add_create_thread_code()
                is_add = True
            if not button.is_function_defined_ast(path_button_click_handler, button.button_click_handler_function):
                print(
                    f'在 {path_button_click_handler} 文件中 为按钮 {button_name} 新增函数 {button.button_click_handler_function}')
                button.add_sj_function_code()
                is_add = True
            button.insert_code_to_start_ui()

            # sj_code = button.make_clicked_connect_code()
            # ls_sj_code.append(sj_code)
        if is_add:
            print('\n新增函数完成...')
        else:
            print('抱歉, 未找到新增项')
    else:
        pass


def create_project(argv_file_name_ui='ui\\StartUI.ui',
                   argv_path_create_thread='create_thread.py',
                   argv_path_start_ui='start_ui.py',
                   argv_path_button_click_handler='button_click_handler.py'):
    run('create', 1, argv_file_name_ui, argv_path_create_thread, argv_path_start_ui, argv_path_button_click_handler)


def update_project(argv_file_name_ui='ui\\StartUI.ui',
                   argv_path_create_thread='create_thread.py',
                   argv_path_start_ui='start_ui.py',
                   argv_path_button_click_handler='button_click_handler.py'):
    run('update', 2, argv_file_name_ui, argv_path_create_thread, argv_path_start_ui, argv_path_button_click_handler)


def get_names_by_class(ui_file_name, class_name):
    """根据 类名查找所有元素name  返回一个列表 """
    text = FileKit.read(ui_file_name)
    # 仅提取 QPushButton 的 name
    pattern_strict = r'<widget\s+class="' + class_name + r'"[^>]*?name="(.*?)"'
    results_strict = re.findall(pattern_strict, text)
    return results_strict


def update_window_el_name(start_ui_file_name, ui_file_name):
    all_code = FileKit.read(start_ui_file_name)
    match = re.search(r'window = MainWindow[\s\S]*ls_plain_edit=\[[\s\S]*\]\)', all_code)
    if match:
        ord_code = match.group()
        ui_file_name = r'C:\Users\Administrator2\Desktop\ScriptUITool\ui\StartUI.ui'
        list_line_edit_name = get_names_by_class(ui_file_name, 'QLineEdit')
        list_check_box_name = get_names_by_class(ui_file_name, 'QCheckBox')
        list_plain_edit_name = get_names_by_class(ui_file_name, 'QPlainTextEdit')

        new_code =\
f"""
    window = MainWindow("", ui_file_name=os.path.join('ui', 'StartUI.ui'), ls_checkbox={list_check_box_name},
                        ls_line_edit={list_line_edit_name}, ls_plain_edit={list_plain_edit_name})
"""
        print( new_code )

        print('更新 界面元素名称 成功')
        all_code = all_code.replace(ord_code, new_code)
        FileKit.write(start_ui_file_name, all_code)
        return True
    else:
        print('没有匹配到关键代码： window = MainWindow...')
        return False


def clear_connect_code(file_name):
    # file_name = 'start_ui.py'
    ls_text = FileKit.read_lines(file_name )
    ls_new_code = []
    for text in ls_text:
        if not ('window.ui.pushButton' in text and '.clicked.connect' in text):
            ls_new_code.append(text)
    FileKit.write_lines(file_name, ls_new_code)


if __name__ == '__main__':

    print(sys.argv)
    if len(sys.argv) == 1:
        run()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'create':
            run(code=1)
        elif sys.argv[1] == 'update':
            run(code=2)




