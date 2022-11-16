
from Models import Account, MerchOrder, AccountOrders, PROMO
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


def product_ordered(accountOrder: AccountOrders, promo: PROMO):
    
    total ="{:.2f}".format(int(accountOrder.order.quantity) * GetPriceRef(accountOrder.order.reference)) 
    price = '{:.2f}'.format(float(GetPriceRef(accountOrder.order.reference)))
    msg = ""

    if promo is None:
        msg = f"""
            Hello {accountOrder.account.firstname},

            You have ordered {accountOrder.order.quantity} - {accountOrder.merch.title.lower()}(P{price} each) which totals to
            ₱{total}, ADDITIONAL INFO: {accountOrder.order.additional_info}, if you have time, you can visit the PSITS Office at 5th floor UC Main bldg. located near room 539 for the payment.

            Your reference code is -> {GetReference(accountOrder.order.reference)}. View your receipt here: http://203.177.71.218:5000/PSITS/Orders/Receipt/{GetReference(accountOrder.order.reference)} Show this to the PSITS Officers upon paying 
            Thank you :D
        """
    elif int(accountOrder.merch.uid) == int(promo.merch):
        if promo.slot > 0:
            msg = f"""
                Hello {accountOrder.account.firstname},

                You have ordered {accountOrder.order.quantity} - {accountOrder.merch.title.lower()}(P{accountOrder.merch.price} each) which totals to
                ₱{total} with a promo '{promo.code}' discount of ₱{promo.discount}, ADDITIONAL INFO: {accountOrder.order.additional_info}, if you have time, you can visit the PSITS Office at 5th floor UC Main bldg. located near room 539 for the payment.

                Your reference code is -> {GetReference(accountOrder.order.reference)}. View your receipt here: http://203.177.71.218:5000/PSITS/Orders/Receipt/{GetReference(accountOrder.order.reference)} Show this to the PSITS Officers upon paying 
                Thank you :D
            """
        else:
            msg = f"""
                Hello {accountOrder.account.firstname},

                You have ordered {accountOrder.order.quantity} - {accountOrder.merch.title.lower()}(P{accountOrder.merch.price} each) which totals to
                ₱{total}. Unfortunately the promo {promo.code} is no longer available, ADDITIONAL INFO: {accountOrder.order.additional_info}, if you have time, you can visit the PSITS Office at 5th floor UC Main bldg. located near room 539 for the payment.

                Your reference code is -> {GetReference(accountOrder.order.reference)}. View your receipt here: http://203.177.71.218:5000/PSITS/Orders/Receipt/{GetReference(accountOrder.order.reference)} Show this to the PSITS Officers upon paying 
                Thank you :D
            """
    else:
        msg = f"""
            Hello {accountOrder.account.firstname},

            You have ordered {accountOrder.order.quantity} - {accountOrder.merch.title.lower()}(P{accountOrder.merch.price} each) which totals to
            ₱{total}. The promo code {promo.code} is not suitable for this merchandise, ADDITIONAL INFO: {accountOrder.order.additional_info}, if you have time, you can visit the PSITS Office at 5th floor UC Main bldg. located near room 539 for the payment.

            Your reference code is -> {GetReference(accountOrder.order.reference)}. View your receipt here: http://203.177.71.218:5000/PSITS/Orders/Receipt/{GetReference(accountOrder.order.reference)} Show this to the PSITS Officers upon paying 
            Thank you :D
        """
    return msg


def product_paid(accountOrder: AccountOrders):
    total ="{:.2f}".format(int(accountOrder.order.quantity) * GetPriceRef(accountOrder.order.reference)) 
    return f"""
        Hello {accountOrder.account.firstname}!\n\n 
        You already have paid the {accountOrder.order.quantity} - {accountOrder.merch.title} [TOTAL: P{total}]. Your reference code is -> {GetReference(accountOrder.order.reference)}. 
        Please wait for the announcement for the claiming schedule at the PSITS page. View your receipt here: http://203.177.71.218:5000/PSITS/Orders/Receipt/{GetReference(accountOrder.order.reference)} Do not lose your reference
        code thank you :D This email is auto generated, please do not reply"
    """


def product_cancel(accountOrder: AccountOrders):
    return f"""
        Hello {accountOrder.account.firstname}!\n\n 
        We're sorry but we have cancelled your order [ref: {GetReference(accountOrder.order.reference)}] Item: {accountOrder.merch.title}. Either you have requested for a cancellation 
        of order or we are out of stock. Sorry for the inconvenience. Please do not reply to this email, thank you.
    """
