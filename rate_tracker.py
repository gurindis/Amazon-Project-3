from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import date,datetime,timedelta
import pandas as pd
import googlemaps
import re

today = date.today().strftime("%Y/%m/%d")
year = today.split('/')[0].strip()
month = today.split('/')[1].strip()
day = today.split('/')[2].strip()
mUrl = ""
cUrl = f"{year}-{month}-{day}"
options = Options()
options.add_experimental_option('detach',True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                        options = options)
columns = {'RouteCode':str,'Company':str,'Stops/hr':int,'StopsPredictedToDeliver':int,
           'StopsPredcitedToNotDeliver':int,'totalStops':int,'StopsDelivered':int,
           'Stopsremaining':int,'FirstDeliveryTime':str,'LatestDeliveryTime':str,
           'TimeSpentDelivering_Frm_1st_Delivery':str,'PlannedEndTime':str,'TimeRemainingInShift':str,
           'TimeRemainingInShift_MINUS_TRAVELTIME':str,'DistanceLastStopToStation':str,'TravelTimeLastStopToStation':str,'LastDeliveryAddress':str}
SCENARIO1_df = pd.DataFrame(columns=columns.keys()).astype(columns)
SCENARIO2_df = SCENARIO1_df
pd.set_option('display.max_columns', None)

def getGoogleMapsData(origin,destination='',mode='driving'):
    gmaps = googlemaps.Client(key='')
    directions_result=gmaps.directions(origin,destination,mode=mode)
    if directions_result:
        total_distance=directions_result[0]['legs'][0]['distance']['text']
        total_duration=directions_result[0]['legs'][0]['duration']['text']
    return [total_distance,total_duration]

