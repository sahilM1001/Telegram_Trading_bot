import re, os
from telethon import TelegramClient, events, sync
from common.filters import buy_filter, exit_filter, book_profits_filter
from dotenv import load_dotenv, find_dotenv
from brokers.FivePaisa import FivePaisa

load_dotenv(find_dotenv())

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('session_28_nov', api_id , api_hash)
five_paisa = FivePaisa()

with client:
    
    client.start()
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
    @client.on(events.NewMessage(chats=1400983952)) # TODO change channel id to tips provider channel id 
    async def handler(event):
        print("New message received")
        print("Event text: ", event.raw_text)
        recommendation = event.raw_text

        buy_regex = re.compile(r'\b(?:buy)\b', re.IGNORECASE)
        exit_regex = re.compile(r'\b(?:exit from)\b', re.IGNORECASE)
        book_profits_regex = re.compile(r'\b(?:book profits)\b', re.IGNORECASE)

        if buy_regex.search(recommendation):
            print("This is a buy call.")
            transaction_details = buy_filter(recommendation)
            print("Cleaned transaction details received: ", transaction_details)
            position_amount = five_paisa.get_position_amount()

            share_qty = five_paisa.get_share_qty(transaction_details['price'], position_amount)
            if share_qty > 0:
                five_paisa.buy(transaction_details['scrip'], transaction_details['stop_loss'], transaction_details['target'], share_qty, transaction_details['price'])
            else:
                print("Not taking trade because share qty is 0 or limit not available")
        elif exit_regex.search(recommendation):
            print("This is a exit call.")
            transaction_details = exit_filter(recommendation)
            print("Cleaned transaction details received: ", transaction_details)
            five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            
        elif book_profits_regex.search(recommendation):
            print("This is a call to book profits")
            transaction_details = book_profits_filter(recommendation)
            five_paisa.sell(transaction_details['scrip'], transaction_details['target'])
            
        else:
            print("No regex match")

        # TODO create broker connectors to execute orders
        


    client.run_until_disconnected()
    