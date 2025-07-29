import unittest,simplejson,sys,traceback
from incli.sfapi import restClient,query,Sobjects,utils,jsonFile
from collections import Counter

class Test_Order_stats(unittest.TestCase):
    dec_num = 0
    orderId = '801cy000004wkrQAAQ'
    print_toFile = True

    def test_order_to_file(self):

        try:
            self.orderId = '801AU00000ljPSJYA2'
            text=''
            org = 'NOSDEV'

            self.orderId = '801AP00000lcQ6WYAU'
            org='qmscopy'

            filename = f'Decomposition_order_{org}_{self.orderId}_{text}_2.txt'
            original_stdout = sys.stdout
            
           # restClient.init('qmscopy')
            restClient.init(org)

            if self.print_toFile:
                with open(filename, 'w') as f:
                    sys.stdout = f 
                    self.test_order()
                    sys.stdout = original_stdout 
            else:
                self.test_order()

        except Exception as e:
            sys.stdout = original_stdout 
            print(traceback.format_exc())

            print(e)

    def get_order_items(self,orderId):
        q = f"select fields(all),Product2.vlocity_cmt__ParentClassId__c from orderitem where OrderId='{orderId}' limit 200"
        order_items = query.query(q)  
        return   order_items

    def get_products_for_order_items(self,order_items):
        product2Ids = [order_item['Product2Id'] for order_item in order_items['records'] ]
        return self.get_products_by_ids(product2Ids)

    def get_products_by_ids(self,product2Ids):
        product2Ids_str = query.IN_clause(product2Ids)
        qp = f"select fields(all) from product2 where Id in ({product2Ids_str})"
        product2s = query.query(qp)
        return product2s
    
    def get_product_by_id(self,productId):
        return self.get_products_by_ids([productId])['records'][0]

    
    def get_fulfilment_requests(self,orderId):
        q2= f"select Id,Name,vlocity_cmt__Status__c,vlocity_cmt__orchestrationPlanId__c from vlocity_cmt__FulfilmentRequest__c where vlocity_cmt__OrderId__c = '{self.orderId}' "
        frs = query.query(q2)
        return frs
    
    def get_frls_for_frs(self,frs):
        if len(frs['records']) == 0:
            print('NO FRLs')
            return
        fr_ids = [r['Id'] for r in frs['records']]
        fr_ids_str = query.IN_clause(fr_ids)

        q3= f"select Id,Name,vlocity_cmt__Product2Id__c,vlocity_cmt__FulfilmentRequestID__c,vlocity_cmt__AttributesMarkupData__c,vlocity_cmt__Action__c,vlocity_cmt__JSONAttribute__c from vlocity_cmt__FulfilmentRequestLine__c where vlocity_cmt__FulfilmentRequestID__c in ({fr_ids_str}) "
        frls = query.query(q3)

        return frls

    def get_product2_for_frls(self,frls):
        if frls==None or len(frls['records']) == 0:
            print('NO FRLs')
            return
        rfl_product2_ids = [r['vlocity_cmt__Product2Id__c'] for r in frls['records']]
        rfl_product2_ids_str = query.IN_clause(rfl_product2_ids)
        rfl_products_q = f"select Id,Name,ProductCode from product2 where Id in ({rfl_product2_ids_str})"
        rfl_products = query.query(rfl_products_q)
        return rfl_products

    def get_decomposition_destinationProducts(self,orderId):
        def add_to_destProdId_2_JSON(res):
            for r in res['records']:
                if r['vlocity_cmt__DestinationProductId__c'] not in destProdId_2_JSON:
                    destProdId_2_JSON[r['vlocity_cmt__DestinationProductId__c']] = r['vlocity_cmt__DestinationProductId__r']['vlocity_cmt__JSONAttribute__c']       

        def add_to_sourceProdId_2_decompRelRecord(res):
            for r in res['records']:
                if sourceProdId_2_decompRelRecord.get(r['vlocity_cmt__SourceProductId__c']) != None:
                    sourceProdId_2_decompRelRecord[r['vlocity_cmt__SourceProductId__c']].append(r)
                else:
                    sourceProdId_2_decompRelRecord[r['vlocity_cmt__SourceProductId__c']] = [r]

        def add_to_parentClassId_2_decompRelRecord(res):
            parentClassId = []
            for r in res['records']:
                a = r['vlocity_cmt__SourceProductId__r']['vlocity_cmt__ParentClassId__c'] 
                if a == None: continue
                if a not in parentClassId: parentClassId.append(a)
            if len(parentClassId) == 0: return
            res1 = query.query(f"{q_fields} where vlocity_cmt__SourceProductId__c in ({query.IN_clause(parentClassId)})")
            for r in res1['records']:
                if parentClassId_2_decompRelRecord.get(r['vlocity_cmt__SourceProductId__c']) != None:
                    parentClassId_2_decompRelRecord[r['vlocity_cmt__SourceProductId__c']].append(r)
                else:
                    parentClassId_2_decompRelRecord[r['vlocity_cmt__SourceProductId__c']] = [r]

        def add_to_parentClassId_2_decompRelRecord2(parentClassIds):

            res1 = query.query(f"{q_fields} where vlocity_cmt__SourceProductId__c in ({query.IN_clause(parentClassIds)})")
            for r in res1['records']:
                if parentClassId_2_decompRelRecord.get(r['vlocity_cmt__SourceProductId__c']) != None:
                    parentClassId_2_decompRelRecord[r['vlocity_cmt__SourceProductId__c']].append(r)
                else:
                    parentClassId_2_decompRelRecord[r['vlocity_cmt__SourceProductId__c']] = [r]

        destProdId_2_JSON = {}
        sourceProdId_2_decompRelRecord = {}
        parentClassId_2_decompRelRecord = {}
        q_fields = 'select Id,Name,vlocity_cmt__ConditionData__c,vlocity_cmt__DestinationProductId__r.vlocity_cmt__JSONAttribute__c,vlocity_cmt__MappingsData__c,vlocity_cmt__DestinationProductId__c,vlocity_cmt__DestinationProductId__r.ProductCode,vlocity_cmt__DestinationProductId__r.Name,vlocity_cmt__SourceProductId__c,vlocity_cmt__SourceProductId__r.ProductCode,vlocity_cmt__SourceProductId__r.Name,vlocity_cmt__SourceProductId__r.vlocity_cmt__ParentClassId__c from vlocity_cmt__DecompositionRelationship__c'

        res0 = query.query(f"select vlocity_cmt__ParentClassId__c from product2 where Id in (select Product2Id from orderitem where OrderId = '{orderId}') and vlocity_cmt__ParentClassId__c != null group by vlocity_cmt__ParentClassId__c")

        parentClassIds = [r['vlocity_cmt__ParentClassId__c'] for r in res0['records']]
        add_to_parentClassId_2_decompRelRecord2(parentClassIds)

        aa= parentClassId_2_decompRelRecord.values()
        destProdIds_c = {r['vlocity_cmt__DestinationProductId__c'] for group in parentClassId_2_decompRelRecord.values() for r in group}
        class_destProdIds = list(destProdIds_c)

        res0 = query.query(f"select Product2Id from orderitem where OrderId = '{orderId}'")
        destProdIds = [r['Product2Id'] for r in res0['records']]

        destProdIds.extend(class_destProdIds)

        res1 = query.query(f"{q_fields} where vlocity_cmt__SourceProductId__c in ({query.IN_clause(destProdIds)}) ")
        destination_ids1 = [r['vlocity_cmt__DestinationProductId__c'] for r in res1['records']]
        add_to_parentClassId_2_decompRelRecord(res1)
        add_to_destProdId_2_JSON(res1)
        add_to_sourceProdId_2_decompRelRecord(res1)

        print(f"First level decompositions: {sum(len(value) for value in sourceProdId_2_decompRelRecord.values())}")
        print(f"First level class decompositions: {sum(len(value) for value in parentClassId_2_decompRelRecord.values())}")
        print(f"First level destination products: {len(destProdId_2_JSON)}")

        res2 = query.query(f"{q_fields} where vlocity_cmt__SourceProductId__c in ({query.IN_clause(destination_ids1)})")
        destination_ids2 = [r['vlocity_cmt__DestinationProductId__c'] for r in res2['records']]
        add_to_parentClassId_2_decompRelRecord(res2)
        add_to_destProdId_2_JSON(res2)
        add_to_sourceProdId_2_decompRelRecord(res2)

        print(f"Second level decompositions: {sum(len(value) for value in sourceProdId_2_decompRelRecord.values())}")
        print(f"Second level class decompositions: {sum(len(value) for value in parentClassId_2_decompRelRecord.values())}")
        print(f"Second level destination products: {len(destProdId_2_JSON)}")

        res3 = query.query(f"{q_fields} where vlocity_cmt__SourceProductId__c in ({query.IN_clause(destination_ids2)})")
        add_to_parentClassId_2_decompRelRecord(res3)
        add_to_destProdId_2_JSON(res3)
        add_to_sourceProdId_2_decompRelRecord(res3)

        print(f"Third level decompositions: {sum(len(value) for value in sourceProdId_2_decompRelRecord.values())}")
        print(f"Third level class decompositions: {sum(len(value) for value in parentClassId_2_decompRelRecord.values())}")
        print(f"Third level destination products: {len(destProdId_2_JSON)}")
        print()
        a=1

        for key in parentClassId_2_decompRelRecord.keys():
            sourceProdId_2_decompRelRecord[key] = parentClassId_2_decompRelRecord[key]

        return destProdId_2_JSON,sourceProdId_2_decompRelRecord,parentClassId_2_decompRelRecord

    
    def get_product_decomposition(self,product,sourceProdId_2_decompRelRecord,orderItem,order):
        product['decompositions'] = []

        if sourceProdId_2_decompRelRecord.get(product['Id']) == None:
            return
        decomposition_relationships = sourceProdId_2_decompRelRecord[product['Id']]
        for decomposition_relationship in decomposition_relationships:
            mappring_data_str = decomposition_relationship['vlocity_cmt__MappingsData__c']
            mappring_data = simplejson.loads(decomposition_relationship['vlocity_cmt__MappingsData__c']) if mappring_data_str != None else None

            mappings =[]
            if mappring_data != None:
                for mapping in mappring_data:
                    self.parse_decomposition_mapping(mapping,mappings)

            condition_data_str = decomposition_relationship['vlocity_cmt__ConditionData__c']
            condition_data = simplejson.loads(condition_data_str) if condition_data_str!=None else None

            if decomposition_relationship['Id'] == 'a2P7a0000017JOCEA2':
                a=1

            condition_str,len_conditions,evaluation,evaluation_str = self.parse_conditions(condition_data,product,orderItem,order)

            decomposition = {
                'Id':decomposition_relationship['Id'],
                'conditions' :len_conditions,
                'conditions_str':condition_str,
                'mapping_rules':len(mappring_data) if mappring_data != None else 0,
                'Name':decomposition_relationship['Name'],
                'destination_Id':decomposition_relationship['vlocity_cmt__DestinationProductId__c'],
                'destination_code':decomposition_relationship['vlocity_cmt__DestinationProductId__r']['ProductCode'],
                'destination_name':decomposition_relationship['vlocity_cmt__DestinationProductId__r']['Name'],
                'source_Id':decomposition_relationship['vlocity_cmt__SourceProductId__c'],
                'source_code':decomposition_relationship['vlocity_cmt__SourceProductId__r']['ProductCode'],
                'source_name':decomposition_relationship['vlocity_cmt__SourceProductId__r']['Name'],
                'mappings':mappings,
                'evaluation':evaluation,
                'evaluation_str':evaluation_str
            }
            product['decompositions'].append(decomposition)

            if decomposition['destination_Id'] != None:
               # q = f"select fields(all) from vlocity_cmt__DecompositionRelationship__c where vlocity_cmt__SourceProductId__c='{decomposition['destination_Id']}' limit 200"
               # res2 = query.query(q)
                if sourceProdId_2_decompRelRecord.get(decomposition['destination_Id']) != None:
                    res2 = sourceProdId_2_decompRelRecord[decomposition['destination_Id']]
                    if len(res2)>0:
                        level = 2 if 'level' not in product else product['level']+1
                        fake_product = {
                            'Id':decomposition['destination_Id'],
                            'level':level
                        }
                        prod = self.get_product_by_id(decomposition['destination_Id'])

                        self.get_product_decomposition(prod,sourceProdId_2_decompRelRecord,orderItem,order)
                        decomposition['next_level'] = prod['decompositions']
            else:
                a=1


    destination_products_drs = []
    destination_products_frls = []

    all_drs_ids = []
    firing_drs_ids = []

    def test_order(self):

        order = query.query(f"select fields(all) from order where id = '{self.orderId}' limit 1")['records'][0]
        destProdId_2_JSON,sourceProdId_2_decompRelRecord,parentClassId_2_decompRelRecord = self.get_decomposition_destinationProducts(self.orderId)
        order_items = self.get_order_items(self.orderId)

        if len(order_items['records']) == 0:
            utils.raiseException('NO_LINE_ITEM',f"No order line items could be found for order {self.orderId}")

        product2s = self.get_products_for_order_items(order_items)

        
        def print_decom(decom,level=0):
            h = ' ' * (2 * level)

            if decom['Id'] not in self.all_drs_ids:
                self.all_drs_ids.append(decom['Id'])
            if decom['evaluation'] == True:
                if decom['Id'] not in self.firing_drs_ids:
                    self.firing_drs_ids.append(decom['Id'])
            
         #   if decom['evaluation'] == False: return
            #print(f"       Decomposition relationship: {decom['Name']:<80}  {decom['source_Id']}->{decom['destination_Id']}  Conditions:{decom['conditions']}  mappings:{decom['mapping_rules']}")
            print(f"{h}       Decomposition relationship: {decom['Id']} {decom['Name']}")
            print(f"{h}         {decom['source_Id']}  {decom['source_code']}  '{decom['source_name']}' -> {decom['destination_Id']}  {decom['destination_code']}   '{decom['destination_name']}'")
            print(f"{h}         Condition: {decom['conditions_str']}")
            print(f"{h}         Evaluation: {decom['evaluation']}   {decom['evaluation_str']}")

            if decom['evaluation'] == True:
                if decom['destination_code'] not in self.destination_products_drs:
                    self.destination_products_drs.append(decom['destination_code'])
                    print(f"destination_products_drs {len(self.destination_products_drs)}")

            for mapping in decom['mappings']:
                print(f"{h}         Mapping: {mapping['from']}-->{mapping['to']}")
         #   if decom['conditions_str']!=None: print(f"               {decom['conditions_str']}")
            self.dec_num = self.dec_num + 1
            if 'next_level' in decom:
                for dec in decom['next_level']:
                    print_decom(dec,level=level+1)

        for x,order_item in enumerate(order_items['records']):
         #   attr_str = order_item['vlocity_cmt__AttributeSelectedValues__c']
            product = [p2 for p2 in product2s['records'] if p2['Id']==order_item['Product2Id']][0]
            order_item['Product2'] = product
            print(f"- Line {x+1} - Product:{product['Name']}  {product['ProductCode']}  Action:{order_item['vlocity_cmt__Action__c']}")

            prod_attr_str = product['vlocity_cmt__AttributeMetadata__c']

            if prod_attr_str ==  None:
                print(f"***************   vlocity_cmt__AttributeMetadata__c for product {product['ProductCode']} in None")
                continue
            #print(f"prod_attr_str --> {prod_attr_str}")
            attributes = simplejson.loads(prod_attr_str)
            for attribute in attributes['records']:
                for product_attributes  in attribute['productAttributes']['records']:
                    count = len(product_attributes['values']) if 'values' in product_attributes and product_attributes['inputType']=='dropdown' else 1
                    values = [value['value'] for value in product_attributes['values']] if product_attributes['inputType'] == 'dropdown' else []
                    val = ", ".join(values)
                    print(f"       Attribute {product_attributes['code']:<50}: {product_attributes['inputType']:<10} ({count:>2})  {val}   v:{product_attributes['userValues']}")

            if product['ProductCode'] == 'C_NOS_EQUIP_SIM_CARD':
                a=1

            self.get_product_decomposition(product,sourceProdId_2_decompRelRecord,order_item,order)
            selecteValues = simplejson.loads( order_item['vlocity_cmt__AttributeSelectedValues__c'])
            for key in selecteValues.keys():
                print(f"       {key}: {selecteValues[key]}")

            print(f"    Number of Decomposition relationship  {len(product['decompositions'])}")
            for decom in product['decompositions']:
                print_decom(decom)

            if parentClassId_2_decompRelRecord.get(product['vlocity_cmt__ParentClassId__c']) != None:
                print(f"    Number of Class Decomposition relationship  {len(parentClassId_2_decompRelRecord.get(product['vlocity_cmt__ParentClassId__c']))}")

                prod = self.get_product_by_id(product['vlocity_cmt__ParentClassId__c'])
                self.get_product_decomposition(prod,sourceProdId_2_decompRelRecord,order_item,order)
                for decom in prod['decompositions']:
                    print_decom(decom)
            else:
                if product['vlocity_cmt__ParentClassId__c'] != None:
                    prod = self.get_product_by_id(product['vlocity_cmt__ParentClassId__c'])
                    self.get_product_decomposition(prod,sourceProdId_2_decompRelRecord,order_item,order)
                    for decom in prod['decompositions']:
                        print_decom(decom) 
            #print(f"    Number of Class Decomposition relationship  {len(product['decompositions'])}")

           # attr = simplejson.loads(attr_str)
        print()
        print(f"total decomposition relationships {self.dec_num}")
        print()
      #  q2= f"select fields(all) from vlocity_cmt__FulfilmentRequest__c where vlocity_cmt__OrderId__c = '{self.orderId}' limit 200"
        frs = self.get_fulfilment_requests(self.orderId)
        if len(frs['records'])==0:
            print('NO Fulfilment records')
            return

        print()
        print(f"Fulfilment Lines {len(frs['records'])}")

        frls = self.get_frls_for_frs(frs)

        rfl_products = self.get_product2_for_frls(frls)

        frls['records'][0]['vlocity_cmt__Product2Id__c']
        for y,fr in enumerate(frs['records']):
            frl_s = [r for r in frls['records'] if r['vlocity_cmt__FulfilmentRequestID__c']==fr['Id']]
            print(f" - FR: Line {y+1} {fr['Name']}  Status:{fr['vlocity_cmt__Status__c']} ")  

            for z,frl in enumerate(frl_s):
                frl_prod = [r for r in rfl_products['records'] if r['Id']==frl['vlocity_cmt__Product2Id__c']][0]
                mu = simplejson.loads(frl['vlocity_cmt__AttributesMarkupData__c'])
                print(f"   - FRL: {z+1} {frl['Name']}  Product:{frl_prod['Name']}  ProductCode:{frl_prod['ProductCode']}  Action:{frl['vlocity_cmt__Action__c']}")  

                if frl_prod['ProductCode'] not in self.destination_products_frls:
                    self.destination_products_frls.append(frl_prod['ProductCode'])
                    print(f'self.destination_products_frls:   {len(self.destination_products_frls)}')
                if frl['Name'] == 'FRL2961925':
                    a=1
                if frl['vlocity_cmt__JSONAttribute__c'] != None:
                    at_json = frl['vlocity_cmt__JSONAttribute__c']
                else:
                    at_json = destProdId_2_JSON.get(frl['vlocity_cmt__Product2Id__c'])

                if at_json == None:
                    print(f"*************************************************  {frl['vlocity_cmt__Product2Id__c']}")
                    continue
                try:
                    at = simplejson.loads(at_json)
                except Exception as e:
                    a=1

                for at_key in at.keys():
                    print(f"      {at_key} {len(at[at_key])}")  
                    frl_att_as = at[at_key]
                    for frl_att_a in frl_att_as:
                        if 'values' not in frl_att_a['attributeRunTimeInfo']:
                            val = frl_att_a['value__c']
                            count = 1
                        else:
                            count = len(frl_att_a['attributeRunTimeInfo']['values']) if frl_att_a['attributeRunTimeInfo']['dataType'] == 'Picklist' else 1
                            values = [value['value'] for value in frl_att_a['attributeRunTimeInfo']['values']] if frl_att_a['attributeRunTimeInfo']['dataType'] == 'Picklist' else []
                            val = ", ".join(values)

                        print(f"          {frl_att_a['attributeuniquecode__c']:<50}  {frl_att_a['attributeRunTimeInfo']['dataType']:<10}  ({count:>2})     {val}")

        q4 = f"select fields(all) from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c = '{frs['records'][0]['vlocity_cmt__orchestrationPlanId__c']}' limit 200"
        res4 = query.query(q4)
        OrchestrationItemTypes=[]
        for rec4 in res4['records']:
            OrchestrationItemTypes.append(rec4['vlocity_cmt__OrchestrationItemType__c'])

        print()
        print()

        c = Counter(OrchestrationItemTypes)
        print(c)

        self.print_differences(self.destination_products_drs,self.destination_products_frls)
        print()
        print(f'ALL  {len(self.all_drs_ids)}')
        print(self.all_drs_ids)
        print(f'firing {len(self.firing_drs_ids)}')
        print(self.firing_drs_ids)

        not_firing = [item for item in self.all_drs_ids if item not in self.firing_drs_ids]
        print(f'Not Firing  {len(not_firing)}')
        print(not_firing)

    def print_differences(self,list1, list2):
        set1, set2 = set(list1), set(list2)

        only_in_list1 = set1 - set2
        only_in_list2 = set2 - set1

        if only_in_list1:
            print("Only in list1:", only_in_list1)
        if only_in_list2:
            print("Only in list2:", only_in_list2)

        if not only_in_list1 and not only_in_list2:
            print("Both lists have the same elements.")
    def test_objects(self):
        restClient.init('NOSQSM')
        
        res = Sobjects.get_with_only_id('a3m3O000000KCjCQAW')

        print()     
    def test_limits(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0/limits'
        res = restClient.callAPI(action)

        print()

    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)

        print()

    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)
        for key in res.keys():
            print()
            action = res[key]
            res1 = restClient.callAPI(action)
            print(action)
            print(res1)

        print()

    def getAttributes(self,product):
        attr_str = product['vlocity_cmt__AttributeMetadata__c']
        if attr_str == None: return None
        atributes = simplejson.loads(attr_str)

        atts = []
        for atribute in atributes['records']:
            for productAttribute in atribute['productAttributes']['records']:
                if 'values' not in productAttribute:
                    a=1
                if productAttribute['values'] == None:
                    a=1
                att = {
                    'att':atribute['Code__c'],
                    'pAtt':productAttribute['code'],
                    'type':productAttribute['inputType'],
                    'len':len(productAttribute['values']) if 'values' in productAttribute and productAttribute['values'] != None else 0
                }
                atts.append(att)
        return atts



    def test_get_product_childrens(self):
        offer = "C_WOO_MOBILE"
        child_product = ""

        restClient.init('NOSQSM')

        q = f"select vlocity_cmt__ProductId__r.name,vlocity_cmt__ProductId__r.ProductCode,  fields(all)  from vlocity_cmt__Datastore__c  where vlocity_cmt__ProductId__r.ProductCode ='{offer}' limit 200"

        res = query.query(q)

        child_ids = res['records'][0]['vlocity_cmt__Value__c'].split(',')

        res2 = query.query(f"select fields(all) from vlocity_cmt__ProductChildItem__c where Id in ({query.IN_clause(child_ids)}) limit 200")

        a=1
    def getChildProducts_dataStore(self,product,level=0,allChilds=None):
        children = []
        if allChilds == None:
            datastore = query.queryRecords(f"select fields(all)  from vlocity_cmt__Datastore__c  where vlocity_cmt__ProductId__c ='{product['Id']}' limit 200")
            ids = datastore[0]['vlocity_cmt__Value__c'].split(',')
            allChilds = query.query(f"select fields(all) from vlocity_cmt__ProductChildItem__c where Id in ({query.IN_clause(ids)}) limit 200")


        childItems = [r for r in allChilds['records'] if r['vlocity_cmt__ParentProductId__c'] == product['Id']]
        if len(childItems) == 0:
            return []

        childItems = sorted(childItems, key=lambda x: x["vlocity_cmt__ChildLineNumber__c"])

        prodIds = [r['vlocity_cmt__ChildProductId__c'] for r in childItems if r['vlocity_cmt__ChildProductId__c'] != None]
        if len(prodIds) == 0:
            return []

        prods = query.query(f"select fields(all) from product2 where Id in ({query.IN_clause(prodIds)}) limit 200")

        for childItem in childItems:
            if childItem['vlocity_cmt__ChildProductId__c'] == None:
                continue
         #   prod = Sobjects.getF('Product2',f"Id:{childItem['vlocity_cmt__ChildProductId__c']}")['records'][0]
            prod = [p for p in prods['records'] if p['Id'] == childItem['vlocity_cmt__ChildProductId__c']][0]
            print(f"{prod['Name']: >{level+len(prod['Name'])}}     {childItem['vlocity_cmt__IsOverride__c']}")

            if childItem['vlocity_cmt__IsOverride__c'] == True:
                a=1

            child = {
                'Name':childItem['vlocity_cmt__ChildProductName__c'],
                'virtual':childItem['vlocity_cmt__IsVirtualItem__c'],
                'Id':childItem['vlocity_cmt__ChildProductId__c'],
                'attributes':self.getAttributes(prod),
                'children':self.getChildProducts_dataStore(prod,level=level+1,allChilds=allChilds),
                'mmq':f"({childItem['vlocity_cmt__MinMaxDefaultQty__c']})".replace(' ',''),
                "child_mm":f"[{int(childItem['vlocity_cmt__MinimumChildItemQuantity__c'])},{int(childItem['vlocity_cmt__MaximumChildItemQuantity__c'])}]"
            }
            children.append(child)
        #    print(childItem['vlocity_cmt__ChildProductName__c'])

        return children
    
    def getChildProducts(self,product,level=0):
        children = []
       # childItems = query.queryRecords(f"select fields(all) from vlocity_cmt__ProductChildItem__c where vlocity_cmt__ParentProductId__c='{product['Id']}' and vlocity_cmt__IsOverride__c = False limit 200")
        childItems = query.queryRecords(f"select fields(all) from vlocity_cmt__ProductChildItem__c where vlocity_cmt__ParentProductId__c='{product['Id']}' limit 200")

        if len(childItems) == 0:
            return []

        childItems = sorted(childItems, key=lambda x: x["vlocity_cmt__ChildLineNumber__c"])

        prodIds = [r['vlocity_cmt__ChildProductId__c'] for r in childItems if r['vlocity_cmt__ChildProductId__c'] != None]
        if len(prodIds) == 0:
            return []

        prods = query.query(f"select fields(all) from product2 where Id in ({query.IN_clause(prodIds)}) limit 200")

        for childItem in childItems:
            if childItem['vlocity_cmt__ChildProductId__c'] == None:
                continue
         #   prod = Sobjects.getF('Product2',f"Id:{childItem['vlocity_cmt__ChildProductId__c']}")['records'][0]
            prod = [p for p in prods['records'] if p['Id'] == childItem['vlocity_cmt__ChildProductId__c']][0]
            print(f"{prod['Name']: >{level+len(prod['Name'])}}     {childItem['vlocity_cmt__IsOverride__c']}")

            if childItem['vlocity_cmt__IsOverride__c'] == True:
                a=1

            child = {
                'Name':childItem['vlocity_cmt__ChildProductName__c'],
                'virtual':childItem['vlocity_cmt__IsVirtualItem__c'],
                'Id':childItem['vlocity_cmt__ChildProductId__c'],
                'attributes':self.getAttributes(prod),
                'children':self.getChildProducts(prod,level=level+1),
                'mmq':f"({childItem['vlocity_cmt__MinMaxDefaultQty__c']})".replace(' ',''),
                "child_mm":f"[{int(childItem['vlocity_cmt__MinimumChildItemQuantity__c'])},{int(childItem['vlocity_cmt__MaximumChildItemQuantity__c'])}]"
            }
            children.append(child)
        #    print(childItem['vlocity_cmt__ChildProductName__c'])

        return children

    code = 'PROMO_NOS_OFFER_005'

    def test_parse_product(self):
        restClient.init('NOSDEV')

        prods = Sobjects.getF('Product2',"Name:NOS4s 40Megas Móvel")

        root = {
            'children':[],
            'Name':'root',
            'Id':'NA',
            'attributes':"NA"
        }

        for prod in prods['records']:
            _product = {
                'Name':prod['Name'],
                'virtual':False,
                'Id':prod['Id'],
                'attributes':self.getAttributes(prod),
                'children':self.getChildProducts_dataStore(prod),
                'mmq':"",
                'child_mm':""
            }
            root['children'].append(_product)
        jsonFile.write(f'prod123_{self.code}',root)

        self.printProduct(root)

    def test_parse_promo(self):
        restClient.init('NOSDEV')

        res = Sobjects.getF('Product2',"ProductCode:C_WOO_MOBILE")

        code='PROMO_WOO_FIXED_INTERNET_MOBILE_12_MONTHS_008'
        promo = Sobjects.getF('vlocity_cmt__Promotion__c',f"vlocity_cmt__Code__c:{self.code}")

        promoItems = query.queryRecords(f"select fields(all) from vlocity_cmt__PromotionItem__c where vlocity_cmt__PromotionId__c='{promo['records'][0]['Id']}' limit 200")
        root = {
            'children':[],
            'Name':'root',
            'Id':'NA',
            'attributes':"NA"
        }
        for promoItem in promoItems:
            prods = Sobjects.getF('Product2',f"Id:{promoItem['vlocity_cmt__ProductId__c']}")

            for prod in prods['records']:
                _product = {
                    'Name':prod['Name'],
                    'virtual':False,
                    'Id':prod['Id'],
                    'attributes':self.getAttributes(prod),
                    'children':self.getChildProducts(prod),
                    'mmq':"",
                    'child_mm':""
                }
                root['children'].append(_product)
        jsonFile.write(f'prod123_{self.code}',root)

        self.printProduct(root)

    def test_print_from_file(self):
        root = jsonFile.read(f'prod123_{self.code}')
        self.printProduct(root)

    def parse_conditions(self,condition_data,product,orderItem,order):
        if condition_data == None: 
            return None,0,True,None

        if 'type' not in condition_data:
            condition_data['type'] = 'SIMPLE'
            a=1
        if condition_data['type'] == 'SIMPLE':
            #condition_str = f"({condition_data['left-side']} {condition_data['op']} {condition_data['right-side']})"
            evaluation,condition_str,condition_values = self.evaluate_condition(condition_data,product,orderItem,order)
            return condition_str,1,evaluation,condition_values

        else:
            operation = condition_data['type']
            if 'singleconditions' not in condition_data:
                a=1
            
            results = []
            for sc in condition_data['singleconditions']:
                results.append(self.parse_conditions(sc,product,orderItem,order))
            conditions_strs = [res[0] for res in results]
            condition_str = F"{operation.join(conditions_strs)}"

            evaluations = [res[2] for res in results]
            evaluation = all(evaluations) if operation == "AND" else any(evaluations)

            eval_strs = [res[3] for res in results]
            eval_str = F"{operation.join(eval_strs)}"

            return condition_str,len(results),evaluation,eval_str


    def parse_conditions2(self,condition_data,product,orderItem,order):
        if condition_data == None: 
            return None,0,True

        def parse_single_condition(single_condition_a,op):
            conditions =[]

            for sc in single_condition_a:
                if 'singleconditions' in sc:
                    conditions.append(parse_single_condition(sc['singleconditions'],sc['type']))
                else:
                    condition = f"({sc['left-side']} {sc['op']} {sc['right-side']})"
                    conditions.append(condition)
            _op = f" {op} "
            condition =F"({_op.join(conditions)})"  
            return condition     

        all_conditions=[]
        all_evaluations = []
        if 'singleconditions' not in condition_data:
            if 'op' in condition_data:
                condition = f"({condition_data['left-side']} {condition_data['op']} {condition_data['right-side']})"
                return condition,1,None
            if condition_data.get('type') == 'SIMPLE':
                condition = f"({condition_data['left-side']} == {condition_data['right-side']})"
                return condition,1,None       

        if 'singleconditions' in condition_data:
            for single_conditions in condition_data['singleconditions']:
                if 'singleconditions' in single_conditions:
                    condition = parse_single_condition(single_conditions['singleconditions'],condition_data['type'])
                else:
                    if 'op' not in single_conditions:
                        a=1
                        single_conditions['op'] = 'NO OPERATOR SELECTED'
                    evaluation = self.evaluate_condition(single_conditions,product,orderItem,order)
                    condition = f"({single_conditions['left-side']} {single_conditions['op']} {single_conditions['right-side']})"
                all_conditions.append(condition)
                all_evaluations.append(evaluation)

        if len(all_conditions)==0:
            a=1

        if len(all_conditions)>1:
            op = F" {condition_data['type']} "
            final_condition = F"{op.join(all_conditions)}"
            final_evaluation = F"{op.join(all_conditions)}"

            return final_condition,len(all_conditions),final_evaluation
        else:
            return all_conditions[0],len(all_conditions),all_evaluations[0]

    def evaluate_condition(self,single_conditions,product,orderItem,order):
        leftSide = 'xxxx'
        rightSide = 'xxxx'
        op = 'NO_OPERATION'
        retValue = None

        #print(single_conditions)
        if single_conditions['left-side-type'] == 'field-OrderItem':    
            if 'Product2.' in single_conditions['left-side']:
                leftSide = orderItem['Product2'][single_conditions['left-side'].split('.')[1]]
            if 'vlocity_cmt__Product2Id__r.' in single_conditions['left-side']:
                leftSide = orderItem['Product2'][single_conditions['left-side'].split('.')[1]]
            if 'Order.' in single_conditions['left-side']:
                leftSide = order[single_conditions['left-side'].split('.')[1]]
            if '.' not in single_conditions['left-side']:
                leftSide = orderItem[single_conditions['left-side']]


        if single_conditions['left-side-type'] == 'attribute':    
            selected = simplejson.loads(orderItem['vlocity_cmt__AttributeSelectedValues__c'])
           # print('selected: ')
           # print(selected)
           # print(single_conditions['left-side'])
            if single_conditions['left-side'] not in selected:
                print(f"    ERROR: Attribute {single_conditions['left-side']}  not in {selected}")
                a=1
                leftSide = ''
            else:
                leftSide = selected[single_conditions['left-side']]

        if leftSide == 'xxxx' :
            a=1

        if 'right-side-type' not in single_conditions:
            if 'left-side-datatype' in single_conditions:
                single_conditions['right-side-type'] = single_conditions['left-side-datatype']
                rightSide = single_conditions['right-side']
            else:
                print(f'    ERROR: right-side-type  {single_conditions}')
                rightSide = ''
                retValue = False
        else:
            if single_conditions['right-side-type'] == 'value':    
                rightSide = single_conditions['right-side']

        if 'op' in single_conditions:
            op = single_conditions['op']

        match single_conditions['left-side-datatype'].lower():
            case 'picklist':
                if leftSide == None: leftSide = '' 
            case 'string':
                if leftSide == None: leftSide = ''
            case 'double':
                if leftSide == None:  leftSide = float('0') 
                if rightSide == '': rightSide = '0'
                rightSide = float(rightSide)
            case 'text':
                if leftSide == None: leftSide = '' 
            case 'currency':
                if leftSide == None:  leftSide = float('0') 
                if rightSide == '': rightSide = '0'
                rightSide = float(rightSide)      
            case 'checkbox':
                if rightSide.lower() == 'false': rightSide = False   
                elif rightSide.lower() == 'true':  rightSide = True          
            case 'boolean':
                if rightSide.lower() == 'false': rightSide = False   
                elif rightSide.lower() == 'true':  rightSide = True   
            case _:
                a=1


        condition_fields =  f"({single_conditions['left-side']} {op} {single_conditions['right-side']})"
        condition_values =  f"({leftSide} {op} {rightSide})"

        if leftSide == 'xxxx' or rightSide == 'xxxx' or op == 'NO_OPERATION':
            a=1

        match op:
            case 'contains':
                retValue = False if leftSide == '' else leftSide.find(rightSide)
            case '=':
                retValue = rightSide == leftSide
            case '!=':
                retValue = rightSide != leftSide

       # if op == 'contains':
       #     retValue = False if leftSide == None else leftSide.find(rightSide)
       # if op == '=':
       #     retValue = rightSide == leftSide
       # if op == '!=':
       #     retValue = rightSide != leftSide

        if retValue == None:
            a=1

        return retValue,condition_fields,condition_values
        
        a=1

    def parse_decomposition_mapping(self,mapping,mappings):
        if mapping['mapping_type'] == 'ad-verbatim':
            if mapping['source_type'] == 'Attribute':
                mappings.append({
                    'from':mapping['source_attr_code'],
                    'to':mapping['destination_attr_code']
                })
            elif mapping['source_type'] == 'Field':
                mappings.append({
                    'from':mapping['source_field_name'],
                    'to':mapping['destination_attr_code']
                })
            else:
                a=1
        elif mapping['mapping_type'] == 'static':
            mappings.append({
                'from':'Static',
                'to':mapping['destination_attr_code']
            })

        elif mapping['mapping_type'] == 'list':
            if mapping['source_type'] == 'Attribute':
                mappings.append({
                    'from':mapping['source_attr_code'],
                    'to':mapping['destination_attr_code']
                })
            elif mapping['source_type'] == 'Field':
                mappings.append({
                    'from':mapping['source_field_name'],
                    'to':mapping['destination_attr_code']
                })
            else:
                a=1
        else:
            a=1
 
    def test_decomposition_rules(self):
        restClient.init('NOSDEV')

        root = jsonFile.read(f'prod123_{self.code}')

        def get_decomposition(product):
            self.get_product_decomposition(product)
            for child in product['children']:
                get_decomposition(child)

        for children in root['children']:
            get_decomposition(children)

        jsonFile.write(f'prod123_decomposed_{self.code}',root)
        print()

    def flatten(self,product):
        a=1

    def printProduct(self,products,path=[]):

        filename = f'prod123_decomposed_{self.code}_csv.csv'
        original_stdout = sys.stdout

        with open(filename, 'w') as f:
            sys.stdout = f 

            def printProduct_inner(products,path=[]):
                if products == None:
                    a=1
                for product in products['children']:
                    spath = path.copy()
                    spath.append(f"{product['Name']}{product['mmq']}{product['child_mm']}")

                    self.printAttribute(spath,product['attributes'])
                    self.print_decomposition(spath,product['decompositions'])
                    try:
                        printProduct_inner(product,spath)
                    except Exception as e:
                        print(e)
            printProduct_inner(products)
        sys.stdout = original_stdout 

        print()


    def printAttribute(self,path,attributes):
        spath = path.copy()
        while len(spath)<5:
            spath.append("")

        _path = ";".join(spath)

        if attributes == None:  return

        for atttribute in attributes:
            print(f"{_path};{atttribute['att']}-{atttribute['pAtt']};{atttribute['type']};{atttribute['len']}")

    def print_decomposition(self,path,decompostions):
        spath = path.copy()
        while len(spath)<8:
            spath.append("")

        _path = ";".join(spath)

        if decompostions == None:      return

        def print_next_level(path,next_decompositions,level):
            for next_decomposition in next_decompositions:
                xx = []
                while len(xx)< (3 + (level-1)):
                    xx.append("")
                spaces = ";".join(xx)
                for next_mapping in next_decomposition['mappings']:
                    print(f"{path};{spaces};{next_decomposition['Name']};{next_mapping['from']}->{next_mapping['to']}")
                if 'next_level' in next_decomposition:
                    print_next_level(f"{_path};{decomposition['Name']};{next_decomposition['Name']}",next_decomposition['next_level'],level+1)

        for decomposition in decompostions:
            for mapping in decomposition['mappings']:
                print(f"{_path};{decomposition['Name']};{decomposition['conditions']};{decomposition['mapping_rules']};{mapping['from']}->{mapping['to']}")
            if 'next_level' in decomposition:
                print_next_level(f"{_path};{decomposition['Name']}",decomposition['next_level'],1)

    def test_print_from_file_deco(self):
        root = jsonFile.read(f'prod123_decomposed_{self.code}')
        self.printProduct(root)

