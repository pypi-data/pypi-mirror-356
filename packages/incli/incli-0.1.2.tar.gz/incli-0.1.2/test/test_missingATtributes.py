import unittest
##from InCli import InCli
from incli.sfapi import file,restClient,query
from types import SimpleNamespace

class Test_File(unittest.TestCase):

    def test_main(self):
        restClient.init('DEVNOSCAT3')

        productId = '01t3N00000AjB61QAF'
        call = query.query(f"SELECT Id, vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c,name from Product2 WHERE Id ='{productId}' ")
        for r in call['records']:
            n = SimpleNamespace(**r)
            #res= self.get_hierarchy(n)
            res = self.add_missing_attr_Assgiment(n)

    def add_missing_attr_Assgiment(self,product,):
        def get_ofa_list(product,object_type_id_list):
            #object_type_id_list = self.get_hierarchy(product)
            ofa_list = []
            if product.vlocity_cmt__ProductSpecId__c is not None:
                product_spec = query.query(f"SELECT Id, vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c from Product2 WHERE Id = {product.vlocity_cmt__ProductSpecId__c}")
                object_type_id_list2 = self.get_hierarchy(product_spec)
                ofa_list = query("SELECT Id, vlocity_cmt__AttributeId__c FROM vlocity_cmt__ObjectFieldAttribute__c WHERE (vlocity_cmt__AttributeId__c != null) AND ((vlocity_cmt__SubClassId__c = null AND vlocity_cmt__ObjectClassId__c = :object_type_id_list2) OR (vlocity_cmt__SubClassId__c = :object_type_id_list2))")
            else:
                ofa_list = query.query(f"SELECT Id, vlocity_cmt__AttributeId__c,name,vlocity_cmt__AttributeId__r.name,vlocity_cmt__SubClassId__c,vlocity_cmt__ObjectClassId__r.name,vlocity_cmt__FieldApiName__c FROM vlocity_cmt__ObjectFieldAttribute__c WHERE (vlocity_cmt__AttributeId__c != null) AND ((vlocity_cmt__SubClassId__c = null AND vlocity_cmt__ObjectClassId__c in ({query.IN_clause(object_type_id_list)}) ) OR (vlocity_cmt__SubClassId__c in ({query.IN_clause(object_type_id_list)})))")
            return ofa_list['records']
        
        def get_aa_list(object_type_id_list):
            aa_list = query.query(f"SELECT Id, vlocity_cmt__AttributeId__c,vlocity_cmt__AttributeId__r.name FROM vlocity_cmt__AttributeAssignment__c WHERE vlocity_cmt__ObjectId__c in ({query.IN_clause(object_type_id_list)}) AND vlocity_cmt__IsOverride__c = false")
            return aa_list['records']

        # This function is assumed to return the Product record
        #product = get_product()
        object_type_id_list = self.get_hierarchy(product)
        ofa_list = get_ofa_list(product,object_type_id_list)
        aa_list = get_aa_list(object_type_id_list)

        # Collect all attribute assignment
        map_of_aa = {}
        for aa in aa_list:
            if aa is not None:
                map_of_aa[aa['vlocity_cmt__AttributeId__c']] = aa

        # Collect all ofa
        map_of_ofa = {}
        for ofa in ofa_list:
            if ofa is not None:
                map_of_ofa[ofa['vlocity_cmt__AttributeId__c']] = ofa

        # Product AA
        aa_list_product = get_aa_list(product.Id)
        map_of_aa_product = {}
        for aa in aa_list_product:
            if aa is not None:
                map_of_aa_product[aa['vlocity_cmt__AttributeId__c']] = aa

        for attr_id in map_of_ofa.keys():
            # Check attribute contains attribute assignment for the given product
            if attr_id not in map_of_aa_product.keys():
                print('****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************** Attribute assignment is missing for product', product.Id, product.Name, 'attribute id', attr_id)
            else:
                print('Attribute assignment is not missing for attribute id', attr_id)

    def get_hierarchy(self, product):
        objectTypeId = None
        objectTypeId_list = [product.Id]

        if product.vlocity_cmt__ObjectTypeId__c is not None:
            objectTypeId = product.vlocity_cmt__ObjectTypeId__c

        if product.vlocity_cmt__ProductSpecId__c is not None:
            product_spec = self.vlocity_cmt.query(
                "SELECT vlocity_cmt__ObjectTypeId__c, vlocity_cmt__ProductSpecId__c FROM Product2 WHERE Id =:product.vlocity_cmt__ProductSpecId__c"
            )['records'][0]
            objectTypeId_list.append(product_spec.Id)

            if product_spec.vlocity_cmt__ObjectTypeId__c is not None:
                objectTypeId = product.vlocity_cmt__ProductSpecId__c

        root_product_object_type_id = 'a3Z3O00000076SPUAY'
        if objectTypeId is not None:
            objectTypeId_list.append(objectTypeId)

        while objectTypeId is not None and objectTypeId != root_product_object_type_id:
            object_type_list = query.query(
                f"SELECT Id, vlocity_cmt__ParentObjectClassId__c, name FROM vlocity_cmt__ObjectClass__c WHERE Id = '{objectTypeId}'"
            )['records']

            print(object_type_list)
            if object_type_list and len(object_type_list) > 0:
                objectTypeId = object_type_list[0]['vlocity_cmt__ParentObjectClassId__c']
                if objectTypeId is not None and objectTypeId != root_product_object_type_id:
                    objectTypeId_list.append(objectTypeId)
            else:
                objectTypeId = None

        print('List of object type id:', objectTypeId_list)
        return objectTypeId_list
