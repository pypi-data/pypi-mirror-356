import unittest
from incli.sfapi import restClient,query,utils,file_csv,DR_IP,jsonFile,tooling,thread
import simplejson
class Test_ProductHierarchy(unittest.TestCase):
    def test_create(self):
        restClient.init('NOSDEV')

        res = query.query("SELECT Id,vlocity_cmt__ParentProductId__c ,         vlocity_cmt__ChildProductId__c  FROM   vlocity_cmt__ProductChildItem__c WHERE vlocity_cmt__IsRootProductChildItem__c = false AND vlocity_cmt__IsOverride__c = false  AND vlocity_cmt__ParentProductId__c != NULL AND vlocity_cmt__ChildProductId__c != NULL ")

        a=1

        hierarchy = {}
        flatenner_hierarchy={}

        for r in res['records']:
            hr = {
                'c':r['vlocity_cmt__ChildProductId__c'],
                'Id':r['Id']
            }
            if r['vlocity_cmt__ParentProductId__c'] in hierarchy:
                hierarchy[r['vlocity_cmt__ParentProductId__c']].append(hr)
            else:
                hierarchy[r['vlocity_cmt__ParentProductId__c']] = [hr]


        all_parents = list(set([r['vlocity_cmt__ParentProductId__c'] for r in res['records'] ]))
        flatened = list(set([r['vlocity_cmt__ChildProductId__c'] for r in res['records'] if r['vlocity_cmt__ChildProductId__c'] not in all_parents ]))





        #  sorted_hierarchy = dict(sorted(hierarchy.items(), key=lambda item: len(item[1])))

        for key in hierarchy.keys():
            items = hierarchy[key]
            for hr in items:
                if hr['c'] in hierarchy:
                    hierarchy[key].extend(hierarchy[hr['c']])
                

      #  print(hierarchy['01t3O00000AZFdbQAH'])
        print(hierarchy['01t3O00000AZFiEQAX'])
      #  print(hierarchy['01t3O00000B0e8uQAB'])
       # print(hierarchy['01t3O00000B0e8sQAB'])

        a=1

    all_parents_records = {}
    def test_create2(self):
        restClient.init('mpomigra')
      #  restClient.init('NOSDEV')

        res = query.query("SELECT Id,vlocity_cmt__ParentProductId__c ,         vlocity_cmt__ChildProductId__c  FROM   vlocity_cmt__ProductChildItem__c WHERE vlocity_cmt__IsRootProductChildItem__c = false AND vlocity_cmt__IsOverride__c = false  AND vlocity_cmt__ParentProductId__c != NULL AND vlocity_cmt__ChildProductId__c != NULL ")


        all_parents = list(set([r['vlocity_cmt__ParentProductId__c'] for r in res['records'] ]))

        for r in res['records']:
            if r['vlocity_cmt__ParentProductId__c'] not in self.all_parents_records:
                self.all_parents_records[r['vlocity_cmt__ParentProductId__c']] = [r]
            else:
                self.all_parents_records[r['vlocity_cmt__ParentProductId__c']].append(r)

            
        hierarchy = {}

        #hs = {}
            

        hl = []
        for parent in all_parents:
            hierarchy[parent] = self.get_siblings(res['records'],parent,hierarchy)
            print(len(hierarchy))

        for parent in all_parents:
            hlr = {
                'Id':parent,
                'h':self.get_hierarchy_s(hierarchy,parent)

            }
            hl.append(hlr)


        if 1==1:
            chunk_size = 1000
            hll= [hl[i:i + chunk_size] for i in range(0, len(hl), chunk_size)]

            for hll_r in hll:
                call = DR_IP.remoteClass('CreateHierarchy','save',input={"data":hll_r})


        if 1==2:

            res2 = query.query(f"select vlocity_cmt__ProductId__c,vlocity_cmt__Value__c from vlocity_cmt__Datastore__c")

            for r2 in res2['records']:
                hl1 = r2['vlocity_cmt__Value__c'].split(',')
                hl2 = self.get_hierarchy_list(hierarchy,r2['vlocity_cmt__ProductId__c'])
                if sorted(hl1) != sorted(hl2):
                    print('Not equal')


        a=1


