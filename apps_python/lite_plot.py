import numpy as np
import warnings
import math
import cv2


class LitePlot:
    """
    Plot based on CV2.
    """
    
    def __init__(self, h, w, color=(255,255,255), title=None, xlabel=None, ylabel=None, text_color = (0,0,0), margins=None, ticks=None, boarders=None):
        self.h = h
        self.w = w

        self.color = color
        self.text_color = text_color


        # title
        self.title_text = None
        self.title_loc = 'center'
        self.title_bot_margin = 0
        self.title_text_color = text_color
        self.title_text_size = 1
        self.title_text_thick = 2
        self.title_text_font = cv2.FONT_HERSHEY_DUPLEX
        if title is not None:
            for key in title:
                match key:
                    case 'text':
                        self.title_text = title[key]
                    case 'loc':
                        self.title_loc = title[key]
                    case 'bot_margin':
                        self.title_bot_margin = title[key]
                    case 'text_color':
                        self.title_text_color = title[key]
                    case 'text_size':
                        self.title_text_size = title[key]
                    case 'text_thick':
                        self.title_text_thick = title[key]
                    case 'text_font':
                        self.title_text_font = title[key]
                    case _ :
                        warnings.warn("Unkown key ", key, " for title properties. The default value is used.")

        # xlabel
        self.xlabel_text = None
        self.xlabel_loc = 'center'
        self.xlabel_top_margin = 0
        self.xlabel_text_color = text_color
        self.xlabel_text_size = 0.3
        self.xlabel_text_thick = 1
        self.xlabel_text_font = cv2.FONT_HERSHEY_DUPLEX
        if xlabel is not None:
            for key in xlabel:
                match key:
                    case 'text':
                        self.xlabel_text = xlabel[key]
                    case 'loc':
                        self.xlabel_loc = xlabel[key]
                    case 'top_margin':
                        self.xlabel_top_margin = xlabel[key]
                    case 'text_color':
                        self.xlabel_text_color = xlabel[key]
                    case 'text_size':
                        self.xlabel_text_size = xlabel[key]
                    case 'text_thick':
                        self.xlabel_text_thick = xlabel[key]
                    case 'text_font':
                        self.xlabel_text_font = xlabel[key]
                    case _ :
                        warnings.warn("Unkown key ", key, " for xlabel properties. The default value is used.")

        # ylabel
        self.ylabel_text = None
        self.ylabel_loc = 'center'
        self.ylabel_right_margin = 0
        self.ylabel_text_color = text_color
        self.ylabel_text_size = 1
        self.ylabel_text_thick = 1
        self.ylabel_text_font = cv2.FONT_HERSHEY_DUPLEX
        if ylabel is not None:
            for key in ylabel:
                match key:
                    case 'text':
                        self.ylabel_text = ylabel[key]
                    case 'loc':
                        self.ylabel_loc = ylabel[key]
                    case 'right_margin':
                        self.ylabel_right_margin = ylabel[key]
                    case 'text_color':
                        self.ylabel_text_color = ylabel[key]
                    case 'text_size':
                        self.ylabel_text_size = ylabel[key]
                    case 'text_thick':
                        self.ylabel_text_thick = ylabel[key]
                    case 'text_font':
                        self.ylabel_text_font = ylabel[key]
                    case _ :
                        warnings.warn("Unkown key ", key, " for ylabel properties. The default value is used.")

        
        # margins
        self.margin_left = 10
        self.margin_right = 10
        self.margin_bottom = 5
        self.margin_top = 5
        if margins is not None:
            for key in margins:
                match key:
                    case 'left':
                        self.margin_left = margins[key]
                    case 'rigth':
                        self.margin_left = margins[key]
                    case 'top':
                        self.margin_top = margins[key]
                    case 'bottom': 
                        self.margin_bottom = margins[key]
                    case _ :
                        warnings.warn("Unkown key ", key, " for plot margin. The default value is used.")

        # boarders
        if boarders is None:
            self.boarder_left = True
            self.boarder_right = True
            self.boarder_bottom = True
            self.boarder_top = True
        else: 
            self.boarder_left = False
            self.boarder_right = False
            self.boarder_bottom = False
            self.boarder_top = False
            for key in boarders:
                match key:
                    case 'left':
                        self.boarder_left = boarders[key]
                    case 'rigth':
                        self.boarder_left = boarders[key]
                    case 'top':
                        self.boarder_top = boarders[key]
                    case 'bottom': 
                        self.boarder_bottom = boarders[key]
                    case _ :
                        warnings.warn("Unkown key ", key, " for plot boarder. The default False is used.")

        
        # ticks
        self.tick_mark_len = 4
        self.tick_mark_thick = 1
        self.tick_mark_color = text_color
        self.tick_text_color = text_color
        self.tick_text_size = 0.5
        self.tick_text_thick = 1
        self.tick_text_font = cv2.FONT_HERSHEY_DUPLEX
        if ticks is not None:
            for key in ticks:
                match key:
                    case 'mark_len':
                        self.tick_mark_len = ticks[key]
                    case 'mark_thick':
                        self.tick_mark_thick = ticks[key]
                    case 'mark_color': 
                        self.tick_mark_color = ticks[key]
                    case 'text_color':
                        self.tick_text_color = ticks[key]
                    case 'text_size':
                        self.tick_text_size = ticks[key]
                    case 'text_thick':
                        self.tick_text_thick = ticks[key]
                    case 'text_font':
                        self.tick_text_font = ticks[key]
                    case _ :
                        warnings.warn("Unkown key ", key, " for ticks properties. The default value is used.")


    def mist(self, x, bins=None, range=None, density=False, weights=None,
                cumulative=False, bottom=None, histtype='bar', align='mid',
                orientation='vertical', rwidth=None, log=False,
                color=None, label=None, stacked=False, **kwargs):
        print(x)


    # draw histogram    
    def hist(self, x, bins=None, yrange=None, color=None,rwidth=None):  

        if color is None:
            bar_colors = (255, 179, 179)
        else:
            bar_colors = color

        if bins is None:
            bins = 'auto'

        if rwidth is None:
            rwidth = 1
        
        if yrange is None:
            yrange = (min(x),max(x))


        # basic dimentions calculations
        # title hight
        if self.title_text is not None:
            (text_w, text_h),_ = cv2.getTextSize(self.title_text, self.title_text_font, self.title_text_size, self.title_text_thick)
            title_h = text_h + self.title_bot_margin
            title_w = text_w
        else:
            title_h = 0
            title_w = 0

        # xlabel
        xlabel_h = 0
        xlabel_w = 0
        if self.xlabel_text is not None:
            if self.xlabel_loc not in ['side_right', 'side_left']:
                (text_w, text_h),_ = cv2.getTextSize(self.xlabel_text, self.xlabel_text_font, self.xlabel_text_size, self.xlabel_text_thick)
                xlabel_h = text_h + self.xlabel_top_margin
                xlabel_w = text_w
            

        # ylabel
        if self.ylabel_text is not None:
            (text_w, text_h),_ = cv2.getTextSize(self.ylabel_text, self.ylabel_text_font, self.ylabel_text_size, self.ylabel_text_thick)
            ylabel_h = text_h + self.ylabel_right_margin
            ylabel_w = text_w
        else:
            ylabel_h = 0
            ylabel_w = 0


        # tiks
        # assuming two characters for y ticks. If text over flow, change plot left margin
        (text_w, text_h),_ = cv2.getTextSize('XX', self.tick_text_font, self.tick_text_size, self.tick_text_thick)
        y_tick_w = text_w + self.tick_mark_len
        x_tick_h = text_h + self.tick_mark_len

        

        # plot
        plot_h = self.h - self.margin_bottom - self.margin_top - title_h - x_tick_h - xlabel_h
        plot_y_start = self.margin_top + title_h

        plot_w = self.w - self.margin_right - self.margin_left -y_tick_w - ylabel_h
        plot_x_start = self.margin_left + y_tick_w + ylabel_h


        back_ground_color = self.color
        text_color = self.text_color

        # Computer Histogram values and bin edges
        val, bin_edge = np.histogram(x,bins=bins, range=yrange)

        # Create Tickete
        ticket = self.create_image(self.h, self.w,back_ground_color)

        

