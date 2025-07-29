import unittest
from incli.sfapi import restClient,CPQ,account,Sobjects,utils,query,jsonFile,debugLogs,cometd
#import traceback
import time
from collections import defaultdict


class Test_Stuff(unittest.TestCase):
  def test_cometD(self):
    restClient.init('NOSDEV')
    cometd.start_connection()

  def test_update_order_items(self):
    restClient.init("qmscopy")

    orderId = '801AP00000iw6LRYAY'

    ois = query.query(f"select id from orderitem where orderid = '{orderId}' and vlocity_cmt__ParentItemId__c=null")
    oiIds = [r['Id'] for r in ois['records']]

    res = query.query(f"SELECT vlocity_cmt__Value__c,vlocity_cmt__ProductId__c FROM vlocity_cmt__Datastore__c WHERE vlocity_cmt__ProductId__c in ({query.IN_clause(oiIds)})")

    for item in res['records']:
      data = {
        'vlocity_cmt__CatalogItemReferenceDateTime__c' : None
      }
      res2 = Sobjects.update(item['Id'],data)

    a=1

  def test_storage(self):
    restClient.init("DEVNOSCAT2")

    res = Sobjects.recordCount('vlocity_cmt__DRBundle__c')

    print()
     
  def test_comparar_v2(self):
    restClient.init("DEVNOSCAT3")

    res = query.query('SELECT fields(all) FROM vlocity_cmt__FulfilmentRequestLine__c WHERE vlocity_cmt__IsMigrated__c = TRUE limit 100')

    restClient.init("DEVNOSCAT2")
    res2 = query.query(f"SELECT fields(all) FROM vlocity_cmt__FulfilmentRequestLine__c WHERE name = '{res['records'][0]['Name']}' limit 100")

    print(len(res['records'][0]['vlocity_cmt__JSONAttribute__c']))
    print(len(res2['records'][0]['vlocity_cmt__JSONAttribute__c']))

    a=1

  def test_comparar_v2_inventory(self):
    restClient.init("DEVNOSCAT3")

    res = query.query('SELECT fields(all) FROM vlocity_cmt__InventoryItem__c WHERE vlocity_cmt__IsMigrated__c = TRUE limit 100')

    restClient.init("DEVNOSCAT2")
    res2 = query.query(f"SELECT fields(all) FROM vlocity_cmt__InventoryItem__c WHERE name = '{res['records'][0]['Name']}' limit 100")

    print(len(res['records'][0]['vlocity_cmt__JSONAttribute__c']))
    print(len(res2['records'][0]['vlocity_cmt__JSONAttribute__c']))

    a=1
  def test_datastore(self):
    restClient.init("mpomigra250")

    res  = query.query(f"select vlocity_cmt__Value__c,")

  def test_Promohierarchy2Product2(self):
    restClient.init("mpomigra250")

    hier = '01tKM000000VI8eYAG<01t2o00000AqmKnAAJ<01t2o00000AqmKqAAJ<01t2o00000AqmKZAAZ<01tKN000000Ly1hYAC<01t7T000002LpnEQAS'


    res0 = query.query(f"select Id,vlocity_cmt__ProductId__r.name,vlocity_cmt__ProductHierarchyPath__c  from vlocity_cmt__PromotionItem__c where vlocity_cmt__PromotionId__r.name = 'P4766 Aluguer Extender Wi-Fi Plume - Desc. Mensal' and vlocity_cmt__OfferId__r.ProductCode = 'C_NOS_OFFER_1691'")

    for record in res0['records']:
      hi = record['vlocity_cmt__ProductHierarchyPath__c']
      his = hi.split('<')
      res = query.query(f"select Id,name from product2 where Id in ({query.IN_clause(his)})")

      nhs = []
      for item in his:
        p_i = [r for r in res['records'] if r['Id'] == item][0]
        nhs.append(p_i['Name'])

      print(nhs)
      a=1

  def test_hierarchy2Product2(self):
    restClient.init("mpomigra250")

    hier = '01tKM000000VI8eYAG<01t2o00000AqmKnAAJ<01t2o00000AqmKqAAJ<01t2o00000AqmKZAAZ<01tKN000000Ly1hYAC<01t7T000002LpnEQAS'

    hiers = hier.split('<')

    res = query.query(f"select Id,Name,productCode from product2 where Id in ({query.IN_clause(hiers)})")
       
    names = []
    codes = []
    for hi in hiers:
      rec = [r for r in res['records'] if r['Id'] == hi][0]
      names.append(rec['Name'])
      codes.append(rec['ProductCode'])

    print(hier)
    print(names)
    print(codes)

  
    a= 1
  def test_get_cardinality(self):

    restClient.init("NOSDEV")

    orderId = '801AU00000XZuYZYA1'
    productCode = 'C_NOS_EQUIP_POD_001'

    res1 = query.query(f"select Id,Product2.ProductCode,vlocity_cmt__ParentItemId__c,vlocity_cmt__RootItemId__c from orderItem where Id = '{orderId}'")

    res2 = query.query(f"select Id,vlocity_cmt__PromotionId__r.name  from vlocity_cmt__OrderAppliedPromotion__c where vlocity_cmt__OrderId__c = '{orderId}' ")

    a=1



  def test_FlexQueue(self):
    restClient.init("NOSPRD")

    while True:
      res = query.query(f"""    SELECT Id, JobType, Status, MethodName, CreatedDate, JobItemsProcessed, TotalJobItems, NumberOfErrors ,ApexClass.name
              FROM AsyncApexJob 
              WHERE Status = 'Holding'
              ORDER BY CreatedDate DESC"""
              )
      if len(res['records'])>0:
        for r in res['records']:
          print(res['records'][0]['ApexClass']['Name'])
        print('')
      time.sleep(1) 
      a=1
      print('')

    
  def test_retrun_promoItems(self):
      restClient.init("NOSQSM")

      orderId = '801AU00000ZpsjmYAB'

      appliedPromotionItemsDefined = query.query(f"""select id,
                                  vlocity_cmt__PromotionId__c,
                                  vlocity_cmt__OfferId__c,
                                  vlocity_cmt__PromotionId__r.name,
                                  vlocity_cmt__ProductId__c,
                                  vlocity_cmt__ProductId__r.name

                         from vlocity_cmt__PromotionItem__c 
                         where vlocity_cmt__PromotionId__c in (select vlocity_cmt__PromotionId__c from vlocity_cmt__OrderAppliedPromotion__c where vlocity_cmt__OrderId__c = '{orderId}') 
                            and vlocity_cmt__ProductId__r.vlocity_cmt__SpecificationType__c = 'Product'""")

      promotionIds = [r['vlocity_cmt__PromotionId__c'] for r in appliedPromotionItemsDefined['records']]
      productIds = [r['vlocity_cmt__ProductId__c'] for r in appliedPromotionItemsDefined['records']]

      ois = query.query(f"select Id,Product2Id from orderitem where OrderId = '{orderId}' and Product2Id in ({query.IN_clause(productIds)})")

      definedPromoItems = []
      for oi in ois['records']:
        for aptd in appliedPromotionItemsDefined['records']:
          if aptd['vlocity_cmt__ProductId__c'] == oi['Product2Id']:
            definedPromoItems.append( {
              'orderItemId':oi['Id'],
              'productId':aptd['vlocity_cmt__ProductId__c'],
              'promotionId':aptd['vlocity_cmt__PromotionId__c']
            })

      appliedPromotionItems = query.query(f"""select Id,
                                  vlocity_cmt__OrderItemId__r.Product2.name, 
                                  vlocity_cmt__OrderItemId__r.Product2Id, 
                                  vlocity_cmt__OrderAppliedPromotionId__r.vlocity_cmt__PromotionId__c,  
                                  vlocity_cmt__OrderAppliedPromotionId__r.vlocity_cmt__PromotionId__r.name 
                         from vlocity_cmt__OrderAppliedPromotionItem__c 
                         where vlocity_cmt__OrderItemId__r.OrderId = '{orderId}' 
                                and vlocity_cmt__OrderAppliedPromotionId__r.vlocity_cmt__PromotionId__c  in ({query.IN_clause(promotionIds)})
                                and vlocity_cmt__OrderItemId__r.Product2.vlocity_cmt__SpecificationType__c = 'Product' """)

      toBeAdded = []
      for dpi in definedPromoItems:
        exists = False
        for api in appliedPromotionItems['records']:
          if (api['vlocity_cmt__OrderItemId__r']['Product2Id'] == dpi['productId']  and api['vlocity_cmt__OrderAppliedPromotionId__r']['vlocity_cmt__PromotionId__c'] == dpi['promotionId'] ):
            exists = True
        if exists == False:
          toBeAdded.append(dpi)

      a=1

  def test_compareItems2(self):
    def get_pc(record):
        pc = record['Product2']['ProductCode'] 
        del record['Product2']['attributes']
        if 'NOS_l_ParentItemId__r' in record and record['NOS_l_ParentItemId__r'] !=None:
            del record['NOS_l_ParentItemId__r']['attributes']
            pc = get_pc(record['NOS_l_ParentItemId__r']) + ':'+pc
        return pc
    
    def get_hierarchy(records):
        for record in records:
            record['pcPath'] = get_pc(record)
    
    def get_orderItemsX(orderId):
        orderitems = query.query(f"select id,CreatedDate,vlocity_cmt__LineNumber__c ,Product2.ProductCode,NOS_l_ParentItemId__r.Product2.ProductCode,NOS_l_ParentItemId__r.NOS_l_ParentItemId__r.Product2.ProductCode,NOS_l_ParentItemId__r.NOS_l_ParentItemId__r.NOS_l_ParentItemId__r.Product2.ProductCode   from orderitem where OrderId = '{orderId}' order by CreatedDate  ")['records']
        get_hierarchy(orderitems)

        grouped_items = defaultdict(list)

        for item in orderitems:
            level = item['vlocity_cmt__LineNumber__c'].count('.') + 1  # Count the number of levels
            grouped_items[level].append(item)
        for level in grouped_items:
            grouped_items[level].sort(key=lambda x: x['vlocity_cmt__LineNumber__c'])

        parent_indices = defaultdict(dict)  # Track indices of parent items at each level

        for level in sorted(grouped_items.keys()):  # Process levels in order
            name_counter = defaultdict(int)  # Track occurrences of names at this level
            
            for item in grouped_items[level]:
                # Assign the index for the current item
                item['index'] = name_counter[item['Product2']['ProductCode']]
                name_counter[item['Product2']['ProductCode']] += 1

                # Derive the parent line number (all but the last segment)
                if '.' in item['vlocity_cmt__LineNumber__c']:
                    parent_line_number = '.'.join(item['vlocity_cmt__LineNumber__c'].split('.')[:-1])
                    parent_index = parent_indices[level - 1].get(parent_line_number, [])
                else:
                    parent_index = []

                # Combine parent indices with the current index to form full_index
                item['full_index'] = parent_index + [item['index']]

                # Store the full_index for potential children
                parent_indices[level][item['vlocity_cmt__LineNumber__c']] = item['full_index']
        return grouped_items
    
    def compute_delta(grouped_items_1, grouped_items_2):
      # Create a set of (name, full_index) for the second grouped_items
      grouped_items_2_set = set(
          (item['Product2']['ProductCode'], tuple(item['full_index'])) 
          for group in grouped_items_2.values() 
          for item in group
      )

      # Prepare the new grouped_items for the delta
      delta_grouped_items = defaultdict(list)

      # Compare items in grouped_items_1 with grouped_items_2
      for level, group in grouped_items_1.items():
          for item in group:
              if (item['Product2']['ProductCode'], tuple(item['full_index'])) not in grouped_items_2_set:
                  # Add item to the delta grouped_items
                  delta_grouped_items[level].append(item)

      return delta_grouped_items
    
    restClient.init("qmscopy")
    orderId1 = '801AU00000eMl4YYAS'
    orderitems1 = get_orderItemsX(orderId1)


    orderId2 = '801AP00000eSHABYA4'
    orderitems2 = get_orderItemsX(orderId2)

    delta = compute_delta(orderitems1,orderitems2)


    a=1




  def test_compareItems(self):

    def get_pc(record):
        pc = record['Product2']['ProductCode'] 
        del record['Product2']['attributes']
        if 'NOS_l_ParentItemId__r' in record and record['NOS_l_ParentItemId__r'] !=None:
            del record['NOS_l_ParentItemId__r']['attributes']
            pc = get_pc(record['NOS_l_ParentItemId__r']) + ':'+pc
        return pc
    def get_hierarchy(records):
        for record in records:
            record['pcPath'] = get_pc(record)
    
    def get_orderItemsX(orderId):
        orderitems = query.query(f"select id,CreatedDate,vlocity_cmt__LineNumber__c ,Product2.ProductCode,NOS_l_ParentItemId__r.Product2.ProductCode,NOS_l_ParentItemId__r.NOS_l_ParentItemId__r.Product2.ProductCode,NOS_l_ParentItemId__r.NOS_l_ParentItemId__r.NOS_l_ParentItemId__r.Product2.ProductCode   from orderitem where OrderId = '{orderId}' order by CreatedDate  ")['records']
        get_hierarchy(orderitems)
        return orderitems
    
    def get_delta_grouped(orderitems1,orderitems2):
      result1 = [item for item in orderitems1 if item['Product2']['ProductCode'] not in {obj['Product2']['ProductCode'] for obj in orderitems2}]
      grouped_items = defaultdict(list)
      for item in result1:
        level = item['vlocity_cmt__LineNumber__c'].count('.') + 1  # Count the number of levels
        grouped_items[level].append(item)

      for level in grouped_items:
        grouped_items[level].sort(key=lambda x: x['vlocity_cmt__LineNumber__c'])
      return grouped_items
    
    restClient.init("qmscopy")

    orderId1 = '801AU00000eMl4YYAS'
    orderId2 = '801AP00000eSHafYAG'

    orderitems1 = get_orderItemsX(orderId1)



    done = False

    while done == False:
      orderitems2 = get_orderItemsX(orderId2)
      items_toAdd = get_delta_grouped(orderitems1,orderitems2)
      if len(items_toAdd) == 0:
        done =True
        continue
      first_level = min(items_toAdd.keys()) 
      for item in items_toAdd[first_level]:
        print(f"  {item['vlocity_cmt__LineNumber__c']} - {item['pcPath']}")


    a=1

  def test_BillingTrio(self):
      restClient.init("qmscopy")

      res = query.query(f"select CPQTriad__c,ProductCode__c,Price__c,PaymentType__c from BillingTriad__c limit 500")

      q = 'select from BillingTriad__c where '
      items =[]
      for r in res['records']:
        item = f"{r['ProductCode__c']}:{r['Price__c']:.5f}:{r['PaymentType__c']}"
        items.append(item)

      res1 = query.query(f"select CPQTriad__c,TM__c, SP__c, SN__c from BillingTriad__c where CPQTriad__c in ({query.IN_clause(items)})")


      a=1

  def test_DR_security(self):
    restClient.init('qmscopy')

    dr_name  ='AccountSearch'
    dr_name  ='CPQ_ExtractAccountIdFromCart'
    dr_name = 'ESMSelfServiceExtractAssetIdsFromOrderMember'
    dr_name = 'AmendFrameContractExtractQuote'
    dr_name = 'CPQGetOrderMembers'

    res = query.query(f" select Id,vlocity_cmt__Type__c,name,vlocity_cmt__DRMapName__c  from  vlocity_cmt__DRBundle__c   where name = '{dr_name}'")

    order = 'vlocity_cmt__DomainObjectCreationOrder__c'
    object = 'vlocity_cmt__InterfaceObjectName__c'
    newNames = {}
    objectFields={}

    for r in res['records']:      
      res2 = query.query(f"   select fields(all) from  vlocity_cmt__DRMapItem__c where name = '{r['Name']}' limit 200")

      for item in res2['records']:
        if item[order] == None:
          item[order] = 0

      grouped = defaultdict(list)
      for item in res2['records']:
          grouped[int(item[order])].append(item)
      grouped = dict(grouped)

      for level in grouped:
        for item in grouped[level]:
          if item[object] != None:
            newNames[item['vlocity_cmt__DomainObjectFieldAPIName__c']] = item[object]
            if item[object] not in objectFields:
              objectFields[item[object]] = [item['vlocity_cmt__InterfaceFieldAPIName__c']]
            else:
               objectFields[item[object]].append(item['vlocity_cmt__InterfaceFieldAPIName__c'])
            a=1

      for level in grouped:
        if level == 0: continue
        for item in grouped[level]:
          if item[object] == None:
             for key in newNames.keys():
                if f"{key}:" in item['vlocity_cmt__InterfaceFieldAPIName__c']:
                  sp = item['vlocity_cmt__InterfaceFieldAPIName__c'].split(':')
                  obj = ":".join(sp[0:-1])
                  field = sp[-1]
                  if field not in objectFields[newNames[obj]]:
                    objectFields[newNames[obj]].append(field)
                  break


         # for key in newNames.keys():
         #   if f"{key}:" in item['vlocity_cmt__DomainObjectFieldAPIName__c']:
         #     item['vlocity_cmt__DomainObjectFieldAPIName__c'] = newNames[key] + '.' + item['vlocity_cmt__DomainObjectFieldAPIName__c'].split('.')[-1]
         #     a=1
      a=1

    a=1