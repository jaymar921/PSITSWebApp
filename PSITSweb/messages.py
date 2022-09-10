
from Models import Account, MerchOrder, AccountOrders
from Util import GetPriceRef, GetReference


def registration_message(firstname: str, hasRFID: bool) -> str:
    if not hasRFID:
        return f"""
        Dear {firstname},
           
        We are happy to know that you've signed up for PSITS!
        For your next step, you need to go to the PSITS officer for RFID Registration.
        
        This email is auto generated, please do not reply :)
        """
    else:
        return f"""
        Dear {firstname},
           
        We are happy to know that you've signed up for PSITS!
        This email is auto generated, please do not reply :)
        """


def product_ordered(accountOrder: AccountOrders):
    total ="{:.2f}".format(int(accountOrder.order.quantity) * GetPriceRef(accountOrder.order.reference)) 

    return f"""
        Hello {accountOrder.account.firstname},

        You have ordered {accountOrder.order.quantity}x {accountOrder.merch.title.lower()} which totals to
        P{total}, ADDITIONAL INFO: {accountOrder.order.additional_info}, if you have time, you can visit the PSITS Office at 5th floor UC Main bldg. located near room 539 for the payment.

        Your reference code is -> {GetReference(accountOrder.order.reference)}. Show this to the PSITS Officers upon paying 
        Thank you :D
    """