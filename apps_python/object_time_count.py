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
from typing import Callable, Optional, Sequence, Tuple
import numpy as np
import cv2
import math
from time import time
from norfair.tracker import TrackedObject
from norfair.drawing.color import Palette


class ObjectTimeCount:
    """
    Count still time and moving time for each tracket object.
    """
    
    def __init__(
                self,
                stand_time_hit: Optional[int] = 10,
        ):
        
        # Time object not moving in seconds before considered standing or setting.
        self.stand_time_hit = stand_time_hit

        # Initialized dictionary lists for 
        self.current_object_time = dict()   # Time of objects currently in frame      
        self.history_object_time = dict()   # Time of history objects i.e no longer in frame


    def update(
            self,
            tracked_objects: Sequence[TrackedObject]
    ):

        current_time = time()
        list_id = []
        # update time list
        for obj in tracked_objects:
            list_id.append(obj.id)
            if obj.id in self.current_object_time:
                self.current_object_time[obj.id].add_time(current_time, obj.estimate)
            else:
                self.current_object_time[obj.id] = ObjectTime(obj.id, obj.estimate,current_time, self.stand_time_hit)
                
            # add/update object in current object time to history    
            self.history_object_time[obj.id] = self.current_object_time[obj.id]

        # keep only new or update objects and delete the rest from the current_object_time.
        # Note: A copy of all objects already saved in the history.
        self.current_object_time = {key: self.current_object_time[key] 
            for key in self.current_object_time if key in list_id}
            
        # set current time as previous time for the next update
       
    def draw_time(self, frame, text_size, text_thickness):
        """
        Overlay time count data on each tracket object.
        Parameters:
            frame (numpy array): a three dimensional array representing the frame (image).
            text_size:
            text_thickness:
        Returns:
            numpy array: a three dimensional array of the frame with timeing data.
        """

        for key in self.current_object_time:

            text = self.format_time(self.current_object_time[key].total_time)

            if self.current_object_time[key].is_still:
                text_still = self.format_time(self.current_object_time[key].still_time)
                text = "{}/{}".format(text_still, text)
            
            text_color = (0,0,0)
            text_color = Palette.choose_color(key)

            box = self.current_object_time[key].prev_bbox

            coordinates = np.mean(np.array(box), axis=0)

            (text_w, text_h),_ = cv2.getTextSize(str(text), cv2.FONT_HERSHEY_SIMPLEX, text_size, text_thickness)

            coordinates[0] = int(coordinates[0] - text_w/2)

            _,frame_width,_ = frame.shape

            coordinates[0] = min(frame_width-text_w,coordinates[0])

            coordinates[0] = max(0,coordinates[0])

            coordinates[1] = int(box[0,1])


            cv2.putText(
            frame,
            text,
            (coordinates.astype(int)),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            text_color,
            text_thickness
            )
           

        # return frame
    
    def format_time(self, time_sec):
        """
        Input is time in seconds,
        Output is string of the time formatted as hh:mm:ss
        """
        time_sec = math.floor(time_sec)
        h, reminder = divmod(time_sec, 3600)
        m, s = divmod(reminder, 60)
        if h == 0:
            text = "{:02}:{:02}".format(m, s)
        else:
            text = "{}:{:02}:{:02}".format(h, m, s)

        return text

    def get_time_history(self):
        
        total_time_array = []
        still_time_array = []

        for key in self.history_object_time:
            total_time_array.append(self.history_object_time[key].total_time)
            for elem in self.history_object_time[key].still_time_history:
                still_time_array.append(elem)

        return total_time_array, still_time_array

    def get_occupancy(self):
        current_occupancy = len(self.current_object_time)
        if self.history_object_time:
            total_vistors = max(self.history_object_time.keys())
        else:
            total_vistors = 0

        return current_occupancy,total_vistors

class ObjectTime:
    """
    Object used for time related information about object including total in frame and total standing duration.
    """
    
    def __init__(self, id, bbox,init_time, stand_time_hit):
        self.BBOX_OVERLAP_THRESHOLD = 0.8
        self.STILL_TIME_THRESHOLD = stand_time_hit
        self.id = id
        self.prev_time = init_time
        self.total_time = 0
        self.still_time = 0
        self.still_time_history = []
        self.prev_bbox = bbox
        self.prev_area = self.area(bbox)
        self.is_still = False

    def add_time(self, time, bbox):

        # add current duration time to total time.
        time_dur = time - self.prev_time
        self.prev_time = time

        # add total time.
        self.total_time += time_dur
        
        # Process still time based on overlapped bounding boxes
        # opject is still if the overlap between current bounding box and previous bounding box is grater then BBOX_OVERLAP_THRESHOLD
        overlapped_area = self.overlap_area(self.prev_bbox ,bbox)

        if overlapped_area/self.prev_area > self.BBOX_OVERLAP_THRESHOLD:
            self.still_time += time_dur
            if self.still_time > self.STILL_TIME_THRESHOLD:
                if self.is_still:
                    self.still_time_history[-1] = self.still_time 
                else:
                    self.still_time_history.append(self.still_time)
                    self.is_still = True
        else:
            self.prev_bbox = bbox
            self.prev_area = self.area(bbox)
            self.still_time = 0
            self.is_still = False


    def area(slef, bbox):
        return (bbox[1,0]-bbox[0,0]) * (bbox[1,1]-bbox[0,1])
    
    def overlap_area(self, bbox1, bbox2):
        # get the top left point of the overlapped area
        
        top_left_point_x = max(bbox1[0,0], bbox2[0,0])
        top_left_point_y = max(bbox1[0,1], bbox2[0,1])

        # get the bottom right point of the overlapped area
        bottom_rigth_point_x = min(bbox1[1,0], bbox2[1,0])
        bottom_rigth_point_y = min(bbox1[1,1], bbox2[1,1])

        return (bottom_rigth_point_x - top_left_point_x) * (bottom_rigth_point_y - top_left_point_y)
