import unittest
from incli.sfapi import restClient,CPQ,account,Sobjects,utils,query,jsonFile,objectUtil,file,timeStats,digitalCommerce,digitalCommerceUtil,CPQUtil,thread,DR_IP,CPQAppHandler
import simplejson,threading,time,multiprocessing,traceback,random,uuid,time,calendar
#import InCli.InCli as incli
import incli

procNum = 10
threadNum = 20
reps = 30
guest_url = 'https://nosdti-parceiros.cs109.force.com/onboarding'
def do_work(details):
  restClient.initWithToken('GUEST',url=guest_url)

  def getOffers(details):

    errors = 0
    ts = timeStats.TimeStats()

    for x in range(0,reps):
      try:
        # cartId = '8017a000002ad21AAA'
        # items2 = CPQ.getCartItems_api(cartId,price=False,validate=False)

        #
        # call = digitalCommerce.getOfferByCatalogue('DC_CAT_WOO_MOBILE')
        # digitalCommerce.createBasket('DC_CAT_WOO_MOBILE','C_WOO_MOBILE')
      #  val = f"{uuid.uuid4()}"
      #  print(val)
        ts.new(["Basket","Error"])
        current_GMT = time.gmtime()

        val = calendar.timegm(current_GMT)
        offerDetails = digitalCommerceUtil.updateOfferField(details,'ATT_NOS_OTT_SUBSCRIPTION_ID','userValues',val,'code')
        print("creating basket")        
        basket2 = digitalCommerce.createBasketAfterConfig('DC_CAT_WOO_MOBILE',offerDetails)
        print("got basket")
        ts.time("Basket")

        call1 = restClient.lastCall()
        if call1['totalCalls'] >1:
          calls = restClient.thread_get_calls()
          times = restClient._get_call_times(call1)
          times2 = restClient._get_call_times(calls[-2])
          ts.time_no("Basket1",times2['delta'])
          ts.time_no("Basket2",times['delta'])

       #   print(f"{times2} {times}",flush=True)

     #   print(restClient.getLastCallAllTimes(),flush=True)
      except Exception as e:
        utils.printException(e)
        errors = errors + 1
        ts.time_no("Error","True")

    ts.print()
      
    print(f"Processed {reps} with errors{errors}")  
     #   print(traceback.format_exc())
     #   print(restClient.lastCall())

  threads =  []
  for x in range(0,threadNum):
      thread = threading.Thread(target=getOffers,args=(details,))
      thread.start()
      threads.append(thread)
  for x,t in enumerate(threads):
    t.join()
    print(f'Thread Done {x}')


class Test_CPQ(unittest.TestCase):
    def test_guestUser(self):
        def do_process():
          restClient.initWithToken('GUEST',url=guest_url)

          print("getting offer details")
          details = digitalCommerce.getOfferDetails('DC_CAT_WOO_MOBILE','C_WOO_MOBILE')
          print("got offer details")

          processes = []
          for x in range(0,procNum):
            process = multiprocessing.Process(target=do_work,args=(details,))
            process.start()  
            processes.append(process)
          for p in processes:
            p.join()
            print('Process Done')

        do_process()

    def test_query_apexlog(self):
      restClient.init('DTI')

      q = "select Operation,StartTime,DurationMilliseconds from Apexlog order by StartTime desc limit 200"
      res = query.query(q)
      for r in res['records']:
        r.pop('attributes')

      utils.printFormated(res['records'])
      print()
    
    def test_createCart(self):
        restClient.init('NOSDEV')

        acc = account.createAccount('Name:unaiTest2',recordTypeName='Consumer')

        self.assertTrue(Sobjects.checkId(acc['Id']))

        cartId = CPQ.createCart(accountF= acc['Id'], pricelistF='Name:B2C Price List',name="testa5",checkExists=True)

        print(cartId)

    def test_delCartItems(self):
        restClient.init('NOSDEV')
        cartId = CPQ.getCartId('name:testa5')

        items = CPQ.getCartItems_api(cartId)

        if items['totalSize'] > 0:
          itemIds = [item['Id']['value'] for item in items['records']]

          dele = CPQ.deleteCartItems_api(cartId,itemIds)

          self.assertEqual(dele['messages'][0]['message'],'Successfully deleted.')
          print()

    def test_deleteCartItem(self):
      restClient.init('NOSDEV')

      res = CPQ.deleteCartItems_api(cartId='801AU00000qTuKdYAK',itemIds='802AU00000KFn07YAD',price=False,validate=False)

      a=1

    def test_getCartItems(self):
      restClient.init('NOSDEV')

      res = CPQ.getCartItems_custom_api(cartId='801AU00000qTRdCYAW')
      f = restClient.callSave('801AU00000qTRdCYAW',logRequest=True)

      a=1  
    def test_getCartItems_mp(self):
      restClient.init('NOSDEV')

      res = CPQ.getCartItems_api(cartId='801AU00000qTRdCYAW',price=False,validate=False,reduced=True)
      f = restClient.callSave('801AU00000qTRdCYAW',logRequest=True)

      a=1  
    def test_delete_applied_promotions(self):
        restClient.init('NOSDEV')

        cartId = CPQ.getCartId('name:testa5')
        applied = CPQ.getCartPromotions_api(cartId,getPromotionsAppliedToCart=True)
        dele = CPQ.deleteCartPromotion_api(cartId,applied[0]['Id']['value'])

    def test_postPromo_items1(self):
        restClient.init('DEVNOSCAT4')

        cartId ='8013O000004ETKRQA4'
        promoId = 'a503O000000AgmzQAC'
        res = CPQ.postCartsPromoItems_api(cartId,promoId,contextLineItemIds=['8023O000006AX9iQAG'])

    def test_postPromo(self):
        restClient.init('NOSDEV')

        promoName = 'NOS4u 100Mb + Móvel'
        promo = CPQ.getCartPromotions('name:testa5',query=promoName,onlyOne=True)

        cartId = CPQ.getCartId('name:testa5')

        res = CPQ.postCartsPromoItems_api(cartId,promo['Id'])

        applied = CPQ.getCartPromotions_api(cartId,getPromotionsAppliedToCart=True)

       # dele = CPQ.deleteCartPromotion_api(cartId,applied[0]['Id']['value'])

        print()

    def test_getErrors(self):
        cartId = CPQ.getCartId('name:testa5')

        all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')

        sim = all['records'][0]['lineItems']['records'][3]['productGroups']['records'][1]['productGroups']['records'][0]['lineItems']['records'][0]
        for key in sim.keys():
          sim2= sim.copy()
          sim2.pop(key)
          items = {"records":[sim2]}
          res = CPQ.updateCartItem_api(cartId,items)
          if res['messages'][0]['message'] == 'Successfully updated.':
            print(f"{key} {res['messages'][0]['message']}")
          else:
            print(f"******************************************************   {key} {res['messages'][0]['message']}")

    def test_updateCartItemXX(self):
        restClient.init('NOSDEV')
        cartId = CPQ.getCartId('Id:801AU00000WYqDCYA1')

        all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')

        sim = all['records'][0]['lineItems']['records'][3]['productGroups']['records'][1]['productGroups']['records'][0]['lineItems']['records'][0]

        print(sim['Quantity'])
        sim_m = {}
        sim_m['vlocity_cmt__LineNumber__c'] = sim['vlocity_cmt__LineNumber__c']
        sim_m['vlocity_cmt__RootItemId__c'] = sim['vlocity_cmt__RootItemId__c']
        sim_m['vlocity_cmt__Action__c'] = sim['vlocity_cmt__Action__c']
        sim_m['Id'] = sim['Id']
      #  sim_m['Quantity'] = sim['Quantity']
      #  sim_m['Quantity']['value'] = 2.0
        items = {"records":[sim_m]}

        sim_m['vlocity_cmt__ServiceAccountId__c'] = '0013O000016sKfwQAE'
        sim_m['vlocity_cmt__BillingAccountId__c'] = '0013O000016sKfwQAE'

        res = CPQ.updateCartItem_api(cartId,items)
        time = restClient.getLastCallElapsedTime()
        print(time)
        print(res['messages'][0]['message'])

        all_2 = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')
        sim_2 = all_2['records'][0]['lineItems']['records'][3]['productGroups']['records'][1]['productGroups']['records'][0]['lineItems']['records'][0]
        print(sim_2['Quantity']['value'])
        print()

    def test_updateCartItem(self):
        restClient.init('DEVNOSCAT4')

        promoName = 'NOS4u 100Mb + Móvel'

        cartId,items =  CPQUtil.create_cart_with_promo('account_2','cart_2',promoName,create=True)

        if 1==2:
          postPromo =True

          acc = account.create('Name:unaiTest21',recordTypeName='Consumer')
          cartId = CPQ.createCart(accountF= acc['Id'], pricelistF='Name:B2C Price List',name="testa_7",checkExists=True)
          print(cartId)

          if postPromo==True:
            promoName = 'NOS4u 100Mb + Móvel'
            promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)

            res = CPQ.postCartsPromoItems_api(cartId,promo['Id'])

          all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')

          codes = ['C_NOS_OFFER_001','C_NOS_AGG_SERVICE_TV_UMA','C_NOS_SERVICE_TV_003','C_NOS_EQUIP_TV_009']
          codes = ['C_NOS_OFFER_001']

          account1Id = acc['Id']
          account2Id = account.getId('name:account_6')

        objs = []
        codes = ['C_NOS_OFFER_001']
        account2Id = account.getId('name:account_6')

        for code in codes:
          lineItem = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue=code,whereKey='itemType',whereValue='lineItem')['object']
          if lineItem == None:
            print(f"None for code {code}")
            continue

        #  assert(lineItem['vlocity_cmt__ServiceAccountId__c']['value'] == account1Id)
        #  assert(lineItem['vlocity_cmt__BillingAccountId__c']['value'] == account1Id)

          obj = {}
          obj['vlocity_cmt__LineNumber__c'] = lineItem['vlocity_cmt__LineNumber__c']
          obj['vlocity_cmt__RootItemId__c'] = lineItem['vlocity_cmt__RootItemId__c']
          obj['vlocity_cmt__Action__c'] = lineItem['vlocity_cmt__Action__c']
          obj['vlocity_cmt__AssetReferenceId__c'] = lineItem['vlocity_cmt__AssetReferenceId__c']
          obj['Id'] = lineItem['Id']
          obj['vlocity_cmt__ServiceAccountId__c'] = account2Id
          obj['vlocity_cmt__BillingAccountId__c'] = account2Id

          objs.append(obj)
       #   objs.append({"records":[obj]})

        items = {"records":objs}
        res = CPQ.updateCartItem_api(cartId,items)
        time = restClient.getLastCallElapsedTime()
        restClient.callSave('minimum',logRequest=True)
        print(time)
        print(res['messages'][0]['message'])

