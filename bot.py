import re, os
from telethon import TelegramClient, events, sync
from common.filters import buy_filter, exit_filter, book_profits_filter
from dotenv import load_dotenv, find_dotenv
from brokers.FivePaisa import FivePaisa

load_dotenv(find_dotenv())

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

five_paisa = FivePaisa()


with TelegramClient('session_1_dec', api_id , api_hash) as client:
    
    client.start()
    print("Client is connected")
    # use below code to find channel id
    """ 
    dialogs = client.get_dialogs()
    five_paisa_id = 0
    for dialog in dialogs:
        print("Dialog: ", dialog.name)
        print("dialog mesage peerchannel: ", dialog.message.peer_id.channel_id)
        five_paisa_id = dialog.message.peer_id.channel_id

        print("Dialog: ", dialog)
        print("==========================================") """
            
    # Sahil test channel ID-> 2129439742
    # 5Paisa telegram channel id -> 1400983952
    @client.on(events.NewMessage(chats=1400983952)) 
    async def handler(event):
        print("New message received")
        print("Event text: ", event.raw_text)
        recommendation = event.raw_text

        buy_regex = re.compile(r'\b(?:buy)\b', re.IGNORECASE)
        exit_regex = re.compile(r'\b(?:exit from)\b', re.IGNORECASE)
        book_profits_regex = re.compile(r'\b(?:book profits)\b', re.IGNORECASE)

        if buy_regex.search(recommendation):
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
        elif exit_regex.search(recommendation):
            print("This is a exit call.")
            scrip_name_regex = r'Exit from\s*\n*\s*(.*)'
            target_regex = r'\bAT:\s*(.*)'

            transaction_details = exit_filter(recommendation, scrip_name_regex, target_regex)
            print("Cleaned transaction details received: ", transaction_details)

            five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            
        elif book_profits_regex.search(recommendation):
            print("This is a call to book profits")
            
            scrip_name_regex = r'Book Profits in\s*\n*\s*(.*)'
            target_regex = r'\bAT CMP :\s*(.*)'
            
            transaction_details = book_profits_filter(recommendation, scrip_name_regex, target_regex)
            five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            
        else:
            print("No regex match")

        # TODO create broker connectors to execute orders
        


    client.run_until_disconnected()
    