import unittest
#from InCli import InCli
from incli.sfapi import restClient,CPQAppHandler

class Test_CPQAppHandler(unittest.TestCase):
    def test_deleteSuplemental(self):

        restClient.init('NOSQSM')

        params= {
          "methodName": "submitCancelOrder",
          "cancelOrderId": "8017a000002xEoDAAU",
          "cartId": "8017a000001VMN4AAO"
        }

        call = CPQAppHandler.call(params['methodName'],params)

        a=1

    def test_getCartItems(self):
        restClient.init('NOSQSM')

        call = CPQAppHandler.getCartsItems('8017a000002xEs5AAE')

        a=1

    def test_admin(self):
        restClient.init('NOSQSM')

        input = {
            "apiName":"CMCatalogProfile", 
            "catalogCode":"DC_CAT_WOO_MOBILE", 
            "effectiveStartTime":None, 
            "expirationTime":None, 
            "forceinvalidatecache":None, 
            "methodName":"getCatalogProfile", 
            "writetocache":None
        }
        call = CPQAppHandler.call('getCatalogProfile',input)

        a=1



        
