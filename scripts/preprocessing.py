#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 16:50:27 2019

@author: weikaikong & zhentaohuang
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import sys


def read_coordinates(path,lane):
    coordinates = []
    try:
        file = open(path, "r")
    except FileNotFoundError:
        print("file is not found")
    else:
        line = file.readline()
        contents = file.readlines()
        list_coordinates = []

        for content in contents:
            if content[-1] == '\n':
                content = content[:-1]

            if (int(content[0]) == int(lane)):
                print('find Coordinates Data!')
                coordinates = content.split(',')
                coordinates = coordinates[1:]

        for i in range(len(coordinates)):
            coordinates[i] = float(coordinates[i])

        file.close()
    return coordinates


def checksection(list_x,list_z,list_t,coordinates):
    # coordinates_4 = [184.000,226.478,958.492,15.679,751.653,42.478]
    if (len(list_x) != len(list_z)): 
        return -1

    sections = [0,0,0,0,0,0]    #starts and ends points

    #section 1: traffic light
    for i in range(len(list_z)):
        if (list_z[i] >= coordinates[0]):            #start from z < 184.0
            sections[1] = i
            break
        elif (i == len(list_z) - 1):        #if not find find the point
            sections[1] = -1

    turn_left = True    #is True if it turns left at the first corner
    #section 2: overtaking
    for i in range(sections[1],len(list_z)):
        if (list_z[i] >= coordinates[1]): #go straight
            sections[2] = i
            turn_left = False
            
            for j in range(sections[2],len(list_z)):
                if (list_z[j] >= coordinates[2]):
                    sections[3] = j
                    break
                elif (j == len(list_z) - 1): #if not find find the point
                    sections[3] = -1
                    print('1')
            
            break
        elif (list_x[i] > coordinates[3]):          #turn left at first corner
            sections[2] = i

            for j in range(sections[2],len(list_z)):
                if (list_x[j] >= coordinates[4]):
                    sections[3] = j
                    break
                elif (j == len(list_z) - 1): #if not find find the point
                    sections[3] = -1
            break        

    #section 3: following
    if (turn_left): #turn left at the first corner
        for i in range(sections[3],len(list_z)):
            if (list_z[i] >= coordinates[1]):
                sections[4] = i
                for j in range(sections[4],len(list_z)):
                    if (list_z[j] >= coordinates[2]):
                        sections[5] = j
                        break
                    elif (j == len(list_z) - 1): #if not find find the point
                        sections[5] = j
                    
                break
            elif (i == len(list_z) - 1): 
                sections[4] = -1
            
    else:   #go straight at the first corner
        for i in range(sections[3],len(list_z)):
            if (list_x[i] >= coordinates[3]):
                sections[4] = i
                for j in range(sections[4],len(list_z)):
                    if(list_x[j] >= coordinates[4]):
                        sections[5] = j
                        break
                    elif (j == len(list_z) - 1):
                        sections[5] = j
                break
            elif (i == len(list_z) - 1): 
                sections[4] = -1                #if not find find the point
                    
    return sections



