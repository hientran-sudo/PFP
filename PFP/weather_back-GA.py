'''
Author: CAM (AMDG)
Language: Python 2
Last Edit: 4/24/18

Description: Program that takes data from TWC PFP API and calculates uncertainty in forecast
             for given hour interval. Can return Temperature, Precipitation, or both.

Setup Instructions: Must install 'numpy' and 'requests' libraries to run.
                    Run 'pip install numpy' and 'pip install requests' from CMD.
                    pip is included with all Python versions.

Execution Instructions: Must run from CMD or Terminal. Run by executing command 'python weather_back.py'.
                        Result be written to JSON file that will be created in the directory where
                        program is run from. It will be called 'output.json'. Every time the program
                        is run, the 'output.json' file will be overwritten.

Notes: Confidence for temperature set to +/- 3.00 degrees based on TWC advisory
       Confidence for precipitation set to +/- 0.04 inches based on TWC advisory
'''

from json import dumps
from numpy import interp
from requests import get

def get_data(lat, lon, parameter):
    '''Get the temperature or qpf data from the API at a given latitude and longitude'''
    raw_data = get('https://api.weather.com/v3/wx/forecast/probabilistic?'\
    'geocode='+str(lat)+','+str(lon)+'&elevation=2000&landuse=1&format=json&units=e&'\
    'percentiles='+parameter+':0:2:4:6:8:10:12:14:16:18:20:22:24:26:28:30:32:34:36:38:40:42:44:46:48:50:52:54:56:58:60:62:64:66:68:70:72:74:76:78:80:82:84:86:88:90:92:94:96:98:100;'+parameter+':10:50:90'\
    '&apiKey=97710d50138743fdb10d50138783fd65').json()['forecasts1Hour']
    return raw_data

def weather(lat, lon, hour, city, parameter, confidence_range):
    '''Parse readings and calculate confidence'''
    data = get_data(lat, lon, parameter)
    percentile_points = data['percentiles'][0]['percentilePoints']
    readings = data['percentiles'][0]['percentileValues'][hour]
    tenth_ninetieth = data['percentiles'][1]['percentileValues'][hour][0], data['percentiles'][1]['percentileValues'][hour][2]
    median = data['percentiles'][1]['percentileValues'][hour][1]

    low = interp(median - confidence_range, readings, percentile_points)
    high = interp(median + confidence_range, readings, percentile_points)
    confidence = round((high-low)/100, 2)
    
    out = {}
    out['City'] = city
    out['Latitude'] = lat
    out['Longitude'] = lon
    out['Confidence'] = confidence
    if parameter == 'qpf':
        out['Median'] = str('%.2f' % median) + ' in.'
        out['Range'] = str('%.2f' % tenth_ninetieth[0]) + ' in. - ' + str('%.2f' % tenth_ninetieth[1]) + ' in.'
    elif parameter == 'temperature':
        out['Median'] = str('%.0f' % median) + ' F'
        out['Range'] = str('%.0f' % tenth_ninetieth[0]) + ' F - ' + str('%.0f' % tenth_ninetieth[1]) + ' F'
    return out

def main(lat, lon, hour, parameter, city):
    '''Run on desired parameter(s) and return result'''
    out = {}
    if parameter == 'qpf':
        out['precipitation'] = weather(lat, lon, hour, city, parameter, confidence_range=0.04)
    if parameter == 'temperature':
        out['temperature'] = weather(lat, lon, hour, city, parameter, confidence_range=3)
    elif parameter == '':
        out['precipitation'] = weather(lat, lon, hour, city, parameter='qpf', confidence_range=0.04)
        out['temperature'] = weather(lat, lon, hour, city, parameter='temperature', confidence_range=3)
    return out

# Map Output #
map_output = {}

