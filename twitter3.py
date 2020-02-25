import folium, json, ssl
from geopy.geocoders import Nominatim
from geopy import ArcGIS
import urllib.request, urllib.parse, urllib.error
import twurl

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
except:
    pass

def find_loc(user):
    #acct = ''
    #if (len(acct) < 1): acct = input('Enter Twitter Account:')
    url = twurl.augment(TWITTER_URL, {'screen_name': str(user), 'count': '20'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    dct = {}
    for n in js["users"]:
        dct1 = {}
        if n["location"] != '':
            dct1[n["profile_image_url"]] = [locator(n["location"]),'@'+n["screen_name"]]
            dct[n['name']] = dct1
    return map(dct)

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
    m = folium.Map(location=(18,-40),tiles='OpenStreetMap', zoom_start=3, control_scale=True)
    for i in dct:
        for icon in dct[i]:
            locationUser = dct[i][icon][0]
            if locationUser == None:
                continue
            iconUser = folium.features.CustomIcon(icon, icon_size=(50,50))
            popupUser = "<strong>{}</strong><br>{}".format(i,dct[i][icon][1])
            folium.Marker(locationUser,tooltip = i, popup=popupUser,icon = iconUser).add_to(m)
    return m

if __name__ == "__main__":
    dic = find_loc()
    map(dic)