#########################################################################################
##########       Draw tile
#########################################################################################
        # title 
        title_h = 0 # the total hieght taken by title including text and margin
        if self.title_text is not None:
            (text_w, text_h),_ = cv2.getTextSize(self.title_text, self.title_text_font, self.title_text_size, self.title_text_thick)
            match self.title_loc:
                case "left":
                    text_x = plot_x_start
                case "center":
                    text_x = int(plot_x_start + plot_w/2 - text_w/2)
                    
                case "right":
                    text_x = self.w - self.margin_right - text_w

            text_bottom = self.margin_top + text_h       
            cv2.putText(ticket, self.title_text,(text_x,text_bottom) , self.title_text_font, self.title_text_size,self.title_text_color, self.title_text_thick)

#########################################################################################
##########       Draw plot
#########################################################################################

       
        # color palette for the bars

        # normalize values
        if max(val) > 0:
            norm_val = [float(i)/max(val) for i in val]
        else:
            norm_val = val

        top_number_h = 40
        max_bar_h = plot_h
        bar_w = plot_w/len(val)

        for i in range(len(val)):
            bar_h = int(max_bar_h * norm_val[i])
            # draw bar
            xc = plot_x_start + bar_w/2 + i * bar_w
            x1 = int(xc - bar_w*rwidth/2)
            x2 = int(xc + bar_w*rwidth/2)
            y1 = int(plot_y_start + (plot_h - bar_h))
            y2 = int(plot_y_start + plot_h)

            cv2.rectangle(ticket, (x1, y1), (x2, y2), bar_colors, -1)

            # add number above bar
            # (text_w, text_h),_ = cv2.getTextSize(str(val[i]), cv2.FONT_HERSHEY_DUPLEX, 1, 2)
            # text_start = x1 + int((bar_w - text_w)/2)
            # cv2.putText(ticket, str(val[i]),(text_start,y1-5) , cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 2)

