from Models import Event, Merchandise, MerchOrder, Account
import Database


def TestDatabase():
    print("Testing database")

    try:
        print("Creating Account")
        Database.registerAccountDB(
            Account(
                19000000,
                0,
                'Firstname Person',
                'Lastname',
                'BSIT',
                0,
                ''
            ),
            "SecurePass123"
        )

        print("Account created successfully")
    except Exception as e:
        print(f"Failed to create Account... {e}")
        raise Exception

    try:
        print("Creating Event")
        Database.CREATEEvent(
            Event(
                None,
                'Sample Event',
                Database.getTime(),
                'Event information...',
                'static/img/sample.png'
            )
        )
        print("Event created successfully")
    except Exception as e:
        print(f"Failed to create Event... {e}")
        raise Exception
    data = []
    try:
        print("Searching Event (get All)")
        data = Database.GETAllEvent()
        print(data)
        print("Search Event was executed successfully")
    except Exception as e:
        print(f"Failed to search Event... {e}")
        raise Exception

    try:
        print("Updating Event")
        Database.UPDATEEvent(data[0])
        print(Database.GETAllEvent())
        print("Update Event was executed successfully")
    except Exception as e:
        print(f"Failed to update Event... {e}")
        raise Exception

    try:
        print("Creating Merchandise")
        Database.CREATEMerchandise(
            Merchandise(
                None,
                'Sample Merch',
                'Merch Information',
                10,
                1,
                100
            )
        )
        print("Merchandise created successfully")
    except Exception as e:
        print(f"Failed to create Merchandise... {e}")
        raise Exception

    try:
        print("Searching Merchandise (get All)")
        data = Database.GETAllMerchandise()
        print(data)
        print("Search Merchandise was executed successfully")
    except Exception as e:
        print(f"Failed to search Merchandise... {e}")
        raise Exception

    try:
        print("Updating Merchandise")
        Database.UPDATEMerchandise(data[0])
        print(Database.GETAllMerchandise())
        print("Update Merchandise was executed successfully")
    except Exception as e:
        print(f"Failed to update Merchandise... {e}")
        raise Exception

    try:
        print("Creating MerchOrder")
        Database.CREATEMerchOrder(
            MerchOrder(
                None,
                19000000,
                Database.getTime(),
                Database.GETAllMerchandise()[0].uid,
                'RESERVE',
                1,
                'extra large fries',
                'NaN'
            )
        )
        print("MerchOrder created successfully")
    except Exception as e:
        print(f"Failed to create MerchOrder... {e}")
        raise Exception

    try:
        print("Searching MerchOrder (get All)")
        data = Database.GETAllMerchOrder()
        print(data)
        print("Search MerchOrder was executed successfully")
    except Exception as e:
        print(f"Failed to search MerchOrder... {e}")
        raise Exception

    try:
        print("Updating MerchOrder")
        Database.UPDATEMerchOrder(data[0])
        print(Database.GETAllMerchOrder())
        print("Update MerchOrder was executed successfully")
    except Exception as e:
        print(f"Failed to update MerchOrder... {e}")
        raise Exception

    try:
        print("Deleting MerchOrder")
        Database.DELETEMerchOrder(Database.GETAllMerchOrder()[0].uid)
        print("Delete MerchOrder was executed successfully")
        print("Deleting Merchandise")
        Database.DELETEMerchandise(Database.GETAllMerchandise()[0].uid)
        print("Delete Merchandise was executed successfully")
        print("Deleting Event")
        Database.DELETEEvent(Database.GETAllEvent()[0].uid)
        print("Delete Event was executed successfully")
        print("Deleting Account")
        Database.removeAccount(19000000)
        print("Delete Account was executed successfully")
    except Exception as e:
        print(f"Failed to execute deletion... {e}")
        raise Exception

    print("Testing Complete, no errors found")