def plot_map(list_x,list_z,sections,coordinates,lane):
    #coordinates_4 = [184.000,226.478,958.492,15.679,751.653,42.478]
    if (len(list_x) != len(list_z)):
        return -1

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(xlim=[-800,1700],ylim=[-250,1200])
    plt.scatter(list_z[sections[0]:sections[1]], list_x[sections[0]:sections[1]], marker='.', lineWidth=0.1,edgecolor='none')
    ax.plot(list_z[sections[0]:sections[1]], list_x[sections[0]:sections[1]], label='Section 1: Traffic Light')
    plt.scatter(list_z[sections[1]:sections[2]], list_x[sections[1]:sections[2]], marker='.', lineWidth=0.1,edgecolor='none', color='blue')
    ax.plot(list_z[sections[1]:sections[2]], list_x[sections[1]:sections[2]], color='blue')
    plt.scatter(list_z[sections[2]:sections[3]], list_x[sections[2]:sections[3]], marker='.', lineWidth=0.1,edgecolor='none')
    ax.plot(list_z[sections[2]:sections[3]], list_x[sections[2]:sections[3]], label='Section 2: Overtaking')
    plt.scatter(list_z[sections[3]:sections[4]], list_x[sections[3]:sections[4]], marker='.', lineWidth=0.1,edgecolor='none', color='blue')
    ax.plot(list_z[sections[3]:sections[4]], list_x[sections[3]:sections[4]], color='blue')
    plt.scatter(list_z[sections[4]:sections[5]], list_x[sections[4]:sections[5]], marker='.', lineWidth=0.1,edgecolor='none')
    ax.plot(list_z[sections[4]:sections[5]], list_x[sections[4]:sections[5]], label='Section 3: Following')
    plt.scatter(list_z[sections[5]:], list_x[sections[5]:], marker='.', lineWidth=0.1, edgecolor='none', color='blue')
    ax.plot(list_z[sections[5]:], list_x[sections[5]:], label='Movement Track', color='blue')
    ax.plot(np.linspace(coordinates[0],coordinates[0],1000),np.linspace(-250,1200,1000),color='black')
    ax.plot(np.linspace(coordinates[1],coordinates[1],1000),np.linspace(-250,1200,1000),color='black')
    ax.plot(np.linspace(coordinates[2]+coordinates[5],coordinates[2]+coordinates[5], 1000), np.linspace(-250, 1200, 1000), color='black')
    ax.plot(np.linspace(coordinates[2],coordinates[2],1000),np.linspace(-250,1200,1000),color='black')
    ax.plot(np.linspace(-800,1700,1000),np.linspace(coordinates[3],coordinates[3],1000),color='black')
    ax.plot(np.linspace(-800,1700,1000), np.linspace(coordinates[3]-coordinates[5],coordinates[3]-coordinates[5], 1000), color='black')
    ax.plot(np.linspace(-800,1700,1000), np.linspace(coordinates[4]+coordinates[5],coordinates[4]+coordinates[5], 1000), color='black')
    ax.plot(np.linspace(-800,1700,1000),np.linspace(coordinates[4],coordinates[4],1000),color='black')
    plt.title('OpenDS Scene Planform and Movement Track of Vehicle--' + str(lane) + ' lanes')
    plt.legend()
    plt.show()
            

def read_data(path):
    lane = 0
    try:
        file=open(path,"r")
    except FileNotFoundError:         
        print("file is not found")
    else:
        line=file.readline()
        print(line)
        for everyChar in line:
            if (everyChar == '4'):
                lane = 4
                break
            else:
                lane = 8
                
        contents=file.readlines()[4:]      
        print("find Car Data!")
        list_x = [] 
        list_z = []
        list_v = [] #list of speed (km/h)
        list_t = [] #list of time (ms)
        list_distance_ahead = [] #distance ahead(meters)
        for content in contents:
            t = content.split(':')[0]
            x = content.split(':')[1]
            z = content.split(':')[3]
            v = content.split(':')[8]
            distance_ahead = content.split(':')[13]
            list_t.append(int(t))
            list_x.append(float(x))
            list_z.append(float(z))
            list_v.append(float(v))
            list_distance_ahead.append(float(distance_ahead))
        file.close()

        return list_x,list_z,list_v,list_t,list_distance_ahead,lane