map_output['Athens'] = main(33.95, -83.36, 12, '', 'Athens') # Both for Atlanta at hour 12
map_output['Atlanta'] = main(33.75, -84.39, 12, '', 'Atlanta') # Both for Atlanta at hour 12
map_output['Augusta'] = main(33.47, -82.01, 12, '', 'Augusta') # Both for Atlanta at hour 12
map_output['Bainbridge'] = main(30.90, -84.58, 12, '', 'Bainbridge') # Both for Atlanta at hour 12
map_output['Blakely'] = main(31.38, -84.93, 12, '', 'Blakely') # Both for Atlanta at hour 12
map_output['Colombus'] = main(32.46, -84.99, 12, '', 'Colombus') # Both for Atlanta at hour 12
map_output['Cordele'] = main(31.96, -83.78, 12, '', 'Cordele') # Both for Atlanta at hour 12
map_output['Dalton'] = main(34.77, -84.97, 12, '', 'Dalton') # Both for Atlanta at hour 12
map_output['Dawson'] = main(31.77, -84.45, 12, '', 'Dawson') # Both for Atlanta at hour 12
map_output['Jesup'] = main(31.61, -81.88, 12, '', 'Jesup') # Both for Atlanta at hour 12
map_output['La_Grange'] = main(33.04, -85.03, 12, '', 'La Grange') # Both for Atlanta at hour 12
map_output['Macon'] = main(32.84, -83.63, 12, '', 'Macon') # Both for Atlanta at hour 12
map_output['Monroe'] = main(33.79, -83.71, 12, '', 'Monroe') # Both for Atlanta at hour 12
map_output['Peachtree_City'] = main(33.40, -84.60, 12, '', 'Peachtree City') # Both for Atlanta at hour 12
map_output['Perry'] = main(32.49, -83.73, 12, '', 'Perry') # Both for Atlanta at hour 12
map_output['Rome'] = main(34.26, -85.16, 12, '', 'Rome') # Both for Atlanta at hour 12
map_output['Savannah'] = main(32.08, -81.10, 12, '', 'Savannah') # Both for Atlanta at hour 12
map_output['Sylvania'] = main(32.75, -81.64, 12, '', 'Sylvania') # Both for Atlanta at hour 12
map_output['Tifton'] = main(31.45, -83.51, 12, '', 'Tifton') # Both for Atlanta at hour 12
map_output['Toccoa'] = main(34.58, -83.33, 12, '', 'Toccoa') # Both for Atlanta at hour 12
map_output['Valdosta'] = main(30.83, -83.28, 12, '', 'Valdosta') # Both for Atlanta at hour 12
map_output['Vidalia'] = main(32.22, -82.41, 12, '', 'Vidalia') # Both for Atlanta at hour 12

# Write result to JSON file #
with open('map_output.json', 'w') as ofile:
    ofile.write(dumps(map_output, indent=2, sort_keys=True))
ofile.close()

# Graph Output #
alldays = {}

day0 = {}
day0['Atlanta'] = main(33.75, -84.39, 0, '', 'Atlanta') # Both for Atlanta at hour 0
alldays['day0'] = day0

day1 = {}
day1['Atlanta'] = main(33.75, -84.39, 24, '', 'Atlanta') # Both for Atlanta at hour 24
alldays['day1'] = day1

day2 = {}
day2['Atlanta'] = main(33.75, -84.39, 48, '', 'Atlanta')
alldays['day2'] = day2

day3 = {}
day3['Atlanta'] = main(33.75, -84.39, 72, '', 'Atlanta')
alldays['day3'] = day3

day4 = {}
day4['Atlanta'] = main(33.75, -84.39, 96, '', 'Atlanta')
alldays['day4'] = day4

day5 = {}
day5['Atlanta'] = main(33.75, -84.39, 120, '', 'Atlanta')
alldays['day5'] = day5

day6 = {}
day6['Atlanta'] = main(33.75, -84.39, 144, '', 'Atlanta')
alldays['day6'] = day6

graph_output = {}
graph_output["alldays"] = alldays

# day7 = {}
# day7['Atlanta'] = main(33.75, -84.39, 168, '', 'Atlanta')
# alldays['day7'] = day7

# day8 = {}
# day8['Atlanta'] = main(33.75, -84.39, 192, '', 'Atlanta')
# alldays['day8'] = day8

# day9 = {}
# day9['Atlanta'] = main(33.75, -84.39, 216, '', 'Atlanta')
# alldays['day9'] = day9

# day_ten = {}
# day_ten['Atlanta'] = main(33.75, -84.39, 240, '', 'Atlanta')
# alldays['day_ten'] = day_ten

# Write result to JSON file #
with open('graph/graph_output.json', 'w') as ofile:
    ofile.write(dumps(graph_output, indent=2, sort_keys=True))
ofile.close()
