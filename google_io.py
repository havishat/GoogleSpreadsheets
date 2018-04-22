import json
import gspread
from apiclient.discovery import build
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client import file, client, tools
import requests


json_key = json.load(open('creds.json')) # json credentials file
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google
sheet = file.open("weather").sheet1 # open sheet

# store = file.Storage('storage.json')
# credz = store.get()
# if not credz or credz.invalid:
#     flow = cline.flow_from_clinetsecrets(CLIENT_SECRET, SCOPE)
#     credz = tools.run(flow, store)

# SERVICE = build(API, VERSION, http=cred.zauthorize(Http()))

all_cells = sheet.range('A1:K6') # to display the cells
sheet.resize(rows=20, cols=20) #set the rows to be till 20 and cols to be till 20

# I have tried to change the color and font of A1 in spreedsheet
# # a = sheet.cell("A1")
# sheet.cell("A1").export('bold', true)
# a.color=(1.0,0,1.0,1.0)

# colors = [["red", "white", "blue"],["#FF0000", "#FFFFFF", "#0000FF"]]
# cell = sheet.range("A1:D1")
# cell.fontcolor(colors)

# DATA = {'requests': [
#     {'repeatCell': {
#         'range': {'endRowIndex': 1},
#         'cell':  {'userEnteredFormat': {'textFormat': {'bold': True}}},
#         'fields': 'userEnteredFormat.textFormat.bold',
#     }}
# ]}

# sheet.spreadsheets().batchUpdate(
#         spreadsheetId=SHEET_ID, body=DATA).execute()

# creates first row with colomn labels 
sheet.update_acell('A1', 'Date')
sheet.update_acell('B1', 'City')
sheet.update_acell('C1', 'Max Temperature')
sheet.update_acell('D1', 'Min Temperature')
sheet.update_acell('E1', 'Max Humidity')
sheet.update_acell('F1', 'Min Humidity')
sheet.update_acell('G1', 'Mean pressure')
sheet.update_acell('H1', 'Mean wind spdm')
sheet.update_acell('I1', 'Precipitation')
sheet.update_acell('J1', 'Heating degree day')
sheet.update_acell('K1', 'Cooling degree day')

w_dates = []
MaxTemp = []
MinTemp = []
# all_responses = []
# all_responses_formatted = []
weatherdata = []
MaxHum = []
MinHum = []

