import unittest
#from InCli import InCli
from incli.sfapi import account,restClient,CPQAppHandler,DR_IP,jsonFile,CPQ,query

class Test_CPQUtils_Class(unittest.TestCase):
    def test_post_promo_items_all(self):
        data = {
            "cartId":"801AP00000fMYaQXXX", 
            "items":[{
                "itemId":"a507a000000Inx5AAC"
            }], 
            "methodName":"postCartsPromoItems", 
            "price":False, 
            "promotionId":"a507a000000Inx5AAC", 
            "validate":False
        }

        restClient.init("qmscopy")
        res=DR_IP.remoteClass('CPQUtils','postCartsPromoItems',data,{})
        filesx1 = restClient.callSave('postCartsPromoItems',logRequest=True,logReply=True)

        return res
    
    def getcartNodes(self,cartItems,productCode,itemType=None):
        inp = {
            'cartItems':cartItems,
            'key':'ProductCode',
            'value':productCode
        }
        if itemType!=None:
            inp['itemType'] = itemType
        res=DR_IP.remoteClass('CPQUtils','getcartNodes',inp,{})

        return res


    def postCartNode(self,orderId,cartNodes):
        inp2 = {
            'orderId':orderId,
          #  'cartItems':cartItems,
          #  'value':productCode,
            'cartNodes':cartNodes
        }

        res=DR_IP.remoteClass('CPQUtils','postCartNode',inp2,{})
        return res
    
    def test_so(self):
        restClient.init('DEVNOSCAT3')

        input = {
            'productId':'01t3N00000AjB61QAF'
        }

        res=DR_IP.remoteClass('CPQUtils','ProductConsoleController',input,{})

        for r in res['so']:
            if r['aaWrapper'] != None:
                print(r['aaWrapper']['attribute']['Name'])
                print(r['aaWrapper']['attributeAssignment']['Name'])
                print()


        print() 
    
    def test_soNOSDEV(self):
        restClient.init('NOSDEV')

        input = {
            'productId':'01t3O000006EbUpQAK'
        }

        res=DR_IP.remoteClass('CPQUtils','ProductConsoleController',input,{})

        for r in res['so']:
            if r['aaWrapper'] != None:
                print(r['aaWrapper']['attribute']['Name'])
                print(r['aaWrapper']['attributeAssignment']['Name'])
                print()


        print() 
    def test_getHierarchy_and_postCartItems(self):
        restClient.init('NOSQSM')
        orderId = '801AU00000WqVzpYAF'
        productCode = 'C_SIM_CARD'

        #cartItems = CPQAppHandler.getCartsItems(orderId)

        inp = {
            'cartItems':cartItems,
            'value':productCode
        }
        res=DR_IP.remoteClass('CPQUtils','getcartNodes',inp,{})

        inp2 = {
            'orderId':orderId,
            'cartItems':cartItems,
            'value':productCode,
            'cartNodes':res['cartNodes']
        }

        res2=DR_IP.remoteClass('CPQUtils','postCartNode',inp2,{})

        print()

    def test_getHierarchy_and_getObject(self):
        restClient.init('NOSQSM')
        orderId = '801AU00000jUIDoYAO'
        productCode = 'C_SIM_CARD'

        cartItems = CPQAppHandler.getCartsItems(orderId)

        inp = {
            'cartItems':cartItems,
            'value':productCode,
            'itemType':'lineItem'
        }
        res=DR_IP.remoteClass('CPQUtils','getcartNodes',inp,{})

        inp2 = {
            'key':'code',
            'value':'ATT_DELIVERY_METHOD',
            'object':res['cartNodes'][0]
        }

        res2=DR_IP.remoteClass('CPQUtils','getObject',inp2,{})

        print()
        res2['data']['userValues']

    def putCartItems(self,orderId,cartNodes,updateAttributeJSON=None,updateFieldsJSON=None):
        inp2 = {
            'orderId':orderId,
      #      'cartItems':cartItems,
      #      'value':productCode,
            'cartNodes':cartNodes
      #      'returnPayload':True,
        }  

        if updateAttributeJSON != None:
            inp2['updateAttributeJSON'] = updateAttributeJSON 
        if updateFieldsJSON != None:
            inp2['updateFieldsJSON'] = updateFieldsJSON 

        res2=DR_IP.remoteClass('CPQUtils','putCartNode',inp2,{})
        return res2


    def test_getHierarchy_and_putCartItems(self):
        restClient.init('NOSQSM')
        orderId = '8017a000002xGaJAAU'
        productCode = 'C_SIM_CARD'

        cartItems = CPQAppHandler.getCartsItems(orderId)

        inp = {
            'cartItems':cartItems,
            'value':productCode,
            'itemType':'lineItem'

        }
        res=DR_IP.remoteClass('CPQUtils','getcartNodes',inp,{})

        inp2 = {
            'orderId':orderId,
      #      'cartItems':cartItems,
            'value':productCode,
            'cartNodes':res['cartNodes'],
      #      'returnPayload':True,
            'updateFieldsJSON':{'vlocity_cmt__ServiceAccountId__c':'0017a00002PTQfaAAH','vlocity_cmt__BillingAccountId__c':'0017a00002HIrh4AAD'}
        }

        res2=DR_IP.remoteClass('CPQUtils','putCartNode',inp2,{})

        inp2 = {
            'orderId':orderId,
      #      'cartItems':cartItems,
            'value':productCode,
            'cartNodes':res['cartNodes'],
      #      'returnPayload':True,
            'updateAttributeJSON':{'ATT_DELIVERY_METHOD':'Técnico'},
            'updateFieldsJSON':{'vlocity_cmt__ServiceAccountId__c':'0017a00002HIrh4AAD','vlocity_cmt__BillingAccountId__c':'0017a00002PTQfaAAH'}

        }

        res3=DR_IP.remoteClass('CPQUtils','putCartNode',inp2,{})

        print()

    def postCartNodePromo(self,orderId,cartNodes,promoId):
        inp2 = {
            'orderId':orderId,
         #   'cartItems':cartItems,
         #   '95':productCode,
            'cartNodes':cartNodes,
            'promotionId':promoId
        }

        res2=DR_IP.remoteClass('CPQUtils','postCartNodePromo',inp2,{})

        return res2
    
    def test_getHierarchy_and_postPromoItems(self):
        restClient.init('NOSQSM')
        orderId = '8017a000002xL5MAAU'
        productCode = 'C_E-SIM_CARD'
        promotionId_trial = 'a507a0000005BjjAAE'
        promotionId_Movel = 'a507a0000005BiDAAU'

        cartItems = CPQAppHandler.getCartsItems(orderId)
        filename = jsonFile.write('cartItems',cartItems)

        inp = {
            'cartItems':cartItems,
            'value':productCode,
            'itemType':'lineItem'
        }
        res=DR_IP.remoteClass('CPQUtils','getcartNodes',inp,{})

        inp2 = {
            'orderId':orderId,
            'cartItems':cartItems,
            'value':productCode,
            'cartNodes':res['cartNodes'],
            'promotionId':promotionId_trial
            ,'returnPayload':True
        }

        res2=DR_IP.remoteClass('CPQUtils','postCartNodePromo',inp2,{})

        if 'returnPayload' in inp2 and inp2['returnPayload'] == True:
            filename = jsonFile.write('funcionndo_test1234',res2['data'])


        inp2['promotionId'] = promotionId_Movel
        res2=DR_IP.remoteClass('CPQUtils','postCartNodePromo',inp2,{})


        print()

    def test_postCartItem(self):
        restClient.init('NOSQSM')

        orderId = '8017a000002xGaJAAU'
        productCode = 'C_SIM_CARD'
        cartItems = CPQAppHandler.getCartsItems(orderId)

        inp = {
            'orderId':orderId,
            'cartItems':cartItems,
            'key':'ProductCode',
            'value':productCode
        }
        res=DR_IP.remoteClass('CPQUtils','postCartItem',inp,{})

        filename = jsonFile.write('no_funcionndo_test1234',res['data'])

        res['data']['items'][0]['parentRecord']['records'][0]['lineItems']['records'] = []
        res['data']['items'][0]['parentRecord']['records'][0]['productCategories']['records'] = []

        res2 = CPQAppHandler.call('postCartItem',res['data'])

        print()


    def test_postCartItem_handler(self):
        restClient.init('NOSQSM')

        orderId = '8017a000002xGaJAAU'
        productCode = 'C_SIM_CARD'
        cartItems = CPQAppHandler.getCartsItems(orderId)

        inp = {
            'orderId':orderId,
            'cartItems':cartItems,
            'key':'ProductCode',
            'value':productCode
        }
        res=DR_IP.remoteClass('CPQUtils','postCartItem',inp,{})

        filename = jsonFile.write('no_funcionndo_test1234',res['data'])


        res['data']['items'][0]['parentRecord']['records'][0]['lineItems']['records'] = []
        res['data']['items'][0]['parentRecord']['records'][0]['productCategories']['records'] = []

        res2 = CPQAppHandler.call('postCartItem',res['data'])


        print()

    def test_brute(self):
        restClient.init('NOSQSM')

        input = {
            "methodName": "xxxxxx",
            "price": False,
            "validate": False,
            "includeAttachment": False,
            "hierarchy": 5,
            "orderId":"8017a000002xGaJAAU"
            }
        
        res2 = CPQAppHandler.call('putCartsItems',input)

        a=1


    def test_query(self):
        restClient.init('NOSQSM')
        orderId = '8017a000002xIzaAAE'
        q = f"select  vlocity_cmt__AssetReferenceId__c from OrderItem where OrderId ='{orderId}' order by vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c desc limit 1"

        inp2 = {
            'query':q
        }
        res2=DR_IP.remoteClass('CPQUtils','query',inp2,{})

        a=1


    def print_attributes(self,cartNodes):
        print('------------------------------------------')
        for attcat in cartNodes[0]['attributeCategories']['records']:
            print(f"{attcat['Name']}  {attcat['Code__c']}")
            for prodcat in attcat['productAttributes']['records']:
                print(f"       {prodcat['code']}   {prodcat['label']} ")
                a=1

    def test_execute(self):
        restClient.init('NOSQSM')


       # amendOrderId = AMEND %orderId%
       # CHECKOUT %amendOrderId%

        instruction = '''
        getCartsItems %amendOrderId%
        postCartItems %TV_equip_code%
        getCartsItems %amendOrderId%
        postCartsPromoItems %TV_equip_code%
        accountId = QUERY "select vlocity_cmt__AssetReferenceId__c, Product2.Name, vlocity_cmt__Action__c from OrderItem where OrderId = %amendOrderId% order by vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c desc"
        putCartsItems %amendOrderId% %TV_equip_code% ATT_NOS_DELIVERY_METHOD="Técnico", vlocity_cmt__ServiceAccountId__c=accountId, vlocity_cmt__BillingAccountId__c=accountId
        equipmentId = QUERY "select  vlocity_cmt__AssetReferenceId__c, Product2.Name, vlocity_cmt__Action__c from OrderItem where OrderId = %amendOrderId% order by vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c desc"
        putCartsItems %amendOrderId% %150Channelds% ATT_EQUIP_ID:%equipmentId%
        '''

        input = {
            'intructions':instruction,
            'data':{
                '150Channelds':'C_NOS_SERVICE_TV_003',
                'TV_equip_code':'C_NOS_EQUIP_TV_017',
                'amendOrderId':'8017a000002xIzaAAE'
            }
        } 

        res2=DR_IP.remoteClass('CPQUtilsExecute','preProcess',input,{})

        a=1


    def test_a(self):

        input = {
            'orderId':'',
            'TV_equip_code':'',
            '150Channelds':''
        }
        instruction = '''
        amendOrderId = AMEND %orderId%
        POST_CARTS_ITEMS TV_equip_code
        accountId = QUERY "select  vlocity_cmt__AssetReferenceId__c, Product2.Name, vlocity_cmt__Action__c from OrderItem where OrderId = $orderId order by vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c desc"
        PUT_CART_ITEMS ATT_NOS_DELIVERY_METHOD="Técnico", vlocity_cmt__ServiceAccountId__c=accountId, vlocity_cmt__BillingAccountId__c=accountId
        equipmentId = QUERY "select  vlocity_cmt__AssetReferenceId__c, Product2.Name, vlocity_cmt__Action__c from OrderItem where OrderId = $orderId order by vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c desc"
        PUT_CART_ITEMS 150Channelds {'ATT_EQUIP_ID':equipmentId}
        '''


    def test_nos4(self):
        restClient.init('NOSQSM')
        orderId = '8017a000002xIzaAAE'
        
        productCode = 'C_NOS_EQUIP_TV_017'
        channels_150 = 'C_NOS_SERVICE_TV_003'

        cartItems = CPQAppHandler.getCartsItems(orderId)


        if 1==2:
            ph = self.getcartNodes(cartItems,productCode)
            ci = self.postCartNode(orderId,ph['cartNodes'])
            cartItems = CPQAppHandler.getCartsItems(orderId)

        ph = self.getcartNodes(cartItems,productCode,itemType='lineItem')



        if 1==2:
            root = ph['cartNodes'][-1]

            for promo in root['promotions']['records']:
                print(promo['Id'])
                pr = self.postCartNodePromo(orderId,ph['cartNodes'],promo['Id'])


        self.print_attributes(ph['cartNodes'])

        res4 = self.putCartItems(orderId,ph['cartNodes'],{'ATT_NOS_DELIVERY_METHOD':'Técnico'},{'vlocity_cmt__ServiceAccountId__c':'0017a00002HIrh4AAD','vlocity_cmt__BillingAccountId__c':'0017a00002PTQfaAAH'})


        q = f"select  vlocity_cmt__AssetReferenceId__c, Product2.Name, vlocity_cmt__Action__c from OrderItem where OrderId ='{orderId}' order by vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c desc"
        inp2 = {
            'query':q
        }
        res2=DR_IP.remoteClass('CPQUtils','query',inp2,{})

        ph = self.getcartNodes(cartItems,channels_150,itemType='lineItem')
        self.print_attributes(ph['cartNodes'])

        res4 = self.putCartItems(orderId,ph['cartNodes'],{'ATT_EQUIP_ID':res2['response'][0]['vlocity_cmt__AssetReferenceId__c']})

        a=1
        
    def test_queue_get(self):
        restClient.init('NOSQSM')

        instruction = '''
        getCartsItems %amendOrderId%
        putCartsItems %productCode% ATT_NOS_DELIVERY_METHOD='Técnico', vlocity_cmt__ServiceAccountId__c=0017a00002PTQfaAAH, vlocity_cmt__BillingAccountId__c=0017a00002PTQfaAAH
        '''

        input = {
            'intructions':instruction,
            'data':{
                'amendOrderId':'8017a000002xIzaAAE',
                'orderId':'8017a000002xIzaAAE',
                'productCode':'C_NOS_EQUIP_TV_017'
            }
        } 

        res2=DR_IP.remoteClass('CPQUtilsExecute','execute',input,{})

        input = {
            'orderId':'8017a000002xIzaAAE'
        }

        res2=DR_IP.remoteClass('CPQUtils','getCartsItems',input,None)


        a=1
