import sqlite3
import math
import matplotlib.pyplot as plt
from obspy.clients.fdsn import Client
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from PIL import Image

class SeismicStationDatabase:
    def __init__(self, db_name="stations.db"):
        """初始化数据库名称，并创建数据库和表格
        示例使用:
            db = SeismicStationDatabase("stations.db")
        """
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """创建SQLite数据库并创建表
        示例使用:
            self.create_database()
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS stations
                          (network TEXT, station TEXT, latitude REAL, longitude REAL, elevation REAL,
                           start_time TEXT, end_time TEXT)''')
        conn.commit()
        conn.close()

    def save_station_to_db(self, network, station, latitude, longitude, elevation, start_time, end_time):
        """将台站信息保存到SQLite数据库
        示例使用:
            self.save_station_to_db("IU", "MAJO", 31.898, 131.420, 160.0, "1996-09-18 00:00:00", None)
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO stations (network, station, latitude, longitude, elevation, start_time, end_time)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (network, station, latitude, longitude, elevation, start_time, end_time))
        conn.commit()
        conn.close()

    def get_station_info(self, network, station):
        """获取指定台站的信息
        示例使用:
            info = self.get_station_info("IU", "MAJO")
            if info:
                print(f"Information for {network}.{station}:")
                print(f"Latitude: {info[2]}, Longitude: {info[3]}, Elevation: {info[4]} meters")
            else:
                print(f"No information found for {network}.{station}")
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM stations WHERE network = ? AND station = ?", (network, station))
        station_info = cursor.fetchone()
        
        conn.close()
        
        return station_info

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """计算两个经纬度之间的地理距离
        示例使用:
            station1 = self.get_station_info("IU", "MAJO")
            station2 = self.get_station_info("IU", "ADK")
            if station1 and station2:
                distance = self.haversine(station1[2], station1[3], station2[2], station2[3])
                print(f"Distance between {station1[1]} and {station2[1]} is {distance:.2f} km")
        """
        R = 6371.0  # 地球半径，单位为公里
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        return distance

    def plot_stations(self, map_image_path=None, network=None, station=None):
        """绘制台站的地理位置分布图，使用自定义地球贴图并支持根据network和station进行筛选
        示例使用:
            self.plot_stations_with_custom_map('path_to_your_map_image.png')
            self.plot_stations_with_custom_map('path_to_your_map_image.png', network='IU')
            self.plot_stations_with_custom_map('path_to_your_map_image.png', network='IU', station='MAJO')
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 构建筛选条件的查询语句
        query = "SELECT latitude, longitude FROM stations"
        params = []
        if network:
            query += " WHERE network = ?"
            params.append(network)
        if station:
            query += " AND station = ?" if network else " WHERE station = ?"
            params.append(station)

        cursor.execute(query, params)
        stations = cursor.fetchall()
        conn.close()

        if stations:
            lats, lons = zip(*stations)
            
            # 创建地图对象
            fig = plt.figure(figsize=(12, 8))
            ax = plt.axes(projection=ccrs.PlateCarree())
            ax.set_global()

            # 加载并显示自定义地图贴图
            try:
                img = Image.open(map_image_path)
                ax.imshow(img, extent=[-180, 180, -90, 90], transform=ccrs.PlateCarree(), 
                          origin='upper')
            except Exception as e:
                print(f"Error displaying image: {e}")
                return

            # 绘制台站
            ax.scatter(lons, lats, c='red', marker='^', s=100, transform=ccrs.PlateCarree())
            plt.title(f"Station Locations{' for ' + network if network else ''}{' - ' + station if station else ''}")
            plt.show()
        else:
            print("No stations found with the specified criteria.")


    def download_and_save_station_info(self, networks):
        """下载台站信息并保存到数据库
        示例使用:
            networks = ["IU", "IC", "CU", "II", "GE"]
            self.download_and_save_station_info(networks)
        """
        client = Client("IRIS")

        for network in networks:
            print(f"Fetching data for network: {network}")
            try:
                inventory = client.get_stations(network=network, level="station")
                for net in inventory:
                    for sta in net:
                        network_code = net.code
                        station_code = sta.code
                        latitude = sta.latitude
                        longitude = sta.longitude
                        elevation = sta.elevation
                        start_time = sta.start_date.strftime('%Y-%m-%d %H:%M:%S') if sta.start_date else None
                        end_time = sta.end_date.strftime('%Y-%m-%d %H:%M:%S') if sta.end_date else None

                        # 保存到数据库
                        self.save_station_to_db(network_code, station_code, latitude, longitude, elevation, start_time, end_time)
                        print(f"Saved {network_code}.{station_code} - Lat: {latitude}, Lon: {longitude}")
            except Exception as e:
                print(f"Error fetching data for network {network}: {e}")
                continue  # 跳过出错的网络，继续处理下一个

    def view_database(self, network=None, station=None):
        """查看SQLite数据库中的表结构和前几条数据，并支持根据network和station进行筛选
        示例使用:
            查看所有表的前几条数据:
                self.view_database()
            仅查看指定network的台站:
                self.view_database(network="IU")
            仅查看指定network和station的台站:
                self.view_database(network="IU", station="MAJO")
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # 列出数据库中的所有表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if not tables:
                print("No tables found in the database.")
                return
                
            print(f"Tables in the database '{self.db_name}':")
            for table in tables:
                print(f" - {table[0]}")

                # 构建筛选条件
                query = f"SELECT * FROM {table[0]}"
                params = []
                if network:
                    query += " WHERE network = ?"
                    params.append(network)
                if station:
                    query += " AND station = ?" if network else " WHERE station = ?"
                    params.append(station)

                query += " LIMIT 10"

                # 查看表的结构
                print(f"\nStructure of table '{table[0]}':")
                cursor.execute(f"PRAGMA table_info({table[0]});")
                columns = cursor.fetchall()
                for column in columns:
                    print(f" {column[1]} ({column[2]})")

                # 查看符合条件的前几条数据
                print(f"\nFirst 10 rows of table '{table[0]}' with filter: {params}:")
                cursor.execute(query, params)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

            conn.close()

        except sqlite3.Error as e:
            print(f"Error viewing database {self.db_name}: {e}")

# 尝试直接加载和显示图像
def test_image_display(image_path):
    try:
        img = Image.open(image_path)
        plt.imshow(img)
        plt.title("Test Image Display")
        plt.show()
        print("Image displayed successfully")
    except Exception as e:
        print(f"Error displaying image: {e}")

def simple_cartopy_test():
    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_global()
    plt.title("Simple Cartopy Test")
    plt.show()


if __name__ == "__main__":
    # 示例使用
    db = SeismicStationDatabase("stations.db")
    networks = ["IU", "IC", "CU", "II", "GE"]
    # db.download_and_save_station_info(networks)
    # db.view_database("IC")

    # db.plot_stations(map_image_path=r"g:\SeisY\seisy\resources\texture\earthmap1k.jpg")

    # 测试调用
    # test_image_display(r"G:\SeisY\seisy\resources\texture\earthmap1k.jpg")
    # simple_cartopy_test()

    import geopandas as gpd
    import matplotlib.pyplot as plt

    # 从 Natural Earth 数据集加载世界地图
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # 简单的世界地图展示
    world.plot()
    plt.show()
