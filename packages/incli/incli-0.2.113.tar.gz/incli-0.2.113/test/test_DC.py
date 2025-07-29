import unittest,simplejson
#from InCli import InCli
from incli.sfapi import account,restClient,digitalCommerce,digitalCommerceUtil,utils,CPQ,timeStats,jsonFile,query

class Test_DC(unittest.TestCase):
    def test_catalogs(self):
        restClient.init('DEVNOSCAT4')

        catalogs = digitalCommerce.getCatalogs()

        print()

    def test_getOffers(self):
        restClient.init('DEVNOSCAT4')

    #    catalogs = digitalCommerce.getCatalogs()
        catalogs =['DCTEST','MPOTEST']
        for catalog in catalogs:
            try:
                offers = digitalCommerce.getOfferByCatalogue(catalog)
                print(f"offers: {len(offers)}")
            except Exception as e:
                print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_getOffer(self):
        restClient.init('NOSDEV')

    #    catalogs = digitalCommerce.getCatalogs()
        try:
            offers = digitalCommerce.getOfferDetails('DC_CAT_WOO_FIXED_INTERNET','PROMO_WOO_FIXED_INTERNET_6_MONTHS_003')
        except Exception as e:
            print(f" {e.args[0]['error']}")

        print()

    def test_create_Basket_config(self):
        restClient.init('DEVNOSCAT4')

        catalog ='DCTEST'
        offer ='C_WOO_MOBILE'
        try:
            details = digitalCommerce.getOfferDetails(catalog,offer)
            digitalCommerce.createBasketAfterConfig(catalog,details)
            print(f"offers: {len(details)}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_getOffer_details(self):
        restClient.init('DEVNOSCAT4')

        catalog ='DCTEST'
        offer ='C_WOO_MOBILE'
        try:
            offers = digitalCommerce.getOfferDetails(catalog,offer)
            print(f"offers: {len(offers)}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_create_Basket(self):
        restClient.init('NOSDEV')

        catalog ='DC_CAT_WOO_MOBILE'
        offer ='PROMO_WOO_MOBILE_016'
        try:
            basket = digitalCommerce.createBasket(catalog,offer)

            print(f"offers: {len(basket)}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_create_Basket_onboarding(self):
        url = 'https://nos--nosdev.sandbox.my.site.com/onboarding/'
        restClient.initWithToken('xxx',url=url)

        catalog ='DC_CAT_WOO_MOBILE'
        offer ='PROMO_WOO_MOBILE_016'
        try:
            basket = digitalCommerce.createBasket(catalog,offer)

            print(f"offers: {len(basket)}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_getBasketDetails(self):
        restClient.init('NOSDEV')

        catalog ='DC_CAT_WOO_FIXED_INTERNET_MOBILE'
        basketId ='ea267c7f3447fcb1b10293a1924f4064'
        basketId = '0dbc91d4d2697e174982824e5a994f58'
        basketId = '1e9216b80dc128dffec432d7d6320495'
        try:
            basket = digitalCommerce.getBasketDetails(catalog,basketId)

            files = restClient.callSave('b_details')
            digitalCommerceUtil.get_basket_lines(basket)
        except Exception as e:
            print(e)

        a=1
    
    def test_getBasketDetails__token(self):
        restClient.initWithToken('any',url='https://sf-dti.nos.pt/onboarding',token='00D0Q0000000fNy!AQEAQHfZohuLJksSMtHEZBlkLMc6hHOuVqSd6ASk8LMFP3c9aaJXEvLsPdhBU8wbO7pdf8MZ_pWOuIX3oWNxaBRvvOXqabol')

        try:
       #     basket = jsonFile.read(file)
            basket = digitalCommerce.getBasketDetails('DC_CAT_WOO_MOBILE','86e89819107d477778e58d21cc72526a')

            digitalCommerceUtil.parse_basket(basket)
        except Exception as e:
            print(e)

        a=1
    def test_getBasketDetails_file(self):
      #  file ='/Users/uormaechea/Documents/Dev/python/InCliLib/xxx.json'
        restClient.init('DTI')

        try:
       #     basket = jsonFile.read(file)
            basket = digitalCommerce.getBasketDetails('DC_CAT_WOO_MOBILE','86e89819107d477778e58d21cc72526a')

            digitalCommerceUtil.parse_basket(basket)
        except Exception as e:
            print(e)

        a=1
    def test_create_Basket_cart(self):
        restClient.init('DEVNOSCAT4')

        catalog ='DCTEST'
        offer ='C_WOO_MOBILE'
        try:
            basket = digitalCommerce.createBasket(catalog,offer)
            accountId ='0013O000017xZ2UQAU'
            digitalCommerce.createCart(accountId,catalog,cartContextKey=basket['cartContextKey'])

            print(f"offers: {len(basket)}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_create_basket_devnoscat2(self):
        url = 'https://nos--devnoscat2.sandbox.my.site.com/onboarding/'
        token = '00D3N000000HGGm!AQYAQF.HTYxFctGu1H3NChYo8E8KAEOKNLCUqC_WLjooMPWeyLzGNF.BrVdf46SwAWZf7hLeL4b0tneITdDxv4b52TtEP5MA'
        token_partner = '00D3N000000HGGm!AQYAQD7.w6vEuCw8eU6S.37OhVwZh1JG3Ud4o7PX4W7ZjXzHhLRP2_Sl.IX6wpuefRisaTkWA48l1RW8H9KXRHF5sSgwaZ_P'

        restClient.initWithToken('xxx',url=url,token=token_partner)
        catalog ='DCTEST'
        offer ='PROMO_WOO_MOBILE_TRIAL'
        try:
            basket = digitalCommerce.createBasket(catalog,offer)
            bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])

            basket = digitalCommerce.addChildBasket(bd,"C_SIM_E-SIM_CARD:C_SIM_CARD",ts_name='add_C_CIM_CARD')
            basket = digitalCommerce.addChildBasket(basket,"C_VOICE_MOBILE_TARIFFS:C_VOICE_MOBILE_SERVICE_016",ts_name='add_C_TARIFF')


            accountId ='0013O000013YjADQA0'
            accountId = '0010Q00001Avtd8QAB'
            res = digitalCommerce.createCart(accountId,catalog,cartContextKey=basket['cartContextKey'])

            print(f"res: {res}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")
        
    def test_create_Basket_cart_token_nosdev(self):
        if 1==2:
            url = 'https://nos--nosdev.sandbox.my.site.com/onboarding/'
            token_partnerOff = '00D3O0000004pzC!AQkAQJyDd1.DKk2gBJKxCKYQphFVSaPxXEBJSs8cOlqm1edWvrRRX4GWjNQTTc9hsojT5RfrJD10fWBkyBZrKuRZ1cQkSAkk'
            token_user ='00D3O0000004pzC!AQEAQIb6dUJkQUWKaRHL8sAabomPcO3k16APCY.8wsRcry0ZPpz_2kgjMIVZvxgPfYqpgToxE2Ib0r5boxsWlyEtmcwql0K2'
            token = token_user
            restClient.initWithToken('xxx',url=url,token=token)
        else:
            restClient.init('NOSDEV')

        catalog ='DC_CAT_DEEPLINK'
        offer ='C_WOO_MOBILE'

     #   catalog = 'test'
     #   offer='C_POWER_WIFI_L'

      #  offer = 'DC_CAT_MPO_PRODUCT_175'
        try:
            basket = digitalCommerce.createBasket(catalog,offer)
            bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])

            basket = digitalCommerce.addChildBasket(bd,"C_SIM_E-SIM_CARD:C_SIM_CARD",ts_name='add_C_CIM_CARD')
            basket = digitalCommerce.addChildBasket(basket,"C_VOICE_MOBILE_TARIFFS:C_VOICE_MOBILE_SERVICE_016",ts_name='add_C_TARIFF')

            accountId ='0013O000013YjADQA0'
            accountId = '001AU00000SPUIvYAP'
            res = digitalCommerce.createCart(accountId,catalog,cartContextKey=basket['cartContextKey'])

            print(f"res: {res}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()
        

    def test_create_Basket_cart_token_devnoscat3(self):
        if 1==1:
            url = 'https://nos--devnoscat3.sandbox.my.site.com/novo'
            token_partner = '00D3N000000HHFa!ARoAQLF2NEn1Gafd9HK_7Ha29Z8p.XFPHp.WF59tt0PD.hMu.Q1b0kKrHFrG5adajoPmXDDZXvrZefXT_hgNv1FFWFATbrKt'
            token = token_partner
            restClient.initWithToken('xxx',url=url,token=token)
        else:
            restClient.init('DEVNOSCAT3')

      #  res =  query.query(f"select fields(all) from vlocity_cmt__CpqConfigurationSetup__c limit 100")

        catalog = 'test'
        offer = 'C_WOO_MOBILE'

        try:
        #    basket = digitalCommerce.createBasket(catalog,offer)
        #    bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])

        #    res = digitalCommerce.addChildBasket(bd,"C_SIM_E-SIM_CARD:C_SIM_CARD",ts_name='add_C_CIM_CARD')
        #    res = digitalCommerce.addChildBasket(res,"C_VOICE_MOBILE_SERVICE_016",ts_name='add_C_VOICE_MOBILE_SERVICE_016')

        #    bd = digitalCommerce.getBasketDetails(catalog,res['cartContextKey'])

        #    digitalCommerceUtil.parse_basket(bd)
            accountId = '0013N00001P4kPMQAZ'
            res = digitalCommerce.createCart(accountId,catalog,cartContextKey='9ffb0dbb2dc8353e4067b986aecb05a7')

            print(f"res: {res}")
        except Exception as e:
            print(f"  {e.args[0]['error']}")

        print()

    def test_create_Basket_cart_token_support(self):
        if 1==1:
            url = 'https://sandeshkul-240219-963-demo.my.site.com/partnercentral'
            token_partner = '00Dal000001aqM5!AQEAQDkhoo1SUxfX1XiKVfnP_oddPH379SwBbBCqYD54AECyYttxpuJthYl6kcLRFgn3eY3jDERcZJ4aVuBD_KUMy2B8kr7X'
            token_user ='00D3O0000004pzC!AQkAQCxVZDZ0lafKu48TdKODht_iFws3V0xmXppGsaju4It4WjmnXvyY8ni4ixXt3HpFv983PLjE.t.IESLhFA0HVmpdlIBp'
            token = token_partner
            restClient.initWithToken('xxx',url=url,token=token)
        else:
            restClient.init('demoParner')

        res =  query.query(f"select fields(all) from Account limit 100")

        catalog ='COM-SMB-CATALOG-INTERNET-BUSINESS'
        offer ='COM-INET-OFR-INET-BUS-FIB-HOME'
        try:
         #   basket = digitalCommerce.createBasket(catalog,offer)
         #   bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])

        #    res = digitalCommerce.addChildBasket(bd,"C_SIM_E-SIM_CARD:C_SIM_CARD",ts_name='add_C_CIM_CARD')

            accountId = '001al000006qlhPAAQ'
            res = digitalCommerce.createCart(accountId,catalog,cartContextKey='52eba69d419bfcd2ab5e392ed4ccbc15')

            print(f"res: {res}")
        except Exception as e:
            print(f"{catalog}  {e.args[0]['error']}")

        print()

    def test_DEVNOSCAT4_C_WOO_MOBILE(self):
        restClient.init('DEVNOSCAT4')
        self.test_WOO_Mobile('DCTEST',userValue=21,iterations=1)

    def test_NOSDEV_C_WOO_MOBILE(self):
        restClient.init('NOSDEV')
        self.test_WOO_Mobile('DC_CAT_WOO_MOBILE')

    def test_WOO_Mobile(self,catalog,userValue=200,iterations=3):
        offer ='C_WOO_MOBILE'

        for i in range(0,iterations):
            try:
                restClient.new_time_record()

                details = digitalCommerce.getOfferDetails(catalog,offer,ts_name='getOfferDetails')

                updated = digitalCommerceUtil.updateOfferField(details,'ATT_NOS_OTT_SUBSCRIPTION_ID','userValues',userValue+i,'code')

                basket = digitalCommerce.createBasketAfterConfig(catalog,updated,ts_name='createBasketAfterConfig')
              #  basket = digitalCommerce.createBasket(catalog,basketAction='AddWithNoConfig',offer=offer)

                bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])

                filename = restClient.callSave('getBasketDetails_111')

                res = digitalCommerce.addChildBasket(bd,"C_VOICE_MOBILE_TARIFFS:C_VOICE_MOBILE_SERVICE_001",ts_name='add_SERVICE_001')

                res = digitalCommerce.addChildBasket(bd,"C_SIM_E-SIM_CARD:C_SIM_CARD",ts_name='add_C_CIM_CARD')

                res = digitalCommerce.addChildBasket(bd,"C_COMPLEMENT_SERVICE:C_EXTRAS_DATA_3GB",ts_name='add_DATA_3GB')

                accountId ='0013O000017xZ2UQAU'
                res = digitalCommerce.createCart(accountId,catalog,cartContextKey=basket['cartContextKey'],ts_name='createCart')

                orderId = res['orderId']

                res1 = CPQ.deleteCart(orderId,ts_name='deleteCart')


            except Exception as e:
                filename = restClient.callSave('request_DC_111',logRequest=True,logReply=False)
                utils.printException(e)
                #ts.time_no("Error",e.args[0]['errorCode'])
               # ts.print()

        restClient.time_print()

        print()

    def test_case(self):
        restClient.init('NOSDEV')

        catalog="DC_CAT_WOO_MOBILE"

        details = digitalCommerce.getOfferDetails(catalog,"PROMO_WOO_MOBILE_014")

        details['result']['offerDetails']['offer']['childProducts'][0]['AttributeCategory']['records'][0]['productAttributes']['records'][0]['userValues'] = 'FTTHNOS'

      #  context = {"DIM_CHANNEL":"APP", "DIM_PROCESS":"SELL", "DIM_ADDRESSCOMPETITOR": "", "DIM_ADDRESSTECH": "FTTH", "DIM_ADDRESSTECHCODE": "FTTHNOS", "DIM_ORDER_TYPE" : "INSTALAÇÃO"}
       # basket = digitalCommerce.createBasketAfterConfig(catalog,details,context=simplejson.dumps( context))
        basket = digitalCommerce.createBasketAfterConfig(catalog,details)

        a=1



    def test_DCTEST_C_MPO_Mobile100(self):
        restClient.init('DEVNOSCAT4')

        catalog ='MPOTEST'
        offer ='C_NOS_OFFER_001'
        ts = timeStats.TimeStats()
        ts.new()

        try:
            details = digitalCommerce.getOfferDetails(catalog,offer)

            ts.time('getOfferDetails')

            filename = restClient.callSave('mpodetails111')

            updated = digitalCommerceUtil.updateOfferField(details,'ATT_SERIAL_NUMBER','userValues',1113,'code')

            basket = digitalCommerce.createBasketAfterConfig(catalog,details)
            #basket = digitalCommerce.createBasket(catalog,basketAction='AddWithNoConfig',offer=offer)

            print(f"createBasketAfterConfig: {restClient.getLastCallAllTimes()}")

            bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])
            ts.time('getBasketDetails')

            filename = restClient.callSave('getBasketDetails_111')

            res = digitalCommerce.addChildBasket(bd,"C_NOS_AGG_EQUIPS_TV_OPT_UMA:C_NOS_EQUIP_TV_005")
            ts.time('add_TV_005')

            res = digitalCommerce.addChildBasket(bd,"C_NOS_AGG_MOBILE_DATA:C_NOS_SERVICE_VM_004")
            ts.time('add_VM_004')

            res = digitalCommerce.addChildBasket(bd,"C_NOS_OFFER_001:C_NOS_AGG_SERVICES_OPT_VM")
            ts.time('add_OPT_VM')

            accountId ='0013O000017xZ2UQAU'
            res = digitalCommerce.createCart(accountId,catalog,cartContextKey=basket['cartContextKey'])
            ts.time('createCart')

            orderId = res['orderId']

            res1 = CPQ.deleteCart(orderId)
            ts.time('deleteCart')

            ts.print()
            print()

        except Exception as e:
            filename = restClient.callSave('request_DC_111',logRequest=True,logReply=False)
            utils.printException(e)
            ts.time_no("Error",e.args[0]['errorCode'])
            ts.print()


        print()

    def test_DCTEST_MOBILE_TRIAL(self):
        restClient.init('DEVNOSCAT4')

        catalog ='DCTEST'
        offer ='PROMO_WOO_MOBILE_TRIAL'
        try:
            details = digitalCommerce.getOfferDetails(catalog,offer)
            print(f"getOfferDetails: {restClient.getLastCallAllTimes()}")

            updated = digitalCommerceUtil.updateOfferField(details,'ATT_NOS_OTT_SUBSCRIPTION_ID','userValues',1113,'code')

           # basket = digitalCommerce.createBasketAfterConfig(catalog,updated)AddAfterConfig
        #    basket = digitalCommerce.createBasket(catalog,basketAction='AddWithNoConfig',offer=offer)
            basket = digitalCommerce.createBasket(catalog,basketAction='AddAfterConfig',offer=offer)

            #basket = digitalCommerce.createBasket(catalog,'',basketAction='AddAfterConfig',productConfig=updated)

            print(f"createBasketAfterConfig: {restClient.getLastCallAllTimes()}")

            bd = digitalCommerce.getBasketDetails(catalog,basket['cartContextKey'])
            print(f"getBasketDetails: {restClient.getLastCallAllTimes()}")

            filename = restClient.callSave('getBasketDetails_111')

            res = digitalCommerce.addChildBasket(bd,"C_VOICE_MOBILE_TARIFFS:C_VOICE_MOBILE_SERVICE_001")
            print(f"addChildBasket: {restClient.getLastCallAllTimes()}")

            res = digitalCommerce.addChildBasket(bd,"C_SIM_E-SIM_CARD:C_SIM_CARD")
            print(f"addChildBasket: {restClient.getLastCallAllTimes()}")

            res = digitalCommerce.addChildBasket(bd,"C_COMPLEMENT_SERVICE:C_EXTRAS_DATA_3GB")
            print(f"addChildBasket: {restClient.getLastCallAllTimes()}")

            accountId ='0013O000017xZ2UQAU'
            res = digitalCommerce.createCart(accountId,catalog,cartContextKey=basket['cartContextKey'])
            print(f"createCart: {restClient.getLastCallAllTimes()}")

            orderId = res['orderId']

            res1 = CPQ.deleteCart(orderId)
            print(f"deleteCart: {restClient.getLastCallAllTimes()}")

            print()

        except Exception as e:
            filename = restClient.callSave('request_DC_111',logRequest=True,logReply=False)
            utils.printException(e)

        print()

    def test_basket_products_hierarchy(self):
      file = '/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/basket.json'
      items = jsonFile.read(file)

      restClient.init('DEVNOSCAT4')

      basketId = '3274e8617a584f7baa7030a8a8126046'

      basket = digitalCommerce.getBasketDetails('MPOTEST',basketId)

      digitalCommerceUtil.basket_products_hierarchy(basket)

      a=1