#        all2 = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')
#
#        for code in codes:
#          lineItem = objectUtil.getSiblingWhere(all2,selectKey='ProductCode',selectKeyValue=code,whereKey='itemType',whereValue='lineItem')['object']
#          print(f"{code}  {lineItem['vlocity_cmt__ServiceAccountId__c']['value']}  {lineItem['vlocity_cmt__BillingAccountId__c']['value']}   {account2Id}")

        incli._main(["-u","DEVNOSCAT4","-q", f"select Id,vlocity_cmt__BillingAccountId__c,vlocity_cmt__LineNumber__c,vlocity_cmt__ServiceAccountId__c,vlocity_cmt__Product2Id__r.productCode from orderitem where OrderId='{cartId}' order by vlocity_cmt__LineNumber__c","-fields","all"])  

        CPQ.deleteCart(cartId)

        print()
    
    def test_updateCartItem_CPQUtil(self):
        restClient.init('DEVNOSCAT4')

        promoName = 'NOS4u 100Mb + Móvel'

        cartId,items =  CPQUtil.create_cart_with_promo('account_2','cart_2',promoName,create=True)

        objs = []
        code = 'C_NOS_OFFER_001'
        account2Id = account.getId('name:account_6')

        obj = {
           'vlocity_cmt__ServiceAccountId__c' : account2Id,
           'vlocity_cmt__BillingAccountId__c' : account2Id
        }

        attr = {
           'ATT_NOS_MATRIX_ID':1111,
           'ATT_SERVICE_ACCOUNT_TYPE':'Móvel'
        }

        call = CPQUtil.update_field(cartId,items,code,obj,attributesDic=attr)

        time = restClient.getLastCallElapsedTime()
        restClient.callSave('minimum',logRequest=True)
        print(time)