#'serverResponse: [{"errorCode":"APEX_ERROR","message":"System.JSONException: Apex Type unsupported in JSON: Schema.SObjectType\\n\\n(System Code)"}]'

#working
    def test_getCartItems2(self):       
        restClient.init('NOSDEV')
        input = {
            'orderId':'801AU00000iz85wYAA'
        }
        res1=DR_IP.remoteClass('CPQUtils','getCartsItems',input,None)


        res2 = CPQAppHandler.getCartsItems('801AU00000iz85wYAA')
        filename = jsonFile.write('funcionndo_test1234',res2)


        res3=DR_IP.remoteClass('CPQUtils','getCartsItemsSimple',input,None)
        filename = jsonFile.write('no_funcionndo_test1234',res3['response'])

        a=1

    def test_get_nodes(self):
        restClient.init('NOSQSM')
        orderId = '801AU00000WqVzpYAF'
      #  orderId = '8017T000003VmC4QAK'
        productCode = 'C_NOS_EVENT_TV_001'
     #   productCode = 'C_NOS_OFFER_002'
     #   productCode = 'C_NOS_EQUIP_TV_014'
    #    productCode = 'C_NOS_AGG_EQUIPS_TV_UMA'
   #    productCode = 'C_NOS_AGG_EQUIPS_TV_UMA:C_NOS_EQUIP_TV_017'

        input = {
            'orderId':orderId,
            'pcPath':productCode
        } 
        res3=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})        
        filename = restClient.callSave('test_getCartNodes',logRequest=True,logReply=True)

       # self.printMessages(res3)


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

    def test_put_new(self):       
        restClient.init('DEVNOSCAT3')
        orderId = '8013N000005aeOJQAY'
        productCode = 'C_NOS_EQUIP_TV_017'

        input = {
            'orderId':orderId,
            'ProductCode':productCode
        }
        
        res=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})       
     #   filename = jsonFile.write('xxx',res)

        for r in res['cartNodes'][0]['attributeCategories']['records']:
            for r1 in r['productAttributes']['records']:
                print(r1['code'])

        input = {
            'orderId':orderId,
            'cartNodes':res['cartNodes'],
            'updateAttributeJSON':{'ATT_NOS_DELIVERY_METHOD':'Técnico'},
            'updateFieldsJSON':{'vlocity_cmt__ServiceAccountId__c':'0013N00001P2huoQAB','vlocity_cmt__BillingAccountId__c':'0013N00001P2huoQAB'}
        }  


        if 1==1:
            res2=DR_IP.remoteClass('CPQUtils','putCartNode',input,{})
        else:
            for promo in res['cartNodes'][4]['promotions']['records']:
                input = {
                        'orderId':orderId,
                        'cartNodes':res['cartNodes'],
                        'promotionId':promo['Id']
                    }
                res2=DR_IP.remoteClass('CPQUtils','postCartNodePromo',input,{})

        return res2

    def test_post_new(self):       
        restClient.init('NOSQSM')
        orderId = '801AU00000WqVzpYAF'
        productCode = 'C_NOS_PREMIUM_TV_119'

        input = {
            'orderId':orderId,
            'key':'ProductCode',
            'pcPath':productCode,
          #  'itemType':'lineItem'
        }
        
        res=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})       
        filename = jsonFile.write('xxx',res)

        inp2 = {
            'orderId':orderId,
          #  'cartItems':cartItems,
          #  'value':productCode,
            'cartNodes':res['cartNodes']
            ,'returnPayload':True

        }

        res=DR_IP.remoteClass('CPQUtils','postCartNode',inp2,{})
        filename = jsonFile.write('xxx1',res)

        a=1

    def test_full(self):
        restClient.init('DEVNOSCAT3')
        orderId = '8013N000006Le7WQAS'
        productCode = 'C_NOS_EQUIP_TV_017'
     #   productCode = 'C_NOS_AGG_EQUIPS_TV_UMA'
   #    productCode = 'C_NOS_AGG_EQUIPS_TV_UMA:C_NOS_EQUIP_TV_017'
        
        input = {
            'orderId':orderId,
            'ProductCode':productCode
        } 
        res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   
        for r in res1['cartNodes']:
            print(f"{r['ProductCode']}    {r['itemType']}")

        inp2 = {
            'cartNodes':res1['cartNodes']
        }

        res2=DR_IP.remoteClass('CPQUtils','postCartNode',inp2,{})
        for r in res2['cartNodes']:
            print(f"{r['ProductCode']}    {r['itemType']}")

        input2 = {
            'cartNodes':res2['cartNodes'],
            'updateAttributeJSON':{'ATT_NOS_DELIVERY_METHOD':'Técnico'},
            'updateFieldsJSON':{'vlocity_cmt__ServiceAccountId__c':'0013N00001P2huoQAB','vlocity_cmt__BillingAccountId__c':'0013N00001P2huoQAB'}
        }  

        res3=DR_IP.remoteClass('CPQUtils','putCartNode',input2,{})

        for promo in res2['cartNodes'][0]['promotions']['records']:
            input = {
                    'cartNodes':res2['cartNodes'],
                    'promotionId':promo['Id']
                }
            res4=DR_IP.remoteClass('CPQUtils','postCartNodePromo',input,{})

        a=1

    def test_delete(self):
        restClient.init('DEVNOSCAT3')
        orderId = '8013N000006Le7WQAS'
        productCode = 'C_NOS_EQUIP_TV_017'
     #   productCode = 'C_NOS_AGG_EQUIPS_TV_UMA'
   #    productCode = 'C_NOS_AGG_EQUIPS_TV_UMA:C_NOS_EQUIP_TV_017'
        
        input = {
            'orderId':orderId,
            'ProductCode':productCode,
            'itemType':'lineItem'
        } 
        res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   
        for r in res1['cartNodes']:
            print(f"{r['v']}    {r['itemType']}   {r['Id']['value']}")

        del_input = {
            'cartNodes':res1['cartNodes']
        } 

        resDel=DR_IP.remoteClass('CPQUtils','deleteCartNode',del_input,{})   

        a=1

    def test_getCartsItems(self):        
        restClient.init('NOSQSM')
        orderId = '801AU00000jUIDoYAO'
        input = {
            'orderId':orderId,
            'pcPath' : 'C_NOS_OFFER_006'
        } 

        res1=DR_IP.remoteClass('CPQUtils','getCartsItems',input,{})   
        filename = restClient.callSave('test_getCartsItems',logRequest=True,logReply=True)


        a=1

        
    def test_getCartTree(self):        
        restClient.init('qmscopy')
        orderId = '801AP00000iDwEcYAK'
        input = {
            'orderId':orderId,
            'pcPath' : 'C_NOS_OFFER_006'
            ,'attributes':'ATT_SERVICE_ACCOUNT_TYPE'
        } 
        input['pcPath'] = 'C_NOS_AGG_EQUIPS_TV_NAGRA_DTH'

        res1=DR_IP.remoteClass('CPQUtils','getCartTree',input,{})   
        filename = restClient.callSave('test_getCartTree',logRequest=True,logReply=True)


        a=1

    def test_getNodes_codes(self):        
        restClient.init('NOSDEV')
        orderId = '801AU00000izRI7YAM'

        input = {
            "query":f"select Product2.ProductCode from orderitem where orderId = '{orderId}'"
        }
        qr=DR_IP.remoteClass('CPQUtils','query',input,{})   

        for r in qr['response']:
            input = {
                'orderId':orderId,
                'pcPath':r['Product2']['ProductCode']
                ,'itemType':'lineItem'
            } 

            res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

            for m in res1['messages']:
                print(m)
            for r in res1['cartNodes']:
                print(f"{r['ProductCode']}    {r['itemType']}   {r['Id']['value']}")

        a= 1
    
    def test_getNodes_orderItem(self):        
        org = 'qmscopy'
        orderId = '801AP00000iDwEcYAK'

        restClient.init(org)

        input = {
            "query":f"select ID from orderitem where orderId = '{orderId}'"
        }
        qr=DR_IP.remoteClass('CPQUtils','query',input,{})   

        for r in qr['response']:
            input = {
                'orderId':orderId,
                'pcPath':r['Id']
                ,'itemType':'lineItem',
                'searchField':'Id'
            } 

            res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

            for m in res1['messages']:
                print(m)
            for r in res1['cartNodes']:
                print(f"   {r['ProductCode']}    {r['itemType']}   {r['Id']['value']}")

        a= 1

    def test_getNodes_Names(self):        
        restClient.init('NOSDEV')
        orderId = '801AU00000izRI7YAM'

        input = {
            "query":f"select product2.Name from orderitem where orderId = '{orderId}'"
        }
        qr=DR_IP.remoteClass('CPQUtils','query',input,{})   

        for r in qr['response']:
            input = {
                'orderId':orderId,
                'pcPath':r['Product2']['Name']
                ,'itemType':'lineItem',
                'searchField':'Name'
            } 

            res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

            for m in res1['messages']:
                print(m)
            for r in res1['cartNodes']:
                print(f"   {r['ProductCode']}    {r['itemType']}   {r['Id']['value']}")

        a= 1

    def test_getNodes(self):        
        restClient.init('NOSDEV')
        orderId = '801AU00000izRI7YAM'
        productCode = 'C_NOS_AGG_EQUIPS_TV_MAND_IRIS'
        productCode = 'C_NOS_EQUIP_TV_005'
        productCode = 'C_NOS_PREMIUM_TV_003'

        input = {
            'orderId':orderId,
            'pcPath':productCode
            ,'itemType':'lineItem'
        } 

        if 1==2:
            input = {
                'orderId':orderId,
                'pcPath':'8023O000008x4RkQAI'
                ,'searchField':'Id'
            # ,'itemType':'lineItem'
            } 

            input = {
                'orderId':'8013O00000541L5QAI',
                'pcPath':'802AU000004mPD7YAM'
                ,'searchField':'Id'
            # ,'itemType':'lineItem'
            } 
        res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   

        filename = restClient.callSave('test_getCartNodes',logRequest=True,logReply=True)

        for m in res1['messages']:
            print(m)
        for r in res1['cartNodes']:
            print(f"{r['ProductCode']}    {r['itemType']}   {r['Id']['value']}")

        a= 1
    def test_promo(self):
        restClient.init('DEVNOSCAT3')
        orderId = '8013N000006Le7WQAS'
        productCode = 'C_NOS_EQUIP_TV_017'
     #   productCode = 'C_NOS_AGG_EQUIPS_TV_UMA'
   #    productCode = 'C_NOS_AGG_EQUIPS_TV_UMA:C_NOS_EQUIP_TV_017'
        
        input = {
            'orderId':orderId,
            'ProductCode':productCode,
            'itemType':'lineItem'
        } 
        res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   
        for r in res1['cartNodes']:
            print(f"{r['ProductCode']}    {r['itemType']}   {r['Id']['value']}")

        for promo in res1['cartNodes'][0]['promotions']['records']:
            input = {
                    'cartNodes':res1['cartNodes'],
                    'promotionId':promo['Id']
                }
            res2=DR_IP.remoteClass('CPQUtils','postCartNodePromo',input,{})
            a=1

        a=1

    def test_promo_wrongPromo(self):
        restClient.init('DEVNOSCAT3')
        orderId = '8013N000006Le7WQAS'
        productCode = 'C_NOS_EQUIP_TV_017'
        
        input = {
            'orderId':orderId,
            'ProductCode':productCode,
            'itemType':'lineItem'
        } 
        res1=DR_IP.remoteClass('CPQUtils','getCartNodes',input,{})   
        for r in res1['cartNodes']:
            print(f"{r['ProductCode']}    {r['itemType']}   {r['Id']['value']}")

        input = {
                'cartNodes':res1['cartNodes'],
                'promotionId':'xxxxxxxxxx'
            }
        res2=DR_IP.remoteClass('CPQUtils','postCartNodePromo',input,{})

        a=1


    def test_hugo(self):
        

        url1= 'https://nos--nosdev.sandbox.my.site.com'
        url2= 'https://nos--nosdev.sandbox.my.site.com/novo'
        url3 = 'https://nos--nosdev.sandbox.my.site.com/onboarding'

        restClient.initWithToken('xxx',url=url3,token='00D3O0000004pzC!AQkAQM7QnQRmF2YIux2STX4.88.8gOK0clIDNQ9Dn8gXj56iVi7ivQvurpmgKNb4xEtmlVfBeNkbbXEaL7OeLQQK.r_KiQrv')

        res = query.query("select fields(all) from order limit 1")

        a= 1
