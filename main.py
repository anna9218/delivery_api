from Domain.DeliveryManager import DeliveryManager
from Domain.TimeslotManager import TimeslotManager
from WebCommunication import DeliveryAPI


if __name__ == '__main__':
    # singleton, in charge of accessing the courier API and retrieve the timeslots
    TimeslotManager()

    # singleton, in charge of managing the deliveries
    DeliveryManager()

    DeliveryAPI.app.run()


# Important Note - the 'Resources' folder should not be shared or uploaded to GiuHub since it contains API keys
# which should remain private!
