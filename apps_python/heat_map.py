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

from norfair.tracker import TrackedObject
from norfair import Detection


class HeatMap:
    """
    Generate heatmap based on history of all detected objects.
    """
    
    def __init__(
                self,
                shape,
                radius: Optional[int] = 10,
        ):
        self.radius = radius
        self.map_shape = shape
        self.map = np.zeros(self.map_shape)
        self.map_gray = np.zeros((self.map_shape[0],self.map_shape[1],1), np.uint8)
        self.map_color = np.zeros((self.map_shape[0],self.map_shape[1],3), np.uint8)

        # create gradient filled circel 
            # create circel
        self.circle_img = np.zeros((self.radius*2, self.radius*2))
            # draw circel with solid fill
        self.circle_img = cv2.circle(self.circle_img, (radius-1, radius-1), radius, 1, -1)
            # create gradient mask
        gradient_mask = np.zeros((self.radius*2, self.radius*2))
        for row in range(0, self.radius*2):
            for col in range(0, self.radius*2):
                current_point = (col,row)
                gradient_mask[row, col] = math.sqrt((self.radius - col)**2 + (self.radius - row)**2)

        gradient_mask = gradient_mask.max() - gradient_mask

        # multiply solid fill circel with gradient mask
        self.circle_img = self.circle_img * gradient_mask

        self.circle_img = cv2.normalize(self.circle_img,None, 0, 1, cv2.NORM_MINMAX)


    def update(self, objects):
        for obj in objects:

            x_circ1 = 0
            y_circ1 = 0

            x_circ2 = self.radius*2 - 1
            y_circ2 = self.radius*2 - 1

            if type(obj) == TrackedObject:
                point_center = tuple(np.mean(np.array(obj.estimate), axis=0).astype(int))
            elif type(obj) ==  Detection:
                point_center = tuple(np.mean(np.array(obj.points), axis=0).astype(int))
            else:
                return

            # point_cetner = point_center.astype(int)
            point_center = point_center[::-1]
            if point_center[0] >= self.map_shape[0] or point_center[0] < 0:
                print("return vertical")
                return
            if point_center[1] >= self.map_shape[1] or point_center[1] < 0:
                print("return horizontal")
                return
            
            # tuple(point.astype(int)),
            x_map1 = point_center[0] - self.radius
            y_map1 = point_center[1] - self.radius

            x_map2 = point_center[0] + self.radius -1
            y_map2 = point_center[1] + self.radius -1

            if x_map1 < 0:
                x_circ1 = abs(x_map1)
                x_map1 = 0
            elif x_map2 >= self.map_shape[0]:
                x_circ2 = x_circ2 - (x_map2 - self.map_shape[0]) -1
                x_map2 = self.map_shape[0] -1

            if y_map1 < 0:
                y_circ1 = abs(y_map1)
                y_map1 = 0
            elif y_map2 >= self.map_shape[1]:
                y_circ2 = y_circ2 - (y_map2 - self.map_shape[1]) -1
                y_map2 = self.map_shape[1] -1

            self.map[x_map1:x_map2, y_map1:y_map2] = self.map[x_map1:x_map2, y_map1:y_map2] + self.circle_img[x_circ1:x_circ2, y_circ1:y_circ2]

        # apply color map
    def draw(self, frame, reseize):

        self.map_gray  = cv2.normalize(self.map,None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        self.map_gray = cv2.equalizeHist(self.map_gray)

        self.map_color = cv2.cvtColor(cv2.applyColorMap(self.map_gray.astype(np.uint8), cv2.COLORMAP_JET), cv2.COLOR_RGB2BGR)
        self.map_color = cv2.addWeighted(src1=frame, src2=self.map_color, alpha=0.5, beta=0.5, gamma=0)
        org_shape = frame.shape
        org_row_col = (org_shape[0], org_shape[1])

        if reseize == org_row_col:
            return self.map_color
        else:
            return cv2.resize(self.map_color,reseize)