#        all2 = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')
#
#        for code in codes:
#          lineItem = objectUtil.getSiblingWhere(all2,selectKey='ProductCode',selectKeyValue=code,whereKey='itemType',whereValue='lineItem')['object']
#          print(f"{code}  {lineItem['vlocity_cmt__ServiceAccountId__c']['value']}  {lineItem['vlocity_cmt__BillingAccountId__c']['value']}   {account2Id}")

        incli._main(["-u","DEVNOSCAT4","-q", f"select Id,vlocity_cmt__BillingAccountId__c,vlocity_cmt__LineNumber__c,vlocity_cmt__ServiceAccountId__c,vlocity_cmt__Product2Id__r.productCode from orderitem where OrderId='{cartId}' order by vlocity_cmt__LineNumber__c","-fields","all"])  

        CPQ.deleteCart(cartId)

        print()

    def test_write_to_file(self):
        restClient.init('NOSDEV')

        cartId = CPQ.getCartId('name:testa_1')
        CPQ.deleteCart(cartId)

        acc = account.createAccount('Name:unaiTest2',recordTypeName='Consumer')
        cartId = CPQ.createCart(accountF= acc['Id'], pricelistF='Name:B2C Price List',name="testa_1",checkExists=True)
        print(cartId)

        promoName = 'NOS4u 100Mb + Móvel'
        promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)

        res = CPQ.postCartsPromoItems_api(cartId,promo['Id'])

        all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c')
        filename = restClient.callSave('getItemsqwe')
        print(filename)

    def test_read_from_file(self):
        restClient.init('NOSDEV')
        account1Id = account.getAccountId('name:unaiTest2')
        account2Id = account.getAccountId('name:unai2')

        print(account2Id)

        stItems = file.read('/Users/uormaechea/Documents/Dev/python/InCliLib/.incli/output/getItemsqwe_res.json')
        stItems2 = stItems.replace(account1Id,account2Id)
        items = simplejson.loads(stItems2)
        cartId = CPQ.getCartId('name:testa_1')
        print(cartId)
     #   res = CPQ.updateCartItem_api(cartId,items)

        C_NOS_OFFER_001 = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_OFFER_001',whereKey='itemType',whereValue='lineItem')['object']
        C_NOS_EQUIP_TV_006 = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_EQUIP_TV_006',whereKey='itemType',whereValue='lineItem')['object']
        C_NOS_EQUIP_TV_009 = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_EQUIP_TV_009',whereKey='itemType',whereValue='lineItem')['object']
        C_NOS_SERVICE_TV_003 = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_TV_003',whereKey='itemType',whereValue='lineItem')['object']

        C_NOS_SERVICE_IF_001 = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_IF_001',whereKey='itemType',whereValue='lineItem')['object']
        C_NOS_EQUIP_GIGA_ROUTER = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_EQUIP_GIGA_ROUTER',whereKey='itemType',whereValue='lineItem')['object']

        C_NOS_DN = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_DN',whereKey='itemType',whereValue='lineItem')['object']
        C_NOS_SERVICE_VF_001 = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_VF_001',whereKey='itemType',whereValue='lineItem')['object']


        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_EQUIP_TV_006)
        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_EQUIP_TV_009)
        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_SERVICE_TV_003)

        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_SERVICE_IF_001)
        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_EQUIP_GIGA_ROUTER)

        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_DN)
        C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_SERVICE_VF_001)
    #    C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_AGG_SERVICE_VF_HFC)

        items = {"records":[C_NOS_OFFER_001]}
        res = CPQ.updateCartItem_api(cartId,items)
        print(restClient.getLastCallElapsedTime())
        print(res['messages'][0]['message'])

        incli._main(["-u","NOSDEV","-q", f"select Id,vlocity_cmt__BillingAccountId__c,vlocity_cmt__LineNumber__c,vlocity_cmt__ServiceAccountId__c,vlocity_cmt__Product2Id__r.productCode from orderitem where OrderId='{cartId}' order by vlocity_cmt__LineNumber__c","-fields","all"])  

        print()

    def lineItem_for_update(self,lineItem):
          obj = {}
          obj['vlocity_cmt__LineNumber__c'] = lineItem['vlocity_cmt__LineNumber__c']
          obj['vlocity_cmt__RootItemId__c'] = lineItem['vlocity_cmt__RootItemId__c']
          obj['vlocity_cmt__Action__c'] = lineItem['vlocity_cmt__Action__c']          
          obj['vlocity_cmt__AssetReferenceId__c'] = lineItem['vlocity_cmt__AssetReferenceId__c']
          obj['Id'] = lineItem['Id']

   #       obj['vlocity_cmt__ServiceAccountId__c'] = account2Id
   #       obj['vlocity_cmt__BillingAccountId__c'] = account2Id

          if 'lineItems2' in lineItem:
            obj['lineItems'] = lineItem['lineItems']
            for li in obj['lineItems']['records']:
              li.pop('productChildItemDefinition')
              li.pop('lineItems',None)
              li.pop('childProducts',None)
              li.pop('productGroups',None)

              li.pop('messages',None)
              li.pop('actions',None)
              li.pop('displaySequence',None)
              li.pop('UnitPrice',None)
              li.pop('Product2',None)

              li.pop('Name',None)
              li.pop('Product2Id',None)
              li.pop('IsActive',None)
              li.pop('ProductCode',None)
              li.pop('vlocity_cmt__RecurringPrice__c',None)

              li.pop('Pricebook2Id',None)
              li.pop('PricebookEntry',None)
              li.pop('productId',None)
              li.pop('defaultQuantity',None)
              li.pop('minQuantity',None)

              li.pop('maxQuantity',None)
              li.pop('groupMinQuantity',None)
              li.pop('groupMaxQuantity',None)
              li.pop('sequenceNumber',None)
              li.pop('productChildItemId',None)
              li.pop('productChildItemDefinition',None)

              li.pop('name',None)
              li.pop('isVirtualItem',None)
              li.pop('hasChildren',None)
              li.pop('orderActive',None)
              li.pop('parentRecordTypeDevName',None)
              li.pop('itemType',None)

              li.pop('action',None)
              li.pop('SellingPeriod',None)
              li.pop('ListPrice',None)
              li.pop('OrderId',None)
              li.pop('PricebookEntryId',None)
              li.pop('Quantity',None)

         #     li.pop('vlocity_cmt__AssetReferenceId__c',None)
              li.pop('vlocity_cmt__CatalogItemReferenceDateTime__c',None)
              li.pop('vlocity_cmt__CurrencyPaymentMode__c',None)
              li.pop('vlocity_cmt__EffectiveOneTimeTotal__c',None)
              li.pop('vlocity_cmt__EffectiveRecurringTotal__c',None)
              li.pop('vlocity_cmt__InCartQuantityMap__c',None)
              li.pop('vlocity_cmt__IsChangesAllowed__c',None)

          if 'lineItems' in lineItem:
            obj['lineItems'] = {}
            obj['lineItems']['records'] = []
            for record in lineItem['lineItems']['records']:
              li = self.lineItem_for_update(record)
              obj['lineItems']['records'].append(li)
          return obj
    
    def test_do_all_puts(self):
        def getObj(lineItem,account2Id):
          obj = {}
          obj['vlocity_cmt__LineNumber__c'] = lineItem['vlocity_cmt__LineNumber__c']
          obj['vlocity_cmt__RootItemId__c'] = lineItem['vlocity_cmt__RootItemId__c']
          obj['vlocity_cmt__Action__c'] = lineItem['vlocity_cmt__Action__c']          
          obj['vlocity_cmt__AssetReferenceId__c'] = lineItem['vlocity_cmt__AssetReferenceId__c']
          obj['Id'] = lineItem['Id']

          obj['vlocity_cmt__ServiceAccountId__c'] = account2Id
          obj['vlocity_cmt__BillingAccountId__c'] = account2Id

          obj['attributeCategories'] = lineItem['attributeCategories']

          if 'lineItems2' in lineItem:
            obj['lineItems'] = lineItem['lineItems']
            for li in obj['lineItems']['records']:
              li.pop('productChildItemDefinition')
              li.pop('lineItems',None)
              li.pop('childProducts',None)
              li.pop('productGroups',None)

              li.pop('messages',None)
              li.pop('actions',None)
              li.pop('displaySequence',None)
              li.pop('UnitPrice',None)
              li.pop('Product2',None)

              li.pop('Name',None)
              li.pop('Product2Id',None)
              li.pop('IsActive',None)
              li.pop('ProductCode',None)
              li.pop('vlocity_cmt__RecurringPrice__c',None)

              li.pop('Pricebook2Id',None)
              li.pop('PricebookEntry',None)
              li.pop('productId',None)
              li.pop('defaultQuantity',None)
              li.pop('minQuantity',None)

              li.pop('maxQuantity',None)
              li.pop('groupMinQuantity',None)
              li.pop('groupMaxQuantity',None)
              li.pop('sequenceNumber',None)
              li.pop('productChildItemId',None)
              li.pop('productChildItemDefinition',None)

              li.pop('name',None)
              li.pop('isVirtualItem',None)
              li.pop('hasChildren',None)
              li.pop('orderActive',None)
              li.pop('parentRecordTypeDevName',None)
              li.pop('itemType',None)

              li.pop('action',None)
              li.pop('SellingPeriod',None)
              li.pop('ListPrice',None)
              li.pop('OrderId',None)
              li.pop('PricebookEntryId',None)
              li.pop('Quantity',None)

         #     li.pop('vlocity_cmt__AssetReferenceId__c',None)
              li.pop('vlocity_cmt__CatalogItemReferenceDateTime__c',None)
              li.pop('vlocity_cmt__CurrencyPaymentMode__c',None)
              li.pop('vlocity_cmt__EffectiveOneTimeTotal__c',None)
              li.pop('vlocity_cmt__EffectiveRecurringTotal__c',None)
              li.pop('vlocity_cmt__InCartQuantityMap__c',None)
              li.pop('vlocity_cmt__IsChangesAllowed__c',None)

          if 'lineItems' in lineItem:
            obj['lineItems'] = {}
            obj['lineItems']['records'] = []
            for record in lineItem['lineItems']['records']:
              li = getObj(record,account2Id)
              obj['lineItems']['records'].append(li)
          return obj

        restClient.init('NOSDEV')

        accountname='unaiTest_1'

        cartId = CPQUtil.create_cart_with_promo(accountname=accountname,cartName='testa_18',promoName='NOS4u 100Mb + Móvel',create=True,pricelistF='Name:B2C Price List')

        all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c',price=False,validate=False,includeAttachment=False)
        print(restClient.getLastCallElapsedTime())

        account1Id = account.getId(f'name:{accountname}')
        account2Id = account.getId('name:unai2')

     #   strAll = simplejson.dumps(all)
     #   stItems2 = strAll.replace(account1Id,account2Id)
        items = objectUtil.replace_everywhere_in_obj(all,account1Id,account2Id)

        print(cartId)

        codes = ['C_NOS_SERVICE_TV_003','C_NOS_EQUIP_TV_006','C_NOS_EQUIP_TV_009','C_NOS_SERVICE_IF_001','C_NOS_EQUIP_GIGA_ROUTER','C_NOS_DN','C_NOS_SERVICE_VF_001','C_NOS_MSISDN','C_NOS_SERVICE_VM_001','C_NOS_EQUIP_SIM_CARD','C_NOS_OFFER_001','C_NOS_OFFER_006','C_NOS_AGG_SERVICE_TV_UMA','C_NOS_AGG_SERVICE_IF_HFC','C_NOS_AGG_SERVICE_VF_HFC','C_NOS_AGG_SERVICES_MAND_VM']
    #    codes = ['C_NOS_OFFER_006']
      #  codes = []
        lineItem = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_OFFER_001',whereKey='itemType',whereValue='lineItem')['object']
   #     for key in lineItem.keys():
   #       print(key)
        C_NOS_OFFER_001 = getObj(lineItem,account2Id)
        C_NOS_OFFER_001['lineItems']['records'] = []
    #    C_NOS_OFFER_001_copy = C_NOS_OFFER_001.copy()
    #    C_NOS_OFFER_001_copy.pop('lineItems')
        if 1==1:
            C_NOS_OFFER_001.pop('vlocity_cmt__LineNumber__c')
            C_NOS_OFFER_001.pop('vlocity_cmt__RootItemId__c')
            C_NOS_OFFER_001.pop('vlocity_cmt__Action__c')
            C_NOS_OFFER_001.pop('Id')
            C_NOS_OFFER_001.pop('vlocity_cmt__ServiceAccountId__c')
            C_NOS_OFFER_001.pop('vlocity_cmt__BillingAccountId__c')
            C_NOS_OFFER_001.pop('vlocity_cmt__AssetReferenceId__c')

    #    C_NOS_OFFER_001['lineItems'] = {}
    #    C_NOS_OFFER_001['lineItems']['records']=[]

    #    C_NOS_OFFER_001['lineItems']['records'].append(C_NOS_OFFER_001_copy)
        for code in codes:
          lineItem = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue=code,whereKey='itemType',whereValue='lineItem')['object']
          li = getObj(lineItem,account2Id)
          C_NOS_OFFER_001['lineItems']['records'].append(li)

        items = {"records":[C_NOS_OFFER_001]}
        res = CPQ.updateCartItem_api(cartId,items)  
        filename = restClient.callSave('records0001',logRequest=True,logReply=False)   

        print(restClient.getLastCallElapsedTime())
        print(res['messages'][0]['message'])

        incli._main(["-u","NOSDEV","-q", f"select Id,vlocity_cmt__BillingAccountId__c,vlocity_cmt__LineNumber__c,vlocity_cmt__ServiceAccountId__c,vlocity_cmt__Product2Id__r.productCode from orderitem where OrderId='{cartId}' order by vlocity_cmt__LineNumber__c","-fields","all"])  

        items = CPQ.getCartItems_api(cartId=cartId)
        print()

    def test_get_order_lines_for_CartId(self):
        cartId = '8013O000003j97nQAA'
        incli._main(["-u","NOSDEV","-q", f"select Id,vlocity_cmt__LineNumber__c,vlocity_cmt__Product2Id__r.productCode,vlocity_cmt__Product2Id__r.name from orderitem where OrderId='{cartId}' order by vlocity_cmt__LineNumber__c","-fields","all"])  

    def test_deleteOrder(self):
      orderId = '8013O000003a9CoQAI'
      restClient.init('NOSDEV')
      try:
        delete = CPQ.deleteCart(orderId)
      except Exception as e:
        utils.printException(e)

    def test_delete_discount(self):

      restClient.init('NOSDEV')

   # def create_cart_with_offer(self,accountname,cartName,offerName,create=False,pricelistF='Name:B2C Price List',timeStats=None):

    #    cartId = CPQ.getCartId(f"name:{cartName}")
    #    if cartId != None:
     #     if create == False:
       #     return cartId
     #     CPQ.deleteCart(cartId)

     #   accountF = f'Name:{accountname}'
     #   accountId = account.create_Id(accountname,recordTypeName='Consumer')

     #   inputFields = {
