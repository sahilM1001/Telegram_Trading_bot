from common.TradingDesk import TradingDesk
import pandas as pd
import time
from datetime import date

class FivePaisa(TradingDesk):
    """
    This is the sample class that inherits functions from the TradingDesk class.
    This class will be used to perform 5 Paisa specific transactions through the python SDK for 5Paisa
    """
    

    def __init__(self):
        self.CAPITAL = 10000
        self.PORTFOLIO_PERCENT = 20
        self.scrip_master = pd.read_csv("brokers/scrip masters/scripmaster-csv-format.csv")

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
        scrip_code_row = self.scrip_master[self.scrip_master['Name'] == scrip_name]
        scrip_code = scrip_code_row.iloc[0]['Scripcode']

        df = pd.read_csv("brokers/order_tracking_v2.csv")

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
            "bought_at": market_price
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        df.to_csv("brokers/order_tracking_v2.csv", index=False)

        self.CAPITAL -= (share_qty * market_price)

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

        scrip_code_row = self.scrip_master[self.scrip_master['Name'] == scrip_name]
        scrip_code = scrip_code_row['Scripcode'].iloc[0]


        df = pd.read_csv("brokers/order_tracking_v2.csv")
        
        
        filtered_row = df[(df['order_type'] == "BUY") & (df['scrip_name'] == scrip_name)]
        quantity_value = filtered_row['quantity'].iloc[0] if not filtered_row.empty else None
        bought_at = filtered_row['price'].iloc[0] if not filtered_row.empty else None

        if filtered_row.shape[0] > 0:
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
                "bought_at": bought_at
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            df.to_csv("brokers/order_tracking_v2.csv", index=False)

            self.CAPITAL += (quantity_value * target)
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