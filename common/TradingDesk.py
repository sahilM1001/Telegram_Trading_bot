from abc import ABC, abstractmethod

class TradingDesk(ABC):
    """
    This abstract class can be used as a blueprint to wrap broker specific calls by inheriting the class
    and utilizing broker specific APIs
    """
    @abstractmethod
    def buy(self):
        print("Buy order received")
    
    @abstractmethod
    def sell(self):
        print("Sell order received")
    
    @abstractmethod
    def get_open_positions(self):
        print("Get open positions")

    @abstractmethod
    def get_available_margin(self):
        print("Get available margin")

    @abstractmethod
    def cancel_order(self):
        print("Cancel order received")
    
    @abstractmethod
    def modify_order(self):
        print("Modify Order received")

    @abstractmethod
    def get_position_amount(self):
        print("Inside position amount")

    @abstractmethod 
    def get_share_qty(self):
        print("Inside get share qty")
        