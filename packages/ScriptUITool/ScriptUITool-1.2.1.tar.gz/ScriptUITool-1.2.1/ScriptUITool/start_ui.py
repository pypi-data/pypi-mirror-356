from ScriptUITool.ui_model import *
from create_thread import *
window = None


if __name__ == '__main__':
    """
        gl.window.ui.lineEdit_run_time.text()
    """
    app = QApplication([])
    
    
    window = MainWindow("", ui_file_name=os.path.join('ui', 'StartUI.ui'), ls_checkbox=['checkBox_test'],
                        ls_line_edit=['lineEdit_run_time'], ls_plain_edit=[])


    window.ui.pushButton_activate.clicked.connect(create_thread_activate)
    window.ui.pushButton_wk.clicked.connect(create_thread_wk)
    window.ui.pushButton_cj.clicked.connect(create_thread_cj)
    window.ui.pushButton_yjcw.clicked.connect(create_thread_yjcw)
    window.ui.pushButton_zfbl.clicked.connect(create_thread_zfbl)
    window.ui.pushButton_cq.clicked.connect(create_thread_cq)
    window.ui.pushButton_gqm.clicked.connect(create_thread_gqm)
    window.ui.pushButton_yz.clicked.connect(create_thread_yz)
    window.ui.pushButton_KeyPressF.clicked.connect(create_thread_KeyPressF)
    window.ui.pushButton_changeCurrentUser.clicked.connect(create_thread_changeCurrentUser)
    window.ui.pushButton_debugStep.clicked.connect(create_thread_debugStep)
    window.ui.pushButton_center.clicked.connect(create_thread_center)
    window.ui.pushButton_hczf.clicked.connect(create_thread_hczf)
    window.ui.pushButton_lxjd.clicked.connect(create_thread_lxjd)

    gl.window = window
    window.ui.show()
    sys.exit(app.exec_())
