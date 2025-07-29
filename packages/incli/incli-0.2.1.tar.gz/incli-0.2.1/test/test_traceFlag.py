import unittest

##from InCli import InCli
from incli.sfapi import file,restClient,tooling,Sobjects,utils,traceFlag,query,DR_IP

class Test_TraceFlag(unittest.TestCase):
    def test_set_InCli_for_user(self):
        restClient.init('NOSDEV')

     #   userId = Sobjects.IdF('User','username:uormaechea_nosdev@nos.pt')
        userF='username:pvg@optimus.force.com.nosdev'
        InCli_trace_flags = traceFlag.get_InCli_traceflags_for_user(userF)

        if InCli_trace_flags == None:
            InCli_trace_flags = traceFlag.create_trace_flag_incli_f(userF)

        InCli_trace_flags = traceFlag.get_InCli_traceflags_for_user(userF)

        InCli_trace_flags = traceFlag.update_trace_flag_incli(InCli_trace_flags['Id'])

        traceFlag.delete_trace_Flag(InCli_trace_flags['Id'])

        print()

    def test_create_debug_level(self):
        restClient.init('DTI')
        traceFlag.create_debug_level_incli()

    def test_set_incli_traceFlag_for_user(self):
        restClient.init('DTI')

        userF = "username:onboarding@nosdti-parceiros.cs109.force.com"
        traceFlag.set_incli_traceFlag_for_user(userF)

    def test_debuglevel_get(self):
        restClient.init('NOSDEV')

        call = tooling.tooling_IdF('DebugLevel',"DeveloperName:XXXX")   
        self.assertTrue(call==None)

        id = tooling.tooling_IdF('DebugLevel',"DeveloperName:InCli")   
        if id != None:
            tooling.tooling_delete('DebugLevel',id)
            id = tooling.tooling_IdF('DebugLevel',"DeveloperName:InCli")   

            print()
        if id == None:
            tooling.create_debug_level_incli()
            print()


    def test_query_using_incli(self):
        restClient.init('NOSDEV')
        debuglevel_ids = traceFlag.get_InCli_debuglevelIds()
        user_ids = traceFlag.get_InCli_usersIds(debuglevel_ids)

        
        q1 = f"select username from User where Id in ({query.IN_clause(user_ids)})"
        res1 = query.query(q1)
        print()

    def test_query_who(self):

        envs = ['DTI',"NOSDEV","NOSQSM","NOSPRD"]
        for env in envs:
            try:
                restClient.init(env)

                DebugLevelId = tooling.IdF('DebugLevel',"DeveloperName:InCli")   
                q = f"select TracedEntityId,StartDate,ExpirationDate from TraceFlag where DebugLevelId='{DebugLevelId}' limit 100"

                res =tooling.query(q)
                q1 = f"select username from User where Id='{res['records'][0]['TracedEntityId']}'"
                res1 = query.query(q1)
                print()
                print(f'Environment: {env}')
                utils.printFormated(res1['records'])
            except Exception as e:
                utils.printException(e)

        print()

    def test_completions(self):
        restClient.init('NOSDEV')
        tooling.completions()

    def test_aync(self):
        restClient.init('DEVNOSCAT4')
        tooling.executeAnonymous()

    def test_aync_EPCProductAttribJSONBatchJob(self):
        restClient.init('NOSDEV')
        code = """
        List<Id> productIds = new List<Id>();
      //  for (Product2 prod : [ Select Id from Product2 where vlocity_cmt__ObjectTypeId__c!= null ]) {
      //      productIds.add(prod.Id);}
        productIds.add('01t3O0000053k50QAA');
        Database.executeBatch(new vlocity_cmt.EPCProductAttribJSONBatchJob(productIds), 1);
        """
        tooling.executeAnonymous(code)

    def test_aync_EPCFixCompiledAttributeOverrideBatchJob(self):
        restClient.init('DEVNOSCAT2')
        code = """
        Database.executeBatch(new vlocity_cmt.EPCFixCompiledAttributeOverrideBatchJob (), 1);
        """
        tooling.executeAnonymous(code)

    def test_limitUsageHistory(self):
        restClient.init('NOSDEV')

        q = "select fields(all) from NetworkPublicUsageDailyMetrics limit 10 "

        res = tooling.query(q)

        print()

    def test_aync_CleanBasketFiles(self):
        restClient.init('DEVNOSCAT4')
        code = """
        Datetime inputDateTime = Datetime.newInstance(2023, 05, 27); 
        BasketCleaner cleaner = new BasketCleaner(inputDateTime);
        Database.executebatch(cleaner, 1);
        """
        tooling.executeAnonymous(code)

    def test_aync_Debug_BasketFiles_dates(self):
        restClient.init('DEVNOSCAT4')
        code = """
        Datetime inputDateTime = Datetime.newInstance(2023, 03, 1); 
        BasketCleaner cleaner = new BasketCleaner(inputDateTime);
        cleaner.debug_files_dates(90);
        """
        tooling.executeAnonymous(code)

    def test_aync_Debug_BasketFiles_dates(self):
        restClient.init('DTI')
        code = """
        system.debug('a');
        """
        res = tooling.executeAnonymous(code)

        a=1

    def test_ApexExecutionOverlayAction_class(self):
        restClient.init('NOSDEV')

        res = tooling.query("select Id from ApexExecutionOverlayAction where ExecutableEntity.Name = 'SystemHelper'")
        for rec in res['records']:
            res1 = tooling.delete('ApexExecutionOverlayAction',rec['Id'])
            print(res1)
        
        connection = restClient.getCurrentThreadConnection()

        script = "System.debug('[Line 29] CPU: ' + Limits.getCpuTime() + '; DB: ' + Limits.getDatabaseTime() + '; Heap: ' + Limits.getHeapSize());"

     #   script = "System.debug('we are here:'+Limits.getHeapSize() + ' ' +inputMap);"
        script = "System.debug('inputMap');"
        script = None

    #    tooling.ApexExecutionOverlayResult_class('SystemHelper',connection['username'],script,29,IsDumpingHeap=True)

        tooling.ApexExecutionOverlayAction_class('SystemHelper',connection['username'],script,29,IsDumpingHeap=True)

        a =  1

    def test_ApexExecutionOverlayAction_heap_result(self):
        restClient.init('DEVNOSCAT3')

        tooling.ApexExecutionOverlayResult_Heap('XOMDecompV2MainManager')
    
    def test_setHeapOverlay(self):        
        restClient.init('DEVNOSCAT3')

        tooling.ApexExecutionOverlayAction_heap('XOMDecompV2MainManager','433')
