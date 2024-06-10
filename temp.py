from connection import kite
from utils import kite_utils as ku

symbol_details = ku.get_basket_item()
print(ku.get_holding_by_symbol(symbol_details["exchange"], symbol_details["tradingsymbol"]))

print(kite.positions())

