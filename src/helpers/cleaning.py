import pandas as pd


class CombineData:
    def __init__(self, spot_path, weather_path):
        """
        Combine spot and weather data.

        Parameters
        ----------
        spot_path : str
            Path to spot data.
        weather_path : str
            Path to weather data.
        """
        self.spot_path = spot_path
        self.weather_path = weather_path

        self.spot_df = None
        self.weather_df = None
        self.full = None

        self.spot()
        self.weather()

    def spot(self):
        """Process the spot data."""
        spot = pd.read_csv(self.spot_path, delimiter=";", decimal=",",
                           index_col=0, parse_dates=True)
        spot.index = pd.to_datetime(spot.index, format="%Y-%m-%d Kl. %H-%S")
        spot.index = spot.index.floor("H")
        spot.index = pd.to_datetime(spot.index)
        spot = spot.resample('H').sum()
        self.spot_df = spot.astype(float)

    def weather(self):
        """Process the weather data."""
        weather = pd.read_csv(self.weather_path, delimiter=",", parse_dates=True)
        weather = weather.set_index("referenceTime", drop=True)
        weather.drop(columns=["unit", "timeOffset", "timeResolution"], inplace=True)

        grouped = weather.groupby(["elementId", "sourceId"])
        grouped = {group: data for group, data in grouped}

        weather_data = []
        for group, data in grouped.items():

            data.index = pd.to_datetime(data.index).strftime('%Y-%m-%d %H:%M:%S')
            data.index = pd.to_datetime(data.index)

            if "elementId" in data.columns:
                data.drop(columns=["elementId"], inplace=True)
            if "sourceId" in data.columns:
                data.drop(columns=["sourceId"], inplace=True)

            if group[0] == "sum(precipitation_amount P1D)":
                try:
                    data = data.groupby(data.index)["value"].mean()
                except TypeError:
                    pass
                data = data.resample('H').ffill()
                data = data.apply(lambda x: x / 24)
                data.index = pd.to_datetime(data.index)
                data = data.to_frame()
            else:
                data = data.resample('H').sum()

            data = data.rename(columns={"value": group})

            weather_data.append(data)

        self.weather_df = pd.concat(weather_data, axis=1)

    def save(self, save_to=None):
        """
        Combine the data.

        Parameters
        ----------
        save_to : str, optional

        Returns
        -------
        pandas.DataFrame
            If `save_to` is None.
        """
        self.full = pd.concat([self.weather_df, self.spot_df], axis=1)

        if save_to is not None:
            self.full.to_csv(save_to, index=True)
            return None
        else:
            return self.full
