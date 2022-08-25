
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import *
from PyQt5 import uic

import secrets
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
Ui_MainWindow = uic.loadUiType(os.path.join(BASE_DIR, "marin_editor.ui"))[0]

ext_list = ['.jpg', '.jpeg', '.png']

# top, bottom, padding
class_dict = {
    't' : {
        'composition' : {'O' : ['상반신', '전신', '하반신', '디테일'], 
                         'X' : ['앞면', '뒷면', '디테일']},
        'detail'      : {'O' : ['넥라인', '중간허리부분', '소매', '포캣', '아래밑단', '후드뒷면'], 
                         'X' : ['넥라인', '안감', '재질트위스트', '지퍼', '소매', '밑단']}
    },
    'p' : {
        'composition' : {'O' : ['상반신', '전신', '디테일'], 
                         'X' : ['앞면', '뒷면', '디테일']},
        'detail'      : {'O' : ['집업', '집업오픈', '소매', '내부포켓', '외부포켓', '포켓손'], 
                         'X' : ['넥라인', '소매', '포켓', '밑단', '안감']}
    },
    'b' : {
        'composition' : {'O' : ['전신', '하반신', '디테일'], 
                         'X' : ['앞면', '뒷면', '디테일']},
        'detail'      : {'O' : ['허리가운데확대', '주머니손', '프린트', '뒷면포켓', '바지밑단'], 
                         'X' : ['허리가운데확대', '허리옆부분', '프린트', '바지밑단', '뒷면포켓', '허리안쪽밴딩', '안감']}        
    }
}

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.b_radio_button.clicked.connect(self.change_combo_box)
        self.p_radio_button.clicked.connect(self.change_combo_box)
        self.t_radio_button.clicked.connect(self.change_combo_box)
        self.is_model_O.clicked.connect(self.change_combo_box)
        self.is_model_X.clicked.connect(self.change_combo_box)
        self.composition_combo_box.activated[str].connect(self.check_detail)

        self.file_list_widget.clicked.connect(self.widget_row_clicked)
        self.changed_file_list_widget.clicked.connect(self.float_about_message)
        self.change_file_name_button.clicked.connect(self.change_file_name_button_clicked)
        self.change_folder_dir_button.clicked.connect(self.exist_folder_dir)

        self.setUI()

    def setUI(self):
        try:
            self.exist_folder_dir()
            self.widget_row_clicked()
            self.product = 'b'
            self.before_currentText = ''
            self.is_model = 'O'
            self.is_detail = '-'
        except Exception as e:
            print(e)

    def float_about_message(self):
        QMessageBox.about(self,'기능 준비중...','아직 기능 준비중입니다 김말이 개발자에게 문의해주세요~')

    def check_detail(self, currentText):
        if currentText == self.before_currentText != '디테일':  pass
        else:                                                  self.change_detail_combo_box()

        self.before_currentText = currentText

    def change_detail_combo_box(self):
        self.is_detail = self.composition_combo_box.currentText()

        if self.is_detail == '디테일':  detail_list = class_dict[self.product]['detail'][self.is_model]
        else:                           detail_list = ['-']

        self.detail_combo_box.clear()
        self.detail_combo_box.addItems(detail_list)

    def change_combo_box(self):
        if self.b_radio_button.isChecked():   self.product = 'b'
        elif self.p_radio_button.isChecked(): self.product = 'p'
        elif self.t_radio_button.isChecked(): self.product = 't'
        
        if self.is_model_O.isChecked(): 
            self.is_model = 'O'
            self.model_num_1.setCheckable(True)
            self.model_num_2.setCheckable(True)
            self.model_num_3.setCheckable(True)
            self.model_num_1.setChecked(True)
        else:                           
            self.is_model = 'X'
            self.model_num_1.setCheckable(False)
            self.model_num_2.setCheckable(False)
            self.model_num_3.setCheckable(False)

            if self.model_num_1.isChecked(): self.model_num_1.setChecked(False)
            elif self.model_num_2.isChecked(): self.model_num_2.setChecked(False)
            elif self.model_num_3.isChecked(): self.model_num_3.setChecked(False)

        self.is_detail = self.composition_combo_box.currentText()

        if self.is_detail == '디테일':
            composition_list = class_dict[self.product]['composition'][self.is_model]
            detail_list = class_dict[self.product]['detail'][self.is_model]
        else:
            composition_list = class_dict[self.product]['composition'][self.is_model]
            detail_list = ['-']

        self.composition_combo_box.clear()
        self.detail_combo_box.clear()

        self.composition_combo_box.addItems(composition_list)
        self.detail_combo_box.addItems(detail_list)

    def checking_result(self):
        result_name = ''

        if self.is_model_O.isChecked(): is_model = 'O'
        else:                           is_model = 'X'

        if self.bg_type_1.isChecked():   bg_type = '1'
        elif self.bg_type_2.isChecked(): bg_type = '2'
        elif self.bg_type_3.isChecked(): bg_type = '3'
        else:                            bg_type = '-'

        composition = self.composition_combo_box.currentText()
        detail      = self.detail_combo_box.currentText()

        if self.color_A.isChecked():   color = 'A'
        elif self.color_B.isChecked(): color = 'B'
        elif self.color_C.isChecked(): color = 'C'
        else:                          color = '-'

        if self.model_num_1.isChecked():   model_num = '1'
        elif self.model_num_2.isChecked(): model_num = '2'
        elif self.model_num_3.isChecked(): model_num = '3'
        else:                              model_num = '-'

        for result in [is_model, bg_type, composition, detail, color, model_num]:
            if result != '-':  result_name += f'{result}_'

        self.show_changed_file_name_text_edit.setPlainText(result_name[:-1])

    def exist_folder_dir(self):
        self.item_idx = 0
        self.folder_dir = QFileDialog.getExistingDirectory(self, 'Get Directory')
        print(self.folder_dir)

        self.image_path_list = get_image_list(self.folder_dir)
        self.changed_image_path_list = []
        self.show_list()

        self.file_list_widget.setCurrentRow(self.item_idx)
        self.widget_row_clicked()

    def show_list(self):
        try:
            self.file_list_widget.clear()
            self.changed_file_list_widget.clear()
            if len(self.image_path_list) > 0:
                for idx, image_path in enumerate(self.image_path_list):
                    self.file_list_widget.insertItem(idx, image_path)
            
            if len(self.changed_image_path_list) > 0:
                for idx, image_path in enumerate(self.changed_image_path_list):
                    self.changed_file_list_widget.insertItem(idx, image_path)

        except Exception as e:
            print(e)
            pass

    def show_image_on_pixmap(self):        
        pixmap = QPixmap(self.file_path)
        p_size = pixmap.size()
        if p_size.height() > p_size.width(): pixmap = pixmap.scaledToHeight(360)
        else:                                pixmap = pixmap.scaledToWidth(360)

        self.image_viewer.setPixmap(QPixmap(pixmap))
        self.show()

    def widget_row_clicked(self):
        try:
            if len(self.image_path_list) > 0:
                self.item_idx = self.file_list_widget.currentRow()
                self.file_path = self.file_list_widget.item(self.item_idx).text()
                self.file_dir = os.path.split(self.file_path)[0]
                self.show_image_on_pixmap()
            else:
                self.exist_folder_dir()
        except Exception as e:
            print(e)
            

    def Critical_event(self, massage) :
        QMessageBox.critical(self,'Error', massage)

    def change_file_name_button_clicked(self):
        try:
            self.checking_result()
            self.image_path_list.remove(self.file_path)

            c_file_name = self.show_changed_file_name_text_edit.toPlainText()            
            c_file_ext = self.ext_combo_box.currentText()
            c_file_name = f'{c_file_name}_{secrets.token_hex(4)}{c_file_ext}'
            
            result, changed_file_name = change_file_name(self.file_path, c_file_name)
            self.changed_image_path_list.append(changed_file_name)
            if result: self.show_changed_file_name_text_edit.setText(os.path.join(os.path.split(self.file_dir)[-1], c_file_name))
            else:      self.Critical_event(changed_file_name)
        except Exception as e:
            print(e)
            pass

        #self.item_idx += 1
        self.show_list()
        self.file_list_widget.setCurrentRow(self.item_idx)
        self.widget_row_clicked()

def get_image_list(image_folder_dir):
    image_list = [os.path.join(image_folder_dir, image_name) for image_name in os.listdir(image_folder_dir) if os.path.splitext(image_name)[-1] in ext_list]
    return image_list

def change_file_name(file_path, change_name):
    try:
        file_dir, _ = os.path.split(file_path)
        c_file_name = os.path.join(file_dir, change_name)
        os.rename(file_path, c_file_name)
        return True, c_file_name
    except Exception as e:
        print(e)
        return False, e

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()