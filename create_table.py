# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QVBoxLayout,
 		QTableWidget, QTableWidgetItem, QTableView)



class TableWindow(QDialog):
    def __init__(self, row_values_obj, column_names, row_size, col_size):
        super().__init__()
        self.row_values = row_values_obj
        self.column_names = column_names
        self.row = row_size
        self.col = col_size

        self.init_table()


    def init_table(self):
        
        self.setWindowTitle("Show Table")

        self.table = QTableWidget()

        # set row count
        self.table.setRowCount(self.row)

        # set column count
        self.table.setColumnCount(self.col)

        # table headline
        self.table.setHorizontalHeaderLabels(self.column_names)
	
	    # set row values
        for i in range(self.row):
            for j in range(self.col):
                self.table.setItem(i, j, QTableWidgetItem(str(self.row_values.iat[i, j])))
        
	    # Vertical layout
        self.v_lay = QVBoxLayout()
        self.setLayout(self.v_lay)

        self.v_lay.addWidget(self.table)

	    # set width and height of dialog
        dialogWidth = self.table.horizontalHeader().length() + 24
        dialogHeight= self.table.height()
        self.setFixedSize(dialogWidth, dialogHeight )
        
        self.move(500,100)

        self.show()


    def quit(self):
        self.destroy()

