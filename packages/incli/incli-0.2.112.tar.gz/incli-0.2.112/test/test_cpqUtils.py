import unittest
#from InCli import InCli
from incli.sfapi import account,restClient,CPQAppHandler,DR_IP,jsonFile,CPQ,query

class Test_CPQUtils(unittest.TestCase):
    def test_getcartNodes(self):
        restClient.init('NOSDEV')
        orderId = '8013O0000053DOGQA2'
        pcPath = 'C_NOS_EQUIP_TV_017'
    #    pcPath = 'C_NOS_AGG_EQUIPS_TV_UMA'

        input = {
            'orderId':orderId,
            'pcPath':pcPath
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})      
        xxx = jsonFile.write('xxxx',res3)  

        self.printMessages(res3)
        self.printCartNodes(res3)
        self.assertFalse(self.checkError(res3))

        input = {
            'orderId':'801xxxxxxxxxxxxx',
            'pcPath':pcPath
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})     
        self.assertTrue(self.checkError(res3))
        self.assertTrue('is not a valid order Id' in res3['messages'][0]['message'])


        input = {
            'orderId':orderId,
            'pcPath':'xxxxxxxx'
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

        self.assertTrue(self.checkError(res3))
        self.assertTrue('The pcPath with value' in res3['messages'][0]['message'])

        input = {
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

        self.assertTrue(self.checkError(res3))
        self.assertTrue('The orderId field must be provided' in res3['messages'][0]['message'])


        input = {
            'orderId':orderId
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

        self.assertTrue(self.checkError(res3))
        self.assertTrue('The pcPath field must be provided' in res3['messages'][0]['message'])


        input = {
            'orderId':1234567
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

        self.assertTrue(self.checkError(res3))
        self.assertTrue('Invalid conversion from runtime type' in res3['messages'][0]['message'])


        pcPath = 'C_NOS_AGG_EQUIPS_TV_UMA:C_NOS_EQUIP_TV_017'
        input = {
            'orderId':orderId,
            'pcPath':pcPath
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})    
        self.printCartNodes(res3)    
        self.assertFalse(self.checkError(res3))

        a=1

    def printCartNodes(self,call):
        if self.checkError(call):
            self.printMessages(call)
            return
        for r in call['cartNodes']:
            if 'value' not in r['ProductCode']:
                print(r['ProductCode'])
            else:
                print(r['ProductCode']['value'])

    def checkError(self,call):
        for m in call['messages']:
            if m['severity'] == 'ERROR':
                return True
        return False
    
    def printMessages(self,call):
        for m in call['messages']:
            print(f"{call['messages'][0]['severity']}  {call['messages'][0]['message']}")
            return True
        return False
     