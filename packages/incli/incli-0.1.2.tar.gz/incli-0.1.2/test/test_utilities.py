import unittest,simplejson,time
from incli.sfapi import restClient,query,Sobjects,tooling,DR_IP,houseKeep,jsonFile
from deepdiff import DeepDiff
import json

class Test_Utilities(unittest.TestCase):
    def test_executeAnonymous2(self):
        restClient.init('qmscopy')

        accountId = '001AP00000ratpIYAQ'
        code = """
            List<Asset> a = [select id from asset where AccountId = '001AP00000ratpIYAQ'];
            system.debug(a);
            Map<String, Object> repricingInput = new Map<String, Object>{ 'objectList' => a };
            repricingInput.put('repriceProvidedLineItemsOnly', false);
            Map<String, Object> repricingOutput = new Map<String, Object>();
            Map<String, Object> repricingOptions = new Map<String, Object>();
            vlocity_cmt.VOIInvoker voi = vlocity_cmt.VOIInvoker.getInstance();
            voi.invoke('Repricing', 'repriceLineItems', repricingInput, repricingOutput, repricingOptions);
            system.debug(repricingOutput);
            """

        res = tooling.executeAnonymous(code)
        a=1


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
    
    def test_delete_decompostion(self):
        restClient.init('qmscopy')
        orderId = '801AU00000c8LPxYAM'

        houseKeep.delete_decompostion_plan(orderId)

    def test_select(self):
        restClient.init('DEVNOSCAT4')

        q = f"select fields(all) from vlocity_cmt__VlocityTrackingEntry__c order by vlocity_cmt__Timestamp__c desc limit 100"
        res = query.query(q)
        for r in res['records']:
            ll = simplejson.loads(r['vlocity_cmt__Data__c'])
            json_formatted_str = simplejson.dumps(ll, indent=2, ensure_ascii=False)
            print(json_formatted_str)
            print()
            
    def test_check_logs(self):
        restClient.init('org62')
        q = "select Id,name from Timesheet limit 10"
        res =  query.query(q)

        a=1
    def test_delete_logs(self):
        restClient.init('qmscopy')

      #  userId = Sobjects.IdF('user','username:uormaechea@salesforce.com.prd.mpomigra')

       # q = f"select Id from ApexLog where LogUserId='{userId}' "
        q = "select Id from ApexLog where Status ='Success'"
        q = "select Id from ApexLog"

       # q = "select id from ApexLog where LogUser.Username!='autoproc@00d3o0000004pzcuaq'"

        self.delete(q)

        #res = query.query(q)

        #id_list = [record['Id'] for record in res['records']]

        #Sobjects.deleteMultiple('ApexLog',id_list)
        print()

    def delete(self,q,size=200):
        res = query.query(q)

        id_list = [record['Id'] for record in res['records']]
        
        print(f"{q}  --> deleteing {len(id_list)} rows.")

        Sobjects.deleteMultiple('ApexLog',id_list,size)
        print()

    def test_update_records(self):
        #restClient.init('DEVNOSCAT3')

        object = 'vlocity_cmt__OmniScript__c'
        field = 'vlocity_cmt__IsActive__c'
        value = True
        newValue = False

        code = f"""
            List<{object}> recordsToUpdate = [SELECT Id, {field} FROM {object} WHERE {field} = TRUE];

            for ({object} rec : recordsToUpdate) {{
                rec.{field} = {newValue};  
            }}
            update recordsToUpdate;
            """

        res = tooling.executeAnonymous(code)
        a=1
        a= 1

    def test_testEPCOTAddMissingAttributeAssignment(self):
        restClient.init('devcs6')

        #01t3O000006l0ekQAA raro

       # 01t3O00000AZFBoQAP

        code = """
List<Id> productIds = new List<Id>{'a3Z5t0000001GmbEAE'};
EPCOTCreateMissingAttributeAssignment aa = new EPCOTCreateMissingAttributeAssignment(null,false);
Integer batchSize = 20;
Database.executeBatch(aa, batchSize);
"""

        res = tooling.executeAnonymous(code)
        print(res)
        a=1
        a= 1

    def test_testTOMASDelete(self):
        restClient.init('DTI')


        code = """
List<vlocity_cmt__CatalogProductRelationship__c> VCR12243_1 = [select Id from vlocity_cmt__CatalogProductRelationship__c where Name in ('DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2121','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2120','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2127','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2125','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2123','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2130','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2124','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2128','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2119','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2122','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2129','DC_CAT_MPO_CHILD_042_C_NOS_OFFER_2126','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2121','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2120','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2127','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2125','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2123','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2130','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2124','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2128','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2119','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2122','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2129','DC_CAT_MPO_CHILD_044_C_NOS_OFFER_2126','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2135','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2133','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2134','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2144','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2142','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2146','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2140','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2145','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2143','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2136','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2132','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2141','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2139','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2138','DC_CAT_MPO_CHILD_036_C_NOS_OFFER_2137','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2121','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2120','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2127','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2125','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2123','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2130','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2124','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2128','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2119','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2122','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2129','DC_CAT_MPO_CHILD_046_C_NOS_OFFER_2126','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2121','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2120','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2127','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2125','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2123','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2130','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2124','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2128','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2119','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2122','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2129','DC_CAT_MPO_CHILD_047_C_NOS_OFFER_2126','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2135','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2133','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2134','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2144','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2142','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2146','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2140','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2145','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2143','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2136','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2132','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2141','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2139','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2138','DC_CAT_MPO_CHILD_037_C_NOS_OFFER_2137','DC_CAT_MPO_CHILD_026_C_NOS_OFFER_2135','DC_CAT_MPO_CHILD_026_C_NOS_OFFER_2133','DC_CAT_MPO_CHILD_026_C_NOS_OFFER_2134','DC_CAT_MPO_CHILD_026_C_NOS_OFFER_2144','DC_CAT_MPO_CHILD_026_C_NOS_OFFER_2142')];
delete VCR12243_1;
"""
        code = """
    Integer sum = 0;
    for (Integer i = 0; i < 100; i++) {
        system.debug(i);
        sum += i;
    }
"""
        code = """
    Integer sum = 0;
    while (true) {
        sum = sum + 1;
        if (sum == 50000) {
            System.debug(sum);
            sum=0;
        }
    }
"""

        res = tooling.executeAnonymous(code)
        print(res)
        a=1
        a= 1
    def test_testEPCAddMissingAttributeAssignment(self):
        restClient.init('devcs6')
