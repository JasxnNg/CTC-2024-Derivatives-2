import random
import pandas as pd
from datetime import datetime

class Strategy:
  
  def __init__(self, start_date, end_date, options_data, underlying) -> None:
    self.capital : float = 100_000_000
    self.portfolio_value : float = 0

    self.start_date : datetime = start_date
    self.end_date : datetime = end_date
  
    self.options : pd.DataFrame = pd.read_csv(options_data)
    self.options["day"] = self.options["ts_recv"].apply(lambda x: x.split("T")[0])

    self.underlying = pd.read_csv(underlying)
    self.underlying.columns = self.underlying.columns.str.lower()

  def generate_orders(self) -> pd.DataFrame:


    # if the difference between the bid and ask price is greater than 0.1, then buy the option
    # and if the quantity of the bid or ask has a greater thing 
    orders = []
    dictionary = {}
    
    # for _ in range(num_orders):
    #   row = self.options.sample(n=1).iloc[0]
    #   action = random.choice(["B", "S"])
      
    #   if action == "B":
    #     if int(row["ask_sz_00"]) > 1:
    #       order_size = random.randint(1, int(row["ask_sz_00"]))
    #   else:
    #     if int(row["bid_sz_00"]) > 1:
    #       order_size = random.randint(1, int(row["bid_sz_00"]))
      
    #   order = {
    #     "datetime" : row["ts_recv"],
    #     "option_symbol" : row["symbol"],
    #     "action" : action,
    #     "order_size" : order_size
    #   }
    #   orders.append(order)


    for index, i in self.options.iterrows(): 
      # print(index)
      # if i["symbol"] in dictionary: 
      #   if i["day"] != dictionary[i["symbol"]][4]:
      #     del dictionary[i["symbol"]]
      #   else: 
      #     if dictionary[i["symbol"]][0] == "B":
      #       if (i["ask_sz_00"] - i["bid_sz_00"]) / max(i["ask_sz_00"], i["bid_sz_00"]) > 0.75 and max(i["ask_sz_00"], i["bid_sz_00"]) > 200:
      #         continue
      #       else: 
      
      #         if i["ask_px_00"] - dictionary[i["symbol"]][2] > 0.3 or dictionary[i["symbol"]][2] - i["ask_px_00"] > 0.4: 
      #           # sell that shit 

      #           order = {
      #             "datetime": i["ts_recv"],
      #             "option_symbol": i["symbol"],
      #             "action": "S", 
      #             "order_size":dictionary[i["symbol"]][1]
      #           }
                
      #           orders.append(order)
              

      #     else: 
      #       pass

      #       if (i["bid_sz_00"] - i["ask_sz_00"]) / max(i["ask_sz_00"], i["bid_sz_00"]) > 0.75 and max(i["ask_sz_00"], i["bid_sz_00"]) > 200:
      #         continue 
      #       else: 
      #         if i["buy_px_00"] - dictionary[i["symbol"]][3] > 0.3 or dictionary[i["symbol"]][3] - i["buy_px_00"] > 0.4: 
      #           order = {
      #             "datetime": i["ts_recv"],
      #             "option_symbol": i["symbol"],
      #             "action": "B", 
      #             "order_size":dictionary[i["symbol"]][1]
      #           }
      #           orders.append(order)


          #     if i["ask_sz_00"] - dictionary[i["symbol"]][1]: 
          #       order_size = dictionary[i["symbol"]][1]
          #     else: 
          #       order_size = i["ask_sz_00"]
          #   if i["ask_sz_00"] - i< 0.1:
          #     if i["bid_sz_00"] - dictionary[i["symbol"]][1]: 
          #       order_size = dictionary[i["symbol"]][1]
          #     else: 
          #       order_size = i["bid_sz_00"]

          #   if i["ask_sz_00"] - dictionary[i["symbol"]][1] > 0.1:
          #   if i["ask_sz_00"] - dictionary[i["symbol"]][1]: 
          #     order_size = dictionary[i["symbol"]][1]
          #   else: 
          #     order_size = i["ask_sz_00"]
          # else:
          #   if i["bid_sz_00"] - dictionary[i["symbol"]][1]: 
          #     order_size = dictionary[i["symbol"]][1]
          #   else: 
          #     order_size = i["bid_sz_00"]

      if i["symbol"] not in dictionary: 
        if abs(i["ask_px_00"] - i["bid_px_00"]) / max(i["ask_px_00"], i["bid_px_00"]) > 0.04: 
          if abs(i["ask_sz_00"] - i["bid_sz_00"]) / max(i["ask_sz_00"], i["bid_sz_00"]) > 0.83 and max(i["ask_sz_00"], i["bid_sz_00"]) > 3000:
            if i["ask_sz_00"] > i["bid_sz_00"]: 
              action = "S"
              order_size = min(i["ask_sz_00"] // 3, 200)
            else:
              action = "B"
              order_size = min(i["bid_sz_00"] // 3, 200)
            if order_size * i["ask_px_00"] < 50: 
              # don't add that bullshit
              continue 
            else: 
              dictionary[i["symbol"]] = [action, order_size, i["ask_px_00"], i["bid_px_00"], i["day"]]
              order = {
                  "datetime": i["ts_recv"],
                  "option_symbol": i["symbol"],
                  "action": action, 
                  "order_size":order_size
                }
              orders.append(order)
    print(len(orders))
    # print(orders)

      # is this an iterable fuck? 

    
    return pd.DataFrame(orders)
  
if __name__ == "__main__":
  start = datetime(2024, 1, 1)
  end = datetime(2024, 3, 30) 
  s = Strategy(start, end, "data/cleaned_options_data.csv", "data/underlying_data_hour.csv")
  s.generate_orders()