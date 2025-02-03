from fastapi import HTTPException
from phonenumbers.phonenumber import PhoneNumber
from phonenumbers.util import prnt
from phonenumbers.carrier import name_for_number

def phone_lookup(phone: int) -> bool:
    if(phone < 1000000000 or phone > 9999999999):
        raise HTTPException(status_code=400, detail="Invalid phone number !")

    phone_obj = PhoneNumber (country_code= 91, national_number=phone)
    carrier = name_for_number(phone_obj, "en")

    if(carrier == ''):
        raise HTTPException(status_code=400, detail="Invalid phone number !")
  
    return True