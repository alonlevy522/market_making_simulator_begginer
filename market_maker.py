k=2.4 # order book liquidity parameter
import math
import random






class MarketMaker:
    def __init__(self, base_spread: float, risk_factor: float,sigma:float ):
        self.step_size=sigma
        self.base_spread = base_spread
        self.risk_factor = risk_factor
        self.inventory: int = 0
        self.cash: float = 0.0

    def get_quotes(self, fair_value: float, time: float) -> tuple[float, float]:

        if self.base_spread!=0:
            reserve_price=fair_value
            optimal_spread=self.base_spread
        else  :
            reserve_price= fair_value-self.inventory*self.risk_factor*((self.step_size)**2)*(1-time)
            optimal_spread=self.risk_factor*((self.step_size)**2)*(1-time)+(2*math.log(1+self.risk_factor/k,math.e))/(self.risk_factor if self.risk_factor!=0 else 1)
        bid_price=reserve_price- optimal_spread/2
        ask_price = reserve_price + optimal_spread / 2
        return bid_price, ask_price

    def record_fill(self, side: str, price: float, quantity: int) -> None:
        if side== "SELL" :
            self.inventory+=quantity
            self.cash-=quantity*price
        if side == "BUY":
            self.inventory -= quantity
            self.cash += quantity * price







