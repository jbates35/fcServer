import psycopg2

class SqlManager:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password= password
        
        # Connection object which will be passed around
        self.conn = None
        
    def __del__(self):
        self.close()
        
    def connect(self):
        self.conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        
    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None 
    
    # Queries SQL table for all sensor readings between two dates and times - this will likely be made into a graph later
    def get_sensor_data(self, date_start="1970-01-01", time_start="00:00:00", date_end="2040-01-01", time_end="00:00:00"):
        wasConnected = True
        
        if self.conn is None:
            self.connect()
            wasConnected = False
        
        #For better query performance, we should concat the date and time columns into a single timestamp column
        start_timestamp = date_start + " " + time_start
        end_timestamp = date_end + " " + time_end
        
        
        #SQL Query part
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM sensor_readings WHERE (reading_date || ' ' || reading_time) BETWEEN %s AND %s", (start_timestamp, end_timestamp))       
        rows = cur.fetchall()
        
        if not wasConnected:
            self.close()
        
        return rows
    
    def get_fish_data(self, id_start=0, id_end=2147483647, date_start="1970-01-01", time_start="00:00:00", date_end="2040-01-01", time_end="00:00:00"):
        wasConnected = True
        
        if self.conn is None:
            self.connect()
            wasConnected = False
        
        #For better query performance, we should concat the date and time columns into a single timestamp column
        start_timestamp = date_start + " " + time_start
        end_timestamp = date_end + " " + time_end
        
        #SQL query part
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM fish_counter WHERE (fish_date || ' ' || fish_time) BETWEEN %s AND %s AND id BETWEEN %s AND %s", (start_timestamp, end_timestamp, id_start, id_end))
        rows = cur.fetchall()
        
        if not wasConnected:
            self.close()
        
        return rows    
    
    def get_last_datapoints(self):
        wasConnected = True
        
        if self.conn is None:
            self.connect()
            wasConnected = False
        
        #SQL query part
        cur = self.conn.cursor()
        cur.execute("SELECT water_temp, depth FROM sensor_readings ORDER BY reading_date DESC, reading_time DESC LIMIT 1")
        rows = cur.fetchall()
        
        if not wasConnected:
            self.close()
        
        return rows
    
    def get_fish_count(self, id_start=0, id_end=2147483647, date_start="1970-01-01", time_start="00:00:00", date_end="2040-01-01", time_end="00:00:00"):
        wasConnected = True
        
        if self.conn is None:
            self.connect()
            wasConnected = False
        
        #For better query performance, we should concat the date and time columns into a single timestamp column
        start_timestamp = date_start + " " + time_start
        end_timestamp = date_end + " " + time_end
        
        # SQL query part
        curr = self.conn.cursor()
        curr.execute("""
            SELECT directions.direction, COALESCE(counts.count, 0) AS count
            FROM (
                SELECT 'R' AS direction
                UNION
                SELECT 'L' AS direction
            ) AS directions
            LEFT JOIN (
                SELECT direction, COUNT(*) AS count
                FROM fish_counter
                WHERE (fish_date || ' ' || fish_time) BETWEEN %s AND %s
                AND id BETWEEN %s AND %s
                GROUP BY direction
            ) AS counts ON directions.direction = counts.direction
            ORDER BY directions.direction
        """, (start_timestamp, end_timestamp, id_start, id_end))
        
        rows = curr.fetchall()
        
        if not wasConnected:
            self.close()
            
        return rows

if __name__ == "__main__":
    sql_manager_obj = SqlManager("localhost", "5432", "fcdb", "fishcens", "fishcens")
    sensor_data = sql_manager_obj.get_sensor_data()
    
    print("Sensor data is: ")
    print(sensor_data)
    
    fish_data = sql_manager_obj.get_fish_data()
    
    print("Fish data is: ")
    print(fish_data)
    
    last_data = sql_manager_obj.get_last_datapoints()
    
    print("Last data is: ")
    print(last_data)
    
    fish_count = sql_manager_obj.get_fish_count()
    
    print("Fish count is: ")
    print(fish_count)
    
