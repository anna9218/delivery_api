from flask import Flask, jsonify, request
from flask_cors import CORS

from Domain import Resolver
from Domain.DeliveryManager import DeliveryManager
from Domain.TimeslotManager import TimeslotManager

app = Flask(__name__)
CORS(app)


# resolves a single line address into a structured address
@app.route('/resolve-address', methods=['POST'])
def resolve_address():
    search_term = request.form['searchTerm']
    # send to resolving function
    response = Resolver.resolve_address(search_term)

    if response:
        if response['status'] == 'OK':
            return jsonify(msg='Address resolved successfully', data=response)
    return jsonify(msg='Error - ' + response['status'], data=False)


# retrieve all available timeslots
@app.route('/timeslots', methods=['POST'])
def timeslots():
    # Assumption - formatted address is a string of city and country names, according to which we can decided if
    # supported or not by a timeslot.
    #  address -> "cityname,countryname"
    address = request.form['address']
    city = address.split(",")[0]
    country = address.split(",")[1]
    timeslots_data = TimeslotManager.get_instance().get_timeslots(city, country)
    if len(timeslots_data) != 0:
        return jsonify(msg='Timeslots retrieved successfully', data=timeslots_data)
    return jsonify(msg='No timeslots available', data=False)


# book a delivery
@app.route('/deliveries', methods=['POST'])
def book_a_delivery():
    user = request.form['user']
    timeslot_id = request.form['timeslotId']
    response = DeliveryManager.get_instance().book_a_delivery(user, timeslot_id)
    if response:
        return jsonify(msg='Delivery booked successfully', data=True)
    return jsonify(msg='Error - delivery was not booked', data=False)


# mark a delivery as completed
@app.route('/deliveries/<deli_id>/complete', methods=['GET'])
def complete_delivery(deli_id):
    delivery_id = deli_id
    response = DeliveryManager.get_instance().complete_delivery(delivery_id)
    if response:
        return jsonify(msg='Delivery completed successfully', data=True)
    return jsonify(msg='Error - delivery was not completed', data=False)


# cancel a delivery
@app.route('/deliveries/<deli_id>', methods=['DELETE'])
def cancel_delivery(deli_id):
    delivery_id = deli_id
    response = DeliveryManager.get_instance().cancel_delivery(delivery_id)
    if response:
        return jsonify(msg='Delivery canceled successfully', data=True)
    return jsonify(msg='Error - delivery was not canceled', data=False)


# retrieve all today's deliveries
@app.route('/deliveries/daily', methods=['GET'])
def get_today_deliveries():
    response = DeliveryManager.get_instance().get_today_deliveries()
    if response:
        return jsonify(msg='Daily deliveries retrieved successfully', data=response)
    return jsonify(msg='Error - daily deliveries were not retrieved', data=[])


# retrieve all weekly deliveries
@app.route('/deliveries/weekly', methods=['GET'])
def get_weekly_deliveries():
    response = DeliveryManager.get_instance().get_weekly_deliveries()
    if response:
        return jsonify(msg='Weekly deliveries retrieved successfully', data=response)
    return jsonify(msg='Error - weekly deliveries were not retrieved', data=[])

