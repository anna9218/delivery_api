from pymongo import MongoClient


class Connect(object):
    @staticmethod
    def get_connection():
        port = 27017
        url = "mongodb://localhost:27017"
        return MongoClient(url)


class DBAccess:
    """
    Class which is responsible for the communication between the Domain and the mongoDB
    It allows to write to and fetch from the deliveries DB.
    Note - it is also possible to implement a timeslots DB, in order to keep the timeslots persistent (didn't do that due to limited time).
    """
    database = None
    DB_name = 'deliveriesDB'
    collection_name = 'deliveries'
    __instance = None  # to ensure its a singleton
    mongo_client = None
    isPopulated = False

    def __init__(self):
        if DBAccess.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.mongo_client = Connect().get_connection()

            # Create the deliveries database under the name 'deliveriesDB'
            self.database = self.mongo_client.deliveriesDB
            self.db_name = "deliveriesDB"
            DBAccess.__instance = self
            if self.database.Deliveries.count() > 0:
                self.isPopulated = True

    @staticmethod
    def getInstance():
        if DBAccess.__instance is None:
            return DBAccess()
        return DBAccess.__instance

    def insert_deliveries(self, data):
        self.database.Deliveries.insert(data)
        if self.database.Deliveries.count() > 0:
            self.isPopulated = True

    def fetch_deliveries(self):
        """
        Fetch the existing deliveries from the DB
        :return: the existing deliveries
        """
        deliveries_cursor = self.database.Deliveries.find()
        deliveries = []
        for delivery in deliveries_cursor:
            delivery.pop('_id', None)
            deliveries.append(delivery)
        return deliveries

    def update_delivery(self, delivery: dict, new_data: dict):
        """
        Update the delivery - in case the status was changed (or any other parameter, if requested)
        :param delivery: dictionary with delivery info
        :param new_data: dictionary with new delivery info
        :return: True if updated successfully
        """
        self.database.Deliveries.update(delivery, {'$set': new_data})
        return True

    def drop_db(self):
        self.mongo_client.drop_database(self.db_name)
        if self.database.Deliveries.count() < 1:
            self.isPopulated = False
