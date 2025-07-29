import unittest
#from InCli import InCli
from incli.sfapi import account,restClient,CPQ,query,jsonFile,Sobjects
import simplejson
from deepdiff import DeepDiff


class Test_Metadata(unittest.TestCase):
    def compare_objects(self,obj1, obj2, path=""):
        differences = []

        if obj1 == obj2:
            return differences

        if isinstance(obj1, dict) and isinstance(obj2, dict):
            for key in obj1:
                new_path = f"{path}.{key}" if path else str(key)
                if key not in obj2:
                    differences.append(f"Missing key {new_path} in second object.")
                    print(f"Missing key <{new_path}> in second object.")
                else:
                    differences.extend(self.compare_objects(obj1[key], obj2[key], new_path))
            for key in obj2:
                if key not in obj1:
                    new_path = f"{path}.{key}" if path else str(key)
                    differences.append(f"Extra key {new_path} in second object.")
                    print(f"Extra key <{new_path}> in second object.")
            return differences

        if isinstance(obj1, list) and isinstance(obj2, list):
            identifiers = ['attributeuniquecode__c','categorycode__c','Code__c','code','displayText','label','defaultValue']
            identifier = None
            for ident in identifiers:
                if ident in obj1[0]:
                    identifier = ident
                    break

        #    print(identifier)
            if identifier == None:
                print(obj1)

            #identifier = 'categorycode__c' if 'categorycode__c' in obj1[0] else 'displayText'
            obj1_dict = {item[identifier]: item for item in obj1}
            obj2_dict = {item[identifier]: item for item in obj2}
            
            # Compare the two dictionaries
            return self.compare_objects(obj1_dict, obj2_dict, path)

        if isinstance(obj1, tuple) and isinstance(obj2, tuple):
            if len(obj1) != len(obj2):
                differences.append(f"Different lengths at {path}: {len(obj1)} vs {len(obj2)}")
            else:
                for i, (item1, item2) in enumerate(zip(obj1, obj2)):
                    new_path = f"{path}[{i}]"
                    differences.extend(self.compare_objects(item1, item2, new_path))
            return differences

        if hasattr(obj1, '__dict__') and hasattr(obj2, '__dict__'):
            return self.compare_objects(obj1.__dict__, obj2.__dict__, path)

        field = path.split('.')[-1]
        if field not in ['id','objectid__c','attributeid__c','attributecategoryid__c','attributeId']:
            print(f"Value mismatch at {path}: {obj1} vs {obj2}")
            differences.append(f"Value mismatch at {path}: {obj1} vs {obj2}")
        return differences


    def test_update_meta(self):
        restClient.init('DTI')

        records1 = jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/working.json')

        for rec1 in records1:
            print(rec1['ProductCode'])

            res = query.query(f"select Id from product2 where ProductCode = '{rec1['ProductCode']}'")

            data = {
             #   'vlocity_cmt__AttributeMetadata__c':rec1['vlocity_cmt__AttributeMetadata__c']
                'vlocity_cmt__AttributeMetadata__c':None

            }

            Sobjects.update(res['records'][0]['Id'],data)

            a=1


    def test_compare_antes_despues(self):
        records1 = jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/working.json')
        records2 = jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/despues.json')

        fields = ['vlocity_cmt__JSONAttribute__c','vlocity_cmt__AttributeMetadata__c','vlocity_cmt__AttributeDefaultValues__c']
        for rec1 in records1:
            print(rec1['ProductCode'])
            for rec2 in records2:
                if rec2['ProductCode'] == rec1['ProductCode']:
                    for field in fields:
                        print(field)
                        obj1 = simplejson.loads(rec1[field])
                        obj2 = simplejson.loads(rec2[field])
                        self.compare_objects(obj1, obj2)
                        print('-----')

        a=1

    def test_compare_files(self):
        obj1 = jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/xxx.json')
        obj2 = jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/xx1.json')


        self.compare_objects(obj1, obj2)
        print('----------------------------------')

    def test_compare_orgs(self):

        product_name = 'Power Router'

        order_id_DEV = '801AU00000TvZslYAF'
        order_id_DTI = '801JW00000PGk25YAD'


        q0 = f"select Id,name,vlocity_cmt__AttributeDefaultValues__c,vlocity_cmt__AttributeMetadata__c,vlocity_cmt__JSONAttribute__c from product2 where name = '{product_name}'"

        q0 = f"""select Id,
                    Product2Id,
                    Product2.name,
                    Product2.vlocity_cmt__AttributeMetadata__c,
                    Product2.vlocity_cmt__AttributeDefaultValues__c,
                    Product2.vlocity_cmt__JSONAttribute__c,
                    vlocity_cmt__AttributeSelectedValues__c,
                    vlocity_cmt__AttributeMetadataChanges__c,
                    Product2.vlocity_cmt__ParentClassId__c,Product2.vlocity_cmt__ParentClassId__r.vlocity_cmt__AttributeDefaultValues__c,
                    Product2.vlocity_cmt__ParentClassId__r.vlocity_cmt__AttributeMetadata__c, 
                    Product2.vlocity_cmt__ParentClassId__r.vlocity_cmt__JSONAttribute__c    
                    from orderitem where OrderId ='{order_id_DEV}'  order by Product2.name"""

       # q1 = f"SELECT ID, ORDERID, ORDER.VLOCITY_CMT__FIRSTVERSIONORDERIDENTIFIER__C, ORDERITEMNUMBER, VLOCITY_CMT__LINENUMBER__C, VLOCITY_CMT__ACTION__C, TOLABEL(VLOCITY_CMT__ACTION__C) VLOCITY_CMT__ACTION__C__TRANSLATED, VLOCITY_CMT__SUBACTION__C, TOLABEL(VLOCITY_CMT__SUBACTION__C) VLOCITY_CMT__SUBACTION__C__TRANSLATED, VLOCITY_CMT__SUPPLEMENTALACTION__C, TOLABEL(VLOCITY_CMT__SUPPLEMENTALACTION__C) VLOCITY_CMT__SUPPLEMENTALACTION__C__TRANSLATED, VLOCITY_CMT__PROVISIONINGSTATUS__C, VLOCITY_CMT__SUPERSEDEDORDERITEMID__C, VLOCITY_CMT__SUPERSEDEDORDERITEMID__R.ORDERID, VLOCITY_CMT__SUPERSEDEDORDERITEMID__R.VLOCITY_CMT__FIRSTVERSIONORDERITEMID__C, VLOCITY_CMT__FIRSTVERSIONORDERITEMID__C, VLOCITY_CMT__FIRSTVERSIONORDERITEMID__R.ORDERID, VLOCITY_CMT__MAINORDERITEMID__C, VLOCITY_CMT__MAINORDERITEMID__R.vlocity_CMT__FIRSTVERSIONORDERITEMID__C, VLOCITY_CMT__ISPONRREACHED__C, VLOCITY_CMT__ISREADYFORACTIVATION__C, VLOCITY_CMT__ISORCHESTRATIONITEMSINFINALSTATE__C, VLOCITY_CMT__ISCHANGESALLOWED__C, PRICEBOOKENTRYID, PRICEBOOKENTRY.PRODUCT2ID, QUANTITY, UNITPRICE, CREATEDDATE, ENDDATE, LASTMODIFIEDDATE, SYSTEMMODSTAMP, SERVICEDATE, VLOCITY_CMT__ASSETREFERENCEID__C, VLOCITY_CMT__BILLINGACCOUNTID__C, VLOCITY_CMT__SERVICEACCOUNTID__C, VLOCITY_CMT__ASSETID__C, VLOCITY_CMT__EXPECTEDCOMPLETIONDATE__C, VLOCITY_CMT__REQUESTEDCHANGE__C, VLOCITY_CMT__REQUESTEDCOMPLETIONDATE__C, VLOCITY_CMT__FULFILMENTSTATUS__C, TOLABEL(vlocity_cmt__FULFILMENTSTATUS__C) vlocity_cmt__FULFILMENTSTATUS__C__TRANSLATED, (SELECT ID,SERIALNUMBER,QUANTITY,vlocity_cmt__ORDERID__C,VLOCITY_CMT__LINENUMBER__C,VLOCITY_CMT__ASSETREFERENCEID__C,vlocity_cmt__PARENTITEMID__C,vlocity_cmt__ROOTITEMID__C,PRODUCT2ID,CONTACTID,ACCOUNTID,STATUS,vlocity_cmt__PROVISIONINGSTATUS__C,vlocity_cmt__BILLINGACCOUNTID__C,vlocity_cmt__SERVICEACCOUNTID__C,PRODUCT2.VLOCITY_CMT__ATTRIBUTEDEFAULTVALUES__C,PRODUCT2.VLOCITY_CMT__ATTRIBUTEMETADATA__C,VLOCITY_CMT__ATTRIBUTEMETADATACHANGES__C,VLOCITY_CMT__ATTRIBUTESELECTEDVALUES__C FROM  vlocity_cmt__ASSETS__R ), PRICEBOOKENTRY.PRODUCT2.VLOCITY_CMT__ATTRIBUTEDEFAULTVALUES__C, PRICEBOOKENTRY.PRODUCT2.VLOCITY_CMT__ATTRIBUTEMETADATA__C, VLOCITY_CMT__ATTRIBUTEMETADATACHANGES__C, VLOCITY_CMT__ATTRIBUTESELECTEDVALUES__C, VLOCITY_CMT__SERVICEIDENTIFIER__C, VLOCITY_CMT__SERIALNUMBER__C FROM OrderItem WHERE  orderid = '{order_id_DEV}' and Product2.name = 'Power Router' order by VLOCITY_CMT__LineNumber__c"

        q=q0
        restClient.init('NOSDEV')
        res1 = query.query(q)

        q = q.replace(order_id_DEV,order_id_DTI)

        restClient.init('DTI')
        res2 = query.query(q)

        fields = ['vlocity_cmt__JSONAttribute__c','vlocity_cmt__AttributeMetadata__c','vlocity_cmt__AttributeDefaultValues__c']
        #fields = ['vlocity_cmt__AttributeSelectedValues__c','vlocity_cmt__AttributeMetadataChanges__c']

        for field in fields:
            print(field + '*******************************************************************')
            for i in range(len(res1['records'])):
                if 1==2:
              #      field = 'vlocity_cmt__JSONAttribute__c'
                    obj1 = simplejson.loads(res1['records'][0][field]) if res1['records'][0][field]!=None else None
                    obj2 = simplejson.loads(res2['records'][0][field]) if res2['records'][0][field]!=None else None
                if 1==2:
                    if res1['records'][i]['Product2']['vlocity_cmt__ParentClassId__c'] == None:
                        continue
                    print(res1['records'][i]['Product2']['Name'])
                   # field = 'vlocity_cmt__AttributeDefaultValues__c'
                    obj1 = simplejson.loads(res1['records'][i]['Product2']['vlocity_cmt__ParentClassId__r'][field])
                    obj2 = simplejson.loads(res2['records'][i]['Product2']['vlocity_cmt__ParentClassId__r'][field])       
                if 1==1:
                   # field = 'vlocity_cmt__JSONAttribute__c'
                    obj1 = simplejson.loads(res1['records'][i]['Product2'][field])
                    obj2 = simplejson.loads(res2['records'][i]['Product2'][field])           

                file1 = jsonFile.write('obj1',obj1)
                file2 = jsonFile.write('obj2',obj2)


                def compare_func(x, y, level=None):
                    try:
                        identifiers = ['attributeuniquecode__c','categorycode__c','Code__c','code','displayText','label','defaultValue']
                        identifier = None
                        for ident in identifiers:
                            if ident in obj1[0]:
                                identifier = ident
                                break
                        if identifier == None:
                            a=1
                        return x[identifier] == y[identifier]
                    except Exception:
                        raise CannotCompare() from None
                    
               # ddiff = DeepDiff(obj1, obj2, ignore_order=True,iterable_compare_func=compare_func)
               # print(ddiff)
               # self.print_difference(obj1,obj2)

                self.compare_objects(obj1, obj2)
                print('----------------------------------')

                if 1==2:
                    for diff in self.compare_objects(obj1, obj2):
                        print(diff)
                        print()

        a=1

    def test_profile_object_field(self):
        restClient.init('NOSDEV')

        name = 'Onboarding Community Login User'
        name = 'Onboarding Community Partner'

        res1 = query.query(f"SELECT Parent.Profile.Name, Parent.Label, Parent.IsOwnedByProfile, SobjectType, Field, PermissionsEdit, PermissionsRead  FROM FieldPermissions where Parent.Profile.name = '{name}' ORDER BY Parent.Profile.Name, Parent.Label, SobjectType, Field")        

        dr1 = {}
        for r in res1['records']:
            dr1[r['Field']] = r

        restClient.init('DEVNOSCAT2')

        name = 'Onboarding Community Partner'
        res2 = query.query(f"SELECT Parent.Profile.Name, Parent.Label, Parent.IsOwnedByProfile, SobjectType, Field, PermissionsEdit, PermissionsRead  FROM FieldPermissions where Parent.Profile.name = '{name}' ORDER BY Parent.Profile.Name, Parent.Label, SobjectType, Field")   

        dr2 = {}
        for r in res2['records']:
            dr2[r['Field']] = r

        for a1 in dr1.keys():
            if a1 not in dr2.keys():
                print(f"{a1} not in Partner")
                continue
            if dr1[a1]['PermissionsEdit'] != dr2[a1]['PermissionsEdit']:
                print(f"{a1} cannot edit  Partner")
            if dr1[a1]['PermissionsRead'] != dr2[a1]['PermissionsRead']:
                print(f"{a1} cannot read  Partner")

        for a2 in dr2.keys():
            if a1 not in dr1.keys():
                print(f"{a2} not in User")

        print()


    def get_sobject_permissions(self,sobjectName):
        res1 = query.query(f"SELECT Id,SObjectType,PermissionsRead,PermissionsCreate,PermissionsEdit,PermissionsModifyAllRecords, PermissionsViewAllRecords,PermissionsDelete FROM ObjectPermissions where parentid in (select id from permissionset where PermissionSet.Profile.Name='{sobjectName}') ")
        
        dr1 = {}
        for r in res1['records']:
            dr1[r['SobjectType']] = r  

        return dr1

    def test_profile_object(self):
        restClient.init('NOSDEV')

        dr1 = self.get_sobject_permissions('Onboarding Community Login User')
        dr2 = self.get_sobject_permissions('Onboarding Community Partner')


        for a1 in dr1.keys():
            if a1 not in dr2.keys():
                print(f"*** {a1} not in Partner")
                continue
            for permission in ['PermissionsCreate','PermissionsRead','PermissionsEdit','PermissionsDelete','PermissionsModifyAllRecords','PermissionsViewAllRecords']:
                if dr1[a1][permission] != dr2[a1][permission]:
                    print(f"{permission} for {a1} is different {dr1[a1][permission]}  {dr2[a1][permission]}  {dr2[a1]['Id']}")


        for a2 in dr2.keys():
            if a1 not in dr1.keys():
                print(f"{a2} not in User")
        a=1
    def print_difference(self,obj1,obj2):

        def compare_func(x, y, level=None):
            try:
                identifiers = ['attributeuniquecode__c','categorycode__c','Code__c','code','displayText','label','defaultValue']
                identifier = None
                for ident in identifiers:
                    if ident in obj1[0]:
                        identifier = ident
                        break
                if identifier == None:
                    a=1
                return x[identifier] == y[identifier]
            except Exception:
                raise CannotCompare() from None
        ddiff = DeepDiff(obj1, obj2, ignore_order=True,iterable_compare_func=compare_func)
        #print (ddiff)
        print("------------------------------")
        print(ddiff)
        print("")

        d = {}

        if 'type_changes' in ddiff:
            print("type_changes")
            d['type_changes'] = []
            for key in ddiff['type_changes']:
                tc = {}
                tc['path'] = key
                tc['old_type'] = str(ddiff['type_changes'][key]['old_type'])
                tc['new_type'] = str(ddiff['type_changes'][key]['new_type'])
                tc['old_value'] = ddiff['type_changes'][key]['old_value']
                tc['new_value'] = ddiff['type_changes'][key]['new_value']

                d['type_changes'].append(tc)

                print(f"{str(tc['path']):50} {str(tc['old_type']):20} {str(tc['new_type']):20} {str(tc['old_value']):20} {str(tc['new_value']):20}")

        print("")

        if 'dictionary_item_removed' in ddiff:
            print("dictionary_item_removed")
            d['dictionary_item_removed'] = []
            for key in ddiff['dictionary_item_removed']:
                item = {}
                item['path'] = key
                item['item']=self._getItem_at_path(obj1,item['path'])

                d['dictionary_item_removed'].append(item)

                #for p in item['path'].split('[')

                #print(item['path'][4:])
                #print(a1[f"{item['path'][4:]}"])



        if 'dictionary_item_added' in ddiff:
            print("dictionary_item_added")
            d['dictionary_item_added'] = []
            for key in ddiff['dictionary_item_added']:
                item = {}
                item['path'] = key
                d['dictionary_item_added'].append(item)
                
                print(item['path'])

        print("")    

        #print(ddiff['values_changed'])
        if 'values_changed' in ddiff:
            d['values_changed'] = []
            print("values_changed")
            for key in ddiff['values_changed']:
                vc = {}
                vc['path'] = key
                vc['new_value'] = ddiff['values_changed'][key]['new_value']
                vc['old_value'] = ddiff['values_changed'][key]['old_value']
                d['values_changed'].append(vc)

                print(f"  {str(vc['path']):80} {str(vc['old_value']):30} {str(vc['new_value']):30}")


        print("")

        if 'iterable_item_removed' in ddiff:
            print("iterable_item_removed")
            d['iterable_item_removed'] = []
            for key in ddiff['iterable_item_removed']:
                item={}
                item['path'] = key
                item['item'] = ddiff['iterable_item_removed'][key]
                d['iterable_item_removed'].append(item)
                print(f'  {str(item["path"]):80} ')

        if 'iterable_item_added' in ddiff:
            print("iterable_item_added")
            d['iterable_item_added'] = []
            for key in ddiff['iterable_item_added']:
                item={}
                item['path'] = key
                item['item'] = ddiff['iterable_item_added'][key]
                d['iterable_item_added'].append(item)
                print(f'  {str(item["path"]):80} ')
                

            #print(ddiff['iterable_item_added'])
        #jsonFile.write('dodo/difference',dj)

        #print(d)
        return d

    def _getItem_at_path(self,a,path):
        print(path)
        t = path[4:]
        print(t)
        t1 = t.split("]")
        print( t1)
        _a = a
        for x in t1:
            x1 = x.split('[')
            print(x1)
            if len(x1)>1:
                key = x1[1]
                if "'" in key:
                    key = key.replace("'","")
                else:
                    key = int(key)
                print(key)
                _a = _a[key]
                print(_a)
        return _a