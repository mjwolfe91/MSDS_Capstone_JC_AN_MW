import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Data
rawData = pd.read_csv('https://raw.githubusercontent.com/mjwolfe91/MSDS_Capstone_JC_AN_MW/master/Data/HAR_FALL-UP_CompleteDataSet.csv')

# Extract Wrist Sensor Data (Angular/Accelerometer) from each trial for every subject
# 17 subjects * 11 activities (ADL/Falls) * 3 trials = 561 trials
# Sensors set at sampling rate of ~18.4 Hz (18-20 Hz)
raw_WristSensor = rawData[['TimeStamps','WristAccelerometer', 'Unnamed: 30', 'Unnamed: 31', 'WristAngularVelocity', 'Unnamed: 33', 'Unnamed: 34','Subject', 'Activity', 'Trial']]
# Rename Columns
raw_WristSensor.rename(columns = {'TimeStamps':'TimeStamp', 'WristAccelerometer': 'Accelerometer (x)', 'Unnamed: 30':'Accelerometer (y)','Unnamed: 31':'Accelerometer (z)', 'WristAngularVelocity': 'Angular Velocity (x)', 'Unnamed: 33':'Angular Velocity (y)','Unnamed: 34':'Angular Velocity (z)'}, inplace = True)
# Change data types 
raw_WristSensor.TimeStamp = pd.to_datetime(raw_WristSensor.TimeStamp)
for col in ['Accelerometer (x)','Accelerometer (y)','Accelerometer (z)','Angular Velocity (x)','Angular Velocity (y)','Angular Velocity (z)']:
    raw_WristSensor[col] = pd.to_numeric(raw_WristSensor[1:][col])
#raw_WristSensor.dtypes

# Magntiude of Accelerometer and Gyroscope sensors
a_mag = np.sqrt(raw_WristSensor['Accelerometer (x)']**2 + raw_WristSensor['Accelerometer (y)']**2 + raw_WristSensor['Accelerometer (z)']**2)
w_mag = np.sqrt(raw_WristSensor['Angular Velocity (x)']**2 + raw_WristSensor['Angular Velocity (y)']**2 + raw_WristSensor['Angular Velocity (z)']**2)
raw_WristSensor.insert(10, 'Acceleration Magntiude', a_mag)
raw_WristSensor.insert(11, 'Angular Velocity Magntiude', w_mag)


# Aggregate Wrist Sensor data by Subjects
WristS_Subjects = {}

for s in np.unique(raw_WristSensor.Subject[1:]):
    WristS_Subjects["S{0}".format(int(s))] = []

for i, row in raw_WristSensor[1:].iterrows():
    if raw_WristSensor.Subject[i] == 1:
        WristS_Subjects['S1'].append(row)
    elif raw_WristSensor.Subject[i] == 2:
        WristS_Subjects['S2'].append(row)
    elif raw_WristSensor.Subject[i] == 3:
        WristS_Subjects['S3'].append(row)
    elif raw_WristSensor.Subject[i] == 4:
        WristS_Subjects['S4'].append(row)
    elif raw_WristSensor.Subject[i] == 5:
        WristS_Subjects['S5'].append(row)
    elif raw_WristSensor.Subject[i] == 6:
        WristS_Subjects['S6'].append(row)
    elif raw_WristSensor.Subject[i] == 7:
        WristS_Subjects['S7'].append(row)
    elif raw_WristSensor.Subject[i] == 8:
        WristS_Subjects['S8'].append(row)
    elif raw_WristSensor.Subject[i] == 9:
        WristS_Subjects['S9'].append(row)
    elif raw_WristSensor.Subject[i] == 10:
        WristS_Subjects['S10'].append(row)
    elif raw_WristSensor.Subject[i] == 11:
        WristS_Subjects['S11'].append(row)
    elif raw_WristSensor.Subject[i] == 12:
        WristS_Subjects['S12'].append(row)
    elif raw_WristSensor.Subject[i] == 13:
        WristS_Subjects['S13'].append(row)
    elif raw_WristSensor.Subject[i] == 14:
        WristS_Subjects['S14'].append(row)
    elif raw_WristSensor.Subject[i] == 15:
        WristS_Subjects['S15'].append(row)
    elif raw_WristSensor.Subject[i] == 16:
        WristS_Subjects['S16'].append(row)
    elif raw_WristSensor.Subject[i] == 17:
        WristS_Subjects['S17'].append(row)

# Change lists to numpy array
# Column idx of numpy array [0:Timestamp, 1: Accelerometer (x), 2: Accelerometer (y), 3: Accelerometer (z),
#                                         4: Angular Velocity (x), 5 Angular Velocity (y), 6: Angular Velocity (z)
#                                         7: Subject, 8: Activity, 9: Trial, 10: Acceleration Magntiude, 11: Angular Velcoity Magntiude]
for subject in WristS_Subjects.keys():
    WristS_Subjects[subject] = np.array(WristS_Subjects[subject])
    WristS_Subjects[subject] = np.reshape(WristS_Subjects[subject], (-1,12))

# Directory to Store Output
path = os.path.dirname(__file__)
output_dir = os.path.join(path,'output\\')
amag_path = 'plots\\MagntiudeRealizations\\Acceleration\\'
wmag_path = 'plots\\MagntiudeRealizations\\AngularVelocity\\'
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)
    for subject in WristS_Subjects.keys():
        os.makedirs(output_dir + amag_path + subject)
        os.makedirs(output_dir + wmag_path + subject)

# Acceleration Magnitude Plot
for subject in WristS_Subjects.keys():
    for activity in np.unique(WristS_Subjects[subject][:,8]):
        a = WristS_Subjects[subject][WristS_Subjects[subject][:,8] == activity]
        T1 = a[:,10][a[:,9] == 1]
        T2 = a[:,10][a[:,9] == 2]
        T3 = a[:,10][a[:,9] == 3]
        plt.figure()
        filename = '{} - Activity {}'.format(subject, int(activity))
        plt.title(filename)
        plt.ylabel('Acceleration Magntiude')
        if activity == 10:
            plt.xlabel('Time (30 second interval)')
        elif activity in [6,7,8,11]: 
            plt.xlabel('Time (60 second interval)')
        else:
            plt.xlabel('Time (10 second interval)')
        plt.plot(T1,'r',T2,'b',T3,'g')
        plt.gca().legend(('T1','T2','T3'))
        plt.savefig(output_dir + amag_path + subject + '\\' + filename, bbox_inches = 'tight')

# Angular Velocity Magnitude Plot
for subject in WristS_Subjects.keys():
    for activity in np.unique(WristS_Subjects['S1'][:,8]):
        w = WristS_Subjects[subject][WristS_Subjects[subject][:,8] == activity]
        T1 = w[:,11][w[:,9] == 1]
        T2 = w[:,11][w[:,9] == 2]
        T3 = w[:,11][w[:,9] == 3]
        plt.figure()
        filename = '{} - Activity {}'.format(subject, int(activity))
        plt.title(filename)
        plt.ylabel('Angular Velocity Magntiude')
        if activity == 10:
            plt.xlabel('Time (30 second interval)')
        elif activity in [6,7,8,11]: 
            plt.xlabel('Time (60 second interval)')
        else:
            plt.xlabel('Time (10 second interval)')
        plt.plot(T1,'r',T2,'b',T3,'g')
        plt.gca().legend(('T1','T2','T3'))
        plt.savefig(output_dir + wmag_path + subject + '\\' + filename, bbox_inches = 'tight')