#####################################################################
    def printProduct2(self,products,path=[]):

        filename = f'prod123_decomposed2_{self.code}_csv.csv'
        original_stdout = sys.stdout

        with open(filename, 'w') as f:
            sys.stdout = f 

            def printProduct_inner(products,path=[]):
                if products == None:
                    a=1
                for product in products['children']:
                    spath = path.copy()
                    virtual = " VIRTUAL " if product['virtual'] == True else ""
                    spath.append(f"{virtual}{product['Name']}{product['mmq']}{product['child_mm']}")

                    self.printAttribute2(spath,product['attributes'])
                    self.print_decomposition2(spath,product['decompositions'])
                    try:
                        printProduct_inner(product,spath)
                    except Exception as e:
                        print(e)
            printProduct_inner(products)
        sys.stdout = original_stdout 

        print()


    def printAttribute2(self,path,attributes):
        spath = path.copy()
        while len(spath)<5:
            spath.append("")

        _path = ";".join(spath)

        if attributes == None: return
        for atttribute in attributes:
            att = f"{atttribute['att']}-{atttribute['pAtt']}"
            print(f"{_path};AT:  {att};AT:{atttribute['type']} {atttribute['len']}")


    def print_decomposition2(self,path,decompostions):
        spath = path.copy()
        while len(spath)<5:
            spath.append("")

        _path = ";".join(spath)

        if decompostions == None: 
     #       print(f"{_path}")
            return

        def print_next_level(path,next_decompositions,level):
            for next_decomposition in next_decompositions:
                xx = []
                while len(xx)< (3 + (level-1)):
                    xx.append("")
                spaces = ";".join(xx)
                spaces = ''
                for next_mapping in next_decomposition['mappings']:
                    print(f"{path};DE: {next_decomposition['Name']};MAP: {next_mapping['from']}->{next_mapping['to']}")
                if 'next_level' in next_decomposition:
                    print_next_level(f"{_path};DE: {decomposition['Name']};DE: {next_decomposition['Name']}",next_decomposition['next_level'],level+1)

        for decomposition in decompostions:
            for mapping in decomposition['mappings']:
                print(f"{_path};DE: {decomposition['Name']}  C:{decomposition['conditions']};MAP: {mapping['from']}->{mapping['to']}")
            if 'next_level' in decomposition:
                print_next_level(f"{_path};DE: {decomposition['Name']}  C:{decomposition['conditions']}",decomposition['next_level'],1)

    def test_print_from_file_deco2(self):
        root = jsonFile.read(f'prod123_decomposed_{self.code}')
        self.printProduct2(root)


    # select Id,vlocity_cmt__ActionType__c, vlocity_cmt__ProductId__r.name  from vlocity_cmt__PromotionItem__c   where vlocity_cmt__PromotionId__r.name = 'Aditivo 500MB - Oferta 3 mensalidades' limit 200