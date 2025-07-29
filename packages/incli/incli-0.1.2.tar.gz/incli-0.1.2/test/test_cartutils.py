import unittest
#from InCli import InCli
from incli.sfapi import jsonFile,restClient,CPQ,cartUtils

class Test_CartUtils(unittest.TestCase):
    def test_removekeys(self):
        restClient.init('qmscopy')

        cartId = '801AP00000rjhkHYAQ'
        res = CPQ.getCartItems_custom_api(cartId=cartId,version='v2')
        cartUtils.simplifyCart(res,createFiles=True)

        a=1

    def test_getCartItems(self):
        restClient.init('qmscopy')

        cartId = '801AP00000rjhkHYAQ'
        res = CPQ.getCartItems_custom_api(cartId=cartId)

        file = jsonFile.write('xxx',res)

        a=1 