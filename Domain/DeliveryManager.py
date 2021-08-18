import threading
from datetime import datetime, timedelta
from time import asctime, strptime

from DBCommunication.DBAccess import DBAccess
from Domain.Delivery import Delivery
from Domain.TimeslotManager import TimeslotManager


class DeliveryManager:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DeliveryManager.__instance is None:
            DeliveryManager()
        return DeliveryManager.__instance

    def __init__(self):
        if DeliveryManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.__deliveries = []
            self.__lock = threading.Lock()
            DeliveryManager.__instance = self

    def book_a_delivery(self, user, timeslot_id):
        # ensuring thread safety when booking a delivery
        with DeliveryManager.get_instance().__lock:
            # check if timeslot available (max of 2 deliveries per timeslot)
            if TimeslotManager.get_instance().is_timeslot_available(timeslot_id):
                delivery = Delivery(user, timeslot_id)
                if TimeslotManager.get_instance().book_timeslot(timeslot_id):
                    DeliveryManager.get_instance().__deliveries.append(delivery)
                    # DB ACCESS - WORKS
                    DBAccess.getInstance().insert_deliveries({'id': delivery.get_id(),
                                                              'status': delivery.get_status(),
                                                              'timeslot_id': delivery.get_timeslot(),
                                                              'user': delivery.get_user()})
                    return True
        return False

    def complete_delivery(self, delivery_id):
        for delivery in DeliveryManager.get_instance().__deliveries:
            if delivery.get_id() == int(delivery_id):
                delivery.set_status("COMPLETED")
                # DB ACCESS
                DBAccess.getInstance().update_delivery({'status': 'COMPLETED'})
                return True
        return False

    def cancel_delivery(self, delivery_id):
        for delivery in DeliveryManager.get_instance().__deliveries:
            if delivery.get_id == delivery_id:
                DeliveryManager.get_instance().__deliveries.remove(delivery)
                # DB ACCESS
                DBAccess.getInstance().update_delivery({'status': 'CANCELED'})
                return True
        return False

    def get_today_deliveries(self):
        deliveries = []
        current_date = datetime.today().strftime('%d-%m-%y')
        for delivery in DeliveryManager.get_instance().__deliveries:
            if current_date == delivery.get_date():
                deliveries.append(delivery)
        return deliveries

    def get_weekly_deliveries(self):
        deliveries = []
        week_dates = DeliveryManager.get_instance().get_weekdates()
        for delivery in DeliveryManager.get_instance().__deliveries:
            for week_date in week_dates:
                if delivery.get_date() == week_date:
                    deliveries.append(delivery)
        return deliveries

    def get_weekdates(self):
        week_num = datetime.now().isocalendar()[1] - 1
        start_date = asctime(strptime('2021 %d 0' % week_num, '%Y %W %w'))
        start_date = datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
        dates = [start_date.strftime('%d-%m-%y')]
        for i in range(1, 7):
            day = start_date + timedelta(days=i)
            dates.append(day.strftime('%Y-%m-%d'))
        return dates
