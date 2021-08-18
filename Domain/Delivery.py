class Delivery:
    def __init__(self, user, timeslot):
        self.__id = id(timeslot)
        self.__status = "PENDING"
        self.__timeslot = timeslot
        self.__user = user

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_timeslot(self):
        return self.__timeslot

    def get_id(self):
        return self.__id

    def get_user(self):
        return self.__user

    def get_date(self):
        return self.__timeslot.get_date()
