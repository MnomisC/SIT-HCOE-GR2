import math
import numpy
import pygame

corner_counter = 0
CORNER_MAX = 10
MAX_DIR = math.pi/3
PRE_TANH_COEFF = 0.2
CORNER_WEIGHT = 0.0020
START_DIRECTION = -1
PART_BACKWARD = 2.5

def is_sorted(target,sortnum):
    for index,value in enumerate(target):
        if value[sortnum] < target[index-1][sortnum] and index != 0:
            return False
    return True
#factory
def get_points(point_data):
    points = [0] * len(point_data)

    points[0] = Point(float(point_data[1][1]-point_data[0][1]),*point_data[0])

    for i in xrange(1,len(point_data)-1):
        points[i] = Point(float(point_data[i+1][1]-point_data[i-1][1]),*point_data[i])

    last_point_data = len(point_data) -1
    points[last_point_data] = Point(float(point_data[last_point_data][1]-point_data[last_point_data-1][1]),*point_data[last_point_data])

    return points


class Point(object):
    def __init__(self,angle_dist,length,angle):
        self.angle = float(angle)
        self.length = float(length)
        self.angle_dist = abs(angle_dist)
        #print angle
        #creating a weight. Can be changed later

        self.weight = (1,-1)[self.angle < 0]*math.cos(self.angle)*self.angle_dist * 1/self.length**2
        #print self.angle,self.length,self.weight
        #print self.weight, self.angle


def run(point_data):
    """
    point_data: list of touples containing (length,angle)
    """
    global corner_counter
    if not is_sorted(point_data,1):
        sorted(point_data,key = lambda x:x[1])
    #They are now sorted
    points = get_points(point_data)
    direction = 0 #marks angel of direction
    #k = []
    #for i,v in enumerate(points):
    #    if v.weight > 0:
    #        k.append(i)
    #print k,len(k)
    #k = []
    #for i,v in enumerate(points):
    #    if v.weight < 0:
    #        k.append(i)
    #print k,len(k)
    #print len([x.weight for x in points if x.weight < 0]),len([x.weight for x in points if x.weight > 0])
    right = sum([x.weight for x in points if x.weight < 0])
    left =  sum([x.weight for x in points if x.weight > 0])

    nom = (abs(left),abs(right))[abs(left)<abs(right)]
    denom = (left,right)[abs(left)>abs(right)]
    direction = (nom/denom) * PRE_TANH_COEFF

    if left > CORNER_WEIGHT and right < -CORNER_WEIGHT and direction < 2*PRE_TANH_COEFF and corner_counter == 0: #determined by testing
        corner_counter = CORNER_MAX
        #pygame.time.wait(2000)
        #print corner_counter
    if corner_counter != 0:
        #its in a cornor
        if CORNER_MAX-corner_counter < CORNER_MAX/PART_BACKWARD:
            direction = math.pi
        else:
            direction = (math.pi- math.pi/2*(PART_BACKWARD/CORNER_MAX))*START_DIRECTION
        corner_counter -= 1
    else:
        direction = math.tanh(direction) * MAX_DIR
    #print direction
    return direction
if __name__ == '__main__':
    run([(1,-90),(1,-30)])
