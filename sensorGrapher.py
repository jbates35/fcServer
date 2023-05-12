import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
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

def plot_both(sensor_data):
    #Arrays to hold water temperature and timestamps
    timestamps = []
    temp_readings = []
    depth_readings = []
    
    for reading in sensor_data:
        #If temperature is -1, it is invalid and we can move to the next reading
        if reading[3] <= -1 or reading[3] >= 60 or reading[4] <= -1:
            continue
        
        #Add temperature which will be y-axis, timestamp which will be x-axis
        temp_readings.append(reading[3])
        depth_readings.append(reading[4])
        
        timestamps.append(datetime.combine(reading[1], reading[2]))
        
    #Clear plot
    plt.clf()
    
    # Set the plot face color to a light brownish green
    plt.rcParams['axes.facecolor'] = '#EEEEEE'
    
    # Plot the water temperature
    ax1 = plt.subplot(111)
    ax1.plot(timestamps, temp_readings, color='blue')
    ax1.set_xlabel('Date and Time')
    ax1.set_ylabel('Water Temperature (C)')
    ax1.grid(True, alpha=0.4)
    ax1.set_ylim(min(temp_readings) - 5, max(temp_readings) + 5)  # Add 5-degree margin
    
    # Plot the water depth on a twin y-axis
    ax2 = ax1.twinx()
    ax2.plot(timestamps, depth_readings, color='green')
    ax2.set_ylabel('Water Depth (mm)')
    ax2.set_ylim(min(depth_readings) - 10, max(depth_readings) + 10)  # Add 10-mm margin
    
    # Set x-axis tick marks to display 5 ticks
    x_ticks = ax1.get_xticks()
    x_tick_interval = len(x_ticks) // 4
    ax1.set_xticks(x_ticks[::x_tick_interval])
    plt.xticks(rotation=45, fontsize=8)
        
    # Legend for the two plots
    ax1.legend(['Temperature'], loc='upper left')
    ax2.legend(['Depth'], loc='upper right')
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    
    # Set the figure size to be 700 pixels wide and 400 pixels tall
    dpi = plt.gcf().dpi
    plt.gcf().set_size_inches(700 / dpi, 400 / dpi)
    
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
    
    both_plot = plot_both(sensor_data)
    both_plot.savefig("static/img/both_sensors.png")