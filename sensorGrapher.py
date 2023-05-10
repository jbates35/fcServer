import matplotlib.pyplot as plt
from datetime import datetime
import SqlManager

def plot_water_temperature(sensor_data):
    #Arrays to hold water temperature and timestamps
    timestamps = []
    temp_readings = []
    
    for reading in sensor_data:
        #If temperature is -1, it is invalid and we can move to the next reading
        if reading[3] <= -1 or reading[3] >= 60:
            continue
        
        #Add temperature which will be y-axis, timestamp which will be x-axis
        temp_readings.append(reading[3])
        timestamps.append(datetime.combine(reading[1], reading[2]))
        
    #Clear plot
    plt.clf()
    
    #Plot the data . . . need a line graph
    plt.plot(timestamps, temp_readings)
    plt.xticks(rotation=45, fontsize=8)
    plt.xlabel('Date and Time')
    plt.ylabel('Water Temperature (C)')
    plt.title('Water temperature versus time')
    plt.grid(True, alpha=0.4)
    
    
    return plt.gcf()

def plot_water_level(sensor_data):
    #Arrays to hold water level and timestamps
    timestamps = []
    depth_readings = []
    
    for reading in sensor_data:
        #If depth is -1, it is invalid and we can move to the next reading
        if reading[4] <= -1:
            continue
        
        #Add depth which will be y-axis, timestamp which will be x-axis
        depth_readings.append(reading[4])
        timestamps.append(datetime.combine(reading[1], reading[2]))
    
    #Clear plot
    plt.clf()
    
    #Plot the data . . . need a line graph
    plt.plot(timestamps, depth_readings)
    plt.xticks(rotation=45, fontsize=8)
    plt.xlabel('Date and Time')
    plt.ylabel('Water Depth (mm)')     
    plt.title('Water depth versus time')
    plt.grid(True, alpha=0.4)
    
    return plt.gcf()

if __name__=="__main__":
    #Connect to the database
    sql_manager_obj = SqlManager.SqlManager("localhost", "5432", "fcdb", "fishcens", "fishcens")
    
    #Get the sensor data
    sensor_data = sql_manager_obj.get_sensor_data()
    
    #Plot the data
    temperature_plot = plot_water_temperature(sensor_data)
    temperature_plot.savefig("static/img/temperature.png")
    
    depth_plot = plot_water_level(sensor_data)
    depth_plot.savefig("static/img/depth.png")
    