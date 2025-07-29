import intake
from intake.source.base import DataSource
import OpenVisus as ov
from datetime import datetime
import numpy as np
import xarray as xr

def calculate_day_of_year(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return (date - datetime(date.year, 1, 1)).days

def get_timestep(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_year = calculate_day_of_year(date_str)
    total_days = 365 + (1 if (date.year % 4 == 0 and date.year % 100 != 0) or (date.year % 400 == 0) else 0)
    return date.year * total_days + day_of_year

class NexGDDPCatalog(DataSource):
    name = 'nex_gddp_cmip6'
    version = '1.0'

    def __init__(self, model, variable, scenario, timestamp, quality=0, lat_range=None, lon_range=None, **kwargs):
        self.model = model
        self.variable = variable
        self.scenario = scenario
        self.timestamp = timestamp
        self.quality = quality
        self.lat_range = lat_range
        self.lon_range = lon_range
        
    def _load(self):
        dataset_url = "http://atlantis.sci.utah.edu/mod_visus?dataset=nex-gddp-cmip6"
        field = f"{self.variable}_day_{self.model}_{self.scenario}_r1i1p1f1_gn"
        timestep = int(get_timestep(self.timestamp))

        db = ov.LoadDataset(dataset_url)
        full_nx, full_ny = db.getLogicBox()[1]  # full resolution shape

        # Define full lat/lon arrays at full resolution
        lat_start, lat_end = -59.88, 90.0
        lon_start, lon_end = 0.125, 360.0
        lat_full = np.linspace(lat_start, lat_end, full_ny, endpoint=False)
        lon_full = np.linspace(lon_start, lon_end, full_nx, endpoint=False)

        y1, y2 = 0, full_ny
        x1, x2 = 0, full_nx

        if self.lat_range:
            lat_min, lat_max = self.lat_range
            y1 = int(np.searchsorted(lat_full, lat_min, side="left"))
            y2 = int(np.searchsorted(lat_full, lat_max, side="right"))

        if self.lon_range:
            lon_min, lon_max = self.lon_range
            x1 = int(np.searchsorted(lon_full, lon_min, side="left"))
            x2 = int(np.searchsorted(lon_full, lon_max, side="right"))

        logic_box = [[x1, y1], [x2, y2]]
        data = db.read(time=timestep, field=field, quality=self.quality, logic_box=logic_box)

        returned_ny, returned_nx = data.shape
        lat_step = lat_full[1] - lat_full[0]
        lon_step = lon_full[1] - lon_full[0]

        lat = np.linspace(lat_full[y1], lat_full[y1] + lat_step * returned_ny, returned_ny, endpoint=False)
        lon = np.linspace(lon_full[x1], lon_full[x1] + lon_step * returned_nx, returned_nx, endpoint=False)

        return xr.DataArray(data, coords=[("lat", lat), ("lon", lon)])

    def read(self):
        return self._load()
