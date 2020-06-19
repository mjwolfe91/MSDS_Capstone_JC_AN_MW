# Aggregate Wrist Sensor data by Activity
WristS_Activity = {}

for s in np.unique(raw_WristSensor.Activity[1:]):
    WristS_Activity["A{0}".format(int(s))] = []

for i, row in raw_WristSensor[1:].iterrows():
    if raw_WristSensor.Activity[i] == 1:
        WristS_Activity['A1'].append(row)
    elif raw_WristSensor.Activity[i] == 2:
        WristS_Activity['A2'].append(row)
    elif raw_WristSensor.Activity[i] == 3:
        WristS_Activity['A3'].append(row)
    elif raw_WristSensor.Activity[i] == 4:
        WristS_Activity['A4'].append(row)
    elif raw_WristSensor.Activity[i] == 5:
        WristS_Activity['A5'].append(row)
    elif raw_WristSensor.Activity[i] == 6:
        WristS_Activity['A6'].append(row)
    elif raw_WristSensor.Activity[i] == 7:
        WristS_Activity['A7'].append(row)
    elif raw_WristSensor.Activity[i] == 8:
        WristS_Activity['A8'].append(row)
    elif raw_WristSensor.Activity[i] == 9:
        WristS_Activity['A9'].append(row)
    elif raw_WristSensor.Activity[i] == 10:
        WristS_Activity['A10'].append(row)
    elif raw_WristSensor.Activity[i] == 11:
        WristS_Activity['A11'].append(row)

# Change lists to numpy array
# Column idx of numpy array [0:Timestamp, 1: Accelerometer (x), 2: Accelerometer (y), 3: Accelerometer (z),
#                                         4: Angular Velocity (x), 5 Angular Velocity (y), 6: Angular Velocity (z)
#                                         7: Subject, 8: Activity, 9: Trial, 10: Acceleration Magntiude, 11: Angular Velcoity Magntiude]
for activity in WristS_Activity.keys():
    WristS_Activity[activity] = np.array(WristS_Activity[activity])
    WristS_Activity[activity] = np.reshape(WristS_Activity[activity], (-1,12))



# Matplotlib Scatterplot EDA Visualization by Activity
%matplotlib inline
fig=plt.figure(figsize = (24,20))
ax=fig.add_axes([0,0,1,1])
colormap = {1:'red',2:'blue',3:'green',4:'red',5:'yellow',6:'pink',7:'purple',8:'orange',9:'grey',10:'cyan',11:'chocolate'}
sizemap = {1:50,2:50,3:50,4:50,5:50,6:25,7:25,8:25,9:25,10:25,11:25}
markermap = {1:'x',2:'x',3:'x',4:'x',5:'x',6:'.',7:'.',8:'.',9:'.',10:'.',11:'.'}
ax.scatter(y=cluster_thresholds["Max Angular Velocity Magnitude"], x=cluster_thresholds["Max Acceleration Magnitude"], c=cluster_thresholds['Activity'].apply(lambda x:colormap[x]), 
s=cluster_thresholds['Activity'].apply(lambda x:sizemap[x]))
ax.set_title("Maximum Magntiude Values per Trial")
ax.set_xlabel("Max Angular Velocity Magnitude")
ax.set_ylabel("Max Acceleration Magntiude")
plt.show()


# Seaborn Scaterplot EDA Visualization by Activity
sns.set(rc={'figure.figsize':(24,20)})
clusters = sns.scatterplot(x="Max Angular Velocity Magnitude", y="Max Acceleration Magnitude", hue=cluster_thresholds["Activity"].astype('category'), data=cluster_thresholds)
clusters.set_title("Maximum Magntiude Values per Trial")
clusters.set(xlabel="Max Angular Velocity Magnitude", ylabel="Max Acceleration Magntiude")