def websiteLoop(progress_status):
    time.sleep(3)
    da_list = driver.find_elements('xpath',"//EXAMPLE_TAG[@class='']")
    len_da_list = len(da_list)
    #EACH ITERATION, GET SCENARIO1 NUMBER USING FIND ELEMENT, KEEP COUNTER OF HOW MANY DAs in dalist u have gone through and at end of loop, subtact counter from SCENARIO1 number
    if progress_status == 'SCENARIO1':
        len_da_list = driver.find_element('xpath',"//*[@class = '']//EXAMPLE_TAG[contains(text(),'SCENARIO1')]/parent::div/parent::div/div").text
    else:
        len_da_list = driver.find_element('xpath',"//*[@class = 'af-link ']//EXAMPLE_TAG[contains(text(),'SCENARIO2')]/parent::div/parent::div/div").text

    if int(len_da_list)>0:
        for x in range(int(len_da_list)):
            if progress_status == 'SCENARIO1':
                len_da_list_current = driver.find_element('xpath',"//*[@class = ' ']//EXAMPLE_TAG[contains(text(),'SCENARIO1')]/parent::div/parent::div/div").text
                if int(len_da_list_current)<int(len_da_list) and x+1==int(len_da_list_current):
                    break
            else:
                len_da_list_current = driver.find_element('xpath',"//*[@class = '']//EXAMPLE_TAG[contains(text(),'SCENARIO2')]/parent::div/parent::div/div").text
                if int(len_da_list_current)<int(len_da_list) and x+1==int(len_da_list_current):
                    break

            route_code = driver.find_element('xpath',f"//EXAMPLE_TAG[@class='']/div[{x+2}]/EXAMPLE_TAG[@class='']/div/div/EXAMPLE_TAG/div/div[1]").text
            dsp = driver.find_element('xpath',f"//EXAMPLE_TAG[@class='']/div[{x+2}]/EXAMPLE_TAG[@class='']/div/div/div/EXAMPLE_TAG/div/p[0]").text
            da_element = driver.find_element('xpath',f"//EXAMPLE_TAG[a[@class='']][{x+1}]")
            da_element.click()
            delivered_stops_list = driver.find_elements('xpath',"//EXAMPLE_TAG[@class='EXAMPLE_TAG']//EXAMPLE_TAG[contains(text(),'Delivered')]")
            delivered_stops_len = len(delivered_stops_list)
            time.sleep(3)
            first_delivered_stop = driver.find_element('xpath',"//EXAMPLE_TAG[@class='']//EXAMPLE_TAG[contains(text(),'Delivered')][1]")
            first_delivered_stop.click()
            first_delivered_stop_time = driver.find_element('xpath',"//EXAMPLE_TAG[@EXAMPLE_TAG='true']").text
            backbutton = driver.find_element('xpath','//*[@EXAMPLE_TAG="true"]')
            backbutton.click()
            last_delivered_stop = driver.find_element('xpath',f"//EXAMPLE_TAG[@class=' '][EXAMPLE_TAG//EXAMPLE_TAG[contains(text(), 'Delivered')]][{delivered_stops_len}]//EXAMPLE_TAG/EXAMPLE_TAG[@style='']")
            last_delivered_stop.click()
            last_delivered_stop_address = driver.find_element('xpath',"//EXAMPLE_TAG[@class='' and not(contains(text(),'')) and not(contains(text(),''))]").text
            last_delivered_stop_time = driver.find_element('xpath',"//p[@EXAMPLE_TAG='true']").text
            googlemapsData = getGoogleMapsData(last_delivered_stop_address)
            DistanceLastStopToStation = googlemapsData[0]
            TravelTimeLastStopToStation = googlemapsData[1]
            backbutton.click()
            total_stops_element = driver.find_element('xpath',"//EXAMPLE_TAG[@class='']//table/EXAMPLE_TAG//EXAMPLE_TAG[2]")
            total_stops_text = total_stops_element.text
            total_stops_index = total_stops_text.split('/')
            delivered_stops = int(total_stops_index[0])
            total_stops = int(total_stops_index[1])
            planned_endtime_element = driver.find_element('xpath',"//EXAMPLE_TAG[EXAMPLE_TAG(text())='']/following-sibling::p[@EXAMPLE_TAG]")
            planned_endtime = planned_endtime_element.text
            time_format = "%I:%M %p"
            first_delivery_time_format = datetime.strptime(first_delivered_stop_time, time_format)
            latest_delivery_time_format = datetime.strptime(last_delivered_stop_time, time_format)
            time_remaining_in_shift_format = datetime.strptime(planned_endtime,time_format)
            time_difference = latest_delivery_time_format - first_delivery_time_format
            total_minutes = time_difference.total_seconds()/60
            if total_minutes <0:
                first_delivered_stop = driver.find_element('xpath',"//a[@EXAMPLE_TAG='']//EXAMPLE_TAG[contains(text(),'')]")
                first_delivered_stop.click()
                first_delivered_stop_time = driver.find_element('xpath',"//EXAMPLE_TAG[@EXAMPLE_TAG='true']").text
                backbutton.click()
                first_delivery_time_format = datetime.strptime(first_delivered_stop_time, time_format)
                time_difference = latest_delivery_time_format - first_delivery_time_format
                total_minutes = time_difference.total_seconds()/60
            delivery_rate_in_mins = delivered_stops/total_minutes
            #Calculate time difference from latest delivery to planned end time
            time_remaining_in_shift = time_remaining_in_shift_format - latest_delivery_time_format
            # Extract hours and minutes from the subtraction string using regular expressions
            match = re.match(r'(\d+)\s*hour', TravelTimeLastStopToStation)
            hours = int(match.group(1)) if match else 0
            match = re.search(r'(\d+)\s*min', TravelTimeLastStopToStation)
            minutes = int(match.group(1)) if match else 0
            # Subtract hours and minutes
            new_time_obj = time_remaining_in_shift - timedelta(hours=hours, minutes=minutes)
            # # Format and return the result
            time_remaining_in_shift_mins = time_remaining_in_shift.total_seconds()/60  
            stops_remaining = total_stops-delivered_stops
            #how many stops driver will get to by EOS
            stops_predicted_to_deliver = (time_remaining_in_shift_mins*delivery_rate_in_mins)
            stops_predicted_to_NOT_deliver = stops_remaining-stops_predicted_to_deliver
            delivery_rate = delivery_rate_in_mins*60
            if progress_status =='SCENARIO1':
                SCENARIO1_df.loc[len(SCENARIO1_df.index)] = [route_code,dsp,delivery_rate,stops_predicted_to_deliver,stops_predicted_to_NOT_deliver,total_stops,delivered_stops,stops_remaining,first_delivered_stop_time,last_delivered_stop_time,total_minutes,planned_endtime,time_remaining_in_shift,new_time_obj,DistanceLastStopToStation,TravelTimeLastStopToStation,last_delivered_stop_address]
            else:
                SCENARIO2_df.loc[len(SCENARIO2_df.index)] = [route_code,dsp,delivery_rate,stops_predicted_to_deliver,stops_predicted_to_NOT_deliver,total_stops,delivered_stops,stops_remaining,first_delivered_stop_time,last_delivered_stop_time,total_minutes,planned_endtime,time_remaining_in_shift,new_time_obj,DistanceLastStopToStation,TravelTimeLastStopToStation,last_delivered_stop_address]
            backbutton.click()

def getdatacUrl():
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(cUrl)
    username = driver.find_element('xpath','//*[@EXAMPLE_TAG = ""]')
    username.send_keys('')
    pin = driver.find_element('xpath','//*[@EXAMPLE_TAG = ""]')
    pin.send_keys('')
    submit = driver.find_element('xpath','//*[@EXAMPLE_TAG=""]')
    submit.click()
    driver.implicitly_wait(30)
    time.sleep(2)
    SCENARIO1_element = driver.find_element('xpath',f"//*[@EXAMPLE_TAG = '']//EXAMPLE_TAG[contains(text(),'SCENARIO1')]")
    SCENARIO2_element = driver.find_element('xpath',f"//*[@EXAMPLE_TAG = '']//EXAMPLE_TAG[contains(text(),'SCENARIO2')]")
    SCENARIO1_element.click()
    websiteLoop('SCENARIO1')
    SCENARIO2_element.click()
    websiteLoop('SCENARIO2')

getdatacUrl() 
SCENARIO1_df.sort_values(by='StopsPredcitedToNotDeliver',ascending=True)
SCENARIO1_df.to_excel('SCENARIO1_DATA.xlsx',index=False)
SCENARIO2_df.sort_values(by='StopsPredcitedToNotDeliver',ascending=True)
SCENARIO2_df.to_excel('SCENARIO2_DATA.xlsx',index=False)
