# -*- coding: utf-8 -*-

import sys
import logging

import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
            QVBoxLayout, QHBoxLayout, QDialog, QFileDialog,
            QLabel, QMessageBox, QComboBox, QFrame)
from PyQt5.QtCore import pyqtSlot


from create_table import TableWindow
from create_graph import PlotCanvas


LOG_FORMAT = "%(levelname)s >  Line:%(lineno)s - %(message)s"
logging.basicConfig(filename="debug.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w",
                    )
logger = logging.getLogger(__name__)



class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'Application'
        self.left = 20
        self.top = 20
        self.width = 800
        self.height = 480
        self.all_item = []
        self.total = dict()
        self.frame = None
        self.siglum_frame = None
        self.sheet_name = ''
        self.initUI()
 
    def initUI(self):
        # Design main window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        # Create button for upload file
        upload_btn = QPushButton('Upload File')
        upload_btn.clicked.connect(self.upload_file)

        self.v_layout.addWidget(upload_btn,)
        self.show()


    @pyqtSlot()
    def upload_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All file(*);;Excel file(*.xlsx)", options=options)
        
        if file_name:
            # Only excel file can be upload otherwise show a error message
            if ('.xlsx' in file_name) or ('.xlsm' in file_name):
                self.read_data_from_excel(file_name)
            else:
                QMessageBox().warning(self, "Invalid file format", "Upload an Excel file!!", QMessageBox.Ok)
        

    # import data form excel
    def read_data_from_excel(self, file_name):
        data = pd.ExcelFile(file_name)

        if 'PO Status' in data.sheet_names:
            self.sheet_name = 'Po Status'
            self.po_status_sheet(data)
        else:
            self.sheet_name = 'Main'
            self.main_sheet(data)


    def po_status_sheet(self, data):
        """
        collect columns name from Po Status sheet and set them into combo box
        """
        data_frame = data.parse('PO Status') # working with 'PO Status' sheet

        # spliting some columns from the 'PO Status'
        x1 = data_frame.loc[:,['Siglum','H/O','Description','Signed','Preise','to be declared','completion']]
        self.frame = x1
        frame_keys =  list(x1.keys())
        self.all_item = [i for i in set(data_frame['Siglum']) if str(i)!='nan']

        for i in self.all_item:
            column_data = (x1.loc[x1['Siglum'] == i ])
            
            if 'Preise' in frame_keys:
                key_name = 'total_'+i.replace(' ','_')
                round_price = column_data['Preise'].sum()
                self.total[key_name] = round(round_price, 2)


        self.create_combo_box()
    

    
    def main_sheet(self, data):
        """
        collect columns name from Main sheet and set them into combo box
        """

        data_frame = data.parse('Main',skiprows = 10) # Working with 'Main' sheet

        # spliting some columns from the 'Main'
        x2 = data_frame.loc[:,['Siglum','HoV','Duration Planned','Duration Real','Deliverable Reference (Document-Nr.)']]
        self.frame = x2
        frame_keys =  list(x2.keys())
        self.all_item = [i for i in set(data_frame['Siglum']) if str(i)!='nan']

        for i in self.all_item:
            column_data = (x2.loc[x2['Siglum'] == i ]).fillna(0)

            if 'Duration Real' in frame_keys and 'Duration Planned' in frame_keys:
                key_name = 'total_real_'+i.replace(' ','_')
                self.total[key_name] = round(column_data['Duration Real'].sum(),2)
                                
                filter_val = []
                for data in column_data['Duration Planned']:
                # remove ',' or '-' from data
                    if isinstance(data,str):
                        if data == '-':
                            filter_val.append(0)
                        elif ',' in data:
                            filter_val.append(float(data.replace(',','.')))
                        else:
                            pass
                    else:
                        filter_val.append(data)
                
                
                key_name = 'total_planned_'+i.replace(' ','_')
                self.total[key_name] = round(sum(filter_val), 2)

        self.create_combo_box()
        
    
    def create_combo_box(self):
        if self.all_item:
            filter_text = self.all_item[0].replace(' ','_')
            
            if self.sheet_name == 'Po Status':
                price = self.total['total_'+filter_text]
                label1_text = ' Total Price'+'('+ self.all_item[0] +'): '+ str(price)
                label2_text = ' '
                
            else:
                duration_real = self.total['total_real_'+filter_text]
                duration_planned = self.total['total_planned_'+filter_text]
                label1_text = 'Total Duration Real'+'('+ self.all_item[0] +'): '+ str(duration_real)
                label2_text = 'Total Duration Planned'+'('+ self.all_item[0] +'): ' + str(duration_planned)
            
            
            self.label1 = QLabel(label1_text)
            self.label2 = QLabel(label2_text)

            combo = QComboBox()
            for i in self.all_item:
                combo.addItem(i)

            # show table button create
            self.siglum_frame = (self.frame.loc[self.frame['Siglum'] == self.all_item[0]]) 
            show_table_btn = QPushButton('Show Table')
            show_table_btn.clicked.connect(self.show_table)

            self.h_layout = QHBoxLayout()
            h_v_layout = QVBoxLayout()
            h_v_layout.addWidget(combo)
            h_v_layout.addWidget(show_table_btn)
            h_v_layout.addWidget(self.label1)
            h_v_layout.addWidget(self.label2)
            self.h_layout.addLayout(h_v_layout)

            frame1 = QFrame()
            self.m = PlotCanvas(self, width=5, height=4, sheet_name = self.sheet_name, item=self.all_item[0], total=self.total)
            
            frame1.setFrameShape(QFrame.StyledPanel)
            
            self.h_layout.addWidget(self.m)
            self.h_layout.addWidget(frame1)
            
            self.v_layout.addLayout(self.h_layout)

            combo.activated[str].connect(self.onActivated) 


    def onActivated(self, text):
        filter_text = text.replace(' ','_')
        
        if self.sheet_name == 'Po Status':
            price = self.total['total_'+filter_text]
            label1_text = ' Total Price'+'('+ text +'): '+ str(price)
            label2_text = ' '
                
        else:
            duration_real = self.total['total_real_'+filter_text]
            duration_planned = self.total['total_planned_'+filter_text]
            label1_text = 'Total Duration Real'+'('+ text +'): '+ str(duration_real)
            label2_text = 'Total Duration Planned'+'('+ text +'): ' + str(duration_planned)
        
        self.m.close()
        self.m = PlotCanvas(self, width=5, height=4, sheet_name = self.sheet_name, item=text, total=self.total)
        self.h_layout.addWidget(self.m)
        self.siglum_frame = (self.frame.loc[self.frame['Siglum'] == text]) 
        
        self.label1.setText(label1_text)
        self.label1.adjustSize()
        self.label2.setText(label2_text)
        self.label2.adjustSize()
    

    def show_table(self):
        row_size,col_size = self.siglum_frame.shape

        column_names =  list(self.siglum_frame.keys())
        row_values_obj = self.siglum_frame

        table_obj = TableWindow(row_values_obj, column_names, row_size, col_size)
        if table_obj.exec_():
            table_obj.quit()
  
  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
