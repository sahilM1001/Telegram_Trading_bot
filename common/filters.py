from common.helper import evaluate_regex_and_return_value

def buy_filter(event_text):
    """
    This function is used to filter out transaction details from the buy message received
    """
    transaction_details = {}
    
    transaction_details['scrip'] = evaluate_regex_and_return_value(r'(?<=\bBUY\b\s)(.*)', event_text)
    transaction_details['stop_loss'] = evaluate_regex_and_return_value(r'\bSL\s*:\s*(.*)', event_text) 
    transaction_details['target'] = evaluate_regex_and_return_value(r'\bTGT\s*:\s*(.*)',event_text)

    return transaction_details


def exit_filter(event_text):
    """
    This function is used to filter out transaction details from the Exit position message received
    """
    print("event text: ", event_text)
    transaction_details = {}
    
    transaction_details['scrip'] = evaluate_regex_and_return_value(r'Exit from\s*\n*\s*(.*)', event_text)
    transaction_details['target'] = evaluate_regex_and_return_value(r'\bAT:\s*(.*)',event_text)

    return transaction_details