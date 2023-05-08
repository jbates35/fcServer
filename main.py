from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import sensorGrapher
import SqlManager

app = Flask(__name__, static_url_path='/static')
scheduler = BackgroundScheduler()

sql_manager_obj = SqlManager.SqlManager("localhost", "5432", "fcdb", "fishcens", "fishcens")
sql_manager_obj.connect()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    depth_graph_link = "static/img/depth.png"
    temp_graph_link = "static/img/temperature.png"
    
    last_datapoints = sql_manager_obj.get_last_datapoints()
    last_temp = last_datapoints[0][0]
    last_depth = last_datapoints[0][1]
    
    return render_template(
        'index.html',
        temp = last_temp,
        depth = last_depth,
        temp_graph = temp_graph_link,
        depth_graph = depth_graph_link
        )

@app.route('/sensors')
@app.route('/sensors.html')
def sensors():
    return render_template('sensors.html')

@app.route('/fishdata')
@app.route('/fishdata.html')
def fishdata():
    return render_template('fishdata.html')

@app.route('/settings')
@app.route('/settings.html')
def settings():
    return render_template('settings.html')

def perform_background_task():
    # Import sensor data from database and plot them
    # First need filenames
    depth_graph_link = "static/img/depth.png"
    temp_graph_link = "static/img/temperature.png"

    sensor_data = sql_manager_obj.get_sensor_data()

    temperature_plot = sensorGrapher.plot_water_temperature(sensor_data)
    temperature_plot.savefig(temp_graph_link)

    depth_plot = sensorGrapher.plot_water_level(sensor_data)
    depth_plot.savefig(depth_graph_link)

# Schedule the background task to run every minute
scheduler.add_job(perform_background_task, 'interval', minutes=5)

if __name__ == "__main__":
    app.run()