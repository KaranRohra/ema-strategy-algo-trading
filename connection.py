import os
import dotenv
import pyotp

from kite.connect import KiteConnect

dotenv.load_dotenv()

kite = KiteConnect(
    user_id=os.environ["KITE_USER_ID"],
    password=os.environ["KITE_PASSWORD"],
    two_fa=pyotp.TOTP(os.environ["KITE_2FA_SECRET"]).now(),
)