#select Id,vlocity_cmt__AttributeDisplayName__c,vlocity_cmt__PicklistId__c,vlocity_cmt__AttributeUniqueCode__c,vlocity_cmt__PicklistId__r.vlocity_cmt__Code__c,vlocity_cmt__AttributeId__c, vlocity_cmt__AttributeId__r.vlocity_cmt__PicklistId__c,  vlocity_cmt__IsActive__c, vlocity_cmt__IsActiveAssignment__c      from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__ObjectId__c ='01t2o00000AqmKDAAZ' order by vlocity_cmt__PicklistId__r.vlocity_cmt__Code__c

    def test_getHierarchy_queries(self):
        restClient.init('DEVNOSCAT')

        productId = '01t2o00000AqmKDAAZ'
        productName = 'Descodificador TV HD'
        productCode = 'C_NOS_EQUIP_TV_008'
        objectTypeId = None
        objectTypeIdList = []


        res = query.query(f"select fields(all) from product2 where ProductCode = '{productCode}' limit 1")

        product = res['records'][0]

        objectTypeIdList.append(product['Id'])

       
        if(product['vlocity_cmt__ObjectTypeId__c'] != None):
            objectTypeId = product['vlocity_cmt__ObjectTypeId__c'] 
        
        if(product['vlocity_cmt__ProductSpecId__c'] != None):
            res = query.query(F"SELECT vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c FROM Product2 WHERE Id = '{product['vlocity_cmt__ProductSpecId__c']}' ")
            productSpec = res['records'][0]
            objectTypeIdList.append(productSpec['vlocity_cmt__ObjectTypeId__c'])
            if productSpec['vlocity_cmt__ObjectTypeId__c'] != None:
                objectTypeId = productSpec['vlocity_cmt__ObjectTypeId__c']
        
        rootProductObjectTypeId = query.queryField("select Id,name from vlocity_cmt__ObjectClass__c where name = 'Product2 Object'",'Id')
         
        if(objectTypeId != None):
            objectTypeIdList.append(objectTypeId)
        

        while(objectTypeId != None and objectTypeId != rootProductObjectTypeId):
            objectTypeList = query.query(f"SELECT Id, vlocity_cmt__ParentObjectClassId__c,name FROM vlocity_cmt__ObjectClass__c WHERE Id ='{objectTypeId}'")['records'];

            if(objectTypeList != None and len(objectTypeList) > 0 ):
                objectTypeId = objectTypeList[0]['vlocity_cmt__ParentObjectClassId__c'];
                if(objectTypeId != None and objectTypeId != rootProductObjectTypeId):
                    objectTypeIdList.append(objectTypeId)
        
            else:
                objectTypeId = None

    
        print( objectTypeIdList)

        for id in objectTypeIdList:
            if id.startswith("a3Z") or id.startswith("a3R") : 
                oc = query.query(f"select fields(all) from vlocity_cmt__ObjectClass__c where Id='{id}' limit 1")['records'][0]
                print(f"{id} {oc['Name']}")
            else:   
                oc = query.query(f"select fields(all) from product2 where Id='{id}' limit 1")['records'][0]
                print(f"{id} {oc['ProductCode']}")
                           
            recs = query.query(f"select fields(all) from vlocity_cmt__ObjectFieldAttribute__c where vlocity_cmt__ObjectClassId__c = '{id}' or vlocity_cmt__SubClassId__c='{id}' limit 200")['records']
            if len(recs)>0:
                for rec in recs:
                    attribId = rec['vlocity_cmt__AttributeId__c']
                    if attribId in [None,'']:
                        continue
                    attrib = query.query(f"select fields(all) from vlocity_cmt__Attribute__c where Id='{attribId}' limit 1")['records'][0]
                    
                    print(f"   {attrib['vlocity_cmt__AttributeCategoryName__c']} -- {attrib['Name']}  --  {attrib['vlocity_cmt__PicklistId__c']}")

                    if attrib['vlocity_cmt__PicklistId__c']!= None:
                        picklist = query.query(f"select fields(all) from vlocity_cmt__Picklist__c where Id='{attrib['vlocity_cmt__PicklistId__c']}' limit 1")['records'][0]
                        print(f"        {picklist['Name']}  {picklist['vlocity_cmt__Description__c']}")

                        p_id = picklist['Id']
                        values = query.query(f"select fields(all) from vlocity_cmt__PicklistValue__c where vlocity_cmt__PicklistId__c = '{p_id}' limit 200")['records']
                        for value in values:
                            print(f"               {value['Name']}    {value['vlocity_cmt__Code__c']}")


    def get_siblings(self,records,parentId,hierarchy):
        if parentId in hierarchy:
            return hierarchy[parentId]
        
        childs = []
        if parentId in self.all_parents_records:
            for r in self.all_parents_records[parentId]:
                hr = {
                    'c':r['vlocity_cmt__ChildProductId__c'],
                    'Id':r['Id']
                }
                childs.append(hr)
                sub_child = self.get_siblings(records,r['vlocity_cmt__ChildProductId__c'],hierarchy) 
                if len(sub_child)>0:
                    childs.extend(sub_child)

        return childs
    
    def get_hierarchy_s(self,hierarchy,key):
        items = hierarchy[key]
        ids = list(set([r['Id'] for r in items]))
        hs = ",".join(ids)

        return hs

    def get_hierarchy_list(self,hierarchy,key):
        items = hierarchy[key]
        ids = list(set([r['Id'] for r in items]))

        return ids
    


    product2_Id2Obj = None
    createFiles = True
    aa_Id2Obj={}
    aa_Id2List=None

    def test_select_aas(self):
        def query_id2Obj(q,Id):
            all = query.query(q)['records']
            return get_Id2Obj(all,Id)

        def get_Id2Obj(all,Id):
            Id2Obj = {}
            for one in all:
                Id2Obj[one[Id]] = one
            return Id2Obj
        def query_id2List(q,Id):
            all = query.query(q)['records']
            return get_Id2List(all,Id)
        def get_Id2List(all,Id):
            Id2List = {}
            for aa in all:
                if aa[Id] in Id2List:
                    Id2List[aa[Id]].append(aa)
                else:
                    Id2List[aa[Id]] = [aa]
            return Id2List
        def get_key_order(aa_objectId2List):
            # Create a list of tuples, where each tuple contains the key and the list's length
            key_length_tuples = [(key, len(value)) for key, value in aa_objectId2List.items()]

            # Sort the list of tuples based on the list's length
            sorted_key_length_tuples = sorted(key_length_tuples, key=lambda x: x[1])

            # Extract the ordered list of keys
            ordered_keys = [t[0] for t in sorted_key_length_tuples]

            return ordered_keys
        
        restClient.init('mpomigra')
        aa_objectId2List = query_id2List(f"""SELECT Id, 
                                                    vlocity_cmt__AttributeId__c,
                                                    vlocity_cmt__AttributeId__r.name,
                                                    vlocity_cmt__ObjectId__c,
                                                    vlocity_cmt__AttributeId__r.vlocity_cmt__Value__c,
                                                    vlocity_cmt__AttributeCategoryId__c,
                                                    vlocity_cmt__CategoryDisplaySequence__c,
                                                    vlocity_cmt__CategoryCode__c,
                                                    vlocity_cmt__CategoryName__c,
                                                    vlocity_cmt__AttributeUniqueCode__c,
                                                    vlocity_cmt__ValueDataType__c,
                                                    vlocity_cmt__IsRequired__c,
                                                    vlocity_cmt__IsReadOnly__c,
                                                    vlocity_cmt__IsActive__c,
                                                    vlocity_cmt__AttributeFilterable__c,
                                                    vlocity_cmt__AttributeName__c,
                                                    vlocity_cmt__HasRule__c,
                                                    vlocity_cmt__IsHidden__c,
                                                    vlocity_cmt__AttributeCloneable__c,
                                                    vlocity_cmt__IsNotTranslatable__c,
                                                    vlocity_cmt__AttributeDisplaySequence__c,
                                                    vlocity_cmt__Value__c,
                                                    vlocity_cmt__PicklistId__c,
                                                    vlocity_cmt__PicklistId__r.vlocity_cmt__DataType__c
                                        FROM vlocity_cmt__AttributeAssignment__c where vlocity_cmt__IsOverride__c = false""","vlocity_cmt__ObjectId__c")


        sss = get_key_order(aa_objectId2List)

        a=1


    def test_parallel_query(self):
        restClient.init('mpomigra')

        res = query.query('select Id from vlocity_cmt__AttributeAssignment__c')

        a=1
    def test_find_aa_from_parents(self):
        def query_id2Obj(q,Id):
            all = query.query(q)['records']
            return get_Id2Obj(all,Id)

        def get_Id2Obj(all,Id):
            Id2Obj = {}
            for one in all:
                Id2Obj[one[Id]] = one
            return Id2Obj
        def query_id2List(q,Id):
            all = query.query(q)['records']
            return get_Id2List(all,Id)
        def get_Id2List(all,Id):
            Id2List = {}
            for aa in all:
                if aa[Id] in Id2List:
                    Id2List[aa[Id]].append(aa)
                else:
                    Id2List[aa[Id]] = [aa]
            return Id2List
        def get_aa():
            self.aa_Id2List = query_id2List(f"""SELECT Id, 
                                                        vlocity_cmt__AttributeId__c,
                                                        vlocity_cmt__AttributeId__r.name,
                                                        vlocity_cmt__ObjectId__c,
                                                        vlocity_cmt__AttributeId__r.vlocity_cmt__Value__c,
                                                        vlocity_cmt__AttributeCategoryId__c,
                                                        vlocity_cmt__CategoryDisplaySequence__c,
                                                        vlocity_cmt__CategoryCode__c,
                                                        vlocity_cmt__CategoryName__c,
                                                        vlocity_cmt__AttributeUniqueCode__c,
                                                        vlocity_cmt__ValueDataType__c,
                                                        vlocity_cmt__IsRequired__c,
                                                        vlocity_cmt__IsReadOnly__c,
                                                        vlocity_cmt__IsActive__c,
                                                        vlocity_cmt__AttributeFilterable__c,
                                                        vlocity_cmt__AttributeName__c,
                                                        vlocity_cmt__HasRule__c,
                                                        vlocity_cmt__IsHidden__c,
                                                        vlocity_cmt__AttributeCloneable__c,
                                                        vlocity_cmt__IsNotTranslatable__c,
                                                        vlocity_cmt__AttributeDisplaySequence__c,
                                                        vlocity_cmt__Value__c,
                                                        vlocity_cmt__PicklistId__c,
                                                        vlocity_cmt__PicklistId__r.vlocity_cmt__DataType__c
                                            FROM vlocity_cmt__AttributeAssignment__c where vlocity_cmt__IsOverride__c = false""","vlocity_cmt__ObjectId__c")
    
            self.aa_Id2Obj = {}

            for key in self.product2_Id2Obj.keys():
                self.aa_Id2Obj[key] =  self.aa_Id2List[key] if key in self.aa_Id2List else []

        def getHierarchy(productId):
            objectTypeIdList = []

            objectTypeIdList.append(productId)

            objectTypeId = None
            product2 = self.product2_Id2Obj[productId] 

            if product2['vlocity_cmt__ObjectTypeId__c']!=None:
                objectTypeId = product2['vlocity_cmt__ObjectTypeId__c']
            if product2['vlocity_cmt__ProductSpecId__c']!=None:
                productSpec = self.product2_Id2Obj['vlocity_cmt__ProductSpecId__c'] 
                if productSpec['vlocity_cmt__ObjectTypeId__c']!=None:
                    objectTypeId = productSpec[0]['vlocity_cmt__ObjectTypeId__c']

            if objectTypeId!= None:
                objectTypeIdList.append(objectTypeId)

            while(objectTypeId != None and objectTypeId != rootProductObjectTypeId):
                if objectTypeId not in objectClass_Id2Obj:
                    objectTypeId = None
                    break

                objectTypeId = objectClass_Id2Obj[objectTypeId]['vlocity_cmt__ParentObjectClassId__c']
                if objectTypeId != None and objectTypeId != rootProductObjectTypeId:
                    objectTypeIdList.append(objectTypeId)
            

            return objectTypeIdList
            a=1
        restClient.init('NOSDEV')




        self.product2_Id2Obj = query_id2Obj(f"SELECT Id,vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c,name,vlocity_cmt__AttributeMetadata__c,vlocity_cmt__AttributeDefaultValues__c FROM Product2 where ProductCode  != null",'Id')
        rootProductObjectTypeId = query.query(f"select Id,name from vlocity_cmt__ObjectClass__c where name = 'Product2 Object'")['records'][0]['Id']
        objectClass_Id2Obj = query_id2Obj(f"SELECT Id, vlocity_cmt__ParentObjectClassId__c,name FROM vlocity_cmt__ObjectClass__c",'Id')
        ofa_all = query.query(f"SELECT Id, vlocity_cmt__AttributeId__c,vlocity_cmt__SubClassId__c,vlocity_cmt__ObjectClassId__c FROM vlocity_cmt__ObjectFieldAttribute__c")['records']

        get_aa()

        key = '01t3O0000053k4MQAQ'
        h = getHierarchy(key)

        ofa_Id2List = {}

        ofa_Id2List[key] = [ofa for ofa in ofa_all if ofa['vlocity_cmt__AttributeId__c'] != None and ( (ofa['vlocity_cmt__SubClassId__c']==None and ofa['vlocity_cmt__ObjectClassId__c'] in h) or (ofa['vlocity_cmt__SubClassId__c'] in h))]

        for p in h:
          #  prod = self.product2_Id2Obj[p]
            if p in self.aa_Id2List:
                for aa in self.aa_Id2List[p]:
                    print(f" {p} {aa['vlocity_cmt__AttributeId__c']}  {aa['vlocity_cmt__AttributeUniqueCode__c']}  {aa['Id']}")

        a=1

    
    def test_JSON_Attributes(self):
        def get_Id2List(all,Id):
            Id2List = {}
            for aa in all:
                if aa[Id] in Id2List:
                    Id2List[aa[Id]].append(aa)
                else:
                    Id2List[aa[Id]] = [aa]
            return Id2List
        
        def get_Id2Obj(all,Id):
            Id2Obj = {}
            for one in all:
                Id2Obj[one[Id]] = one
            return Id2Obj
        
        def query_id2Obj(q,Id):
            all = query.query(q)['records']
            return get_Id2Obj(all,Id)

        def query_id2List(q,Id):
            all = query.query(q)['records']
            return get_Id2List(all,Id)

        def getHierarchy(productId):
            objectTypeIdList = []

            objectTypeIdList.append(productId)

            objectTypeId = None
            product2 = self.product2_Id2Obj[productId] 

            if product2['vlocity_cmt__ObjectTypeId__c']!=None:
                objectTypeId = product2['vlocity_cmt__ObjectTypeId__c']
            if product2['vlocity_cmt__ProductSpecId__c']!=None:
                productSpec = self.product2_Id2Obj['vlocity_cmt__ProductSpecId__c'] 
                if productSpec['vlocity_cmt__ObjectTypeId__c']!=None:
                    objectTypeId = productSpec[0]['vlocity_cmt__ObjectTypeId__c']

            if objectTypeId!= None:
                objectTypeIdList.append(objectTypeId)

            while(objectTypeId != None and objectTypeId != rootProductObjectTypeId):
                if objectTypeId not in objectClass_Id2Obj:
                    objectTypeId = None
                    break

                objectTypeId = objectClass_Id2Obj[objectTypeId]['vlocity_cmt__ParentObjectClassId__c']
                if objectTypeId != None and objectTypeId != rootProductObjectTypeId:
                    objectTypeIdList.append(objectTypeId)
            

            return objectTypeIdList
            a=1
 
        def get_aa():
            aa_Id2List = query_id2List(f"""SELECT Id, 
                                                            vlocity_cmt__AttributeId__c,
                                                            vlocity_cmt__AttributeId__r.name,
                                                            vlocity_cmt__ObjectId__c,
                                                            vlocity_cmt__AttributeId__r.vlocity_cmt__Value__c,
                                                            vlocity_cmt__AttributeCategoryId__c,
                                                            vlocity_cmt__CategoryDisplaySequence__c,
                                                            vlocity_cmt__CategoryCode__c,
                                                            vlocity_cmt__CategoryName__c,
                                                            vlocity_cmt__AttributeUniqueCode__c,
                                                            vlocity_cmt__ValueDataType__c,
                                                            vlocity_cmt__IsRequired__c,
                                                            vlocity_cmt__IsReadOnly__c,
                                                            vlocity_cmt__IsActive__c,
                                                            vlocity_cmt__AttributeFilterable__c,
                                                            vlocity_cmt__AttributeName__c,
                                                            vlocity_cmt__HasRule__c,
                                                            vlocity_cmt__IsHidden__c,
                                                            vlocity_cmt__AttributeCloneable__c,
                                                            vlocity_cmt__IsNotTranslatable__c,
                                                            vlocity_cmt__AttributeDisplaySequence__c,
                                                            vlocity_cmt__Value__c,
                                                            vlocity_cmt__PicklistId__c,
                                                            vlocity_cmt__PicklistId__r.vlocity_cmt__DataType__c
                                                FROM vlocity_cmt__AttributeAssignment__c where vlocity_cmt__IsOverride__c = false""","vlocity_cmt__ObjectId__c")
        
            self.aa_Id2Obj = {}

            for key in self.product2_Id2Obj.keys():
                self.aa_Id2Obj[key] =  aa_Id2List[key] if key in aa_Id2List else []
 
        def create_AA(attrId,prodId):
            created_aa = True
            dd = {
                'attrId':attrId,
                'prodId':prodId
            }
            if 1==2:
                res = DR_IP.remoteClass('CreateHierarchy','createAttributeAssigment',input=dd)
            else:

                attrId = dd['attrId']
                prodId = dd['prodId']
                code0 = f"""
                    Id attrId = '{attrId}';
                    Id prodId = '{prodId}';

                """
                code1 = """
                    Map<String,Object> cm = new Map<String,Object>{
                        'attributeId' => attrId,
                        'objectId'=> prodId
                    };

                    String serializedInputs = JSON.serialize(cm);
                    vlocity_cmt.ProductConsoleController.invokeMethod('getAttributeAssignmentByAttributeId',serializedInputs);

                """

                code = code0 + code1

                res = tooling.executeAnonymous(code=code)


        #restClient.init('NOSDEV')
        restClient.init('mpomigra250')
        #restClient.init('NOSPRD')
        #restClient.init('NOSQSM')

        self.product2_Id2Obj = query_id2Obj(f"SELECT Id,vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c,Name,vlocity_cmt__AttributeMetadata__c,vlocity_cmt__AttributeDefaultValues__c FROM Product2  where Id = '01t2o00000AqmKDAAZ'",'Id')
        #self.product2_Id2Obj = query_id2Obj(f"SELECT Id,vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c,name,vlocity_cmt__AttributeMetadata__c,vlocity_cmt__AttributeDefaultValues__c FROM Product2 where ProductCode  != null",'Id')
       # self.product2_Id2Obj = query_id2Obj(f"SELECT Id,vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c,name,vlocity_cmt__AttributeMetadata__c,vlocity_cmt__AttributeDefaultValues__c FROM Product2 where Id in (select vlocity_cmt__ProductId__c from vlocity_cmt__PriceListEntry__c where vlocity_cmt__PriceListId__r.name = 'WOO Price List')",'Id')

        objectClass_Id2Obj = query_id2Obj(f"SELECT Id, vlocity_cmt__ParentObjectClassId__c,name FROM vlocity_cmt__ObjectClass__c",'Id')

        rootProductObjectTypeId = query.query(f"select Id,name from vlocity_cmt__ObjectClass__c where name = 'Product2 Object'")['records'][0]['Id']

        ofa_all = query.query(f"SELECT Id, vlocity_cmt__AttributeId__c,vlocity_cmt__SubClassId__c,vlocity_cmt__ObjectClassId__c FROM vlocity_cmt__ObjectFieldAttribute__c")['records']

        attributes_Id2Obj = query_id2Obj(f"""select    Id,
                                                            vlocity_cmt__DisplaySequence__c,
                                                            vlocity_cmt__AttributeCategoryCode__c,
                                                            vlocity_cmt__AttributeCategoryName__c,
                                                            vlocity_cmt__AttributeCategoryId__c,
                                                            vlocity_cmt__Code__c,
                                                            vlocity_cmt__ValueType__c,
                                                            Name,
                                                            vlocity_cmt__Filterable__c,
                                                            vlocity_cmt__isDefaultHidden__c,
                                                            vlocity_cmt__IsCloneable__c,
                                                            vlocity_cmt__Value__c ,
                                                            vlocity_cmt__ActiveFlg__c,
                                                            vlocity_cmt__PicklistId__r.vlocity_cmt__DataType__c,
                                                            vlocity_cmt__AttributeCategoryId__r.vlocity_cmt__DisplaySequence__c

                                              from vlocity_cmt__Attribute__c""","Id")

        get_aa()

        hierarchies = {}
        ofa_Id2List = {}

        for key in self.product2_Id2Obj.keys():
            hierarchies[key] = getHierarchy(key)
            ofa_Id2List[key] = [ofa for ofa in ofa_all if ofa['vlocity_cmt__AttributeId__c'] != None and ( (ofa['vlocity_cmt__SubClassId__c']==None and ofa['vlocity_cmt__ObjectClassId__c'] in hierarchies[key]) or (ofa['vlocity_cmt__SubClassId__c'] in hierarchies[key]))]


        for prodId in self.aa_Id2Obj:
            if prodId not in ofa_Id2List:
                print(f"{prodId} not in ofa_Id2List")
                continue

            num_ocurrences = {}
            for attribute_aa in self.aa_Id2Obj[prodId]:
                num_ocurrences[attribute_aa['vlocity_cmt__AttributeId__c']] = num_ocurrences[attribute_aa['vlocity_cmt__AttributeId__c']] +1 if attribute_aa['vlocity_cmt__AttributeId__c'] in num_ocurrences else 1
                exists = False
                ofa_tribs = ofa_Id2List[prodId]
                for attribute_ofa in ofa_Id2List[prodId]:
                    if attribute_aa['vlocity_cmt__AttributeId__c'] == attribute_ofa['vlocity_cmt__AttributeId__c']:
                        exists = True
                if exists == False:
                    print(f"NO in ofa -->productID:{prodId} <{self.product2_Id2Obj[prodId]['Name']}> Attribute {attribute_aa['vlocity_cmt__AttributeId__c']}")
                
            for ocurrence in num_ocurrences.keys():
                if num_ocurrences[ocurrence] > 1:
                    print(f"Product {prodId} {self.product2_Id2Obj[prodId]['Name']} has duplicated attribute assigments for attribute assigment {ocurrence} ")

        count = 0

        created_aa = False
        for prodId in ofa_Id2List:
            if prodId not in self.aa_Id2Obj:
                print(f"{prodId} not in self.aa_Id2Obj")
                continue
            for atribute_ofa in ofa_Id2List[prodId]:
                exists = False

                for attribute_aa in self.aa_Id2Obj[prodId]:
                    #print(f"{atribute_ofa['vlocity_cmt__AttributeId__c']}    {attribute_aa['vlocity_cmt__AttributeId__c']}")
                    if atribute_ofa['vlocity_cmt__AttributeId__c'] == attribute_aa['vlocity_cmt__AttributeId__c']:
                        exists = True
                        break
                if exists == False:
                    print(f"productID:{prodId} <{self.product2_Id2Obj[prodId]['Name']}> Attribute {atribute_ofa['vlocity_cmt__AttributeId__c']}:{attributes_Id2Obj[atribute_ofa['vlocity_cmt__AttributeId__c']]['Name']}")
                    if 1==2:
                        create_AA(atribute_ofa['vlocity_cmt__AttributeId__c'],prodId)
                        created_aa = True
                    count = count + 1 

        if created_aa == True:
            get_aa()

        records_to_update = []
        print(count)

        stats = []
    
        for key in self.product2_Id2Obj.keys():
            print(f"PROCESSING {key}   {self.product2_Id2Obj[key]['Name']}")
            #attributes = []
            aas = []
            for aa in self.aa_Id2Obj[key]:
                aas.append(aa)
            sorted_list = sorted(aas, key=lambda x: x['vlocity_cmt__CategoryDisplaySequence__c'])
            attMeta,default_values = self.create_attribute_metadata_from_aa(sorted_list)

            update_def_vals = self.validate_default_values(default_values,key)
            update_metadata = self.validate_attr_meta(attMeta,key)

            if update_def_vals==False or update_metadata==False:

                stat = {
                    'Id':key,
                    'Name':self.product2_Id2Obj[key]['Name'],
                    'Meta':update_metadata,
                    'Def':update_def_vals
                }
                stats.append(stat)
                update_r = {
                    'Id':key
                }
                
                update_r['vlocity_cmt__AttributeMetadata__c'] = simplejson.dumps( attMeta) if attMeta != None else None
                update_r['vlocity_cmt__AttributeDefaultValues__c'] = simplejson.dumps(default_values) if default_values != None else None
                records_to_update.append(update_r)

            a=1

        a=1

        def save_product2(records_to_update):
            res = DR_IP.remoteClass('CreateHierarchy','save_product2',input={"data":records_to_update})
            print(res)
            return res

        if 1==2:
            chunck_size = 30
            records_to_update_chunks = [records_to_update[i:i + chunck_size] for i in range(0, len(records_to_update), chunck_size)]

            thread.processList(save_product2,records_to_update_chunks,20)

        fff = file_csv.write('stats',stats)

      #  for chunck in records_to_update_chunks:
      #      res = DR_IP.remoteClass('CreateHierarchy','save_product2',input={"data":chunck})

    def create_attribute_metadata_from_attributes(self,attributes):
        category_id = {}

        for attribute in attributes:
            if attribute['vlocity_cmt__AttributeCategoryId__c'] not in category_id:
                category_id[attribute['vlocity_cmt__AttributeCategoryId__c']] = [attribute]
            else:
                category_id[attribute['vlocity_cmt__AttributeCategoryId__c']].append(attribute)


        attribute_meta = {
            "totalSize": 0,
            "messages": [],
            "records": []
        }

        for key in category_id:
            category = {
                "messages": [],
                "displaySequence": int(category_id[key][0]['vlocity_cmt__AttributeCategoryId__r']['vlocity_cmt__DisplaySequence__c']),
                "Code__c": category_id[key][0]['vlocity_cmt__AttributeCategoryCode__c'],
                "Name": category_id[key][0]['vlocity_cmt__AttributeCategoryName__c'],
                "id": category_id[key][0]['vlocity_cmt__AttributeCategoryId__c'],
                "productAttributes":{
                    "totalSize": 0,
                    "messages": [],
                    "records": []
                }
            }
            attribute_meta['records'].append(category)
            attribute_meta['totalSize'] = attribute_meta['totalSize'] + 1

            pa = category['productAttributes']
            par = pa['records']

            for attribute in category_id[key]:
                pa['totalSize'] = pa['totalSize'] + 1
                r = {
                    "messages": [],
                    "code": attribute['vlocity_cmt__Code__c'],
                    "dataType": attribute['vlocity_cmt__ValueType__c'].lower(),
                    "inputType": attribute['vlocity_cmt__ValueType__c'].lower(),
                    "multiselect": attribute['x'],
                    "required": attribute['x'],
                    "readonly": attribute['x'],
                    "disabled": attribute['vlocity_cmt__ActiveFlg__c'] == False,
                    "filterable": attribute['vlocity_cmt__Filterable__c'],
                    "attributeId": attribute['Id'],
                    "label": attribute['Name'],
                    "displaySequence": int(attribute['vlocity_cmt__DisplaySequence__c']),
                    "hasRules": attribute['x'],
                    "hidden": attribute['vlocity_cmt__isDefaultHidden__c'],
                    "cloneable": attribute['vlocity_cmt__IsCloneable__c'],
                    "isNotTranslatable": attribute['x'],    
                    "values":{

                    },   
                    "userValues": attribute['vlocity_cmt__Value__c']
                }
                if r['inputType'] == "picklist":  
                    r['inputType'] = 'dropdown'
                    r['dataType'] = attribute['vlocity_cmt__PicklistId__r']['vlocity_cmt__DataType__c'].lower()
                par.append(r)

        print( simplejson.dumps( attribute_meta))

    def create_attribute_metadata_from_aa(self,aas):

        if len(aas) == 0:
            return None,None
        category_id = {}

        for aa in aas:
            if aa['vlocity_cmt__AttributeCategoryId__c'] not in category_id:
                category_id[aa['vlocity_cmt__AttributeCategoryId__c']] = [aa]
            else:
                category_id[aa['vlocity_cmt__AttributeCategoryId__c']].append(aa)

        for Id in category_id.keys():
            category_id[Id] = sorted(category_id[Id], key=lambda x: int(x['vlocity_cmt__AttributeDisplaySequence__c']))

        attribute_meta = {
            "totalSize": 0,
            "messages": [],
            "records": []
        }

        selected_values = {}

        for key in category_id:
            category = {
                "messages": [],
                "displaySequence": int(category_id[key][0]['vlocity_cmt__CategoryDisplaySequence__c']),
                "Code__c": category_id[key][0]['vlocity_cmt__CategoryCode__c'],
                "Name": category_id[key][0]['vlocity_cmt__CategoryName__c'],
                "id": category_id[key][0]['vlocity_cmt__AttributeCategoryId__c'],
                "productAttributes":{
                    "totalSize": 0,
                    "messages": [],
                    "records": []
                }
            }
            attribute_meta['records'].append(category)
            attribute_meta['totalSize'] = attribute_meta['totalSize'] + 1

            pa = category['productAttributes']
            par = pa['records']

            for aa in category_id[key]:
                pa['totalSize'] = pa['totalSize'] + 1
                r = {
                    "messages": [],
                    "code": aa['vlocity_cmt__AttributeUniqueCode__c'],
                    "dataType": aa['vlocity_cmt__ValueDataType__c'].lower(),
                    "inputType": aa['vlocity_cmt__ValueDataType__c'].lower(),
                    "multiselect": False, #This needs to be corrected?
                    "required": aa['vlocity_cmt__IsRequired__c'],
                    "readonly": aa['vlocity_cmt__IsReadOnly__c'],
                    "disabled": aa['vlocity_cmt__IsReadOnly__c'], #aa['vlocity_cmt__IsActive__c'] == False, parece que lee el readonly
                    "filterable": aa['vlocity_cmt__AttributeFilterable__c'],
                    "attributeId": aa['vlocity_cmt__AttributeId__c'],
                    "label": aa['vlocity_cmt__AttributeName__c'],
                    "displaySequence": int(aa['vlocity_cmt__AttributeDisplaySequence__c']),
                    "hasRules": aa['vlocity_cmt__HasRule__c'],
                    "hidden": aa['vlocity_cmt__IsHidden__c'],
                    "cloneable": aa['vlocity_cmt__AttributeCloneable__c'],
                    "isNotTranslatable": aa['vlocity_cmt__IsNotTranslatable__c'],    
                    "values" : self.get_values_other( aa['vlocity_cmt__IsReadOnly__c'], aa['vlocity_cmt__IsReadOnly__c']),
                    "userValues": aa['vlocity_cmt__Value__c']
                   # ,"aaId":aa['Id']
                }

                selected_values[aa['vlocity_cmt__AttributeUniqueCode__c']] = aa['vlocity_cmt__Value__c']

                if r['inputType'] == "picklist":  
                    r['inputType'] = 'dropdown'
                    r['dataType'] = aa['vlocity_cmt__PicklistId__r']['vlocity_cmt__DataType__c'].lower()
                    r['values'],selected_value = self.get_values_picklist(aa['vlocity_cmt__PicklistId__c'],r['readonly'],disabled=False,aa_value=aa['vlocity_cmt__Value__c'])
                    r["userValues"]= None
                    selected_values[aa['vlocity_cmt__AttributeUniqueCode__c']] = selected_value
                
                if r['inputType'] == "checkbox":  
                    r['values'] = self.get_values_checkbox(r['readonly'],disabled=r['readonly'],defaultVal=aa['vlocity_cmt__Value__c'])
                    r["userValues"]= None
                    selected_values[aa['vlocity_cmt__AttributeUniqueCode__c']] = aa['vlocity_cmt__Value__c'] == "true"
                    r['dataType'] = 'text'


                if r['inputType'] == "number":  
                    r['values'] = self.get_values_number(r['readonly'],disabled=r['readonly'],value=aa['vlocity_cmt__Value__c'])
                    r["userValues"]= None
                    if aa['vlocity_cmt__Value__c'] != None:
                        selected_values[aa['vlocity_cmt__AttributeUniqueCode__c']] = int(aa['vlocity_cmt__Value__c'])

                if r['inputType'] == "text":  
                    r['values'] = self.get_values_text(r['readonly'],disabled=r['readonly'],value=aa['vlocity_cmt__Value__c'])
                    r["userValues"]= None

              #  if r['inputType'] == "checkbox":  

                par.append(r)

        return attribute_meta,selected_values
      #  print( simplejson.dumps( attribute_meta,ensure_ascii=False))

    def  get_values_number(self,readonly,disabled,value):
        values =[
            {
                "readonly": readonly,
                "disabled": disabled
            }
        ]
        if value != None:
            values[0]["defaultValue"] = int(value)
        return values
    def  get_values_text(self,readonly,disabled,value):
        values =[
            {
                "readonly": readonly,
                "disabled": disabled
            }
        ]
        if value != None:
            values[0]["defaultValue"] = value
        return values
    def  get_values_other(self,readonly,disabled):
        values =[
            {
                "readonly": readonly,
                "disabled": disabled
            }
        ]
        return values
    def  get_values_checkbox(self,readonly,disabled,defaultVal):
        values =[
            {
                "readonly": readonly,
                "disabled": disabled,
                "defaultValue": defaultVal == 'true'
            }
        ]

        if values[0]['defaultValue'] == True:
            values[0]["defaultSelected"] = True
        return values
    picklistValues_picklistId = None
    def get_values_picklist(self,picklistId,readonly,disabled,aa_value):
        if self.picklistValues_picklistId == None:
            self.picklistValues_picklistId = {}
            picklistValues = query.queryRecords(f"""select  Id,
                                                    vlocity_cmt__PicklistId__c,
                                                    Name,
                                                    vlocity_cmt__GlobalKey__c,
                                                    vlocity_cmt__TextValue__c,
                                                    vlocity_cmt__Sequence__c,
                                                    vlocity_cmt__IsDefault__c
                                        from vlocity_cmt__PicklistValue__c """)
            
            for value in picklistValues:
                if value['vlocity_cmt__PicklistId__c'] in self.picklistValues_picklistId:
                    self.picklistValues_picklistId[value['vlocity_cmt__PicklistId__c']].append(value)
                else:
                    self.picklistValues_picklistId[value['vlocity_cmt__PicklistId__c']] = [value]

        selected_value = None
        picklistValues = []
        for picklistValue in self.picklistValues_picklistId[picklistId]:
            if picklistValue['vlocity_cmt__Sequence__c'] == None:
                a=1
            r =               {
                "id": picklistValue['vlocity_cmt__GlobalKey__c'],
                "name": picklistValue['vlocity_cmt__GlobalKey__c'],
                "label": picklistValue['Name'],
                "readonly": readonly,
                "disabled": disabled,
                "value": picklistValue['vlocity_cmt__TextValue__c'],
                "defaultSelected": picklistValue['vlocity_cmt__TextValue__c'] == aa_value,
                "displaySequence": int(picklistValue['vlocity_cmt__Sequence__c']) if picklistValue['vlocity_cmt__Sequence__c'] != None else 1234 #$$$ this should be not null
            }
            picklistValues.append(r)
            if r['defaultSelected'] == True:
                 selected_value = r['value']

        sorted_list = sorted(picklistValues, key=lambda x: x['displaySequence'],reverse=True)
        return sorted_list,selected_value
    

    def validate_default_values(self,default_values,prodId):
        try:
            default = self.product2_Id2Obj[prodId]['vlocity_cmt__AttributeDefaultValues__c']
            defaultObject = simplejson.loads( default)
        except Exception as e:
            if default_values == None:
                return True
            print(f"          The Default Values file is empty in the DB")
            return False

        if default_values == None:
            return False

        default_values_s = dict(sorted(default_values.items()))
        defaultObject_s = dict(sorted(defaultObject.items()))

        errors = ''

        for key in default_values_s:
            if key not in defaultObject_s:
                errors += f"          {key} not in DB\n"
                continue
            if default_values_s[key] != defaultObject_s[key]:
                errors += f"          {key} value is different {default_values_s[key]}  -- DB: {defaultObject_s[key]} \n"
        for key in defaultObject_s:
            if key not in default_values_s:
                errors += f"          {key} not in default_values_s\n"   

        if errors != '':
            print(f"     Default Values failed -->{prodId}  {self.product2_Id2Obj[prodId]['Name']}")
            print(errors)
            comp = False
        else:
            comp = self.deep_compare(default_values_s,defaultObject_s)
            if comp == False:
                print(f"     Default Values failed  (OTHER)-->{prodId}  {self.product2_Id2Obj[prodId]['Name']}")


        #if comp == False and self.createFiles == True:
        jsonFile.write('c1',default_values_s)
        jsonFile.write('c2',defaultObject_s)
        a=1

        return comp

    
    def validate_attr_meta(self,attMeta,prodId):
        try:
            meta = self.product2_Id2Obj[prodId]['vlocity_cmt__AttributeMetadata__c']
            attMeta_DB = simplejson.loads( meta)
        except Exception as e:
            if attMeta == None:
                return True
            print(f"          The Matadata file is empty in the DB")
            return False
        
        if attMeta == None:
            return False
        
        for r in attMeta['records']:
            r['productAttributes']['records'] = sorted(r['productAttributes']['records'], key=lambda x: str(x)) 
            for rr in r['productAttributes']['records']:
                rr['values'] = sorted(rr['values'], key=lambda x: str(x)) 

        for r in attMeta_DB['records']:
            r['productAttributes']['records'] = sorted(r['productAttributes']['records'], key=lambda x: str(x)) 
            for rr in r['productAttributes']['records']:
                if type(rr['values']) == list:
                    rr['values'] = sorted(rr['values'], key=lambda x: str(x)) 

        a=1

        errors = ''

        for r in attMeta['records']:
            cats = [r_db['Code__c'] for r_db in attMeta_DB['records'] ]
            if r['Code__c'] not in cats:
                errors = f"     METADATA failed   ATtribute Category {r['Code__c']} Not in DB\n"
            else:
                par = r['productAttributes']['records']
                par_db = attMeta_DB['records'][cats.index(r['Code__c'])]['productAttributes']['records']
                for rr in par:
                    if rr['code'] not in [rr_db['code'] for rr_db in par_db]:
                        errors += f"     METADATA failed    Attribute  {r['Code__c']}-->{rr['code']} Not in DB\n"
                

        for r in attMeta_DB['records']:
            cats = [r_db['Code__c'] for r_db in attMeta['records'] ]
            if r['Code__c'] not in cats:
                errors = f"     METADATA Attribute Category {r['Code__c']} Not in Memory\n"

        if errors != '':
            print(errors)
            comp = False
        else:
            comp = self.deep_compare(attMeta,attMeta_DB)
            if comp == False:
                print(f"     METADATA failed  (OTher)")


        #if comp == False and self.createFiles == True:
        jsonFile.write('b1',attMeta)
        jsonFile.write('b2',attMeta_DB)
        a=1

        return comp


    def deep_compare(self,obj1, obj2):

        # Base case: if both objects are of different types, they are not equal
        if type(obj1) != type(obj2):
            return False

        # If both objects are dictionaries, recursively compare their keys and values
        if isinstance(obj1, dict):
            if len(obj1) != len(obj2):
                print(f"    Dictionary Lenght is different {len(obj1)}  {len(obj2)}")
                return False
            for key in obj1:
                if key not in obj2:
                    return False
                if not self.deep_compare(obj1[key], obj2[key]):
                    return False
            return True

        # If both objects are lists, recursively compare their elements
        elif isinstance(obj1, list):
            if len(obj1) != len(obj2):
                print(f"    List Lenght is different {len(obj1)}  {len(obj2)}")
                return False
            obj1_sorted = sorted(obj1, key=lambda x: str(x))  # Sort obj1
            obj2_sorted = sorted(obj2, key=lambda x: str(x))  # Sort obj2
            for i in range(len(obj1_sorted)):
                if not self.deep_compare(obj1_sorted[i], obj2_sorted[i]):
                    return False
            return True

        # For other types (primitives), simply compare for equality
        else:
            val = obj1 == obj2
            if val == False:
                print(f"       No same value in JSON memory <{obj1}>  in DB <{obj2}>")
            return val



        


