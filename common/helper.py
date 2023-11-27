import re
    
def evaluate_regex_and_return_value(regex, message):
    """
    This is a common function to evaluate a given regex and return value if there is a match
    """
    reg = re.compile(regex, re.IGNORECASE)
    match = reg.search(message)

    if match:
        text = match.group(1)
        return text
    else:
        print("No text found for the sent regex")


