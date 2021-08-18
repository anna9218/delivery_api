import requests

KEY_PATH = "D:\Coding\DropitTask\Resources\geocoding_api_key.txt"


def resolve_address(search_term):
    # get api key
    with open(KEY_PATH) as f:
        api_key = f.readlines()

    # make http request to geocoding api
    search_terms = search_term.split(" ")
    address_terms = ""
    for term in search_terms:
        address_terms += term + "+"
    address_terms = address_terms[:-1]

    query = {'address': address_terms, 'key': api_key}
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=query).json()

    # extract various address properties
    if response['status'] == "OK":
        city = extract_city(response)
        postcode = extract_postcode(response)
        country = extract_country(response)
        state = extract_state(response)
        formatted_addr = extract_formatted_address(response)
    else:
        return {"status": response['status']}
    return {"status": response['status'], "city": city, "state": state, "country": country, "postcode": postcode,
            "formatted_addr": formatted_addr}


def extract_city(response):
    """
    Receives a json object and extracts the city which is represented by 'locality' type
    :param response: json object from geocode googleapis
    :return: a string of the extracted city
    """
    city = ""
    results = response['results'][0]
    for component in results['address_components']:
        for comp_type in component['types']:
            if comp_type == "locality":
                city = component['long_name']
                break
    return city


def extract_postcode(response):
    """
    Receives a json object and extracts the postcode which is represented by 'postcode' type
    :param response: json object from geocode googleapis
    :return: a string of the extracted postcode
    """
    postcode = ""
    results = response['results'][0]
    for component in results['address_components']:
        for comp_type in component['types']:
            if comp_type == "postal_code":
                postcode = component['long_name']
                break
    return postcode


def extract_country(response):
    country = ""
    results = response['results'][0]
    for component in results['address_components']:
        for comp_type in component['types']:
            if comp_type == "country":
                country = component['short_name']
                break
    return country


def extract_state(response):
    state = ""
    results = response['results'][0]
    for component in results['address_components']:
        for comp_type in component['types']:
            if comp_type == "administrative_area_level_1":
                state = component['long_name']
                break
    return state


def extract_formatted_address(response):
    results = response['results'][0]
    return results['formatted_address']


# print(resolve_address("1600 Amphitheatre Parkway, Mountain View, CA"))

