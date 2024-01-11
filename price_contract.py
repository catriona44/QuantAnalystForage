import datetime
import pricing_model
import numpy


def price(inj_day: datetime, with_day: datetime, buy_price: float, sell_price: float,
          store_cost: float, volume: int, rate: int, inj_cost: int) -> object:

    # Initial profit
    total = (sell_price - buy_price) * volume

    # Injection/withdrawal costs
    total -= 2 * inj_cost * volume / rate

    # Storage costs
    total -= store_cost * ((with_day - inj_day) / datetime.timedelta(days=1) - 2 * volume / rate)

    return total


model = pricing_model.initialise_model()

inj_day = datetime.datetime.strptime(input("Enter injection day in format YY/MM/DD: "), '%y/%m/%d')
with_day = datetime.datetime.strptime(input("Enter withdrawal day in format YY/MM/DD: "), '%y/%m/%d')
store_cost = float(input("Enter the storage cost in price/day: "))
volume = int(input("Enter the storage volume: "))
rate = int(input("Enter the injection/withdrawal rate in units/day: "))
inj_cost = int(input("Enter the injection/withdrawal cost per day: "))

amount = price(inj_day, with_day, pricing_model.predict(model, inj_day), pricing_model.predict(model, with_day),
      store_cost, volume, rate, inj_cost)[0]
print(round(amount, 2))


