import re
import pandas as pd
from datetime import date    
def evaluate_regex_and_return_value(regex, message):
    """
    This is a common function to evaluate a given regex and return value if there is a match
    :param regex -> regex that needs to be matched on the received message
    :param message -> Message text that was received on the channel
    """
    reg = re.compile(regex, re.IGNORECASE)
    match = reg.search(message)

    if match:
        text = match.group(1)
        try: 
            # used to return numeric float values such as market price, etc
            return float(text)
        except:
            return text.strip()
    else:
        print("No text found for the sent regex")

def get_scrip_name_from_scrip_master(scrip_master, scrip_name, channel_num):
    
    current_year = date.today().year
    scrip_name = scrip_name.strip()
    print("above if condition match")
    scrip_row = scrip_master[scrip_master['Name'] == scrip_name]
    if scrip_row.shape[0] > 0:
        print("Inside if condition match")
        row = ["", ""]
        return scrip_name
        row[0] = scrip_master[scrip_master['Name'] == scrip_name].iloc[0]['Scripcode']
        row[1] = scrip_master[scrip_master['Name'] == scrip_name].iloc[0]['Exch']
        return row
    else:
        if channel_num == "channel_3":
            print("Inside channel 3")
            scrip_arr = scrip_name.split(" ")
            search_key = scrip_arr[0] + " " + scrip_arr[1] + " " + scrip_arr[2].title() + " " + str(current_year) + " " + scrip_arr[-1] + " " + str(format(float(scrip_arr[-2]),'.2f'))
            return search_key
            row = ["", ""] 
            row[0] = scrip_master[scrip_master['Name'] == search_key].iloc[0]['Scripcode']
            row[1] = scrip_master[scrip_master['Name'] == search_key].iloc[0]['Exch']
            return row

