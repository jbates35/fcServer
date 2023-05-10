from flask import Flask, render_template, Response, send_from_directory, Request
import os
from apscheduler.schedulers.background import BackgroundScheduler
import sensorGrapher
import SqlManager
from video_stream import gen_feed
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')
scheduler = BackgroundScheduler()

sql_manager_obj = SqlManager.SqlManager("localhost", "5432", "fcdb", "fishcens", "fishcens")
sql_manager_obj.connect()

depth_graph_link = "static/img/depth.png"
temp_graph_link = "static/img/temperature.png"

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    current_datetime = datetime.now()
    
    weeks_back = 6
    days_back = 0
    hours_back = 0
    minutes_back = 0
    
    datetime_string = ""
    if weeks_back > 0:
        datetime_string += str(weeks_back) + " weeks,"
    if days_back > 0:
        datetime_string += str(days_back) + " days,"
    if hours_back > 0:
        datetime_string += str(hours_back) + " hours,"
    if minutes_back > 0:
        datetime_string += str(minutes_back) + " minutes,"
    
    if datetime_string == "": 
        datetime_string = "No time"
    else: 
        datetime_string = datetime_string[:-1]
    
    yest_datetime = current_datetime - timedelta(weeks=weeks_back, days=days_back, hours=hours_back, minutes=minutes_back)
    
    current_time = current_datetime.strftime("%H:%M:%S")
    current_date = current_datetime.strftime("%Y-%m-%d")
    yest_time = yest_datetime.strftime("%H:%M:%S")
    yest_date = yest_datetime.strftime("%Y-%m-%d")   
    
    depth_graph_link = "static/img/depth.png"
    temp_graph_link = "static/img/temperature.png"
    
    #Sort sensor readings
    last_datapoints = sql_manager_obj.get_last_datapoints()
    sensor_dict = {"temp": last_datapoints[0][0], "depth": last_datapoints[0][1]}
    
    fish_count = sql_manager_obj.get_fish_count(date_start=yest_date, time_start=yest_time, date_end=current_date, time_end=current_time)
    fish_dec = fish_count[0][1]
    fish_inc = fish_count[1][1]
    fish_net = abs(fish_dec - fish_inc)
    fish_dir = "Upstream" if fish_dec <= fish_inc else "Downstream"
    fish_dict = {"dec": fish_dec, "inc": fish_inc, "net": fish_net, "dir": fish_dir}
    
    return render_template(
        'index.html',
        datetime_string = datetime_string,
        fish_data = fish_dict,
        sensor_data = sensor_dict,
        temp_graph = temp_graph_link,
        depth_graph = depth_graph_link
        )

@app.route('/video_feed')
def video_feed():
    return Response(
        gen_feed(), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
        )

@app.route('/sensors')
@app.route('/sensors.html')
def sensors():
    return render_template('sensors.html')

@app.route('/fishdata')
@app.route('/fishdata.html')
def fishdata():
    fish_data = sql_manager_obj.get_fish_data(limit=5)

    fish_with_urls = []
    for fish in fish_data:
        file_path = fish[3]  # Assuming fish[3] contains the file path
        file_name = file_path.split('/')[-2] + '/' + file_path.split('/')[-1]  # Extract the file name from the file path
        image_url = f"../fishPictures/{file_name}"  # Construct the image URL

        fish_with_urls.append((fish[0], fish[1], fish[2], image_url, fish[4]))  # Update the tuple with the image URL

    return render_template(
        'fishdata.html',
        fish_data=fish_with_urls
    )


@app.route('/settings')
@app.route('/settings.html')
def settings():
    return render_template('settings.html')

def perform_background_task():
    # Import sensor data from database and plot them
    # First need filename
    sensor_data = sql_manager_obj.get_sensor_data()

    temperature_plot = sensorGrapher.plot_water_temperature(sensor_data)
    temperature_plot.savefig(temp_graph_link)

    depth_plot = sensorGrapher.plot_water_level(sensor_data)
    depth_plot.savefig(depth_graph_link)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Schedule the background task to run every minute
scheduler.add_job(perform_background_task, 'interval', minutes=5)

if __name__ == "__main__":
    #perform_background_task()
    app.run()