def save_data(list_x,list_z,list_v,list_t,list_distance_ahead,sections,lane):
    
     
    list_s = [0] #list of distance (meters)
    list_a = [0] #list of acceleration (m/s^2)

    for i in  range(len(list_x) - 1):
        x1 = list_x[i]
        x2 = list_x[i + 1]
        z1 = list_z[i]
        z2 = list_z[i + 1]
        v1 = list_v[i] / 3.6      #convert to m/s
        v2 = list_v[i + 1] /3.6
        t1 = list_t[i] / 100      #convert to seconds
        t2 = list_t[i + 1] / 100  
        s = math.sqrt((x1-x2)*(x1-x2) + (z1-z2)*(z1-z2)) + list_s[i]
        a = abs(v2 - v1) / (t2 - t1)
        list_s.append(s)    #store the distance (m) to list_s
        list_a.append(a)    #store the acceleration (m/s^2) to list_a
    
    with open('section_1.txt', 'a') as month_file: #store the data into "positions.txt"
        month_file.write('Time (ms):Distance (meters): Speed (km/h) : Acceleration (m/s^2): Distance Ahead (meters) \n')
        for i in range(sections[1]):
            month_file.write(str(list_t[i]))
            month_file.write(':')
            month_file.write(str(list_s[i]))
            month_file.write(':')
            month_file.write(str(list_v[i]))
            month_file.write(':')
            month_file.write(str(list_a[i]))
            month_file.write(':')
            month_file.write(str(list_distance_ahead[i]))
            month_file.write('\n')

    with open('position_1.txt', 'a') as month_file: #store the data into "positions.txt"
        month_file.write('%d %s Position(x,z) \n' %(lane,'lane'))
        for i in range(sections[1]):
            month_file.write(str(list_x[i]))
            month_file.write(':')
            month_file.write(str(list_z[i]))
            month_file.write('\n')

    with open('section_2.txt', 'a') as month_file: #store the data into "positions.txt"
        month_file.write('Time (ms): Distance (meters): Speed (km/h) : Acceleration (m/s^2): Distance Ahead (meters) \n')
        for i in range(sections[2],sections[3]):
            month_file.write(str(list_t[i]))
            month_file.write(':')
            month_file.write(str(list_s[i]))
            month_file.write(':')
            month_file.write(str(list_v[i]))
            month_file.write(':')
            month_file.write(str(list_a[i]))
            month_file.write(':')
            month_file.write(str(list_distance_ahead[i]))
            month_file.write('\n')

    with open('position_2.txt', 'a') as month_file: #store the data into "positions.txt"
        month_file.write('%d %s Position(x,z) \n' %(lane,'lane'))
        for i in range(sections[2],sections[3]):
            month_file.write(str(list_x[i]))
            month_file.write(':')
            month_file.write(str(list_z[i]))
            month_file.write('\n')
        

    with open('section_3.txt', 'a') as month_file: #store the data into "positions.txt"
        month_file.write('Time (ms): Distance (meters): Speed (km/h) : Acceleration (m/s^2): Distance Ahead (meters) \n')
        for i in range(sections[4],sections[5]):
            month_file.write(str(list_t[i]))
            month_file.write(':')
            month_file.write(str(list_s[i]))
            month_file.write(':')
            month_file.write(str(list_v[i]))
            month_file.write(':')
            month_file.write(str(list_a[i]))
            month_file.write(':')
            month_file.write(str(list_distance_ahead[i]))
            month_file.write('\n')

    with open('position_3.txt', 'a') as month_file: #store the data into "positions.txt"
        month_file.write('%d %s Position(x,z) \n' %(lane,'lane'))
        for i in range(sections[4],sections[5]):
            month_file.write(str(list_x[i]))
            month_file.write(':')
            month_file.write(str(list_z[i]))
            month_file.write('\n')
        
    return 0

def main():
    #usage: python preprocessing.py
    list_x,list_z,list_v,list_t,list_distance_ahead,lane = read_data(path = sys.argv[1])
    #'C:\\Users\\q4349\\Desktop\\827\\analyzerData\\analyzerData\\p2\\2019_08_12-12_26_49\\carData_track1.txt'
    coordinates = read_coordinates('coordinates.txt', lane)

    if (lane == 4):
        sections = checksection(list_x,list_z,list_t,coordinates)
        plot_map(list_x,list_z,sections,coordinates,lane)
    else:
        sections = checksection(list_x,list_z,list_t,coordinates)
        plot_map(list_x,list_z,sections,coordinates,lane)
    print(sections)
    save_data(list_x,list_z,list_v,list_t,list_distance_ahead,sections,lane)


main()
