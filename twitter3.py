import geopy, folium, json, ssl, sys
from geopy.geocoders import Nominatim
from geopy import ArcGIS
from folium.plugins import MiniMap
import urllib.request, urllib.parse, urllib.error
import twurl

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def find_loc():
    acct = ''
    if (len(acct) < 1): acct = input('Enter Twitter Account:')
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '15'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    dct = {}
    for n in js["users"]:
        dct1 = {}
        if n["location"] != '':
            dct1[n["profile_image_url"]] = locator(n["location"])
            dct[n['name']] = dct1
    return dct

def locator(place):
    locator = Nominatim(user_agent="myGeocoder")
    try:
        locator = ArcGIS(timeout = 10)
        location = locator.geocode(place)
        coord = (location.latitude, location.longitude)
    except AttributeError:
        return None
    except:
        return None
    return coord

def map(dct):
    m = folium.Map(tiles='OpenStreetMap', zoom_start=12, control_scale=True)
    for i in dct:
        for icon in dct[i]:
            locationUser = dct[i][icon]
            iconUser = folium.features.CustomIcon(icon, icon_size=(50,50))
            popupUser = "<strong>{}".format(i)
            folium.Marker(locationUser,tooltip = i, popup=popupUser,icon = iconUser).add_to(m)
    m.save('twitter.html')



#print(find_loc())
map({'Tsapiv Volodymyr': {'http://pbs.twimg.com/profile_images/1230103797780951040/sCXhfrQ6_normal.jpg': (1.513805689000037, 32.335706651000066)}, 'GitHub': {'http://pbs.twimg.com/profile_images/1157035760085684224/iuxTnT5g_normal.jpg': (37.777120000000025, -122.41963999999996)}, 'Yevhen': {'http://pbs.twimg.com/profile_images/1230103064922804227/3hAiXqLw_normal.jpg': (49.84441000000004, 24.02543000000003)}, 'Anna Pashuk': {'http://pbs.twimg.com/profile_images/1230441927054700544/Mv9O1Dy8_normal.jpg': (49.84441000000004, 24.02543000000003)}, 'Donald J. Trump': {'http://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg': (38.890370000000075, -77.03195999999997)}, 'Intl. Space Station': {'http://pbs.twimg.com/profile_images/1189945624583720960/k6MtoeIt_normal.jpg': (28.334830000000068, -81.59277999999995)}, 'CALVIN KLEIN': {'http://pbs.twimg.com/profile_images/889490770687905792/N8mVqffO_normal.jpg': (40.71455000000003, -74.00713999999994)}})