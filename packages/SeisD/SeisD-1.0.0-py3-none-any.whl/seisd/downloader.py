import os
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, Stream

class EarthquakeDownloader():
    def __init__(self, client_name="IRIS"):
        self.client_name = client_name
        self.update_client()

    def update_client(self):
        self.client = Client(self.client_name)
    
    def download_waveforms(self, network="XA", station="S12", location="00", channel="MHZ",
                            starttime=UTCDateTime("1973-12-10T08:30:00.000"), endtime=UTCDateTime("1973-12-10T16:30:00.000"),
                            filename="example.mseed",file_format = "MSEED"):
        try:
            self.st = self.client.get_waveforms(network, station, location, channel, starttime, endtime)
            # 支持的文件格式
            supported_formats = ["MSEED", "SAC", "SEGY", "WAV", "GSE2", "SACXY", "Q", "SH_ASC", "SLIST", "TSPAIR", "PICKLE", "SU", "AH", "GCF"]
            
            if file_format.upper() not in supported_formats:
                raise ValueError(f"Unsupported file format: {file_format}. Supported formats are: {supported_formats}")
            if file_format.upper() == "SEGY":
                new_traces = []
                for tr in self.st:
                    new_traces.extend(self.split_trace(tr))
                self.st = Stream(traces=new_traces)

            # 将数据写入文件，使用指定的格式
            self.st.write(filename, format=file_format.upper())
            # st.plot()
            return filename, self.st
        
        except Exception as e:
            return f"Error downloading data: {e}", None
        
    def split_trace(self,trace, max_samples=32767):
        traces = []
        for start in range(0, len(trace.data), max_samples):
            end = min(start + max_samples, len(trace.data))
            new_trace = trace.copy()
            new_trace.data = trace.data[start:end]
            traces.append(new_trace)
        return traces

    def download_event_waveforms(self, min_magnitude, starttime, endtime, output_directory):
        results = []
        try:
            cat = self.client.get_events(starttime=starttime, endtime=endtime, minmagnitude=min_magnitude)
            for event in cat:
                origin_time = event.origins[0].time
                magnitude = event.magnitudes[0].mag
                event_id = event.resource_id.id.split('/')[-1]
                filename = os.path.join(output_directory, f"{event_id}_{origin_time}.mseed")
                
                self.st = Stream()
                for network in self.client.get_stations(level="response").networks:
                    for station in network.stations:
                        try:
                            self.st += self.client.get_waveforms(network.code, station.code, "*", "BH?", origin_time, origin_time + 60*60)
                        except Exception as e:
                            results.append(f"Error downloading waveform for station {station.code}: {e}")
                
                if self.st:
                    self.st.write(filename, format="MSEED")
                    results.append(f"Event {event_id} with magnitude {magnitude} saved to {filename}")
                    # st.plot()
                else:
                    results.append(f"No data for event {event_id}")
        except Exception as e:
            results.append(f"Error downloading events: {e}")
        return results, self.st

if __name__ == "__main__":
    process = EarthquakeDownloader()
    _,st = process.download_waveforms()
    print(_)
    if st:
        st.plot()