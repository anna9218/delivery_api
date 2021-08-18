import json

from Domain.Timeslot import Timeslot

JSON_PATH = "D:\Coding\DropitTask\Resources\courierAPI.json"


class TimeslotManager:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if TimeslotManager.__instance is None:
            TimeslotManager()
        return TimeslotManager.__instance

    def __init__(self):
        if TimeslotManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TimeslotManager.__instance = self
            self.__business_capacity = {}
            self.__timeslots = self.retrieve_available_timeslots()

    def get_timeslots(self, city, country):
        """
        Retrieves the available timeslots which support the given city
        :param city: city name string
        :param country: country name string
        :return: available timeslots that support the given city
        """
        available_timeslots = []
        for timeslot in self.__timeslots:
            if not timeslot.is_holiday(country, timeslot.get_date()):
                for supported_city in timeslot.get_supported_addresses():
                    if supported_city == city:
                        available_timeslots.append({'date': timeslot.get_date(),
                                                    'delivery_count': timeslot.get_delivery_count(),
                                                    'start': timeslot.get_start_time(),
                                                    'end': timeslot.get_end_time(),
                                                    'supported_addresses': timeslot.get_supported_addresses(),
                                                    'id': timeslot.get_id()})
        return available_timeslots

    def retrieve_available_timeslots(self):
        """
        Calculate timeslots from json file, check whether timeslot is not a holiday, and within business capacity
        :return: timeslots
        """
        # read json (courier API)
        file = open(JSON_PATH)
        data = json.load(file)

        if data is None:
            return None

        timeslots = []
        for timeslot_data in data['timeslots']:
            timeslot = Timeslot(timeslot_data)
            # if not(timeslot.is_holiday()) and self.is_business_capacity(timeslot.get_date()):
            if self.is_business_capacity(timeslot.get_date()):
                timeslots.append(timeslot)
        file.close()
        return timeslots

    def is_business_capacity(self, timeslot_date):
        """
        Checks if there are up to 10 deliveries per day
        :param timeslot_date: date string
        :return: True is within capacity, False otherwise
        """
        if timeslot_date in TimeslotManager.get_instance().__business_capacity:
            if TimeslotManager.get_instance().__business_capacity[timeslot_date] >= 10:
                return False
            else:
                TimeslotManager.get_instance().__business_capacity[timeslot_date] += 1
        else:
            TimeslotManager.get_instance().__business_capacity[timeslot_date] = 1

        return True

    def is_timeslot_available(self, timeslot_id):
        for timeslot in TimeslotManager.get_instance().__timeslots:
            if timeslot.get_id() == int(timeslot_id):
                if timeslot.get_delivery_count() >= 2:
                    return False
                else:
                    return True
        return False

    def book_timeslot(self, timeslot_id):
        for timeslot in TimeslotManager.get_instance().__timeslots:
            if timeslot.get_id() == int(timeslot_id):
                timeslot.increase_delivery_count()
                return True
        return False