meanpressurei = []
preci = []
heatingdegreedays = []
coolingdegreedays = []
meanwindspdm = []
# passing single day in the function 
def get_dates(dates):
    # url start 
    urlstart = 'http://api.wunderground.com/api/d224206bf1617448/history_'
    # url end 
    urlend = '/q/CA/Los_Angeles.json'
    
    # w_dates = ['20130101','20130102','20130103','20130104', '20130105'] dates are stored in an array
    w_dates.append(dates)

    # for loop to iterate each date from w_dates array
    for i in xrange(0,len(w_dates)):
        # enters dates in column A
        sheet.update_acell('A'+ str(i+2), w_dates[i])

        # concatenates the url start and url end with date
        url = urlstart + str(w_dates[i]) + urlend

    # data is json information in a responses formatte
    data = requests.get(url).json()
        
    # for loop to iterate data responses formate
    for summary in data['history']['dailysummary']:
        print ','.join((summary['date']['year'],summary['date']['mon'],summary['date']['mday'],summary['precipm'], summary['maxtempm'], summary['meantempm'],summary['mintempm']))
        
        # y is max temperature 
        y = summary['maxtempi']

        # x is min temperature
        x = summary['mintempi']

        # max_humidity is max humidity
        max_humidity = summary['maxhumidity']

        # min humidity 
        min_humidity = summary['minhumidity']

        # mean pressure
        mean_pressure = summary['meanpressurei']

        # meanwindspd
        mean_windspdm = summary['meanwindspdm']

        # Precipitation
        precipm = summary['precipm']

        # Heating degree days
        heating_degreedays = summary['heatingdegreedays']

        # Cooling degree days
        cooling_degreedays = summary['coolingdegreedays']

        # city name 
        city = summary['date']['tzname']

        # appended to an array 
        meanpressurei.append(mean_pressure)
        meanwindspdm.append(mean_windspdm)
        preci.append(precipm)
        heatingdegreedays.append(heating_degreedays)
        coolingdegreedays.append(cooling_degreedays)
        MaxHum.append(max_humidity)
        MinHum.append(min_humidity)
        MaxTemp.append(y)
        MinTemp.append(x)


    
    # for loop to iterate city string "America/Los_Angeles" and creat new string Los_Angeles
    for i in xrange(0,len(city)): 
        if(city[i] == "/"):
            w_city = city[i+1:(len(city)-1)]
            # print w_city

    print MaxTemp
    print MinTemp
    print MaxHum
    print MinHum
    print coolingdegreedays
    print heatingdegreedays

    # a, b, c, d, e, f, g, h, k are used as variable to increment the rows for max and min temprature and humidity
    a = 2
    b = 2
    c = 2
    d = 2
    e = 2
    f = 2
    g = 2
    h = 2
    k = 2


    # lenght of Max Temp array
    len_MaxTemp = len(MaxTemp) 
    # for loop to itereate the max Temeprature and print to the google sheet for C column and city name in B column
    for i in xrange(0,len_MaxTemp): 
        # enters city name in column B + increment of a
        sheet.update_acell('B'+ str(a), w_city)
        # enters Max Temp in column C
        sheet.update_acell('C'+ str(a), MaxTemp[i])
        a=a+1
        
    # length of Min temp array
    len_MinTemp = len(MinTemp) 
    # for loop to itereate the min Temp and print to the google sheet for D column
    for i in xrange(0,len_MinTemp): 
         # enters Min Temp in column B + increment of b
        sheet.update_acell('D'+ str(b), MinTemp[i])
        b=b+1
    # length of Max Hmuidity
    len_MaxHum = len(MaxHum) 
    # for loop to itereate the max humidity and print to the google sheet for E column
    for i in xrange(0,len_MaxHum): 
        sheet.update_acell('E'+ str(c), MaxHum[i])
        c=c+1

    # length of Min Hmuidity  
    len_MinHum = len(MinHum)
    # for loop to itereate the min humidity and print to the google sheet for F column
    for i in xrange(0,len_MinHum): 
        sheet.update_acell('F'+ str(d), MinHum[i])
        d=d+1

    # length of mean pressure
    len_meanpressurei = len(meanpressurei)
    # for loop to itereate the mean pressure and print to the google sheet for G column
    for i in xrange(0,len_meanpressurei): 
        sheet.update_acell('G'+ str(e), meanpressurei[i])
        e=e+1
    # length of mean wind spd
    len_meanwindspdm = len(meanwindspdm)
    # for loop to itereate the mean wind spd and print to the google sheet for H column
    for i in xrange(0,len_meanwindspdm): 
        sheet.update_acell('H'+ str(k), meanwindspdm[i])
        k=k+1
    # length of Precipitation
    len_preci = len(preci)
    # for loop to itereate the hPrecipitation and print to the google sheet for I column
    for i in xrange(0,len_preci): 
        sheet.update_acell('I'+ str(f), preci[i])
        f=f+1
    # length of heatingdegreedays
    len_heatingdegreedays = len(heatingdegreedays)
    # for loop to itereate the heatingdegreedays and print to the google sheet for J column
    for i in xrange(0,len_heatingdegreedays): 
        sheet.update_acell('J'+ str(g), heatingdegreedays[i])
        g=g+1
    
    # length of coolingdegreedays
    len_coolingdegreedays = len(coolingdegreedays)
    # for loop to itereate the coolingdegreedays and print to the google sheet for K column
    for i in xrange(0,len_coolingdegreedays): 
        sheet.update_acell('K'+ str(h), coolingdegreedays[i])
        h=h+1


# ///

    # for responds in all_responses:
    #     all_responses_formatted.append(responds.json())
    #     # print all_responses_formatted

    # for formatted_response in all_responses_formatted:
    #     weatherdata.append(get_weatherdata(formatted_response))
        # print formatted_response
   

# The value of __name__  attribute is set to '__main__'  when module run as main program. 
# Otherwise the value of __name__  is set to contain the name of the module. 
if __name__ == "__main__":
    from datetime import date
    from dateutil.rrule import rrule, DAILY

    # start date
    start = date(2013, 1, 1) 
    # end date
    end = date(2013, 1, 5)

    # for loop iterates start to end dates
    for dt in rrule(DAILY, dtstart=start, until=end):
        get_dates(dt.strftime("%Y%m%d"))


# prints all the cells in the spreedsheet
# for cell in all_cells:
# 	print cell.value