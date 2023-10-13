import requests
import pandas as pd


class WeatherData:
    def __init__(self, stations, elements, time, client_id, steps=True,
                 url='https://frost.met.no/observations/v0.jsonld'):
        """
        Fetch weather data from the Frost API.

        Parameters
        ----------
        stations : list
            List of station IDs.
        elements : list
            List of elements to fetch.
        time : str
            Time to fetch data from.
        client_id : str
            Client ID for the Frost API.
        url : str, optional
            URL to the Frost API.
        """
        self.stations = stations
        self.elements = elements
        self.client_id = client_id
        self.url = url

        if not steps:
            self.data = self.fetch(time)
        else:
            start_date_str, end_date_str = time.split('/')

            start_date = pd.to_datetime(start_date_str)
            end_date = pd.to_datetime(end_date_str)

            date_range = pd.date_range(start=start_date, end=end_date, freq='100D')

            data = []
            for i in range(len(date_range) - 1):
                start = date_range[i].strftime('%Y-%m-%d')
                end = date_range[i + 1].strftime('%Y-%m-%d')

                date_range_str = f"{start}/{end}"
                data.append(self.fetch(date_range_str))

            self.data = pd.concat(data)

    def fetch(self, time):
        """
        Fetch weather data.

        Returns
        -------
        pandas.DataFrame
        """
        parameters = {
            'sources': ",".join(self.stations),
            'elements': self.elements,
            'referencetime': time,
        }

        _response = requests.get(self.url, parameters, auth=(self.client_id, ''))
        response = _response.json()

        return pd.json_normalize(response['data'], record_path='observations',
                                 meta=['sourceId', 'referenceTime'])

    def clean(self, remove=None):
        """
        Remove unnessecary columns of the data.

        Parameters
        ----------
        remove : list, optional
            List of columns to remove.

        Notes
        -----
        The following columns are removed by default:
        - timeSeriesId
        - performanceCategory
        - exposureCategory
        - qualityCode
        - level.unit
        - level.levelType
        - level.value
        """
        if remove is None:
            remove = ["timeSeriesId", "performanceCategory", "exposureCategory",
                      "qualityCode", "level.unit", "level.levelType", "level.value"]
        self.data.drop(columns=remove, inplace=True)

    def save(self, path):
        """Save the data to a CSV file."""
        self.data.to_csv(path, index=False)
