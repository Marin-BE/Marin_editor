
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import *
from PyQt5 import uic

import datetime
import secrets
import json
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, 'data')

Ui_MainWindow = uic.loadUiType(os.path.join(BASE_DIR, "marin_editor.ui"))[0]

with open(os.path.join(DATA_DIR, 'colors_per_folder.json'), 'r') as colors_per_folder_j:
    colors_per_folder = dict(json.load(colors_per_folder_j))

with open(os.path.join(DATA_DIR, 'spao_color.json'), 'r') as spao_color_j:
    spao_colors = dict(json.load(spao_color_j))

with open(os.path.join(DATA_DIR, 'class_dict.json'), 'r', encoding="utf-8") as class_dict_j:
    class_dict = dict(json.load(class_dict_j))

ext_list = ['.jpg', '.jpeg', '.png']

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.b_radio_button.clicked.connect(self.change_combo_box)
        self.p_radio_button.clicked.connect(self.change_combo_box)
        self.t_radio_button.clicked.connect(self.change_combo_box)
        self.check_box_no_model.stateChanged.connect(self.change_combo_box)
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
            self.cloth_type = 'b'
            self.before_currentText = ''
            self.is_model = 'O'
            self.is_detail = '-'
        except Exception as e:
            print(e)

    def float_about_message(self):
        QMessageBox.about(self,'기능 준비중...','아직 기능 준비중입니다 김말이 개발자에게 문의해주세요~')

    def check_detail(self, currentText):
        if currentText == self.before_currentText != '디테일':  pass
        else:                                                 self.change_detail_combo_box()

        self.before_currentText = currentText

    def change_color_combo_box(self):
        folder_name = os.path.split(self.folder_dir)[-1]
        try:     color_list = colors_per_folder[folder_name]
        except:  color_list = ['A', 'B', 'C', 'D', 'E']
        self.colors_combo_box.clear()
        self.colors_combo_box.addItems(color_list)

    def change_detail_combo_box(self):
        self.is_detail = self.composition_combo_box.currentText()

        if self.is_detail == '디테일':  detail_list = class_dict[self.cloth_type]['detail'][self.is_model]
        else:                         detail_list = ['-']

        self.detail_combo_box.clear()
        self.detail_combo_box.addItems(detail_list)

    def change_combo_box(self):
        if self.b_radio_button.isChecked():   self.cloth_type = 'b'
        elif self.p_radio_button.isChecked(): self.cloth_type = 'p'
        elif self.t_radio_button.isChecked(): self.cloth_type = 't'
        
        composition_list = class_dict[self.cloth_type]['model_composition']

        if self.check_box_no_model.isChecked(): 
            self.is_model = 'X'
            composition_list = ['디테일', '디테일 없음']
        else:                                   
            self.is_model = 'O'
        
        self.is_detail = self.composition_combo_box.currentText()

        if self.is_detail == '디테일':  detail_list = class_dict[self.cloth_type]['detail'][self.is_model]
        else:                         detail_list = ['-']

        self.composition_combo_box.clear()
        self.detail_combo_box.clear()

        self.composition_combo_box.addItems(composition_list)
        self.detail_combo_box.addItems(detail_list)

    def checking_result(self):
        self.model_list = []
        if self.check_box_m1.isChecked(): self.model_list.append('m1')
        if self.check_box_m2.isChecked(): self.model_list.append('m2')
        if self.check_box_m3.isChecked(): self.model_list.append('m3')
        if self.check_box_m4.isChecked(): self.model_list.append('m4')
        if self.check_box_m5.isChecked(): self.model_list.append('m5')
        if self.check_box_m6.isChecked(): self.model_list.append('m6')
        if self.check_box_m7.isChecked(): self.model_list.append('m7')
        if self.check_box_f1.isChecked(): self.model_list.append('f1')
        if self.check_box_f2.isChecked(): self.model_list.append('f2')
        if self.check_box_f3.isChecked(): self.model_list.append('f3')
        if self.check_box_f4.isChecked(): self.model_list.append('f4')
        if self.check_box_f5.isChecked(): self.model_list.append('f5')
        if self.check_box_f6.isChecked(): self.model_list.append('f6')
        if self.check_box_no_model.isChecked(): self.model_list.clear()

        if self.bg_type_1.isChecked():   self.bg_type = '1'
        elif self.bg_type_2.isChecked(): self.bg_type = '2'
        elif self.bg_type_3.isChecked(): self.bg_type = '3'
        elif self.bg_type_4.isChecked(): self.bg_type = '4'
        elif self.bg_type_5.isChecked(): self.bg_type = '5'
        elif self.bg_type_6.isChecked(): self.bg_type = '6'
        elif self.bg_type_7.isChecked(): self.bg_type = '7'
        elif self.bg_type_8.isChecked(): self.bg_type = '8'
        else:                            self.bg_type = '-'

        if self.front_radio_button.isChecked():  self.image_composition = 'front'
        elif self.side_radio_button.isChecked(): self.image_composition = 'side'
        elif self.back_radio_button.isChecked(): self.image_composition = 'back'
        else:                                    self.image_composition = '-'

        self.model_composition = self.composition_combo_box.currentText()
        if self.model_composition != '디테일':   
            self.model_composition = '-'

        self.detail            = self.detail_combo_box.currentText()
        color                  = self.colors_combo_box.currentText()
        
        try:    self.color_code = spao_colors['reverse'][color]
        except: self.color_code = color

    def exist_folder_dir(self):
        self.item_idx = 0
        self.folder_dir = QFileDialog.getExistingDirectory(self, 'Get Directory')
        print(self.folder_dir)

        self.image_path_list = get_image_list(self.folder_dir)
        self.changed_image_path_list = []
        self.change_color_combo_box()
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
            
    def check_json_and_remove(self):
        json_file = os.path.splitext(self.file_path)[0] + '.json'

        if os.path.isfile(json_file):
            os.remove(json_file)

    def Critical_event(self, massage) :
        QMessageBox.critical(self,'Error', massage)

    def change_file_name_button_clicked(self):
        self.check_json_and_remove()

        try:
            self.checking_result()
            self.image_path_list.remove(self.file_path)
     
            c_file_ext = self.ext_combo_box.currentText()
            c_file_name = f'{secrets.token_hex(4)}{c_file_ext}'

            result, changed_file_name = change_file_name(self.file_path, c_file_name)
            self.changed_image_path_list.append(changed_file_name)
            if result: 
                self.show_changed_file_name_text_edit.setText(os.path.join(self.file_dir, c_file_name))
                self.make_json_result(c_file_name=c_file_name)
            else:      
                self.Critical_event(changed_file_name)
            
            self.show_changed_file_name_text_edit.setText(os.path.join(self.file_dir, c_file_name))
        except Exception as e:
            print(e)
            pass

        self.show_list()
        self.file_list_widget.setCurrentRow(self.item_idx)
        self.widget_row_clicked()

    def make_json_result(self, c_file_name):
        result_dict = {}

        result_dict['date'] = str(datetime.datetime.now())
        result_dict['file_name'] = c_file_name
        
        result_dict['result'] = {}
        result_dict['result']['cloth_type']        = self.cloth_type
        result_dict['result']['model']             = self.model_list
        result_dict['result']['bg_type']           = self.bg_type
        result_dict['result']['image_composition'] = self.image_composition
        result_dict['result']['model_composition'] = self.model_composition
        result_dict['result']['detail']            = self.detail
        result_dict['result']['color']             = self.color_code
        
        result_file_name = os.path.splitext(c_file_name)[0] + '.json'

        with open(os.path.join(self.file_dir, result_file_name), 'w', encoding='utf-8') as result_file:
            json.dump(result_dict, result_file, indent=4, ensure_ascii=False)

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