#01t5t000009WP1lAAG
        #01t5t000009XpiDAAS
        code = """
            List<Id> productIds = new List<Id>{'01t5t000009WP1lAAG'};
            EPCCreateMissingAttributeAssignment aa = new EPCCreateMissingAttributeAssignment(productIds,false);
            Integer batchSize = 50;
            Database.executeBatch(aa, batchSize);
            """

        res = tooling.executeAnonymous(code)
        print(res)
        a=1
        a= 1
    def test_ProductConsoleController(self):
        restClient.init('DEVNOSCAT3')

        data = {
            "objectId":"01t3N00000AjB61QAF"
        }

        call = DR_IP.ProductConsoleController(methodName='getAppliedAttributesFields',inner=data)

        a= 1
    def test_check_objectTypes(self):
        restClient.init('devcs6')

        res = query.query('select Id,Name from vlocity_cmt__ObjectClass__c    where vlocity_cmt__ParentObjectClassId__c != null')

        objectclassIds = [r['Id'] for r in res['records']]

        ofas = query.query(f"select Id,vlocity_cmt__AttributeId__c,vlocity_cmt__AttributeId__r.name,vlocity_cmt__ObjectClassId__c,vlocity_cmt__ObjectClassId__r.name  from vlocity_cmt__ObjectFieldAttribute__c   where vlocity_cmt__ObjectClassId__c in ({query.IN_clause(objectclassIds)})  and vlocity_cmt__AttributeId__c != null")

        aas = query.query(f"select Id,name,vlocity_cmt__AttributeId__c,vlocity_cmt__AttributeId__r.name,vlocity_cmt__ObjectId__c from vlocity_cmt__AttributeAssignment__c    where vlocity_cmt__ObjectId__c   in ({query.IN_clause(objectclassIds)}) and vlocity_cmt__AttributeId__c != null")

        for r in res['records']:
            print()
            print(f"{r['Id']}:{r['Name']}")

            s_ofas = [ofa for ofa in ofas['records'] if r['Id'] == ofa['vlocity_cmt__ObjectClassId__c'] ]
            s_aas = [aa for aa in aas['records'] if r['Id'] == aa['vlocity_cmt__ObjectId__c']]

            if len(s_ofas) == 0 and len(s_aas)==0:
                continue

            if len(s_ofas) == 0:
                for s_aa in s_aas:
                    print(f"  AA should not exist: <{s_aa['vlocity_cmt__AttributeId__c']}:{s_aa['vlocity_cmt__AttributeId__r']['Name']}>")
                continue


            if s_ofas[0]['vlocity_cmt__ObjectClassId__c']=='a3Z5t0000001GocEAE':
                a=1

            for s_ofa in s_ofas:
                exits = False
                for s_aa in s_aas:
                    if s_aa['vlocity_cmt__AttributeId__c'] == s_ofa['vlocity_cmt__AttributeId__c']:
                        exits = True
                        break
                if exits == False:
                    print(f"  AA missing:          <{s_ofa['vlocity_cmt__AttributeId__c']}:{s_ofa['vlocity_cmt__AttributeId__r']['Name']}>")

            for s_aa in s_aas:
                exist = False
                for s_ofa in s_ofas:
                    if s_aa['vlocity_cmt__AttributeId__c'] == s_ofa['vlocity_cmt__AttributeId__c']:
                        exist = True
                        break
                if exits == False:
                    print(f"  AA should not exist: <{s_aa['vlocity_cmt__AttributeId__c']}:{s_aa['vlocity_cmt__AttributeId__r']['Name']}>")
            a=1

    def test_deactivate(self):
        """
            List<vlocity_cmt__OmniScript__c> acctList = [SELECT Id,vlocity_cmt__IsActive__c  FROM vlocity_cmt__OmniScript__c LIMIT 2000];

            for(vlocity_cmt__OmniScript__c acct :acctList){
                acct.vlocity_cmt__IsActive__c  = False;
            }

            update acctList;
        """
    def test_delete_allLogs(self):
        restClient.init('mpomigra')

        q = "select Id from ApexLog "

        self.delete(q)

    def test_coult_logs(self):
        restClient.init('DEVNOSCAT3')

        q = "select Count(Id) from ApexLog "

        a=1
        while a==1:
            res = query.query(q)
            print(f"Total logs in the Org-->{res['records'][0]['expr0']}")
            time.sleep(1)

        a=1
    def test_delete_countAllLogs(self):
        restClient.init('NOSQSM')

        q = "select count(Id) from ApexLog "

        res = query.query(q)

        print(f"Total size {res['records'][0]['expr0']}")



    def test_delete_allRows(self):
        restClient.init('NOSQSM')

        q = "select Id from ApexLog where LogUser.Username like 'uor%' "
        q = "select Id from ApexLog  "

        self.delete(q)

    def test_deleteAllRowsObject_multiple(self):
        restClient.init('mpomigra250')
        self.delete("select ID from vlocity_cmt__PriceListEntry__c where vlocity_cmt__PromotionId__r.name like 'TESTb%' and vlocity_cmt__PromotionItemId__c=null ")
       # self.delete("select ID from vlocity_cmt__PriceListEntry__c where vlocity_cmt__PromotionId__r.name like 'TESTb%' and vlocity_cmt__OfferId__c!=null ")

        
     #   self.delete("select Id from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__ObjectId__c like 'a3Z%'")

  #  timez = '2000-12-12T17:19:35Z'

        a=1

    def test_deleteObject_anonymous(self):
        restClient.init('mpomigra')
        object = 'vlocity_cmt__Datastore__c'

        Sobjects.delete_all_async(object)
        a=1

    def test_a(self):
        restClient.init('DTI')
        Sobjects.delete_all_async('vlocity_cmt__CachedAPIResponse__c')


    def test_update_field(self):

      #  code = """--max-old-space-size=4096"""
        code = """  
        String q = 'select Id from product2 where CreatedBy.Username=\\'migration.moon@nos.pt.mpomigra\\' and LastModifiedBy.Username!=\\'uormaechea@salesforce.com.prd.mpomigra\\' limit 1500';
        List<SObject> recordsToUpdate = Database.query(q);
                    
        for (SObject record : recordsToUpdate) {
            record.put('vlocity_cmt__AttributeDefaultValues__c', null);
        }
                    
        update recordsToUpdate;
        """
        
        restClient.init('mpomigra')
        
        res = query.query("select count() from product2 where CreatedBy.Username = 'migration.moon@nos.pt.mpomigra' and LastModifiedBy.Username!= 'uormaechea@salesforce.com.prd.mpomigra' ")

        while (res['totalSize']>0):
            ex = tooling.executeAnonymous(code)
            res = query.query("select count() from product2 where CreatedBy.Username = 'migration.moon@nos.pt.mpomigra' and LastModifiedBy.Username!= 'uormaechea@salesforce.com.prd.mpomigra' ")
            print(res['totalSize'])


        a=1
        

    def test_update_field_2(self):

      #  code = """--max-old-space-size=4096"""
        code = """  
        String q = 'select Id from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__ValueDataType__c = \\'Picklist\\' and CreatedBy.Username=\\'migration.moon@nos.pt.mpomigra\\' and LastModifiedBy.Username!=\\'uormaechea@salesforce.com.prd.mpomigra\\' limit 10000';
        List<SObject> recordsToUpdate = Database.query(q);
                    
        for (SObject record : recordsToUpdate) {
            record.put('vlocity_cmt__ValidValuesData__c', null);
        }
                    
        update recordsToUpdate;
        """
        
        restClient.init('mpomigra')
        
        res = query.query("select Id from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__ValueDataType__c = 'Picklist' and CreatedBy.Username='migration.moon@nos.pt.mpomigra' and LastModifiedBy.Username!='uormaechea@salesforce.com.prd.mpomigra'")

        while (res['totalSize']>0):
            ex = tooling.executeAnonymous(code)
            res = query.query("select Id from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__ValueDataType__c = 'Picklist' and CreatedBy.Username='migration.moon@nos.pt.mpomigra' and LastModifiedBy.Username!='uormaechea@salesforce.com.prd.mpomigra'")            
            print(res['totalSize'])


        a=1

    def test_StandardCPQ(self):
        restClient.init('DEVNOSCAT4')
        Sobjects.delete_all_async('vlocity_cmt__CachedAPIResponse__c')
        Sobjects.delete_all_async('vlocity_cmt__AsyncProcess__c')
        Sobjects.delete_all_async('vlocity_cmt__ConfigurationSnapshot__c')

        code = """
            vlocity_cmt__CpqConfigurationSetup__c configSnapshotLock = vlocity_cmt__CpqConfigurationSetup__c.getInstance('ConfigurationSnapshotLock');

            if(configSnapshotLock==null) {

            configSnapshotLock = new vlocity_cmt__CpqConfigurationSetup__c(

            Name='ConfigurationSnapshotLock', vlocity_cmt__SetupValue__c = 'False');

            }

            configSnapshotLock.vlocity_cmt__SetupValue__c = 'False';

            upsert configSnapshotLock;
            """

        res = tooling.executeAnonymous(code)
        print(res)

    def test_get_All(self):
        restClient.init('DEVNOSCAT3')
        name = 'BASE_V2_4_0'
        houseKeep.get_all(name)


    def test_delete_Account_and_1(self):

        restClient.init('DEVNOSCAT3')

        name = 'BASE_V2_3_0'
        houseKeep.test_delete_Account_and_All(name)

    def test_delete_Account_and_X(self):
        restClient.init('DEVNOSCAT3')
       # self.delete("SELECT Id, Name FROM Account WHERE Id NOT IN ( SELECT AccountId FROM Order) ")
        self.delete("SELECT Id FROM Account WHERE Id NOT IN (SELECT AccountId FROM Order WHERE Status = 'Activated' ) ",size=1)
        self.delete("select Id from vlocity_cmt__VlocityTrackingEntry__c")

    def test_clean_orphans(self):
        restClient.init('DEVNOSCAT3')

        houseKeep.clean_orphans()
        
    def test_b(self):
        restClient.init('DEVNOSCAT2')
        Sobjects.delete_all_async('vlocity_cmt__CachedAPIResponse__c')

    def test_get_orphans(self):
        restClient.init('NOSDEV')
        houseKeep.get_orphans()

    def test_deleteAllRows_multiple(self):
        restClient.init('DEVNOSCAT3')
  #      self.delete("select Id from order ")

        if 1==1:
            self.delete("select Id from vlocity_cmt__OmniScript__c ")
            self.delete("select Id from vlocity_cmt__Element__c ")
            self.delete("select Id from vlocity_cmt__DRMapItem__c ")
            self.delete("select Id from vlocity_cmt__CalculationMatrixRow__c ")
            self.delete("select Id from product2 ")
            self.delete("select Id from PricebookEntry")
            self.delete("select Id from order ")
        self.delete("select Id from vlocity_cmt__ObjectSection__c ")
        self.delete("select Id from vlocity_cmt__ObjectFieldAttribute__c ")
        self.delete("select Id from vlocity_cmt__AttributeAssignment__c ")
        self.delete("select Id from vlocity_cmt__AttributeCategory__c ")
     #   self.delete("select Id from vlocity_cmt__CalculationMatrixRow__c ")
        self.delete("select Id from vlocity_cmt__AsyncProcessJob__c ")
        self.delete("select Id from vlocity_cmt__OrchestrationDependency__c ")
        self.delete("select Id from vlocity_cmt__OrchestrationDependencyDefinition__c ")
        self.delete("select Id from vlocity_cmt__OrchestrationItemDefinition__c ")
        self.delete("select Id from vlocity_cmt__OrchestrationItem__c ")
        self.delete("select Id from vlocity_cmt__OrchestrationScenario__c ")
        self.delete("select Id from vlocity_cmt__OrchestrationPlan__c ")
        self.delete("select Id from vlocity_cmt__DecompositionRelationship__c ")
        self.delete("select Id from vlocity_cmt__ObjectFacet__c ")
        self.delete("select Id from vlocity_cmt__PriceListEntry__c ")
        self.delete("select Id from vlocity_cmt__Attribute__c ")
        self.delete("select Id from vlocity_cmt__ProductChildItem__c ")
        self.delete("select Id from vlocity_cmt__Promotion__c ")
     #   self.delete("select Id from product2 ")
        self.delete("select Id from vlocity_cmt__PriceList__c ")
        self.delete("select Id from vlocity_cmt__OverrideDefinition__c ")
        self.delete("select Id from vlocity_cmt__CatalogProductRelationship__c ")
        self.delete("select Id from vlocity_cmt__CatalogRelationship__c ")
        self.delete("select Id from vlocity_cmt__Catalog__c	 ")
      #  self.delete("select Id from PricebookEntry	 ")
  #      self.delete("select Id from order ")


    def test_fixAttributes(self):
        #Database.executeBatch(new vlocity_cmt.FixProductAttribJSONBatchJob());
        a=1
    def test_delete_anonumexecuteAnonymousus(self):
        restClient.init('DEVNOSCAT2')

        object_name = 'vlocity_cmt__CachedAPIResponse__c'
        code = f"delete[SELECT id FROM {object_name} LIMIT 10000];"

        res = tooling.executeAnonymous(code)
        a=1


    def test_delete_something(self):
        restClient.init('DEVNOSCAT2')
      #  self.delete("select Id from apexlog ")
        self.delete("select Id from vlocity_cmt__CachedAPIResponse__c ")

        s=1

  #  def test_getAssret(self):
  #      q = f"select fields(all) from asset where vlocity_cmt__RootItemId__c='{assetId}' limit 200"

    def test_querySomething(self):
        restClient.init('NOSDEV')
        q = f"select fields(all) from EventLogFile limit 200"

        call = query.query(q)

        print()

    def test_delete_fulfil(self):
        restClient.init('DEVNOSCAT4')

        q = "select Id from vlocity_cmt__FulfilmentRequestDecompRelationship__c  "
        self.delete(q)

        q = "select Id from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c  "
        self.delete(q)
        
        q = "select Id from vlocity_cmt__FulfilmentRequest__c  "
        self.delete(q)

        q = "select Id from vlocity_cmt__InventoryItem__c  "
        self.delete(q)

        q = "select Id from vlocity_cmt__InventoryItemDecompositionRelationship__c  "
        self.delete(q)

        q = "select Id from AssetRelationship  "
        self.delete(q)

        q = "select Id from vlocity_cmt__OrderAppliedPromotionItem__c  "
        self.delete(q)

    def test_call_something(self):
        restClient.init('NOSDEV')

       # res = restClient.requestWithConnection(action='resource/1641908190000/vlocity_cmt__OmniscriptLwcCompiler')
        res = restClient.requestRaw('https://nos--nosqms.sandbox.my.salesforce.com/resource/1641908190000/vlocity_cmt__OmniscriptLwcCompiler')

        print(res)
        print()

    def test_call_REST(self):
        restClient.init('NOSDEV')

       # res = restClient.requestWithConnection(action='resource/1641908190000/vlocity_cmt__OmniscriptLwcCompiler')
        res = restClient.requestRaw(action="")

        print(res)
        print()

    def test_iJoin_code(self):
        restClient.init('NOSQSM')

        name = 'd9b0fe97-8d5a-b2b6-8293-f5abe8f4b675'

        q = f"select name, Content__c from Dataframe__c where name ='{name}' "

        res = query.query(q)

        print(res['records'][0]['Content__c'])
       # print(res)
        print()

    def test_update_something(self):
        restClient.init('NOSQSM')

        Sobjects.update()

    def test_inventory_stuff(self):
        restClient.init('NOSDEV')

        accountId ='0013O00001B0lHvQAJ'

        q = f"select fields(all) from asset where accountid='{accountId}' limit 100"

        call = query.query(q)

        assetIds = [asset['Id'] for asset in call['records']]

        q = f"select fields(all) from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__SourceAssetId__c in ({query.IN_clause(assetIds)}) limit 100"

        call2 = query.query(q)

        sourceInventoryItemIds = [rel['vlocity_cmt__SourceInventoryItemId__c'] for rel in call2['records'] if rel['vlocity_cmt__SourceInventoryItemId__c']!=None]
        destinationInventoryItemIds = [rel['vlocity_cmt__DestinationInventoryItemId__c'] for rel in call2['records'] if rel['vlocity_cmt__DestinationInventoryItemId__c'] != None]

        q = f"select fields(all) from vlocity_cmt__InventoryItem__c where Id in ({query.IN_clause(destinationInventoryItemIds)}) limit 100"

        call3 = query.query(q)

        q= f"select fields(all) from vlocity_cmt__InventoryItem__c  where vlocity_cmt__AccountId__c='{accountId}' limit 100"

        call4 = query.query(q)

        a=1

    def test_storage(self):
        restClient.init('NOSPRD')

        q_total = "SELECT vlocity_cmt__IsActive__c,Name, vlocity_cmt__Type__c, vlocity_cmt__SubType__c, vlocity_cmt__Language__c,  Id,vlocity_cmt__OmniProcessType__c  from vlocity_cmt__OmniScript__c   where vlocity_cmt__OmniProcessType__c = 'OmniScript'"
        res = query.query(q_total)

        q_elements_total = "select count(Id) from vlocity_cmt__Element__c"
        res = query.query(q_elements_total)

        q_unique = "SELECT vlocity_cmt__IsActive__c,Name, vlocity_cmt__Type__c, vlocity_cmt__SubType__c, vlocity_cmt__Language__c,  Id,vlocity_cmt__OmniProcessType__c  from vlocity_cmt__OmniScript__c   where vlocity_cmt__IsActive__c = True and vlocity_cmt__OmniProcessType__c = 'OmniScript'"

        res = query.query(q_unique)

        total_elements = 0

        for omni in res['records']:
            q2 = f" select count(Id) from vlocity_cmt__Element__c where vlocity_cmt__OmniScriptId__c ='{omni['Id']}'"
            res2 = query.query(q2)
            elements = res2['records'][0]['expr0']
            total_elements = total_elements + elements
            print(f"{omni['Name']}  {elements}")
            a=1

        a=1

    def test_storage_orchestration(self):
        restClient.init('NOSPRD')

        plan_id = 'a457T0000015OchQAE'

        q_items = f"select Id,Name from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c = '{plan_id}'"

        r1 = query.query(q_items)

        itemIds = [rec['Id'] for rec in r1['records']]

        q_source = f"select Id,vlocity_cmt__OrchestrationItemId__c,vlocity_cmt__SourceOrderItemId__c from vlocity_cmt__OrchestrationItemSource__c where vlocity_cmt__OrchestrationItemId__c in ({query.IN_clause(itemIds)})"

        r2 = query.query(q_source)

        q_dependency = f"select Id,Name,vlocity_cmt__OrchestrationItemId__c from vlocity_cmt__OrchestrationDependency__c where vlocity_cmt__OrchestrationItemId__c in ({query.IN_clause(itemIds)})"

        r3 = query.query(q_dependency)

        a=1

    def test_ipCallQueueViaRest(self):

        restClient.init('NOSDEV')

        input = {
            'cartId' : '8013O0000053k5yQAA'
        }

        options =  {
            "isDebug": True,
            "chainable": False,
            "resetCache": False,
            "ignoreCache": True,
            "queueableChainable": True,
            "useQueueableApexRemoting": False
        }
        
        for i in range(5): 
            res = DR_IP.remoteClass('ipCallQueueViaRest','unai_chainableIpsTest',input,options)

        a=1


    def test_performance(self):
        def callback(data):
            res = DR_IP.remoteClass('SystemHelper','debug2',data)

        self.test_performance_X(callback)


    def test_performance_ip(self):        
        def callback(data):
            DR_IP.ip('unai_test1',data)
        self.test_performance_X(callback)

    def test_perf_ipSimple(self):
        def callback(data):
            DR_IP.ip('unai_test1Simple',data)
        self.test_performance_X(callback)

    def test_performance_X(self,callback):        
        restClient.init('NOSQSM')

        data = {
            'This':1
        }
        b=1
        total = 0
        while b < 100:
            callback(data)
            print(restClient.getLastCallElapsedTime())
            total = total + restClient.getLastCallElapsedTime()
            b=b+1
        a=1

        print(total/100)

    def test_performance_ip_simple(self):        
        restClient.init('NOSQSM')

        data = {
            'This':1
        }
        b=1
        total = 0
        while b < 100:
            res = DR_IP.ip('unai_test1Simple',data)
            print(restClient.getLastCallElapsedTime())
            total = total + restClient.getLastCallElapsedTime()
            b=b+1
        a=1

        print(total/100)

    def test_rest_getX(self):
        def callback(data):
            action = '/services/apexrest/restTest'
            restClient.callAPI(action,method='get')

        self.test_performance_X(callback)

    def test_rest_post(self):
        def callback(data):
            action = '/services/apexrest/restTest'
            restClient.callAPI(action,method='post',data=data)

        self.test_performance_X(callback)
        
    def test_apex_class_access(self):
        restClient.init('NOSDEV')

        q1 = query.query("SELECT Id, SetupEntityId, Parent.Profile.Name, SetupEntityType FROM SetupEntityAccess WHERE Parent.Profile.Name = 'Onboarding Community Partner'")
        q2 = query.query("SELECT Id, SetupEntityId, Parent.Profile.Name, SetupEntityType FROM SetupEntityAccess WHERE Parent.Profile.Name = 'Onboarding Community Login User'")

        q1_class_ids = [r['SetupEntityId'] for r in q1['records'] if r['SetupEntityType']=='ApexClass']
        q2_class_ids = [r['SetupEntityId'] for r in q2['records'] if r['SetupEntityType']=='ApexClass']

        not_in_1 =[]
        not_in_2 =[]
        for r1 in q1_class_ids:
            if r1 not in q2_class_ids:
                not_in_2.append(r1)

        for r2 in q2_class_ids:
            if r2 not in q1_class_ids:
                not_in_1.append(r2)              
        print(not_in_2)
        print(not_in_1)

        q2_c = query.query(f"select Id,NamespacePrefix,Name,isValid from apexclass where Id in ({query.IN_clause(not_in_1)})")

        for c in q2_c['records']:
            print(f"{c['NamespacePrefix']}   {c['Name']}")

        a=1

    def test_cache(self):
        restClient.init('NOSDEV')

        if 1==1:
            url = 'https://sandeshkul-240219-963-demo.my.site.com/partnercentral'
            url = 'https://nos--nosdev.sandbox.my.site.com/onboarding'
            token_partner = '00D3O0000004pzC!AQkAQJYDW2DwJQPDt22Zp0P.cKbvsyK7SxX.qQkMVnPgP6Yr4VafZncQJ0E8Qb2gC_CmGJNz7jslaEYL9gE_U6lC3IgGlwZd'
            token_partnerOff = '00D3O0000004pzC!AQkAQJyDd1.DKk2gBJKxCKYQphFVSaPxXEBJSs8cOlqm1edWvrRRX4GWjNQTTc9hsojT5RfrJD10fWBkyBZrKuRZ1cQkSAkk'
            token_user ='00D3O0000004pzC!AQkAQECRGLSlJVRpE4e3Ya5EtURjJCE69kP_eIZopONfJSDaVVChPZf2q7W0FjSMi4oxh4QDkPu7QF.yvS.mOcr5Zsqbi_j6'
            token = token_partnerOff
            restClient.initWithToken('xxx',url=url,token=token)
       # else:
       #     restClient.init('demoParner')

        code = """
        Cache.OrgPartition orgPart = Cache.Org.getPartition('AttributePricingPartition');

        Object cachedData = orgPart.get('cacheKey');
        System.debug(cachedData);
        orgPart.put('cacheKey','cacheValue');
        system.debug(orgPart.get('cacheKey'));
        orgPart.remove('cacheKey');
        """

        #code  = "String a='a';"
        res = tooling.executeAnonymous(code)

        print(res)

        a=1

    def test_activate_omnis(self):
        restClient.init('DEVNOSCAT3')

        res = query.query("select Id,vlocity_cmt__IsActive__c,vlocity_cmt__Version__c,vlocity_cmt__Type__c,name,vlocity_cmt__OmniProcessType__c  from vlocity_cmt__OmniScript__c  order by vlocity_cmt__Version__c desc")

        donelist = []
        records = []
        for r in res['records']:
            xn = f"{r['vlocity_cmt__OmniProcessType__c']}{r['vlocity_cmt__Type__c']}{r['Name']}"
            if xn not in donelist:
                print(xn)
                donelist.append(xn)
                records.append(r)

        for r in records:
            if r['vlocity_cmt__IsActive__c'] == True:
                continue
            r['vlocity_cmt__IsActive__c'] = True
            Id = r['Id']
            r.pop('Id')
            r.pop('vlocity_cmt__Version__c')
            r.pop('vlocity_cmt__Type__c')
            r.pop('Name')
            r.pop('vlocity_cmt__OmniProcessType__c')

            Sobjects.update(Id,r,'vlocity_cmt__OmniScript__c')
        a=1

    def test_rowLock(self):
        restClient.init('NOSDEV')

        orderId = '801AU00000LUpH7YAL'



        code = f"""
List<Order> orderList = [SELECT Id FROM Order WHERE Id = '{orderId}' FOR UPDATE];
system.debug(orderList);
        """

        for i in range(0,10000):
            res = tooling.executeAnonymous(code)
            print(res)
            time.sleep(1)


       # res = tooling.executeAnonymous(code)
       # print(res)
        a=1

    def test_read_allproducts(self):
        restClient.init('qmscopy')

        res = query.query('select id,vlocity_cmt__JSONAttribute__c from product2')
        jsonFile.write('allProducts',res['records'])
        
        a=1

    def test_delete_json(self):

        restClient.init('qmscopy')

        code = """
                List<Product2> allProducts = [SELECT Id, vlocity_cmt__JSONAttribute__c,ExternalId FROM Product2 where ExternalId = null order by Id limit 400];
                System.debug(allProducts.size());
                for (Product2 prod:allProducts) {
                    prod.vlocity_cmt__JSONAttribute__c = null;
                    prod.ExternalId = 'Done';
                }

                update allProducts;
            """

        while True:
            res = tooling.executeAnonymous(code)
            rr = query.query('SELECT count(Id) FROM Product2 where ExternalId = null ')
            print(rr['records'][0]['expr0'])
            if rr['records'][0]['expr0'] == 0:
                break

    def test_delete_json_desc(self):

        restClient.init('qmscopy')

        code = """
                List<Product2> allProducts = [SELECT Id, vlocity_cmt__JSONAttribute__c,ExternalId FROM Product2 where ExternalId = null order by Id desc limit 100];
                System.debug(allProducts.size());
                for (Product2 prod:allProducts) {
                    prod.vlocity_cmt__JSONAttribute__c = null;
                    prod.ExternalId = 'Done';
                }

                update allProducts;
            """

        while True:
            res = tooling.executeAnonymous(code)
            rr = query.query('SELECT Id FROM Product2 where ExternalId = null ')
            if len(rr['records']) == 0:
                break

    def test_diff(self):
        with open("/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_bt_res.json") as f1, open("/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_reduced_res.json") as f2:
            json1 = json.load(f1)
            json2 = json.load(f2)

        diff = DeepDiff(json1, json2, ignore_order=True)
        print(diff)

    def test_diff_1(self):
        filename2 = '/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_bt_res.json'
        filename1 = '/Users/uormaechea/Documents/Dev/python/InCliLib/incli/output/getItems_reduced_res.json'
        outputfilename = ''

        a1 = jsonFile.read(filename1)
        a2 = jsonFile.read(filename2)

        b1 = a1['records'][0]

        for r in a2['records']:
            if r['ProductCode'] == a1['records'][0]['ProductCode']:
                b2 = r


        ddiff = DeepDiff(b1, b2, ignore_order=False)
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
                item['item']=self._getItem_at_path(b1,item['path'])

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
        jsonFile.write(outputfilename,d)

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