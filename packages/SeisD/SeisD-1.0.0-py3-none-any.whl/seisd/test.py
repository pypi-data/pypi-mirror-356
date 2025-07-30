import numpy as np
from scipy.optimize import minimize
import datetime
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, Stream

class EarthquakeLocator:
    def __init__(self, network="IU", stations=["MAJO", "COLA", "TATO", "MAKZ", "ULN"], duration=600, p_wave_velocity=6.0):
        """
        初始化地震定位类
        :param network: 台网代码，例如 "IU"
        :param stations: 台站代码列表
        :param duration: 获取的数据时长，单位为秒，默认600秒（10分钟）
        :param p_wave_velocity: P波的传播速度（假设为常数，单位：公里/秒）
        """
        self.network = network
        self.stations = stations
        self.duration = duration
        self.p_wave_velocity = p_wave_velocity
        self.client = Client("IRIS")  # 使用IRIS数据库，你可以根据需要更改为其他数据库

    def get_waveform_by_stations(self, start_time=None, end_time=None):
        """
        从数据库中获取多个台站的地震波形数据。
        :param start_time: 开始时间（UTCDateTime对象），默认为None，表示使用end_time前半小时的时间作为start_time
        :param end_time: 结束时间（UTCDateTime对象），默认为None，表示使用当前时间
        :return: 包含每个台站波形数据的列表，每个元素为 {station, coords, waveform_data}
        """
        if end_time is None:
            end_time = UTCDateTime()  # 默认使用当前UTC时间作为结束时间
        if start_time is None:
            start_time = end_time - 1800  # 默认为end_time前30分钟

        st = Stream()
        stations_data = []
        for station in self.stations:
            try:
                print(f"正在下载{station}台站的波形数据")
                # 请求波形数据，前 duration 秒
                waveform = self.client.get_waveforms(network=self.network, station=station, location="00",
                                                     channel="BHZ", starttime=start_time, endtime=end_time)
                st += waveform
                print(f"{station}台站的波形数据下载成功:",st)

                # 获取台站的地理位置
                print(f"正在获取{station}台站的地理位置")
                inventory = self.client.get_stations(network=self.network, station=station, level="station")
                station_coords = (inventory[0][0].latitude, inventory[0][0].longitude)
                print(f"{station}台站的地理位置为：{station_coords}")

                # 存储台站的波形数据和位置信息
                stations_data.append({"station": station, "coords": station_coords, "waveform_data": waveform[0]})
            except Exception as e:
                print(f"Failed to get data for station {station}: {e}")
                continue

        return stations_data

    def autoidentify_p_wave_time_by_waveform(self, stations_data):
        """
        从波形数据中自动识别P波到达的时刻。
        :param stations_data: 包含每个台站波形数据的列表，每个元素为 {station, coords, waveform_data}
        :return: 返回一个包含每个台站 P 波到达时刻的列表，每个元素为 {station, coords, p_wave_time}
        """
        identified_p_wave_times = []
        for station_data in stations_data:
            print(f"正在识别{station_data['station']}波形记录的地震到达时刻")

            waveform_data = station_data["waveform_data"]
            # 使用一个简单的阈值法或更复杂的算法来检测P波
            # 这里简化为检测波形最大值出现的时间点作为P波到达时间（这只是一个示例，实际情况可能更复杂）
            p_wave_index = np.argmax(waveform_data.data)
            # 将索引转换为实际的到达时刻
            p_wave_time = waveform_data.stats.starttime + p_wave_index / waveform_data.stats.sampling_rate
            print(f"{station_data['station']}波形记录的地震到达时刻为：{p_wave_time}")
            identified_p_wave_times.append({
                "station": station_data["station"],
                "coords": station_data["coords"],
                "p_wave_time": p_wave_time.datetime
            })

        return identified_p_wave_times

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        计算两个经纬度坐标点之间的球面距离（单位：公里）
        :param lat1, lon1: 第一个点的纬度和经度
        :param lat2, lon2: 第二个点的纬度和经度
        :return: 两点之间的距离（公里）
        """
        R = 6371.0  # 地球半径，单位：公里
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        a = np.sin(delta_phi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c

    def locate_earthquake(self, stations_data):
        """
        定位地震源位置
        :param stations_data: 包含台站信息和P波到达时刻的列表，每个元素为 {station, coords, p_wave_time}
        :return: 估计的地震发生时刻 t0 和震源位置 (lat, lon)
        """
        # 1. 假设一个理论发震时刻，最早接收到P波的时刻向前推5分钟
        p_wave_times = [station['p_wave_time'] for station in stations_data]
        earliest_time = min(p_wave_times)
        initial_t0 = earliest_time - datetime.timedelta(minutes=15)
        print("正在进行地震实际发生时刻估算及震源定位")
        def objective_function(params):
            t0, lat0, lon0 = params
            residuals = []
            for station in stations_data:
                lat, lon = station['coords']
                distance = self.haversine(lat0, lon0, lat, lon)
                predicted_time = t0 + distance / self.p_wave_velocity
                residuals.append((predicted_time - station['p_wave_time'].timestamp()))
            return np.sum(np.square(residuals))

        # 2. 初始化参数：t0 (初始估计为 initial_t0), lat0, lon0 (假设在台站平均位置)
        initial_guess = [
            initial_t0.timestamp(),  # 将 datetime 转换为时间戳（秒）
            np.mean([station['coords'][0] for station in stations_data]),
            np.mean([station['coords'][1] for station in stations_data])
        ]

        # 3. 优化过程，找到最小化残差平方和的 t0, lat0, lon0
        result = minimize(objective_function, initial_guess, method='L-BFGS-B')

        # 4. 返回最优解，即估计的地震发生时刻 t0 和震源位置 (lat0, lon0)
        t0_timestamp, lat0, lon0 = result.x
        t0 = datetime.datetime.utcfromtimestamp(t0_timestamp)
        return t0, (lat0, lon0)

    def hypocenter_locating(self, start_time=None, end_time=None):
        """
        主函数，用于执行地震定位的整个过程
        :param start_time: 开始时间（UTCDateTime对象），默认为None
        :param end_time: 结束时间（UTCDateTime对象），默认为None，表示使用当前时间
        """
        stations_data = self.get_waveform_by_stations(start_time=start_time, end_time=end_time)
        identified_p_wave_times = self.autoidentify_p_wave_time_by_waveform(stations_data)
        t0, epicenter = self.locate_earthquake(identified_p_wave_times)
        print(f"Estimated earthquake time: {t0} UTC")
        print(f"Estimated epicenter location: {epicenter} (latitude, longitude)")

if __name__ == "__main__":
    
    # 创建类的实例并调用主函数进行定位
    locator = EarthquakeLocator()
    # 例如，假设你要从某一观测台站识别到地震时刻的前半小时开始
    observed_time = UTCDateTime(2024, 8, 25, 2, 22, 0)
    start_time = observed_time - 1800  # 30分钟前
    locator.hypocenter_locating(start_time=start_time,end_time=observed_time)