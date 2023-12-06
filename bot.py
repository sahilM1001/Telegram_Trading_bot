import re, os
from telethon import TelegramClient, events, sync
from common.filters import buy_filter, exit_filter, book_profits_filter
from common.helper import get_scrip_name_from_scrip_master, create_error_message
from dotenv import load_dotenv, find_dotenv
from brokers.FivePaisa import FivePaisa
import sys, traceback

load_dotenv(find_dotenv())

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

five_paisa = FivePaisa()


with TelegramClient('session_7_dec', api_id , api_hash) as client:
    
    client.start()
    print("Client is connected")
    # use below code to find channel id
 
    """dialogs = client.get_dialogs()
    five_paisa_id = 0
    for dialog in dialogs:
        print("Dialog: ", dialog.name)
        print("dialog mesage peerchannel: ", dialog.message.peer_id.channel_id)
        five_paisa_id = dialog.message.peer_id.channel_id

        print("Dialog: ", dialog)
        print("==========================================") 
            

    sys.exit()"""
    # Sahil test channel ID-> 2129439742
    # 5Paisa telegram channel id -> 1400983952
    @client.on(events.NewMessage(chats=1400983952)) 
    async def handler(event):
        """
        This handler is used to get trade recommendations from 5Paisa channel
        """
        print("New message received on 5PAISA Channel")
        print("Event text: ", event.raw_text)
        recommendation = event.raw_text

        buy_regex = re.compile(r'\b(?:buy)\b', re.IGNORECASE)
        exit_regex = re.compile(r'\b(?:exit from)\b', re.IGNORECASE)
        book_profits_regex = re.compile(r'\b(?:book profits)\b', re.IGNORECASE)

        if buy_regex.search(recommendation):
            try:
                print("This is a buy call.")
                
                scrip_name_regex = r'(?<=\bBUY\b\s)(.*)'
                price_regex = r'\bCMP\s*:\s*(.*)'
                stop_loss_regex = r'\bSL\s*:\s*(.*)'
                target_regex = r'\bTGT\s*:\s*(.*)'

                transaction_details = buy_filter(recommendation, scrip_name_regex, price_regex, stop_loss_regex, target_regex)
                print("Cleaned transaction details received: ", transaction_details)
                
                position_amount = five_paisa.get_position_amount()
                share_qty = five_paisa.get_share_qty(transaction_details['price'], position_amount)

                if share_qty > 0:
                    five_paisa.buy(transaction_details['scrip'], transaction_details['stop_loss'], transaction_details['target'], share_qty, transaction_details['price'])
                else:
                    print("Not taking trade because share qty is 0 or limit not available")
            except Exception as e:
                # TODO add exception alerting to telegram channel for manual intervention
                exception_details = str(e)
                traceback_details =  traceback.format_exc()
                error_message = create_error_message("5Paisa Channel", recommendation, exception_details, traceback_details)
                await client.send_message(entity=2067424743, message=error_message)
                print("Exception occured while processing BUY call from 5 Paisa")
        elif exit_regex.search(recommendation):
            try:
                print("This is a exit call.")
                scrip_name_regex = r'Exit from\s*\n*\s*(.*)'
                target_regex = r'\bAT\s*:\s*(.*)'

                transaction_details = exit_filter(recommendation, scrip_name_regex, target_regex)
                print("Cleaned transaction details received: ", transaction_details)
                
                """print("Transaction details of target: ", type(transaction_details['Target']))
                if transaction_details['target'] == None:
                    target_regex = r'\bAt :\s*(.*)'
                    transaction_details = exit_filter(recommendation, scrip_name_regex, target_regex)

                print("transaction details: ", transaction_details)"""
                five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            except Exception as e:
                # TODO add exception alerting to telegram channel for manual intervention

                exception_details = str(e)
                traceback_details =  traceback.format_exc()
                error_message = create_error_message("5Paisa Channel", recommendation, exception_details, traceback_details)
                await client.send_message(entity=2067424743, message=error_message)

                print("Exception occured while processing EXIT call from 5 Paisa")
            
        elif book_profits_regex.search(recommendation):
            try:
                print("This is a call to book profits")
                
                scrip_name_regex = r'Book Profits in\s*\n*\s*(.*)'
                target_regex = r'\bAT CMP :\s*(.*)'

                transaction_details = book_profits_filter(recommendation, scrip_name_regex, target_regex)
                five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            except Exception as e:
                # TODO add exception alerting to telegram channel for manual intervention

                exception_details = str(e)
                traceback_details =  traceback.format_exc()
                error_message = create_error_message("5Paisa Channel", recommendation, exception_details, traceback_details)
                await client.send_message(entity=2067424743, message=error_message)

                print("Exception occured while processing BOOK PROFITS call from 5 Paisa")
            
        else:
            print("No regex match")

        # TODO create broker connectors to execute orders
        
    
    # Angel one channel id -> 1354170870
    @client.on(events.NewMessage(chats=2129439742)) 
    async def handler_2(event):
        """
        This handler is used to filter trade recommendations from Angel One's Advisory channel
        """
        print("New message received on ANGEL ONE SECOND channel")
        print("Event text: ", event.raw_text)
        recommendation = event.raw_text

        buy_short_term_regex = re.compile(r'\bBUY', re.IGNORECASE)
       
        exit_regex = re.compile(r'\b(Exit )\b', re.IGNORECASE)
        book_profits_regex = re.compile(r'\b(Book profits In)\b', re.IGNORECASE)

        if buy_short_term_regex.search(recommendation):
            try: 
                print("This is a buy call.")
                scrip_name_regex = r'BUY\s+(.+?)\s\d+\s+(?:shares|lot) at \d+\.'
                price_regex = r'at (\d+)'
                stop_loss_regex = r'Message : SL (.*?) TGT'
                target_regex= r'TGT\s*(\d+) MODIFY'

                
                transaction_details = buy_filter(recommendation, scrip_name_regex, price_regex, stop_loss_regex, target_regex)
                transaction_details['scrip'] = get_scrip_name_from_scrip_master(five_paisa.scrip_master, transaction_details['scrip'], "channel_3")

                print("Cleaned transaction details received: ", transaction_details)
                print("---------------------------------------------")
                print("---------------------------------------------")
                
                
                position_amount = five_paisa.get_position_amount()
                share_qty = five_paisa.get_share_qty(transaction_details['price'], position_amount)

                if share_qty > 0:
                    five_paisa.buy(transaction_details['scrip'], transaction_details['stop_loss'], transaction_details['target'], share_qty, transaction_details['price'])
                else:
                    print("Not taking trade because share qty is 0 or limit not available")
            except Exception as e:
                # TODO add exception alerting to telegram channel for manual intervention
                exception_details = str(e)
                traceback_details =  traceback.format_exc()
                error_message = create_error_message("Angel One Channel", recommendation, exception_details, traceback_details)
                await client.send_message(entity=2067424743, message=error_message)
                print("Exception occured while processing BUY call from Angel One")
        elif exit_regex.search(recommendation):
            try:
                print("This is a exit call.")
                scrip_name_regex =""
                target_regex = ""
                if "@" in recommendation or "AT" in recommendation or "at" in recommendation:
                    scrip_name_regex =  r'EXIT\s+([^@]+) (?:@|at)'
                    target_regex = r'@\s*(\d+\.\d+)'
                else:
                    scrip_name_regex =  r'EXIT\s+(.+)'
                    target_regex = None

                transaction_details = exit_filter(recommendation, scrip_name_regex, target_regex)
                print("Cleaned transaction details received: ", transaction_details)

                five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            except Exception as e:
                # TODO add exception alerting to telegram channel for manual intervention
                exception_details = str(e)
                traceback_details =  traceback.format_exc()
                error_message = create_error_message("Angel One Channel", recommendation, exception_details, traceback_details)
                await client.send_message(entity=2067424743, message=error_message)
                print("Exception occured while processing EXIT CALL from Angel One")
                pass
            
        elif book_profits_regex.search(recommendation):
            try:
                print("This is a call to book profits")
                
                scrip_name_regex = r'Book Profits? IN\s+([^@]+) (?:@|at)'
                target_regex = r'(?:@|at)\s*([\d.]+)'
                
                transaction_details = book_profits_filter(recommendation, scrip_name_regex, target_regex)
                transaction_details['scrip'] = get_scrip_name_from_scrip_master(five_paisa.scrip_master, transaction_details['scrip'], "channel_3")
                
                print("cleaned transaction details in book profits: ", transaction_details)
                five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            except Exception as e:
                # TODO add exception alerting to telegram channel for manual intervention
                exception_details = str(e)
                traceback_details =  traceback.format_exc()
                error_message = create_error_message("Angel One Channel", recommendation, exception_details, traceback_details)
                await client.send_message(entity=2067424743, message=error_message)
                print("Exception occured while processing BOOK PROFITS call from Angel One")    
        else:
            print("No regex match")


    client.run_until_disconnected()
    