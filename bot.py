import re, os
from telethon import TelegramClient, events, sync
from common.filters import buy_filter, exit_filter
from dotenv import load_dotenv

load_dotenv()

client = TelegramClient('session_name', os.getenv('api_id'), os.getenv('api_hash'))

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
            

    @client.on(events.NewMessage(chats=2129439742)) # TODO change channel id to tips provider channel id 
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
        elif exit_regex.search(recommendation):
            print("This is a exit call.")
            transaction_details = exit_filter(recommendation)
            print("Cleaned transaction details received: ", transaction_details)
        elif book_profits_regex.search(recommendation):
            print("This is a call to book profits")
            # TODO create book profits filter
        else:
            print("No regex match")

        # TODO Add strategy to execute trades based on capital value so that not all capital is employed to a single trade
        # TODO create broker connectors to execute orders
        # TODO Add logging to file to record transaction details


    client.run_until_disconnected()
    