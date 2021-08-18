import requests

KEY_PATH = "D:\Coding\DropitTask\Resources\holiday_api_key.txt"


class Timeslot:
    def __init__(self, timeslot_json):
        self.__id = id(timeslot_json)
        self.__start_time = timeslot_json["start"].split(" ")[0]
        self.__end_time = timeslot_json["end"].split(" ")[0]
        self.__date = timeslot_json["start"].split(" ")[1]
        self.__supported_addresses = timeslot_json["supported_addresses"]
        self.__delivery_count = 0   # each timeslot can be used for 2 deliveries max

    # TODO - make sure timeslot does not fall on holiday
    def is_holiday(self, country, date):
        # get holiday api key
        with open(KEY_PATH) as f:
            api_key = f.readlines()

        # api get request
        # date is of format "19-08-21"
        query = {'key': api_key, 'country': country, 'year': "20" + date.split("-")[2],
                 'month': date.split("-")[1], 'day': date.split("-")[0]}
        response = requests.get("https://holidayapi.com/v1/holidays", params=query).json()

        # extract various address properties
        if response['status'] == 200:
            holidays = response['holidays']
            if len(holidays) == 0:  # empty array, no holidays
                return False
        elif response['status'] == 402:     # limited usage of api, only for last year 2020
            return False
        return True

    def get_delivery_count(self):
        return self.__delivery_count

    def increase_delivery_count(self):
        self.__delivery_count += 1

    def get_date(self):
        return self.__date

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_id(self):
        return self.__id

    def get_supported_addresses(self):
        return self.__supported_addresses
