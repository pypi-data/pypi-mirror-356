import pytest
import os,sys
from ..downloader import EarthquakeDownloader
from obspy import UTCDateTime

def test_download_waveforms():
    downloader = EarthquakeDownloader()
    starttime = UTCDateTime("2023-01-01")
    endtime = UTCDateTime("2023-01-02")
    downloader.download_waveforms("IU", "ANMO", "00", "BHZ", starttime, endtime, "test.mseed")
    assert os.path.exists("test.mseed")
    os.remove("test.mseed")

def test_download_event_waveforms():
    downloader = EarthquakeDownloader()
    starttime = UTCDateTime("2023-01-01")
    endtime = UTCDateTime("2023-01-02")
    downloader.download_event_waveforms(5.0, starttime, endtime, "test_data")
    # You can add assertions to verify the downloaded data
    # Cleanup
    if os.path.exists("test_data"):
        for file in os.listdir("test_data"):
            os.remove(os.path.join("test_data", file))
        os.rmdir("test_data")

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_downloader.py"])