#########################################################################################
##########       Draw tick / lables
#########################################################################################

        # draw y_tick
        max_bin = max(val)
        y_tick_setp,r = divmod(max_bin, 4)
        y_tick_setp +=1
        y_tick = np.arange(0,y_tick_setp*4, y_tick_setp)

        y_tick_max = y_tick.max()
        y_tick_norm = y_tick / y_tick_max

        y_ticks = ["%.0f" % number for number in y_tick]

        text_bottom = self.h - self.margin_bottom
        y_tick_h = plot_h/(len(y_tick)-1)
        for i in range(len(y_tick)):
            yc = int(math.ceil(plot_y_start +  (1 -y_tick_norm[i]) * plot_h))


            (text_w, text_h),_ = cv2.getTextSize(y_ticks[i], self.tick_text_font, self.tick_text_size, self.tick_text_thick)
            text_x = int(plot_x_start - self.tick_mark_len - text_w)
            text_bottom = int(yc + (text_h/2))
            cv2.putText(ticket, y_ticks[i],(text_x,text_bottom) , self.tick_text_font, self.tick_text_size, self.tick_text_color, self.tick_text_thick)

            # tick mark
            x1 = plot_x_start
            x2 = plot_x_start - self.tick_mark_len
            cv2.line(ticket,(x1, yc), (x2, yc), self.tick_mark_color, self.tick_mark_thick)
        

    
        # draw x ticks
        ticks = ["%.0f" % number for number in bin_edge]
        text_bottom = plot_y_start + plot_h + x_tick_h
        tick_w = plot_w/(len(ticks)-1)
        for i in range(len(ticks)):
            xc = int(plot_x_start+ i * tick_w)
            for j, line in enumerate(ticks[i].split(' ')):
                (text_w, text_h),_ = cv2.getTextSize(line, self.tick_text_font, self.tick_text_size, self.tick_text_thick)
                text_x = int(xc - text_w/2)
                cv2.putText(ticket, line,(text_x,text_bottom) , self.tick_text_font, self.tick_text_size, self.tick_text_color, self.tick_text_thick)

            # tick mark
                y1 = text_bottom- text_h 
                y2 = y1 - self.tick_mark_len
                cv2.line(ticket,(xc, y1), (xc, y2), self.tick_mark_color, self.tick_mark_thick)

        # draw x label
        if self.xlabel_text is not None:
            (text_w, text_h),_ = cv2.getTextSize(self.xlabel_text, self.xlabel_text_font, self.xlabel_text_size, self.xlabel_text_thick)
            match self.xlabel_loc:
                case "left":
                    text_x = plot_x_start
                case "center":
                    text_x = int(plot_x_start + plot_w/2 - text_w/2)
                case "right":
                    text_x = self.w - self.margin_right - text_w
                case "side_left":
                    text_x = plot_x_start - text_w - 10
                case "side_right":
                    text_x = plot_x_start + plot_w

            text_bottom = self.h - self.margin_bottom       
            cv2.putText(ticket, self.xlabel_text,(text_x,text_bottom) , self.xlabel_text_font, self.xlabel_text_size,self.xlabel_text_color, self.xlabel_text_thick)

        # draw y label
        if self.ylabel_text is not None:
            (text_w, text_h),_ = cv2.getTextSize(self.ylabel_text, self.ylabel_text_font, self.ylabel_text_size, self.ylabel_text_thick)
            match self.xlabel_loc:
                case "top":
                    text_x = plot_x_start
                case "center":
                    text_x = int(plot_x_start + plot_w/2 - text_w/2)
                case "bottom":
                    text_x = self.w - self.margin_right - text_w

            text_bottom = self.margin_left + xlabel_h       
            cv2.putText(ticket, self.ylabel_text,(text_x,text_bottom) , self.ylabel_text_font, self.ylabel_text_size,self.ylabel_text_color, self.ylabel_text_thick)



#########################################################################################
##########       Draw boarders
#########################################################################################
        # top
        if self.boarder_top:
            x1 = plot_x_start
            x2 = plot_x_start + plot_w
            y1 = plot_y_start
            y2 = plot_y_start
            cv2.line(ticket,(x1, y1), (x2, y2), self.tick_mark_color, self.tick_mark_thick)

        # bottom
        if self.boarder_bottom:
            x1 = plot_x_start
            x2 = plot_x_start + plot_w
            y1 = plot_y_start + plot_h
            y2 = plot_y_start + plot_h
            cv2.line(ticket,(x1, y1), (x2, y2), self.tick_mark_color, self.tick_mark_thick)

        # right
        if self.boarder_right:
            x1 = plot_x_start + plot_w
            x2 = plot_x_start + plot_w
            y1 = plot_y_start
            y2 = plot_y_start + plot_h
            cv2.line(ticket,(x1, y1), (x2, y2), self.tick_mark_color, self.tick_mark_thick)

        # left
        if self.boarder_left:
            x1 = plot_x_start
            x2 = plot_x_start
            y1 = plot_y_start
            y2 = plot_y_start + plot_h
            cv2.line(ticket,(x1, y1), (x2, y2), self.tick_mark_color, self.tick_mark_thick)



        return ticket
    
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
