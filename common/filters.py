from common.helper import evaluate_regex_and_return_value

def buy_filter(event_text, scrip_reg, price_reg, stop_loss_reg=None, target_reg=None):
    """
    This function is used to filter out transaction details from the buy message received
    :param event_text -> Message text that was received on the channel
    """
    transaction_details = {}
    
    transaction_details['scrip'] = evaluate_regex_and_return_value(scrip_reg, event_text)
    transaction_details['price'] = evaluate_regex_and_return_value(price_reg, event_text) 
    if stop_loss_reg is not None:
        transaction_details['stop_loss'] = evaluate_regex_and_return_value(stop_loss_reg, event_text) 
    if target_reg is not None:
        transaction_details['target'] = evaluate_regex_and_return_value(target_reg,event_text)

    return transaction_details


def exit_filter(event_text, scrip_reg, target_reg=None):
    """
    This function is used to filter out transaction details from the Exit position message received
    :param event_text -> Message text that was received on the channel
    """
    print("event text: ", event_text)
    transaction_details = {}
    
    transaction_details['scrip'] = evaluate_regex_and_return_value(scrip_reg, event_text)
    if target_reg is not None:
        transaction_details['target'] = evaluate_regex_and_return_value(target_reg,event_text)

    return transaction_details


def book_profits_filter(event_text, scrip_reg, target_reg=None):
    """
    This function is used to filter out transaction details from the book profits message received
    :param event_text -> Message text that was received on the channel
    """
    print("event text: ", event_text)
    transaction_details = {}
    
    transaction_details['scrip'] = evaluate_regex_and_return_value(scrip_reg, event_text)
    if target_reg is not None:
        transaction_details['target'] = evaluate_regex_and_return_value(target_reg,event_text)

    return transaction_details