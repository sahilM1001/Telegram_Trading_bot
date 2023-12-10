from common.TradingDesk import TradingDesk
import pandas as pd
import time, os
from datetime import date
from py5paisa import FivePaisaClient
from py5paisa.order import Order, OrderType, Exchange
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class FivePaisa(TradingDesk):
    """
    This is the sample class that inherits functions from the TradingDesk class.
    This class will be used to perform 5 Paisa specific transactions through the python SDK for 5Paisa
    """
    

    def __init__(self):
        self.CAPITAL = 20000
        self.PORTFOLIO_PERCENT = 20
        self.scrip_master = self.get_scrip_master()
        self.cred = {
            "APP_NAME": os.getenv("FIVE_PAISA_APP_NAME"),
            "APP_SOURCE":os.getenv("FIVE_PAISA_APP_SOURCE"),
            "USER_ID":os.getenv("FIVE_PAISA_USER_ID"),
            "PASSWORD":os.getenv("FIVE_PAISA_PASSWORD"),
            "USER_KEY":os.getenv("FIVE_PAISA_USER_KEY"),
            "ENCRYPTION_KEY":os.getenv("FIVE_PAISA_ENCRYPTION_KEY")
        }

        print("self.creds: ", self.cred)

        """self.five_paisa_broker = FivePaisaClient() 

        self.five_paisa_broker.get_totp_session('Your ClientCode','TOTP from authenticator app','Your Pin') """

    def get_scrip_master(self):
        """
        This function is used to download scrip master file from 5 paisa whenever the instance is created.
        """
        print("Inside 5Paisa scrip master")
        scrip_master = pd.read_csv("https://images.5paisa.com/website/scripmaster-csv-format.csv")
        return scrip_master


    def buy(self, scrip_name, stop_loss, target, share_qty, market_price):
        """
        This function is used to execute buy orders on 5Paisa platform.
        Currently function only adds data to excel for performance tracking purposes.
        :param scrip_name -> Name of the stock that needs to be purchased
        :param stop_loss -> Price for stop_loss
        :param target -> Target/take profit price for the order
        :param share_qty -> Number of stocks to be purchased
        :param market_price -> Market price of the stocks that are to be purchased 
        """
        # TODO Add 5Paisa API calls to actually execute orders on 5Paisa account
        print("Buy order received")

        print(f"Buy {scrip_name} with stop loss {stop_loss} and target {target} with quantity {share_qty}")
        scrip_code_row = self.scrip_master[self.scrip_master['Name'] == scrip_name].iloc[0]
        scrip_code = scrip_code_row['Scripcode']

        lot_size = self.get_lot_size(scrip_code)
        approved_position_amount = self.get_position_amount()

        if lot_size != 1:
            share_qty = lot_size
            print(f" for approved_postion_amount: {approved_position_amount} lot size is {share_qty}")
            if (share_qty * market_price) < approved_position_amount: 
                share_qty = self.get_max_share_qty(share_qty * market_price, approved_position_amount, lot_size)
                print(f" for approved_postion_amount: {approved_position_amount} share_qty from get max share qty is {share_qty}")
        
        if (share_qty * market_price) <= approved_position_amount:


            """order_response = self.five_paisa_broker.place_order(OrderType='B', Exchange=scrip_code_row['Exch'], 
                                               ExchangeType=scrip_code_row['ExchType'], ScripCode = scrip_code_row['Scripcode'], 
                                               Qty=share_qty, Price=market_price, StopLossPrice = stop_loss)"""
            
            df = pd.read_csv("brokers/order_tracking_v3.csv")

            self.CAPITAL -= (share_qty * market_price)
            new_row = {
                "date": str(date.today()),
                "time": str(time.strftime("%H:%M:%S", time.localtime())),
                "order_type": "BUY",
                "scrip_code": scrip_code,
                "scrip_name": scrip_name,
                "price": market_price,
                "quantity": share_qty,
                "stop_loss": stop_loss,
                "target": target,
                "bought_at": market_price,
                "position": "OPEN",
                "capital_remaining": self.CAPITAL,
                "brokerage": 20
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            df.to_csv("brokers/order_tracking_v3.csv", index=False)

            
        else:
            print(f"Shares were not bought because position amount {share_qty * market_price} > {self.get_position_amount()} approved position amount")

    def sell(self, scrip_name, target):
        """
        This function is used to execute SELL orders on 5Paisa platform.
        Currently function only adds data to excel for performance tracking purposes.
        :param scrip_name -> Name of the stock that needs to be SOLD
        :param target -> Target/take profit price for the order
        """
        # TODO Add 5Paisa API calls to actually execute sell orders on 5Paisa account
        print("Sell order received")
        print(f"Sell {scrip_name} at price {target}")

        scrip_code_row = self.scrip_master[self.scrip_master['Name'] == scrip_name].iloc[0]
        scrip_code = scrip_code_row['Scripcode']


        df = pd.read_csv("brokers/order_tracking_v3.csv")
        
        
        filtered_row = df[(df['order_type'] == "BUY") & (df['scrip_name'] == scrip_name) & (df['position'] == "OPEN")]
        quantity_value = filtered_row['quantity'].iloc[0] if not filtered_row.empty else 0
        bought_at = filtered_row['price'].iloc[0] if not filtered_row.empty else 0

        if filtered_row.shape[0] > 0:
            self.CAPITAL += (quantity_value * target)
            new_row = {
                "date": str(date.today()),
                "time": str(time.strftime("%H:%M:%S", time.localtime())),
                "order_type": "SELL",
                "scrip_code": scrip_code,
                "scrip_name": scrip_name,
                "price": target,
                "quantity": quantity_value ,
                "stop_loss": "",
                "target": "",
                "bought_at": bought_at,
                "position": "CLOSED",
                "capital_remaining": self.CAPITAL,
                "brokerage": 20
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            df.to_csv("brokers/order_tracking_v3.csv", index=False)
        else:
            print("Not selling as no previous buy found")
            
    def get_open_positions(self):
        print("Get open positions")

    def get_available_margin(self):
        print("Get available margin")
 
    def cancel_order(self):
        print("Cancel order received")
     
    def modify_order(self):
        print("Modify Order received")

    def get_position_amount(self):
        """
        This function is used to find capital that can be alloted to a specific BUY ORDER.
        Used to restrict allocating entire capital to one trade-> Risk Management 
        """
        # TODO Make this more robust based on options or Equity calls
        return (self.CAPITAL * self.PORTFOLIO_PERCENT ) / 100
    
    def get_share_qty(self, share_price, position_amount):
        """
        This function is used to get the number of shares that can be purchased given the price of one share, 
        and available amount for the position.
        :param share_price -> Price of one share
        :param position_amount -> Available position amount that can be used for this trade 
        """
        print(f"You can buy {int(position_amount/share_price)} shares with share price {share_price} and position size Rs {position_amount}")
        return int(position_amount/share_price)

    def get_lot_size(self, scrip_code):
        """
        This function is used to get lot size for any stock/F&O recommendation based on the scrip_code
        :param scrip_code -> Scrip code of the recommended security. This can be obtained from scrip master
        """
        row = self.scrip_master[self.scrip_master['Scripcode'] == scrip_code]
        return row.iloc[0]['LotSize']
    
    def get_max_share_qty(self, lot_price, approved_position_amount, lot_size):
        """
        This function is used to find maximum share quantity that can be purchased while being under the approved position amount (20% of capital per trade)
        :param lot_price -> price of the lot
        :param approved_position_amount -> approved position amount (20% of capital per trade)
        :param lot_size -> Size of lot. BANKNIFTY lot size is 15, NIFTY is 50
        """
        return ((approved_position_amount // lot_price) * lot_size)

