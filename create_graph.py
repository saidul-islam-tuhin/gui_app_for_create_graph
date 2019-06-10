# -*- coding: utf-8 -*-

import random

import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFrame, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100, sheet_name='', item='', total={}):
        """[Create plot graph]
        
        Keyword Arguments:
            sheet_name {str} -- [Name of the sheet] (default: {''})
            item {str} -- [item name] (default: {''})
            total {dict} -- [total price of every item in this sheet ] (default: {{}})
        """
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.sheet_name = sheet_name
        self.item = item
        self.total = total
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.plot()
 
 
    def plot(self):

        filter_text = self.item.replace(' ','_')

        if self.sheet_name == 'Po Status':
            data = [random.random() for i in range(25)]
            ax = self.figure.add_subplot(111)
            ax.plot(data, 'r-')
            ax.set_title('Po Status Example')
            self.draw()
        else:
            n_groups = 1

            duration_real = int(self.total['total_real_'+filter_text])
            duration_planned = int(self.total['total_planned_'+filter_text])
            means_real = (duration_real,)
            means_planned = (duration_planned,)
            
            # create plot
            ax = self.figure.add_subplot(111)
            
            index = np.arange(n_groups)
            bar_width = 0.35
            opacity = 0.8
            
            rects1 = ax.bar(index, means_real, bar_width,
                            alpha=opacity,
                            color='b',
                            label='Duration Real')
            
            rects2 = ax.bar(index + bar_width, means_planned, bar_width,
                            alpha=opacity,
                            color='g',
                            label='Duration Planned')
            
            ax.set_xlabel('Duration real and planned')
            ax.set_ylabel('Items')

            ax.set_title('Duration real vs Duration Planned')
            ax.set_xticks(index + bar_width, (self.item,))
            ax.legend()
            
            self.draw()
 