#'NOS_t_CoverageTechnology__c':'FTTH'
 #       }
     #   cartId = CPQ.createCart(accountF= accountId, pricelistF=pricelistF,name=cartName,checkExists=True,inputFields=inputFields)

     #   offer = CPQ.getCartsProducts(cartId,query=offerName,onlyOne=True)
     #   res = CPQ.addItemstoCart(cartId,productCode=offer['ProductCode']['value'],pricelistF=pricelistF)

      #  return cartId  
    
    #def create_cart_with_promo(self,accountname,cartName,promoName,create=False,pricelistF='Name:B2C Price List'):

     #   cartId = CPQ.getCartId(f"name:{cartName}")
     #   if cartId != None:
     #     if create == False:
     #       return cartId
     #     CPQ.deleteCart(cartId)

     #   accountF = f'Name:{accountname}'
     #   accountId = account.create_Id(accountname,recordTypeName='Consumer')
     #   cartId = CPQ.createCart(accountF= accountId, pricelistF=pricelistF,name=cartName,checkExists=True)

     #   promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)

     #   res = CPQ.postCartsPromoItems_api(cartId,promo['Id'],price=False,validate=False)

      #  return cartId

    def test_post_cart_item(self):
        restClient.init('NOSDEV')
        restClient.setLoggingLevel()
        cartName = 'testa_4c'

        cartId = CPQ.getCartId(f"name:{cartName}")
        if cartId != None:
          CPQ.deleteCart(cartId)

        accountId = account.create_Id('unaiTest1c',recordTypeName='Consumer')
        cartId = CPQ.createCart(accountF= accountId, pricelistF='Name:B2C Price List',name=cartName,checkExists=True)
        print(restClient.getLastCallElapsedTime())

        promoName = 'NOS4u 100Mb + Móvel - Desc. Mensal'
        promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)

        res = CPQ.postCartsPromoItems_api(cartId,promo['Id'])
        print(restClient.getLastCallElapsedTime())

        all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c',price=False,validate=False,includeAttachment=False)
        print(restClient.getLastCallElapsedTime())

    def test_create_cart_from_asset(self):
        restClient.init('NOSQSM')

        restClient.setLoggingLevel()
        cartName = 'testa_4'

        assetId='02i7a00000TMXGcAAP'
        accId ='0017a00002HIKq2AAH'
        servId ='0017a00002HIKqRAAX'

        aaa = '0017a00002HIEefAAH'
        accountId=servId

        cartId = CPQ.createCartFromAsset(assetId=assetId,accountId=accountId,date='2023-06-22',inputFields={"Name":cartName})
        print(cartId)

        items = CPQ.getCartItems_api(cartId,price=False,validate=False)

        print()

    def test_update_attribute2(self):
        restClient.init('DEVNOSCAT4')
        restClient.setLoggingLevel()
        cartName = 'testa_4'

        promoName = 'NOS4u 100Mb + Móvel'

        cartId,items =  CPQUtil.create_cart_with_promo('account_2','cart_2',promoName,create=True)
        print(cartId)
        items = CPQ.getCartItems_api(cartId,price=False,validate=False)
        lineItem = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_TV_003',whereKey='itemType',whereValue='lineItem')['object']
        line2 = self.lineItem_for_update(lineItem)

        def onlyValue(line):
          obj = {}
          obj['value'] = line['value']
          return obj

        line2['vlocity_cmt__LineNumber__c'] = onlyValue(line2['vlocity_cmt__LineNumber__c'])
        line2['vlocity_cmt__RootItemId__c'] = onlyValue(line2['vlocity_cmt__RootItemId__c'])
        line2['vlocity_cmt__AssetReferenceId__c'] = onlyValue(line2['vlocity_cmt__AssetReferenceId__c'])
        line2['Id'] = onlyValue(line2['Id'])
      #  line2['vlocity_cmt__Action__c'] = onlyValue(line2['vlocity_cmt__Action__c'])
        line2['vlocity_cmt__Action__c'].pop('previousValue')
        line2['vlocity_cmt__Action__c'].pop('originalValue')
        line2['vlocity_cmt__Action__c'].pop('messages')
        line2['vlocity_cmt__Action__c'].pop('actions')
        line2['vlocity_cmt__Action__c'].pop('hidden')
      #  line2['vlocity_cmt__Action__c'].pop('editable')  #REQ
      #  line2['vlocity_cmt__Action__c'].pop('dataType')  #REQ
        line2['vlocity_cmt__Action__c'].pop('alternateValues')
      #  line2['vlocity_cmt__Action__c'].pop('label')
       # line2['vlocity_cmt__Action__c'].pop('fieldName')  #REQ

        if 1==1:
          line2['attributeCategories'] = lineItem['attributeCategories']
          line2['attributeCategories']['records'][0]['productAttributes']['records'][2]['userValues'] = 'yyyy5'
          line2['attributeCategories']['records'].pop()
          line2['attributeCategories']['records'].pop()
          line2['attributeCategories']['records'][0]['productAttributes']['records'].pop(0)
          line2['attributeCategories']['records'][0]['productAttributes']['records'].pop(0)

          line2['attributeCategories']['records'][0]['productAttributes'].pop('totalSize')
          line2['attributeCategories']['records'][0]['productAttributes'].pop('messages')

          line2['attributeCategories']['records'][0].pop('displaySequence')
          line2['attributeCategories']['records'][0].pop('Name')
          line2['attributeCategories']['records'][0].pop('id')
          line2['attributeCategories']['records'][0].pop('messages')

        # line2['attributeCategories']['records'][0].pop('Code__c')  REQ

          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('messages')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('dataType')
      #   line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('inputType',None)   REQ
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('hasRules')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('cloneable')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('multiselect')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('isNotTranslatable')


      #   line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('required')     REQ
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('attributeId')

          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('filterable')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('label')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('displaySequence')

          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('disabled',None)
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('readonly',None)
          line2['attributeCategories'].pop('totalSize')
          line2['attributeCategories'].pop('messages')

          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('values')
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('hidden',None)
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('disabled',None)
          line2['attributeCategories']['records'][0]['productAttributes']['records'][0].pop('readonly',None)

        items = {"records":[line2]}
        res = CPQ.updateCartItem_api(cartId,items)  
        filepath = restClient.callSave("update1111",logRequest=True,logReply=False)
        print(res['messages'][0]['message'])
        print(restClient.getLastCallElapsedTime())

        itemsAfter = CPQ.getCartItems_api(cartId,price=False,validate=False)

        line3 = objectUtil.getSiblingWhere(itemsAfter,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_TV_003',whereKey='itemType',whereValue='lineItem')['object']
        print(line3['attributeCategories']['records'][0]['productAttributes']['records'][2]['userValues'])
        print()

    def test_update_attribute(self):
        restClient.init('NOSQSM')
        restClient.setLoggingLevel()

        cartId = CPQUtil.create_cart_with_promo('account_2','cart_2','NOS4u 100Mb + Móvel',create=False)

        items = CPQ.getCartItems_api(cartId)

        item = items['records'][1]['lineItems']['records'][0]
        item2 = {}
        item2['attributeCategories'] = item['attributeCategories']
        item2['attributeCategories']['records'].pop()
        item2['attributeCategories']['totalSize'] = 1

        item2['Id'] = item['Id']
        item2['Product2'] = item['Product2']

        item2['PricebookEntry'] = {}
        item2['PricebookEntry']['attributes'] = item['PricebookEntry']['attributes']
        item2['PricebookEntry']['Product2Id'] = item['PricebookEntry']['Product2Id']
        item2['PricebookEntry']['Pricebook2Id'] = item['PricebookEntry']['Pricebook2Id']
        item2['PricebookEntry']['Product2'] = item['PricebookEntry']['Product2']
        item2['PricebookEntry']['Id'] = item['PricebookEntryId']['value']
     #   item2['PricebookEntry']['value'] = item['PricebookEntry']['value']

        item2['PricebookEntry']['Product2'].pop('vlocity_cmt__AttributeDefaultValues__c')
        item2['PricebookEntry']['Product2'].pop('vlocity_cmt__AttributeMetadata__c')

        item2['PricebookEntryId'] = item['PricebookEntryId']

        attributes = CPQ.update_item_attribute_api(cartId,item2)


        print()


    def test_get_cart_items2(self):
        restClient.init('upgrade248')
        cartId = "8011l000005yayFAAQ"

        items = CPQ.getCartItems_api(cartId,price=False,validate=False)

        ff = jsonFile.write('items',items)


        print()
    def test_get_cart_items(self):
        restClient.init('qmscopy')
        cartId = "801AP00000j0bs7YAA"
        cartId = '801AU00000dTUnRYAW'

        #items = CPQ.getCartItems_api(cartId,price=False,validate=False,reduced=False)
        #filename = restClient.callSave('getItems_full')
        items2 = CPQ.getCartItems_api(cartId,price=False,validate=False,reduced=True)
        filename2 = restClient.callSave('getItems_reduced')


        print()

    def test_postCartItem_JSON(self):
        restClient.init('NOSDEV')
        cartId = '801AU00000kUsWmYAK'
       # action = f'/services/apexrest/v2/postcartitems/{cartId}/items?noResponseNeeded=true'
        action = f'/services/apexrest/vlocity_cmt/v2/cpq/carts/{cartId}/items'

        data = {"cartId":"801AU00000kUsWmYAK","items":[{"parentId":"802AU00000GlXQlYAN","parentHierarchyPath":"01tAU00000CBStJYAX<01t3O000006l0gqQAA","itemId":"01u3O00002kKh4eQAC","parentRecord":{"records":[{"productHierarchyPath":"01tAU00000CBStJYAX<01t3O000006l0gqQAA","ProductCode":{"value":"C_NOS_AGG_INST_SERVICES_HFC","label":"Product Code"},"Id":{"value":"01u3O00002UHszFQAT","label":"Price Book Entry ID"}}]},"fieldsToUpdate":{"quantity":1}}],"methodName":"postCartsItems","price":False,"validate":False}
        call = restClient.callAPI(action,method='post',data=data)
        a=1


    def test_get_cart_items_bt(self):
        res = restClient.init('NOSDEV')
        cartId = "801AP00000j0bs7YAA"
        cartId = '801AU00000dTUnRYAW'
        cartId = 'test123'

        items = CPQ.getCartItems_custom_api(cartId,price=False,validate=False)
        filename = restClient.callSave('getItems_bt')

        print()


    def test_sort_items_NOT_REDUCED(self):
       restClient.init('NOSDEV')
      # restClient.init('qmscopy')

       cartId = "801AP00000hXXsXYAW" #large 174
       cartId = '801AP00000jXbYOYA0'
       cartId = '801AU00000nSZ0QYAW'

       self.compare_getItems(cartId,getreduced=False,fields='vlocity_cmt__ConnectDate__c,NOS_t_MacAddress__c,NOS_t_MtaMacAddress__c,vlocity_cmt__ServiceIdentifier__c,vlocity_cmt__SerialNumber__c')


    def test_sort_items_ALSO_REDUCED(self):
       restClient.init('NOSDEV')

       cartId = "801AU00000pMr6jYAC"
       self.compare_getItems(cartId,fields='vlocity_cmt__ConnectDate__c,NOS_t_MacAddress__c,NOS_t_MtaMacAddress__c,vlocity_cmt__ServiceIdentifier__c,vlocity_cmt__SerialNumber__c')

    def test_sort_items_list(self):
       restClient.init('qmscopy')
       cartIds = ['801AU00000dTUnRYAW',"801AP00000j0bs7YAA"]
       for cartId in cartIds:
          self.compare_getItems(cartId)
          a=1

    def test_sort_items_query(self):
       restClient.init('qmscopy')

       res = query.query('select Id from order order by CreatedDate desc limit 100')
       for r in res['records']:
          try:
            self.compare_getItems(r['Id'])
            a=1
          except Exception as e:
             print(e)

    def compare_getItems(self,cartId,getreduced=True,fields=None):
       
      def update_json(obj):
          if isinstance(obj, dict): 
              if "attributeId" in obj:
                if "disabled" in obj:  
                  obj["disabled"] = "XXX"  
              if "editable" in obj:  
                obj["editable"] = "XXX"  
              if "hidden" in obj:  
                obj["hidden"] = "XXX"  
              for key in obj: 
                  obj[key] = update_json(obj[key])
          elif isinstance(obj, list):  
              obj = [update_json(item) for item in obj]
          return obj  
      
      if (getreduced):
          if (1==2):
            print('getting full')
            items = CPQ.getCartItems_api(cartId,price=False,validate=False,reduced=False)
            f = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_reduced_res_full.json',items)

          try:
            print('getting reduced')
            items = CPQ.getCartItems_api(cartId,price=False,validate=False,reduced=True,fields=fields)
            print(f'Reduced time: {restClient.getLastCallElapsedTime()}')

            f0 = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_reduced_res.json',items)
          except Exception as e:
             items = restClient.lastCall('response')
             print(e)

          print('sort reduced')
          reduced_sorted = CPQUtil.sort_cartItems(items,deleteFields=['Product2','PricebookEntry','actions'])
          reduced_updated = update_json(reduced_sorted)
         # f1 = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_reduced_res_sort.json',reduced_sorted)

      print('getting new')
      items = CPQ.getCartItems_api_custom(cartId,price=False,validate=False,fields=fields)
      print(f'BT time: {restClient.getLastCallElapsedTime()}')

      print('sort new')
      custom_sorted = CPQUtil.sort_cartItems(items)
      custom_updated= update_json(custom_sorted)
      if (getreduced):
        f1_reduced_sorted = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_reduced_res_sort.json',reduced_updated)

      f3_custom_sorted = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_bt_res_sort.json',custom_updated)

      print('done')
      print() 
      a=1

    def test_compare_getItems_files(self):
      j1 = jsonFile.read("/Users/uormaechea/Downloads/getCartItemsUnai.txt")
      CPQUtil.sort_cartItems(j1)
      f1a = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/f1.json',j1)

      j2 = jsonFile.read('/Users/uormaechea/Downloads/getCartitemsOriginal.txt')
      CPQUtil.sort_cartItems(j2)
      f2a = jsonFile.write('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/f2.json',j2)

      a=1


    def test_submit_order(seld):
        restClient.init('DEVNOSCAT2')
        restClient.setLoggingLevel()
        cartId = "8013O000003izGtQAI"

        items = CPQ.checkOut_api(cartId)

        print()

    def test_post_cart_items_Movel(self):
        restClient.init('NOSDEV')
        pricelistF = "Name:Woo Price List"

        self.create_cart_with_offer('account_2','cart_a4','Móvel',pricelistF=pricelistF,create=False)

        print()


    def test_post_cart_items(self):
        restClient.init('DEVNOSCAT4')
        restClient.setLoggingLevel()
        pricelistF = "Name:B2C Price List"

        ts = timeStats.TimeStats()

        #cartId = CPQ.getCartId(f"name:cart_7a3")
        cartId = CPQ.getCartId(f"8013O0000046OraQAE")

        
       # cartId = self.create_cart_with_promo('account_2','cart_7a4','NOS4u 100Mb + Móvel',pricelistF=pricelistF,create=True)
        print(cartId)
        #items = CPQ.getCartItems_api(cartId,price=False,validate=False)
     #   while 1==1:
        items = CPQ.getCartItems_api(cartId,price=False,validate=False)

      #  return

        siblings = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_OTT_PWR_WIFI_L',whereKey='itemType',whereValue='childProduct')
        C_NOS_SERVICE_OTT_PWR_WIFI_L = siblings['object']
        parentRecord = siblings['objects'][5]

        powerWifi = CPQ._getItemAtPathEx(items,'C_NOS_SERVICE_OTT_PWR_WIFI_L')

        req1,res1 = restClient.callSave('getITems123')
      #  parentRecord = items['records'][0]['productGroups']['records'][0]

        priceBookEntryId = C_NOS_SERVICE_OTT_PWR_WIFI_L['Id']['value']
        parentId = parentRecord['parentLineItemId']
        parentHierarchyPath = parentRecord['productHierarchyPath']

        parentRecord2 = {}
        parentRecord2['Id'] = parentRecord['Id']['value']
        parentRecord2['productId'] = parentRecord['productId']
        parentRecord2['productHierarchyPath'] = parentRecord['productHierarchyPath']
        parentRecord2['itemType'] = parentRecord['itemType']
        parentRecord2['parentLineItemId'] = parentRecord['parentLineItemId']
     #   parentRecord = items['records'][0]['productGroups']['records'][0]

   #     priceBookEntryId = parentRecord['childProducts']['records'][0]['Pricebook2Id']['value']
   #     parentId = items['records'][0]['Id']['value']
   #     parentHierarchyPath = parentRecord['productHierarchyPath']

   #     parentRecord2 = {}
   #     parentRecord2['Id'] = parentRecord['Id']['value']
   #     parentRecord2['productId'] = parentRecord['productId']
   #     parentRecord2['productHierarchyPath'] = parentRecord['productHierarchyPath']
   #     parentRecord2['itemType'] = parentRecord['itemType']
  #      parentRecord2['parentLineItemId'] = parentRecord['parentLineItemId']

        for x in range(0,10):
          ts.new()

          call = CPQ.addItemstoCart_api(cartId,priceBookEntryId,parentRecord=parentRecord,parentId=parentId,parentHierarchyPath=parentHierarchyPath,noResponseNeeded=False,price=False,validate=False)
          ts.time('postCartItem')

          req2,res2 = restClient.callSave("addItemstoCart_api123",logReply=True,logRequest=True)
          
          items2 = CPQ.getCartItems_api(cartId,price=False,validate=False)
          ts.time('getCartItems')

          C_NOS_SERVICE_OTT_PWR_WIFI_L = objectUtil.getSiblingWhere(items2,selectKey='ProductCode',selectKeyValue='C_NOS_SERVICE_OTT_PWR_WIFI_L',whereKey='itemType',whereValue='lineItem')['object']

          itemIds = C_NOS_SERVICE_OTT_PWR_WIFI_L['Id']['value']

          call2 = CPQ.deleteCartItems_api(cartId,itemIds=[itemIds],parentRecord=parentRecord2,price=False,validate=False)
          ts.time('deleteCartItem')

        ts.print()
        print()

    def test_post_cart_items_util(self):
        restClient.init('DEVNOSCAT4')
        pricelistF = "Name:B2C Price List"

        time_series = True
        if time_series:
           timestamp = False
           time_series_dic = {
              'env':'CAT4',
              'offer':'NOS4u 100Meg Movel'
           }
           filename = 'test_stats_ts'
        else:
          timestamp = True
          time_series_dic=None
          filename = 'test_stats'

        ts = timeStats.TimeStats(filename=f'/Users/uormaechea/Documents/Dev/tableau/summer23/{filename}',timestamp=timestamp,append=True,timeseries_dic=time_series_dic)

        for x in range(0,1000):
          try:
            ts.new()

            cartId = CPQ.getCartId(f"8013O0000046OraQAE")

            print(cartId)
            items = CPQ.getCartItems_api(cartId,price=False,validate=False)
            ts.time('getCartItems')

            productCodes = ['C_NOS_SERVICE_OTT_PWR_WIFI_L','C_NOS_SERVICE_COMP_VM_008','C_NOS_SERVICE_COMP_VM_005','C_NOS_SERVICE_COMP_VM_004','C_NOS_EQUIP_SMART_NUMBER_001']
            productCodes = ['C_NOS_SERVICE_OTT_PWR_WIFI_L']

            def pc_name(pc):
              if 'C_NOS_SERVICE_' in pc:
                pname = pc.split('C_NOS_SERVICE_')[1]
              if 'C_NOS_EQUIP_SMART_' in pc:
                pname = pc.split('C_NOS_EQUIP_SMART_')[1]

              return pname
            
            for pc in productCodes:
              pname = pc_name(pc)

              call = CPQUtil.post_cart_item(cartId,items,pc)
              ts.time(f'post_{pname}')
              items2 = CPQ.getCartItems_api(cartId,price=False,validate=False)
              ts.time(f'get_{pname}')

            for pc in productCodes:
              pname = pc_name(pc)
              call = CPQUtil.delete_cart_item(cartId,items2,pc)
              ts.time(f'del_{pname}')

            ts.print()
          except Exception as e:
             print('Exception')

    def test_post_cart_items_util_new(self):
        restClient.init('DEVNOSCAT4')
        pricelistF = "Name:B2C Price List"

        time_series_dic = {
          'env':'CAT4',
          'offer':'NOS4u 100Meg Movel',
          'product':'',
          'create_cart':True,
          'price':False,
          'validate':False,
          'filename':'/Users/uormaechea/Documents/Dev/tableau/summer23/test_stats_ts_xx.csv',
        }
        filename = 'test_stats_ts'

        ts = timeStats.TimeStats(append=True,timeseries_dic=time_series_dic)

        for x in range(0,1000):
          try:
            ts.new()

            if time_series_dic['create_cart']:
              cartId = CPQUtil.create_cart_with_offer(accountname='account_5',cartName='test12',offerName='NOS4u 100Megas Móvel',create=True,timeStats=ts)
            else:
              cartId = CPQ.getCartId(f"8013O0000046OraQAE")

            print(cartId)
            items = CPQ.getCartItems_api(cartId,price=time_series_dic['price'],validate=time_series_dic['validate'])
            ts.time('getCartItems')

            productCodes = ['C_NOS_SERVICE_OTT_PWR_WIFI_L','C_NOS_SERVICE_COMP_VM_008','C_NOS_SERVICE_COMP_VM_005','C_NOS_SERVICE_COMP_VM_004','C_NOS_EQUIP_SMART_NUMBER_001']
            productCodes = ['C_NOS_SERVICE_OTT_PWR_WIFI_L']
            
            for pc in productCodes:
              call = CPQUtil.post_cart_item(cartId,items,pc,price=False,validate=False)
              ts.field('product',pc)
              ts.time(f'post')
              items2 = CPQ.getCartItems_api(cartId,price=False,validate=False)

            for pc in productCodes:
              call = CPQUtil.delete_cart_item(cartId,items2,pc,price=False,validate=False)
              ts.field('product',pc)
              ts.time(f'del')

            if time_series_dic['create_cart']:
              CPQ.deleteCart(cartId)
              ts.time(f'delCart')


            ts.print()
          except Exception as e:
             print('Exception')

    def test_promo_times(self):
        time_series_dic = {
          'init':'DEVNOSCAT4',
          'env':'CAT4',
          'offer':'NOS4u 100Mb + Móvel',
          'promo':True,
          'product':'',
          'create_cart':True,
          'price':False,
          'validate':False,
          'filename':'/Users/uormaechea/Documents/Dev/tableau/summer23/test_stats_ts_xx.csv',
          'productCodes' : ['C_NOS_AGG_SERVICES_OPT_VM']
        }

        restClient.init(time_series_dic['init'])
        pricelistF = "Name:B2C Price List"   

        ts = timeStats.TimeStats(append=True,timeseries_dic=time_series_dic)

        productCodes = time_series_dic['productCodes']
        time_series_dic.pop('init',None)
        time_series_dic.pop('promo',None)
        time_series_dic.pop('filename',None)
        time_series_dic.pop('productCodes',None)


        for x in range(0,10000):
          ts.new()

          cartId,items = CPQUtil.create_cart_with_promo(accountname='account_6',cartName='testPromo1',promoName=time_series_dic["offer"],create=True,timeStats=ts,price=time_series_dic['price'],validate=time_series_dic['validate'])

          print(cartId)
        #  items = CPQ.getCartItems_api(cartId,price=time_series_dic['price'],validate=time_series_dic['validate'])
        #  filename = restClient.callSave('xxxxxx')
        #  ts.time('getCartItems')

          for pc in productCodes:
              call = CPQUtil.post_cart_item(cartId,items,pc,price=False,validate=False)
              ts.field('product',pc)
              ts.time(f'post')

          items2 = CPQ.getCartItems_api(cartId,price=False,validate=False)
          ts.time('getCartItems')

          for pc in productCodes:
              call = CPQUtil.post_promo_item(cartId,items2,pc,time_series_dic['offer'],price=True,validate=True)
              ts.time(f'promoItem')

          for pc in productCodes:
              call = CPQUtil.delete_cart_item(cartId,items2,pc,price=False,validate=False)
              ts.field('product',pc)
              ts.time(f'del')

          if time_series_dic['create_cart']:
              CPQ.deleteCart(cartId)
              ts.time(f'delCart')


    def test_promo_from_file(self):
       jstr= jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/xxxxx2_res.json')

       CPQUtil.post_promo_item(jstr,'C_NOS_SERVICE_OTT_PWR_WIFI_L','NOS4u 100Mb + Móvel') 
       print()

    def test_getCartItems_x(self):
        restClient.init('NOSDEV')
        q="""SELECT id,
                    pricebook2id,
                    accountid,
                    createddate,
                    vlocity_cmt__defaultcurrencypaymentmode__c,
                    vlocity_cmt__effectiverecurringtotal__c,
                    vlocity_cmt__effectiveonetimetotal__c,
                    vlocity_cmt__numberofcontractedmonths__c,
                    vlocity_cmt__pricelistid__c,
                    recordtypeid,
                    recordtype.developername,
                    status,
                    effectivedate,
                    vlocity_cmt__requestdate__c,
                    vlocity_cmt__orderstatus__c,
                    vlocity_cmt__ischangesallowed__c,
                    vlocity_cmt__ischangesaccepted__c,
                    vlocity_cmt__supplementalaction__c,
                    vlocity_cmt__supersededorderid__c,
                    vlocity_cmt__firstversionorderidentifier__c,
                    vlocity_cmt__requestedstartdate__c,
                    vlocity_cmt__originatingcontractid__c,
                    vlocity_cmt__lastpricedat__c,
                    vlocity_cmt__validationdate__c,
                    vlocity_cmt__ordergroupid__c,
                    vlocity_cmt__ordergroupid__r.vlocity_cmt__groupcartid__c,
                    nos_t_scenariolevel__c,
                    nos_t_coveragetechnology__c,
                    nos_t_businessscenario__c,
                    nos_t_channel__c,
                    nos_t_process__c,
                    nos_b_isbsimulation__c 
                    FROM Order WHERE Id IN ('8013O000003keqvQAA')"""
        res = query.query(q)

        print(restClient.getLastCallAllTimes())

        q2 =f"""SELECT Id,
                      Quantity,
                      vlocity_cmt__AssetReferenceId__c,
                      vlocity_cmt__ParentItemId__c,
                      vlocity_cmt__RootItemId__c,
                      PriceBookEntry.Product2Id,
                      PriceBookEntry.Name,
                      PriceBookEntry.Product2.vlocity_cmt__GlobalGroupKey__c,
                      vlocity_cmt__LineNumber__c,
                      vlocity_cmt__Product2Id__c,
                      vlocity_cmt__Action__c,
                      PricebookEntryId,
                      vlocity_cmt__ProvisioningStatus__c,
                      vlocity_cmt__ProductHierarchyPath__c,
                      vlocity_cmt__ProductHierarchyGroupKeyPath__c,
                      vlocity_cmt__CatalogItemReferenceDateTime__c,
                      OrderId,
                      vlocity_cmt__SupplementalAction__c,
                      vlocity_cmt__IsChangesAllowed__c 
                      FROM OrderItem WHERE OrderId = '{res['records'][0]['Id']}'  ORDER BY vlocity_cmt__LineNumber__c """
        res2 = query.query(q2)
        print(restClient.getLastCallAllTimes())

        idl = [r['Id'] for r in res2['records']]
        lineItemIds = query.IN_clause(idl)

        q3 = f"""SELECT vlocity_cmt__OrderAppliedPromotionId__r.vlocity_cmt__PromotionId__c,
                        vlocity_cmt__OrderAppliedPromotionId__r.vlocity_cmt__Action__c,
                        vlocity_cmt__OrderItemId__c 
                        FROM vlocity_cmt__OrderAppliedPromotionItem__c 
                        WHERE vlocity_cmt__OrderItemId__c IN ({lineItemIds})"""
        res3 = query.query(q3)

        print(restClient.getLastCallAllTimes())
        print()
    def test_clone_item(self):
        restClient.init('DEVNOSCAT4')

        CPQ.clone_item_api("8013O000004AoXHQA0","8023O0000060FZJQA2",None)

    def test_save_order(self):
        restClient.init('DEVNOSCAT4')
        cartId = '8013O000004AoXHQA0'

        items = CPQ.getCartItems_api(cartId,price=False,validate=False)

        filename = restClient.callSave(f'cartItems{cartId}')

        print()

    def test_order_stats(self):
      file = '/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/cartItems8013O000004AoXHQA0_res.json'
      
      items = jsonFile.read(file)

      counters = CPQUtil.cart_stats(items)

      print(counters)

    def test_getting_siblings(self):
      file = '/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/cartItems8013O000004AoXHQA0_res.json'
      
      items = jsonFile.read(file)

      CPQUtil.get_ol(items,'C_NOS_OFFER_017:C_NOS_AGG_SERVICES_OPT_VM|2:C_NOS_SERVICE_VM_001')      
      
      CPQUtil.get_ol(items,'C_NOS_OFFER_017XXX:C_NOS_AGG_SERVICES_OPT_VM|2:C_NOS_SERVICE_VM_001')

      CPQUtil.get_ol(items,'C_NOS_OFFER_017:C_NOS_AGG_SERVICES_OPT_VM|9:C_NOS_SERVICE_VM_001')      

      ##siblings = objectUtil.getSiblingWhere(items,selectKey='ProductCode',selectKeyValue='C_NOS_AGG_SERVICES_OPT_VM',whereKey='itemType',onlyOne=False)
      print()

    def test_cart_products_hierarchy(self):
      file = '/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/cartItems8013O000004AoXHQA0_res.json'
     # items = jsonFile.read(file)

      restClient.init('qmscopy')
      items = CPQ.getCartItems_api('801AU00000eMl4YYAS',price=False,validate=False)

      CPQUtil.cart_products_hierarchy(items)

      a=1

    def test_postCartPromo_Validate(self):
      restClient.init('NOSQSM')

      cartId = '801AU00000ZpsjmYAB'
      promoId = 'a50AU00000EqpOoYAJ'
      
      res = CPQ.postCartsPromoItems_api(cartId,promoId,price=False,validate=False)

      res1 = CPQ.validate_cart(cartId,price=True,validate=True)

      a=1

    def test_validate_cart(self):
       restClient.init('devesmb2b')

       Id = '0Q0AP000001OamX0AS'


       res1 = CPQ.validate_cart(Id,price=True,validate=True)

       #res2 = CPQ.validate_cart_get(Id,price=True)

       a=1

    def test_validate_cart_DEV(self):
       restClient.init('NOSDEV')

       Id = '801AU00000pIRKaYAO'


       res1 = CPQ.validate_cart(Id,price=True,validate=True)

       #res2 = CPQ.validate_cart_get(Id,price=True)

       a=1

    def test_create_work(self):

      restClient.init('NOSQSM')

      q = "select Id from order limit 50000"

      res = query.query(q) 
   #   for rec in res['records']:
   #     res1 = CPQ.validate_cart(rec['Id'],price=True,validate=True)

      def do_work(rec):
         # res = CPQ.validate_cart(rec['Id'],price=True,validate=True)
          try:
            print(rec['Id'])
            res = CPQ.getCartItems_api(rec['Id'])
            return res
          except Exception as e:
             print(f"orderId: <{rec['Id']}>  ---  {e}")
      
      def on_done(attachment,result):
          a=1

      thread.execute_threaded(res['records'],None,do_work,on_done,threads=100)

    def test_getCartsProducts(self):
      restClient.init('DEVNOSCAT2')

      cartId = '8013N000005Gu93QAC'

      res = CPQ.getCartsProducts_api(cartId)
      filename = restClient.callSave('test_getCartsProducts2',logRequest=False,logReply=True)

      a=1
      
    def test_CPQV2(self):
        restClient.init('NOSQSM')
        cartId = '801AU00000WqVzpYAF'  

        input = {
            'methodName' :'getCartsItems',
            'cartId' : cartId,
            'price' : True,
            'validate':True,
            'pagesize' : 10,
            'hierarchy':1,
            'pagesize':1
        }

        res = DR_IP.remoteClass('CPQReductor','getCartsItems',input,{})

        a= 1

#curl -X GET -H 'accept: */*' -H 'accept-encoding: gzip' -H 'api-key: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJleHAiOjE3MzE1MTg2NzIsImlhdCI6MTczMTUxMTQ3MiwianRpIjoiMzBlMGFiMGItOTkyNy00MTY2LWE0ZjgtZGYyZTJjOTAxY2FmIn0.PILKTjEhKstiZfcTK8ZG_dfZyYnL8sknNzgwZZTkTCwTeTyYfbQog6Q2z6zHJ6OOvej_bXMTR6BxTn8UQ_iQ4b7OBXgJIKl5TnrwLYYyfPUAf6uXa0oNveV6-GvswfmhUWQznp66liZkp1WcmzOq-miVZJYik9p_G8N1Z9pxojyjbZDasp3zC5cu0KJOLbFH8s1cmi-eANy2ahm-m9y8SxqByeQkS1jpR6achb9xkB0I03oPZ_yO7pCxwI5YcobL2baJ6q5rQjEXZZb17NATszqrmL4BuL6TIb69cBE-5cUgLuRCK6zeBw9ZiQd0ECZk5St3tt2ZqYEzKjjPrHc1eg' -H 'Authorization: *****' -H 'Content-Type: application/json' -H 'traceparent: 00-bdeb2eba9ebf99a6d68ed861e05b6f81-a151a17222171aa1-01' -H 'tracestate: 395a46f-f954f44f@dt=fw4;3;51e6ffc8;2d2b;0;0;0;104;ebda;2h01;3h51e6ffc8;4h2d2b;5h01;6hbdeb2eba9ebf99a6d68ed861e05b6f81;7ha151a17222171aa1' -H 'X-application: Salesforce' -H 'X-dynaTrace: FW4;-111872945;3;1374093256;11563;0;60138607;260;ebda;2h01;3h51e6ffc8;4h2d2b;5h01;6hbdeb2eba9ebf99a6d68ed861e05b6f81;7ha151a17222171aa1' -H 'X-eTrackingID: a3dAU000001bOUEYA2|729748ac-99d9-4173-4478-2967ef4569c5' -H 'X-Forwarded-For: 34.22.191.121' -H 'X-Forwarded-Port: 443' -H 'X-Forwarded-Proto: https' -H 'X-iTrackingID: rrt-013394c6616b8bd0f-b-de-1263734-14108487-3' -H 'X-OP-numberOfResults: ' -H 'X-originalApplication: Salesforce' -H 'X-process: CheckoutVirtualCart' -H 'X-timeout: 20000' -H 'X-user: Salesforce' -d '{"price":false,"cartId":"801AU00000ZSPNcYAP","methodName":"getCartsItems","fields":"vlocity_cmt__ConnectDate__c,NOS_t_MacAddress__c,NOS_t_MtaMacAddress__c,vlocity_cmt__ServiceIdentifier__c,vlocity_cmt__SerialNumber__c","validate":false}' 'https://nos--nosqms.sandbox.my.salesforce.com/services/apexrest/vlocity_cmt/v2/cpq/carts/801AU00000ZSPNcYAP/items?fields=vlocity_cmt__ConnectDate__c%2CNOS_t_MacAddress__c%2CNOS_t_MtaMacAddress__c%2Cvlocity_cmt__ServiceIdentifier__c%2Cvlocity_cmt__SerialNumber__c&validate=false&price=false&reduced=true'

#{"cartId":"801AU00000e3eZvYAI","methodName":"getCartsItems","price":false,"validate":false,"fields":"vlocity_cmt__ConnectDate__c,NOS_t_MacAddress__c,NOS_t_MtaMacAddress__c,vlocity_cmt__ServiceIdentifier__c,vlocity_cmt__SerialNumber__c"}

    def test_getCartsItems_reduced(self):
      #restClient.init('NOSDEV')
      #cartId = '801AU00000XZuYZYA1'
      #cartId = '801AU00000X8kcBYAR'
      restClient.init('NOSQSM')
      cartId = '801AU00000jUIDoYAO'

      fields = "vlocity_cmt__ConnectDate__c,NOS_t_MacAddress__c,NOS_t_MtaMacAddress__c,vlocity_cmt__ServiceIdentifier__c,vlocity_cmt__SerialNumber__c"

      res = CPQ.getCartItems_api(cartId,price=False,validate=False,fields=fields,reduced=True)
      #filename2 = restClient.callSave('test_getCartsItemsReduced',logRequest=False,logReply=True)

      #a=1
      a=1



    def test_getCartsItems(self):
     # restClient.init('vinodint')
      restClient.init('NOSQSM')

      cartId = '801AU00000WqVzpYAF'  

      fields = "vlocity_cmt__ConnectDate__c,NOS_t_MacAddress__c,NOS_t_MtaMacAddress__c,vlocity_cmt__ServiceIdentifier__c,vlocity_cmt__SerialNumber__c"

      #for _ in range(1):         
      res = CPQ.getCartItems_api(cartId,price=False,validate=False,fields=fields,pagesize=1)
      filename1 = restClient.callSave('test_getCartsItems1',logRequest=False,logReply=True)

      res = CPQ.getCartItems_api(cartId,price=False,validate=False,fields=fields,pagesize=1,lastRecordId='802AU00000B7isiYAB')
      filename2 = restClient.callSave('test_getCartsItems2',logRequest=False,logReply=True)

      print(restClient.getLastCallAllTimes())

      a=1

    #  'PricebookEntry not found for product : 01t0Q000005TfxWQAS with globalGroupKey 2992f846-f087-3d68-9444-93d45efccea4'

    def test_refresh_cart_page(self):
      restClient.init('mpomigra250')

      data = "{\"cartId\":\"801KM000000Tdn6YAC\",\"fields\":\"vlocity_cmt__BillingAccountId__c,vlocity_cmt__ServiceAccountId__c,Quantity,vlocity_cmt__RecurringTotal__c,vlocity_cmt__OneTimeTotal__c,vlocity_cmt__OneTimeManualDiscount__c,vlocity_cmt__RecurringManualDiscount__c,vlocity_cmt__ProvisioningStatus__c,vlocity_cmt__RecurringCharge__c,vlocity_cmt__OneTimeCharge__c,ListPrice,vlocity_cmt__ParentItemId__c,vlocity_cmt__BillingAccountId__r.Name,vlocity_cmt__ServiceAccountId__r.Name,vlocity_cmt__PremisesId__r.Name,vlocity_cmt__InCartQuantityMap__c,vlocity_cmt__EffectiveQuantity__c\",\"pagesize\":\"10\",\"price\":false,\"priceDetailsFields\":\"vlocity_cmt__OneTimeCharge__c,vlocity_cmt__OneTimeManualDiscount__c,vlocity_cmt__OneTimeCalculatedPrice__c,vlocity_cmt__OneTimeTotal__c,vlocity_cmt__RecurringCharge__c,vlocity_cmt__RecurringCalculatedPrice__c,vlocity_cmt__RecurringTotal__c,vlocity_cmt__OneTimeLoyaltyPrice__c,vlocity_cmt__UsageUnitPrice__c,vlocity_cmt__UsagePriceTotal__c\",\"validate\":false}"
      res = CPQAppHandler.call(method='getCartsItems',data=data)
      print(res)


      data ="{\"cartId\":\"801KM000000Tdn6YAC\",\"validate\":\"false\"}"
      res = CPQAppHandler.call(method='getCarts',data=data)
      print(res)
      print()

      data = "{\"cartId\":\"801KM000000Tdn6YAC\",\"fields\":\"IsActive,Id,Name,UnitPrice,ProductCode,vlocity_cmt__RecurringPrice__c\",\"includeIneligible\":\"true\",\"pagesize\":\"10\",\"offsetSize\":\"0\",\"localeCode\":\"pt_PT\"}"
      res = CPQAppHandler.call(method='getCartsProducts',data=data)
      print(res)
      print()

      data = "{\"cartId\":\"801KM000000Tdn6YAC\",\"includeIneligible\":\"true\",\"includeProducts\":\"true\",\"localeCode\":\"pt_PT\",\"offsetSize\":\"0\",\"pagesize\":\"10\"}"
      res = CPQAppHandler.call(method='getCartsDiscounts',data=data)
      print(res)
      print()

      data = "{\"cartId\":\"801KM000000Tdn6YAC\",\"fields\":\"IsActive,Id,Name,UnitPrice,ProductCode,vlocity_cmt__RecurringPrice__c\",\"includeIneligible\":\"true\",\"localeCode\":\"pt_PT\",\"offsetSize\":\"0\",\"pagesize\":\"10\"}"
      res = CPQAppHandler.call(method='getCartsTargetOffers',data=data)
      print(res)
      print()

      data = "{\"cartId\":\"801KM000000Tdn6YAC\",\"price\":\"false\",\"validate\":\"false\"}"
      res = CPQAppHandler.call(method='getCarts',data=data)
      print(res)
      print()

      data = "{\"cartId\":\"801KM000000Tdn6YAC\",\"includeIneligible\":\"true\",\"pagesize\":\"10\",\"localeCode\":\"pt_PT\"}"
      res = CPQAppHandler.call(method='getCartsPromotions',data=data)
      print(res)
      print()

      data = "{\"cartId\":\"801KM000000Tdn6YAC\"}"
      res = CPQAppHandler.call(method='getPriceLists',data=data)
      print(res)
      print()


      a=1



    def test_getCartsItems_tomas(self):
      restClient.init('NOSPRD')

      cartId = '8017T000003VmC4QAK'  

      res = CPQ.getCartItems_api(cartId,price=True,validate=True,fields='NOS_c_BasePriceRC__c')
      filename = restClient.callSave('test_getCartsItems',logRequest=True,logReply=True)


      a=1

    def test_compare_CPQ_config(self):
      a='vlocity_cmt__CpqConfigurationSetup__c'
      b = 'vlocity_cmt__XOMSetup__c'
      c = 'vlocity_cmt__XOMParameter__c'


      org1 = 'NOSDEV'
      org2 = 'DTI'
      restClient.init(org1)

      res = query.query("select Id,name,vlocity_cmt__SetupValue__c from vlocity_cmt__CpqConfigurationSetup__c")


      restClient.init(org2)
      res2 = query.query("select Id,name,vlocity_cmt__SetupValue__c from vlocity_cmt__CpqConfigurationSetup__c")
      
      for r in res['records']:
        matchh = [rr for rr in res2['records'] if rr['Name'] == r['Name']]
        if len(matchh) == 0:
           print(f"DOES NOT EXIST  in {org1}.  {r['Name']} : {r['vlocity_cmt__SetupValue__c']} in {org2}")
        else:
           if r['vlocity_cmt__SetupValue__c'] != matchh[0]['vlocity_cmt__SetupValue__c']:
              print(f"NOT EQUAL       {org1}  {r['Name']} : {r['vlocity_cmt__SetupValue__c']}   {org2}  {matchh[0]['Name']} : {matchh[0]['vlocity_cmt__SetupValue__c']} ")

      for rr in res2['records']:
        matchh = [r for r in res['records'] if r['Name'] == rr['Name']]
        if len(matchh) == 0:
           print(f"DOES NOT EXIST  in {org2}.  {rr['Name']} : {rr['vlocity_cmt__SetupValue__c']} in {org1}")

    def test_compare_XOM_config(self):
      a='vlocity_cmt__CpqConfigurationSetup__c'
      b = 'vlocity_cmt__XOMSetup__c'
      c = 'vlocity_cmt__XOMParameter__c'


      org1 = 'DEVNOSCAT3'
      org2 = 'NOSQSM'
      restClient.init(org1)

      res = query.query("select Id,name,vlocity_cmt__Value__c from vlocity_cmt__XOMSetup__c")



      restClient.init(org2)
      res2 = query.query("select Id,name,vlocity_cmt__Value__c from vlocity_cmt__XOMSetup__c")
      
      for r in res['records']:
        matchh = [rr for rr in res2['records'] if rr['Name'] == r['Name']]
        if len(matchh) == 0:
           print(f"DOES NOT EXIST  {org1}  {r['Name']} in {org2}")
        else:
           if r['vlocity_cmt__Value__c'] != matchh[0]['vlocity_cmt__Value__c']:
              print(f"NOT EQUAL  {org1}  {r['Name']} : {r['vlocity_cmt__Value__c']}   {org2}  {matchh[0]['Name']} : {matchh[0]['vlocity_cmt__Value__c']} ")

      for rr in res2['records']:
        matchh = [r for r in res['records'] if r['Name'] == rr['Name']]
        if len(matchh) == 0:
           print(f"DOES NOT EXIST  {org2}  {rr['Name']} : {rr['vlocity_cmt__Value__c']} in {org1}")

    def test_compare_object(self):
      org1 = 'DEVNOSCAT3'
      org2 = 'NOSQSM'   

      q = F"select fields(all) from vlocity_cmt__PricingVariable__c limit 200"

      restClient.init(org1)
      res1 =  query.query(q)

      restClient.init(org2)
      res2 =  query.query(q)

      for r in res1['records']:
        matchh = [rr for rr in res2['records'] if rr['Name'] == r['Name']]
        if len(matchh) == 0:
           print(f"DOES NOT EXIST  {org1}  {r['Name']} in {org2}")
        else:
           if r['vlocity_cmt__Code__c'] != matchh[0]['vlocity_cmt__Code__c']:
              print(f"NOT EQUAL  {org1}  {r['Name']} : {r['vlocity_cmt__Code__c']}   {org2}  {matchh[0]['Name']} : {matchh[0]['vlocity_cmt__Code__c']} ")

      for rr in res2['records']:
        matchh = [r for r in res1['records'] if r['Name'] == rr['Name']]
        if len(matchh) == 0:
           print(f"DOES NOT EXIST  {org2}  {rr['Name']} : {rr['vlocity_cmt__Code__c']} in {org1}")
    
    def test_orderSubmit(self):
        restClient.init('NOSDEV')
       
        input = {
            'orderIds':['801AU00000LOWNgYAP']
        }
        rres = DR_IP.remoteClass('OrderSubmit','decomposeAndQueueOrchestration',input)

        a=1

#"8013O00000545WYQAY", "8013O00000545WZQAY", "8013O00000545WaQAI"

# this one plan remaining 8013O00000546JVQAY
# this one decomposition and plan remaining 8013O00000546JWQAY

        #EXIST(iChangeDeleteCartItems_RemAct:messages:severity, "ERROR")

    def test_orderSubmit_Plan(self):
        restClient.init('NOSDEV')
       
        input = {
            'orderIds':['801AU00000LKmfXYAT']
        }

        rres = DR_IP.remoteClass('OrderSubmit','createOrchestrationPlan',input)

       # for i in range(1,100):       
       #   rres = DR_IP.remoteClass('OrderSubmit','createOrchestrationPlan',input)
       #   time.sleep(100)


        a=1


    def test_update_DR_originalVal(self):
        restClient.init('qmscopy')
       
        res1 = query.query('select id,vlocity_cmt__SourceProductId__c,SourceIdOriginalVal__c  from vlocity_cmt__DecompositionRelationship__c ')

        


       # for i in range(1,100):       
       #   rres = DR_IP.remoteClass('OrderSubmit','createOrchestrationPlan',input)
       #   time.sleep(100)


        a=1
    def test_applyAdjustment(self):
        restClient.init('NOSDEV')

        res = CPQ.applyAdjustmentPercentage('801AU00000pU98lYAC','802AU00000JS1UVYA1',value=7)

        a=1



