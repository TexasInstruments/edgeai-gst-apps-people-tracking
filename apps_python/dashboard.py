 
#  Copyright (C) 2021 Texas Instruments Incorporated - http://www.ti.com/
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#    Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#
#    Neither the name of Texas Instruments Incorporated nor the names of
#    its contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
from lite_plot import LitePlot
import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2

from time import time

class Dashboard:
    """
    Create and update a graphical dashboard for object detection models. 
    The created dashboard consists of an over view, histogram graphs, and heatmap. 
    The overview contains two numbers: Total Vistors and Current Occupancy. 
    The two histogram show analysis of still time and total time.
    """
    def __init__(self, update_freq, heatmap_obj, timecount_obj):
        """
        Initialize dashboard. 
        Parameters:
            update_freq (int): The frequency at which the dashoard is updated.
            heatmap_obj (HeatMap): Object used to generate heatmap
            timecount_obj (ObjectTimeCount): Object used for time counting
        """

        # Constants
        self.dashboard_color = [22,17,58]       # RGB

        self.ticket_color = [39,41,83]

        self.text_color = [255, 255, 255]

        self.back_color = np.array([83, 39, 41]) / 255           # GBR

        self.bin_color_blue = (1,209,255)      # RGB

        self.bin_color_red = (166,0,0)         # RGB

        self.bin_color_green = (19,196,84)    # RGB

        self.size = [720,560]

        self.dashboard = self.create_image(self.size[0], self.size[1], self.dashboard_color)
        self.output_frame = self.create_image(720, 1840, self.dashboard_color)

        self.update_freq = update_freq

        self.heatMap = heatmap_obj

        self.timeCount = timecount_obj

        self.prev_time =  time()

        self.current_occupancy = 0
        self.total_vistors = 0

        self.fig, self.canvas, self.ax = self.plot_prepare()

        # initiate dashboard for the first time.
        self.init_dashboard()

    
    def init_dashboard(self):

        ticket_h = 70
        ticket_w = 265

        current_occupancy = 0
        total_vistors = 0
        # add current occupancy ticket
        self.dashboard[10:80, 285:550, :] = self.single_value_ticket(ticket_h, ticket_w, self.ticket_color, self.text_color, "Current Occupancy", current_occupancy)

        # add total visitors ticket
        self.dashboard[10:80, 10:275, :] = self.single_value_ticket(ticket_h, ticket_w, self.ticket_color, self.text_color, "Total Visitors", total_vistors)

        total_time_array = [0]
        still_time_array = [0]
   
        self.dashboard[90:240, 10:550, :] = self.hist_plot_test("Still Time", still_time_array, self.back_color, self.bin_color_green)

        self.dashboard[250:400, 10:550, :] = self.hist_plot_test("Total Time", total_time_array, self.back_color, self.bin_color_blue)

        self.dashboard[410:710, 10:550, :] = self.create_image(300, 540, self.ticket_color)

        return self.dashboard

    def update_dashboard(self, frame):

        ticket_h = 70
        ticket_w = 265

        current_occupancy,total_vistors = self.timeCount.get_occupancy()
        if self.current_occupancy != current_occupancy:
            self.current_occupancy = current_occupancy
            # add current occupancy teicket
            self.dashboard[10:80, 285:550, :] = self.single_value_ticket(ticket_h, ticket_w, self.ticket_color, self.text_color, "Current Occupancy", current_occupancy)
        
        if self.total_vistors !=  total_vistors:
            self.total_vistors = total_vistors
            # add total visitors ticket
            self.dashboard[10:80, 10:275, :] = self.single_value_ticket(ticket_h, ticket_w, self.ticket_color, self.text_color, "Total Visitors", total_vistors)

        current_time = time()

        if current_time - self.prev_time < self.update_freq:
            return self.dashboard

        self.prev_time = current_time

        total_time_array, still_time_array = self.timeCount.get_time_history()

        self.dashboard[90:240, 10:550, :] = self.hist_plot_test("Still Time", still_time_array, self.back_color, self.bin_color_green)

        self.dashboard[250:400, 10:550, :] = self.hist_plot_test("Total Time", total_time_array, self.back_color, self.bin_color_blue)
        

        resize = (540,300)

        self.dashboard[410:710, 10:550, :] = self.heat_map(frame, resize, title="Occupancy HeatMap", title_color=(255,255,255))

        return self.dashboard

    
    def single_value_ticket(self, h, w, back_color, text_color, title, value):
        """
        Create a ticket with a title and a value.
        Parameters:
            h (int): image height.
            w (int): image width.
            back_color (tuple): three integers representing the color as RGB for the ticket background.
            text_color (tuple): three integers representing the color as RGB for text.
            title (string): Ticket title to be shown in bold.
            value (float or int): Value to be shown on ticket.

        Returns:
            im (numpy array): an image representing the ticket
        """
        # Create ticket with solid color
        ticket = self.create_image(h, w, back_color)

        # add title
        for i, line in enumerate(title.split(' ')):

            (text_w, text_h),_ = cv2.getTextSize(line, cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
            x = 10
            y = int((i+1)*(text_h+5) + 10)
            cv2.putText(ticket, line,(x,y) , cv2.FONT_HERSHEY_DUPLEX, 0.8, text_color, 1)

        # add value 
        (text_w, text_h),_ = cv2.getTextSize(str(value), cv2.FONT_HERSHEY_DUPLEX, 2, 2)
        text_start = int(w-10 - text_w)
        y = int(text_h + (h - text_h)/2)
        cv2.putText(ticket, str(value),(text_start,y) , cv2.FONT_HERSHEY_DUPLEX, 2, text_color, 2)


        return ticket
    
    def heat_map(self, frame, resize, title=None, title_color=(0,0,0)):

        hm = self.heatMap.draw(frame, resize)

        # add title to heatmap
        if title is not None:
            (text_w, text_h),_ = cv2.getTextSize(title, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
            text_bottom = 10 + text_h
            cv2.putText(hm, title,(10,text_bottom) , cv2.FONT_HERSHEY_DUPLEX, 1, title_color, 2)

        return hm


    def hist_plot(self, title, data, back_color, bin_color):
        # make a Figure and attach it to a canvas.
        fig = Figure(figsize=(5.4, 1.5), dpi=100)
        fig.set_facecolor(back_color)
        fig.subplots_adjust(bottom=0.18, top=0.8)
        canvas = FigureCanvasAgg(fig)

        ax = fig.gca()
        # ax.set_adjustable
        if not data:
            bin_range = (0,60)
        else:
            bin_range = (0,max([60,max(data)]))

        n,_,_ = ax.hist(data, bins=12,range= bin_range, color=bin_color, rwidth=0.7)
        
        ax.set_title(title, loc='left', color='white', fontsize= 16, fontweight='bold')

        ax.set_xlabel("Time [Sec]", color='white', fontsize= 10)
        ax.xaxis.set_label_coords(-0.05,-0.08)


        ax.set_facecolor(self.back_color)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        ax.spines['left'].set_color('white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        max_bin = max(n)
        y_tick_setp,r = divmod(max_bin, 4)
        y_tick_setp +=1
        y_tick = np.arange(0,y_tick_setp*4, y_tick_setp)
        ax.set_yticks(y_tick)

        ax.margins(0.01)
        # Retrieve a view on the renderer buffer
        canvas.draw()
        buf = canvas.buffer_rgba()
        # convert to a NumPy array
        hist_img = np.asarray(buf)

        hist_img = cv2.cvtColor(hist_img, cv2.COLOR_RGB2BGR)

        
        return hist_img
    
    def create_image(self, h,w,color):
        """
        Create a colored image and fill it with a single color.
        Parameters:
            h (int): image height.
            w (int): image width.
            color (tuple): three integers representing the color as RGB.
        """
        image = np.zeros((h, w, 3), np.uint8)
        image[:] = color
        return image
    
    def hist_plot_test(self, title, data, back_color, bin_color):

        margin = {'left': 40, 'bottom': 5}
        tick_dict = {'text_size': 0.5}
        title_dict = {'text': title ,'text_size': 1, 'loc':'left', 'bot_margin': 10}
        boarder_dict = {'left':True, 'bottom': True}

        xlabel_dict = {'text': 'Time' ,'text_size': 0.6, 'text_thick':1, 'loc':'side_left', 'top_margin': 5}

        lp = LitePlot(150,540, title=title_dict,
                      xlabel=xlabel_dict,
                      color=self.ticket_color, 
                      text_color=(255,255,255),
                      margins=margin,
                      boarders=boarder_dict,
                      ticks=tick_dict)

        if not data:
            bin_range = (0,60)
        else:
            bin_range = (0,max([60,max(data)]))

        hist_ticket = lp.hist(data, bins = 12, yrange=bin_range, rwidth=0.7, color=bin_color)
    
        return hist_ticket
    

    def plot_prepare(self):
        # make a Figure and attach it to a canvas.
        fig = Figure(figsize=(5.4, 1.5), dpi=100)
        fig.set_facecolor(self.back_color)
        fig.subplots_adjust(bottom=0.18, top=0.8)
        canvas = FigureCanvasAgg(fig)

        ax = fig.gca()

        return fig, canvas, ax
    
    def add_dashboard(self, frame):
        self.output_frame[0:720,0:560,:] = self.dashboard
        self.output_frame[0:720, 560:1840, :] = frame
        return self.output_frame