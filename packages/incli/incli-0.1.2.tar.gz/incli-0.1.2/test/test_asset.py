import unittest
from incli.sfapi import query,restClient,DR_IP,Sobjects,jsonFile

class Test_Asset(unittest.TestCase):
    def test_get(self):
        restClient.init('NOSDEV')
        assetId = '02i3O00000LF5TCQA1'
        tvCabo = '02i3O00000KmxRkQAJ'
        cloned = '02i3O00000LIFngQAH'
        assetId = cloned
       # assetId = assetId

        q = f"select fields(all) from asset where Id='{assetId}' limit 100"

        res = query.query(q)

        ra = res['records'][0]
        for key in ra.keys():
            print(f"{key},")

        q = f"select fields(all) from asset where vlocity_cmt__RootItemId__c='{assetId}' limit 200"
        assets_r = query.query(q)

        rootAsset = [record for record in assets_r['records'] if record['vlocity_cmt__ParentItemId__c'] == None][0]
        rootAssetId = rootAsset['Id']

        assetIds = [record['Id'] for record in assets_r['records']]

        qr = f"select fields(all) from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__SourceAssetId__c in ({query.IN_clause(assetIds)}) limit 100"
        Inv_rel_r = query.query(qr)

        ra = Inv_rel_r['records'][0]
        for key in ra.keys():
            print(f"{key},")

        vlocity_cmt__DestinationInventoryItemIds = [des['vlocity_cmt__DestinationInventoryItemId__c'] for des in Inv_rel_r['records']]

        inv_items_ids_q = vlocity_cmt__DestinationInventoryItemIds.copy()

        while len(inv_items_ids_q)>0:
            q = f"select fields(all) from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__SourceInventoryItemId__c in ({query.IN_clause(inv_items_ids_q)}) limit 200"
            inv_items_child = query.query(q)
            inv_items_ids_q = [r['vlocity_cmt__DestinationInventoryItemId__c'] for r in inv_items_child['records']]
            vlocity_cmt__DestinationInventoryItemIds.extend(inv_items_ids_q)

        
        q = f"select fields(all) from vlocity_cmt__InventoryItem__c where Id in ({query.IN_clause(vlocity_cmt__DestinationInventoryItemIds)}) limit 200"
        inv_items = query.query(q)

        inv_items_ids = [r['Id'] for r in inv_items['records']]

        productIds = [r['vlocity_cmt__ProductId__c'] for r in inv_items['records']]
        q=f"select fields(all) from product2 where Id in ({query.IN_clause(productIds)})"
        products = query.query(q)
        prodId_2_name={}
        for prod in products['records']:
            prodId_2_name[prod['Id']] = prod['Name']

        missing = [id for id in inv_items_ids if id not in vlocity_cmt__DestinationInventoryItemIds]

        ra = inv_items['records'][0]
        print("Inventory Items")
        for key in ra.keys():
            print(f"{key},")

        for item in inv_items['records']:
            print(f"{item['Name']}   {prodId_2_name[item['vlocity_cmt__ProductId__c']]}")
        a=1

        inv_items['records'][0]['vlocity_cmt__AccountId__c']


    def test_deepClone(self):
        restClient.init('NOSDEV')

        accountId_current = '0013O00001CoyfqQAB'
        rootAssetIds = query.queryFieldList(f"select Id from asset where AccountId = '{accountId_current}' and vlocity_cmt__ParentItemId__c = null")

        accountId_new = '0013O00001BfQ8yQAF'

        input = {
            "rootAssetIds":rootAssetIds,
            "accountId":accountId_new
        }
        res = DR_IP.remoteCallable('AssetsDeepClone','getAssets',input)

        print(res)

    def test_deepClone_getPromos(self):
        restClient.init('NOSDEV')

        accountId_current = '0013O00001CoyfqQAB'
        rootAssetIds = query.queryFieldList(f"select Id from asset where AccountId = '{accountId_current}' and vlocity_cmt__ParentItemId__c = null")

        accountId_new = '0013O00001BfQ8yQAF'

        input = {
            "rootAssetIds":rootAssetIds,
            "accountId":accountId_new,
            "accountsMap":{
                accountId_current:accountId_new
            }
        }
        res = DR_IP.remoteCallable('AssetsDeepClone','getPromos',input)

        print(res)

    def test_deepClone_deleteAssets(self):
        restClient.init('NOSDEV')

        accountId_new = '0013O00001BfQ8yQAF'

        rootAssetIds = query.queryFieldList(f"select Id from asset where AccountId = '{accountId_new}' and vlocity_cmt__ParentItemId__c = null")

        input = {
            "rootAssetIds":rootAssetIds
        }
        res = DR_IP.remoteCallable('AssetsDeepClone','deleteAssets',input)

        print(res)

    def test_deepClone_getAll(self):
        restClient.init('NOSDEV')

        accountId_new = '0013O00001BfQ8yQAF'
        accountId_current = '0013O00001CoyfqQAB'

        rootAssetIds = query.queryFieldList(f"select Id from asset where AccountId = '{accountId_new}' and vlocity_cmt__ParentItemId__c = null")

        input = {
            "rootAssetIds":rootAssetIds
        }
        res = DR_IP.remoteCallable('AssetsDeepClone','getAll',input)

        print(res)
    def test_delete_deepClone(self):
        restClient.init('NOSDEV')

        delete = False

        accountId_existing = '0013O00001CoyfqQAB'
        accountId_new = '0013O00001BfQ8yQAF'

        accountId = accountId_existing

        q0 = f"select IDs from asset where AccountId = '{accountId}'"
        res0 = query.query(q0)

        q1 = f"select Id from vlocity_cmt__InventoryItem__c where vlocity_cmt__GasPressureLevel__c != null and vlocity_cmt__AccountId__c = '{accountId}'  "
        q1 = f"select Id from vlocity_cmt__InventoryItem__c where  vlocity_cmt__AccountId__c = '{accountId}'  "

        print(q1)
        res1 = query.query(q1)

        itemIds = [r['Id'] for r in res1['records']]

        q2 = f"select Id from vlocity_cmt__InventoryItemDecompositionRelationship__c where Name like 'CLONING%' and vlocity_cmt__DestinationInventoryItemId__c in ({query.IN_clause(itemIds)})  "
        q2 = f"select Id from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__DestinationInventoryItemId__c in ({query.IN_clause(itemIds)})  "

        print(q2)
        res2 = query.query(q2)

        sobjectsToCloneIdsList= query.queryFieldList(f"select Id from asset where accountId='{accountId}'")

        q3 = f"Select Id,vlocity_cmt__AppliedPromotionId__c from vlocity_cmt__AccountAppliedPromotionItem__c  where vlocity_cmt__AssetId__c IN ({query.IN_clause(sobjectsToCloneIdsList)})"
        res3 = query.query(q3)

        appliedPromoIds = [r['vlocity_cmt__AppliedPromotionId__c'] for r in res3['records']]

        q4 = f"SELECT Id FROM vlocity_cmt__AccountAppliedPromotion__c WHERE  Id in ({query.IN_clause(appliedPromoIds)})"
        res4 = query.query(q4)

        q5 = f"select Id from vlocity_cmt__AccountPriceAdjustment__c where vlocity_cmt__AssetId__c in ({query.IN_clause(sobjectsToCloneIdsList)}) "
        print(q5)
        res5 = query.query(q5)

        output = {
            'res0':res0,
            'res1':res1,
            'res2':res2,
            'res3':res3,
            'res4':res4,
            'res5':res5
        }

        filename = jsonFile.write(f"{accountId}_output",output)

        if delete:
            self.delete(q2)
            self.delete(q1)
            self.delete(q0)
            self.delete(q3)
            self.delete(q4)
            self.delete(q5)

        s=1

    def test_get_deepClone(self):
        restClient.init('NOSDEV')

        delete = False

        accountId_existing = '0013O00001CoyfqQAB'
        accountId_new = '0013O00001BfQ8yQAF'

        accountId = accountId_new

        q0 = f"select fields(all) from asset where AccountId = '{accountId}' limit 200"
        res0 = query.query(q0)

        q1 = f"select Id from vlocity_cmt__InventoryItem__c where vlocity_cmt__GasPressureLevel__c != null and vlocity_cmt__AccountId__c = '{accountId}'  "
        q1 = f"select fields(all) from vlocity_cmt__InventoryItem__c where  vlocity_cmt__AccountId__c = '{accountId}'  limit 200"

        print(q1)
        res1 = query.query(q1)

        itemIds = [r['Id'] for r in res1['records']]

        q2 = f"select Id from vlocity_cmt__InventoryItemDecompositionRelationship__c where Name like 'CLONING%' and vlocity_cmt__DestinationInventoryItemId__c in ({query.IN_clause(itemIds)})  "
        q2 = f"select fields(all) from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__DestinationInventoryItemId__c in ({query.IN_clause(itemIds)})  limit 200 "

        print(q2)
        res2 = query.query(q2)

        sobjectsToCloneIdsList= query.queryFieldList(f"select Id from asset where accountId='{accountId}'")

        q3 = f"Select fields(all) from vlocity_cmt__AccountAppliedPromotionItem__c  where vlocity_cmt__AssetId__c IN ({query.IN_clause(sobjectsToCloneIdsList)}) limit 200"
        res3 = query.query(q3)

        appliedPromoIds = [r['vlocity_cmt__AppliedPromotionId__c'] for r in res3['records']]

        q4 = f"SELECT fields(all) FROM vlocity_cmt__AccountAppliedPromotion__c WHERE  Id in ({query.IN_clause(appliedPromoIds)}) limit 200"
        res4 = query.query(q4)

        q5 = f"select fields(all) from vlocity_cmt__AccountPriceAdjustment__c where vlocity_cmt__AssetId__c in ({query.IN_clause(sobjectsToCloneIdsList)})  limit 200"
        print(q5)
        res5 = query.query(q5)

        output = {
            'res0':res0,
            'res1':res1,
            'res2':res2,
            'res3':res3,
            'res4':res4,
            'res5':res5
        }

        filename = jsonFile.write(f"{accountId}_output",output)

        s=1
    def delete(self,q):
            res = query.query(q)

            id_list = [record['Id'] for record in res['records']]
            
            Sobjects.deleteMultiple('ApexLog',id_list)
            print()


    def test_select_in_a_different_Way(self):
        restClient.init('NOSDEV')
        accountId = '0013O00001BfQ8yQAF'
        dele = True

        q0 = f"select fields(all) from vlocity_cmt__InventoryItem__c where vlocity_cmt__AccountId__c='{accountId}' limit 200"
        res0= query.query(q0)

        inventoryItemIds = [r['Id'] for r in res0['records']]

        if len(inventoryItemIds) >0:
            q01 = f"select fields(all) from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__DestinationInventoryItemId__c in ({query.IN_clause(inventoryItemIds)}) limit 200"
            res01= query.query(q01)
            if dele: self.delete(q01)

        if dele: self.delete(q0)

        q1 = f"select fields(all) from vlocity_cmt__AccountPriceAdjustment__c where vlocity_cmt__BillingAccountId__c ='{accountId}' limit 50"
        res1= query.query(q1)
        if dele: self.delete(q1)

        q2 = f"select fields(all) from vlocity_cmt__AccountAppliedPromotion__c where vlocity_cmt__BillingAccountId__c ='{accountId}' limit 50"
        res2= query.query(q2)
        if dele: self.delete(q2)

        if len(res2['records'])>0:
            q3 = f"select fields(all) from vlocity_cmt__AccountAppliedPromotionItem__c where vlocity_cmt__AppliedPromotionId__c ='{res2['records'][0]['Id']}' limit 50"
            res3 = query.query(q3)
            if dele: self.delete(q3)

        a=1
    def test_select_promoItems(self):
        restClient.init('NOSDEV')


        accountId ='0017a00002IJykLAAT'
        accountId = '0013O00001CoyfqQAB'

        sobjectsToCloneIdsList= query.queryFieldList(f"select Id from asset where accountId='{accountId}'")
        requestedStartDate ='2023-06-20T09:50:36Z'

        q = f"Select fields(all) from vlocity_cmt__AccountAppliedPromotionItem__c  where vlocity_cmt__AssetId__c IN ({query.IN_clause(sobjectsToCloneIdsList)})  AND (vlocity_cmt__AssetId__r.vlocity_cmt__DisconnectDate__c = null OR vlocity_cmt__AssetId__r.vlocity_cmt__DisconnectDate__c >= {requestedStartDate})  AND (vlocity_cmt__AppliedPromotionId__r.vlocity_cmt__CommitmentEndDate__c = null OR vlocity_cmt__AppliedPromotionId__r.vlocity_cmt__CommitmentEndDate__c >= {requestedStartDate})  AND (vlocity_cmt__AppliedPromotionId__r.vlocity_cmt__CancellationDate__c = null OR vlocity_cmt__AppliedPromotionId__r.vlocity_cmt__CancellationDate__c >= {requestedStartDate}) limit 200"

        res = query.query(q)

        for key in res['records'][0].keys():
            print(key)
            
        appliedPromotionIds = [r['vlocity_cmt__AppliedPromotionId__c'] for r in res['records']]

        q2= f"SELECT fields(all) FROM vlocity_cmt__AccountAppliedPromotion__c WHERE  Id IN ({query.IN_clause(appliedPromotionIds)}) AND (vlocity_cmt__CancellationDate__c = null OR vlocity_cmt__CancellationDate__c >= {requestedStartDate}) AND (vlocity_cmt__CommitmentEndDate__c = null OR vlocity_cmt__CommitmentEndDate__c >= {requestedStartDate}) "
        res2 = query.query(q2)
        print('---------------------------------------------------------------')
        for key in res2['records'][0].keys():
            print(key)

        q3 = f"SELECT fields(all) FROM vlocity_cmt__AccountPriceAdjustment__c WHERE vlocity_cmt__AssetId__c IN ({query.IN_clause(sobjectsToCloneIdsList)})  AND (vlocity_cmt__CancellationDate__c = null OR vlocity_cmt__CancellationDate__c >= {requestedStartDate}) AND (vlocity_cmt__EffectiveEndDate__c = null OR  vlocity_cmt__EffectiveEndDate__c >= {requestedStartDate})  AND (( vlocity_cmt__AdjustmentPricingVariableId__r.vlocity_cmt__AppliesToVariableId__c != NULL AND vlocity_cmt__AdjustmentPricingVariableId__r.vlocity_cmt__AppliesToVariableId__r.vlocity_cmt__ChargeType__c != 'One-time')  OR (vlocity_cmt__AdjustmentPricingVariableId__r.vlocity_cmt__AppliesToVariableId__c = NULL AND vlocity_cmt__AdjustmentPricingVariableId__r.vlocity_cmt__ChargeType__c != 'One-time' )) limit 200"
        
        res3 = query.query(q3)
        print('---------------------------------------------------------------')
        for key in res3['records'][0].keys():
            print(key+',')

        a = 1





