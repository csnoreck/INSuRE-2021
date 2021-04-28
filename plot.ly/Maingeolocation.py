import requests
import json

def find_geolocation(target_ip, access_key):
    '''
    Function uses the ipstack api, to get the geolocation data of input parameter target_ip.

    API reference: https://ipstack.com/quickstart
    '''
    # generate request url using target_ip and access_key
    request_url = 'http://api.ipstack.com/{}?access_key={}'.format(target_ip, access_key)

    # make get request to api server
    reply = requests.get(request_url)

    # load json reply to data dictionary
    data = json.loads(reply.text)

    # parse the required info from data
    region = data['region_name']
    country = data['country_name']
    longitude = data['longitude']
    latitude = data['latitude']

    # return info as a four element tuple
    return region, country, longitude, latitude


def main():
    # loop forever
    while True:
        # prompt user for target ip
        target_ip = input('Enter valid ipv4 address to geolocate: ')

        # if sentinel value 'exit' is entered, break from while loop
        if target_ip.lower() == 'exit':
            break

        # replace with your own access_key
        access_key = '4161891258a7709af5e6f58c1e9c3c89'

        # call the function find_geolocation and parse the returned results
        region, country, longitude, latitude = find_geolocation(target_ip, access_key)

        # print the results
        print('{}, {}, {}'.format(target_ip, region, country))
        print('{}, {}'.format(longitude, latitude))
        print()

if __name__ == '__main__':
    main()
