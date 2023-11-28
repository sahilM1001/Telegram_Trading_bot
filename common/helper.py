import re
    
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


