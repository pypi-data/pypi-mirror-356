from incli.sfapi import restClient ,utils,file,jsonFile,query,thread,Sobjects,digitalCommerce,DR_IP
import simplejson,difflib

import unittest,logging,os,shutil,time

class Test_RestClient(unittest.TestCase):
    def call_ServicesData(self):
        action = '/services/data'
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)  


    def test_goToken(self):
        restClient.init('DEVNOSCAT3')
        print(simplejson.dumps(restClient._initializedConnections[0],indent=4))    

    def test_configFile(self):
        restClient.setLoggingLevel(logging.INFO)
        try:
            restClient.setConfigFile('sss')
        except Exception as e:
            utils.printException(e)
            self.assertTrue(e.args[0]['errorCode'] == 'NO_CONFIG')

        restClient.setConfigFile('/Users/uormaechea/Documents/Dev/python/Industries/config/ConnectionsParams.json')

        try:
            restClient.initWithConfig('XXXX')
        except Exception as e:
            utils.printException(e)
            self.assertTrue(e.args[0]['errorCode'] == 'NO_ORG')

        try:
            restClient.initWithConfig('DEVCS9')

            print(restClient._initializedConnections[0]['access_token'])
            self.assertTrue(restClient._currentConnectionName=='DEVCS9')

            folder = restClient.debugFolder()

            st = '2222222'
            file.write(f"{folder}test.txt",st)
            st2 = file.read(f"{folder}test.txt")
            self.assertTrue(st==st2)

            
        except Exception as e:
            utils.printException(e)
            self.assertTrue(1==2)
        print()

    def test_debug_action(self):
     #   restClient.setConfigFile('/Users/uormaechea/Documents/Dev/python/Industries/config/ConnectionsParams.json')
        restClient.init("DEVNOSCAT2")   
        action = '/services/data'

        #Test  callAPI_debug 
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)    
        restClient.callSave("testFile")
        lc = restClient.lastCall()

        self.assertTrue('responseFilePath' in lc)
        fileContent = jsonFile.read(lc['responseFilePath'])

        self.assertEqual(call,fileContent)

        q = query.query(" select fields(all) from Account limit 1")
        print(q)

 
    def test_debug_guest(self):
        restClient.setConfigFile('/Users/uormaechea/Documents/Dev/python/Industries/config/ConnectionsParams.json')

        restClient.initWithConfig('NOSDEV_Partner')
        action = '/services/data'
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)    

        try:
            q = query.query(" select fields(all) from Account limit 1")
        except Exception as e:
            utils.printException(e)
            self.assertTrue(e.args[0]['errorCode'] ==  'HTTPs Error: 401')

    def test_authenticate(self):
        consumerKey = "3MVG90J3nJBMnqrQ.7tXwQ6mdD2sMudQVPWQWPSDE4MaLjTIF7EusaVt2DW2di0MLPxRKeEifOtz0sik0XV1H"
        consumerSecret = "9FDF26CCC4765814B582A07AC7AD68F2ABF3AF765A325E07A986B6C255890CA7"
        restClient.authenticate(client_id=consumerKey,client_secret=consumerSecret,username='partner.unai.nosdev@nos.pt',password='Kamilo123!',isSandbox=True)
        a=1

    def test_debug_withToken(self):
        restClient.setLoggingLevel(logging.DEBUG)
        restClient.init('DEVNOSCAT2')
        
        action = '/services/data'

        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)  
        
        url = restClient._initializedConnections[0]['instance_url']
        token = restClient._initializedConnections[0]['access_token']
    
        restClient.initWithToken('test',url,token=token)
        self.assertTrue(restClient._currentConnectionName == 'test')
        call = restClient.callAPI(action)
        self.assertTrue(len(call)>0)  

        q = query.query(" select fields(all) from Order limit 1")
        print(q)

    def test_debug_threaded(self):
        restClient.init("DEVNOSCAT2") 

        a = [1]*100

        allTimes = []
        def doWork(a):
            action = '/services/data'
            call = restClient.callAPI(action)
            times= {
                "elapsed":restClient.lastCall()
            } 
            allTimes.append(times)

        thread.processList(doWork,a,10)

        utils.printFormated(allTimes)

    def test_login_sfdx(self):
        try:
            outputs = utils.executeCommandParse(["sfdxXXXX","auth:web:login","-r", "https://nos--devnoscat2.sandbox.my.salesforce.com"])
        except Exception as e:
            self.assertTrue(e.strerror ==  'No such file or directory')
            utils.printException(e)

        try:
            restClient.init("xxx.xxx@nos.pt")

        except Exception as e:
            self.assertTrue(e.args[0]['errorCode'] ==  'ConnectionError')
            utils.printException(e)

        try:            
            restClient.init("uormaechea.devnoscat2@nos.pt")
            q = query.query(" select fields(all) from Order limit 1")
            lc = restClient.lastCall()
            self.assertEqual(lc['status_code'],200)
            print(q)

        except Exception as e:
            self.assertEqual('This','Should not happen')

    def test_sfdx_env(self):
        try:
            outputs = utils.executeCommandParse(["sfdx","force:org:display","-u", "DEVNOSCAT2"])
        except Exception as e:
            self.assertTrue(e.strerror ==  'No such file or directory')
            utils.printException(e)

        try:
            restClient.init("DEVNOSCAT2")

        except Exception as e:
            self.assertTrue(e.args[0]['errorCode'] ==  'ConnectionError')
            utils.printException(e)

        try:            
            restClient.init("uormaechea.devnoscat2@nos.pt")
            q = query.query(" select fields(all) from Order limit 1")
            lc = restClient.lastCall()
            self.assertEqual(lc['status_code'],200)
            print(q)

        except Exception as e:
            self.assertEqual('This','Should not happen')

    def test_congifData(self):        
        return
        dir = os.path.abspath("tmp")
        try:
            os.mkdir(dir)
        except Exception as e:
            self.assertTrue(e.strerror=='File exists')
        os.chdir(dir)
        current = os.getcwd()

        config = restClient.loadConfigData()

        self.assertTrue('orgs' in config)
        self.assertTrue(file.exists(restClient._configDataName))

        shutil.rmtree(current)


    def test_saveOrg(self):
        restClient.init("DEVNOSCAT2") 

        url = restClient._initializedConnections[0]['instance_url']
        token = restClient._initializedConnections[0]['access_token']

        restClient.saveOrg_inConfigFile('test1',url,token)
        restClient.initWithConfig('test1')
        self.assertTrue(restClient._currentConnectionName=='test1')
        self.call_ServicesData()

        restClient.saveOrg_inConfigFile('testGuest',url)
        restClient.initWithConfig('testGuest')
        self.assertTrue(restClient._currentConnectionName=='testGuest')
        self.call_ServicesData()
        try:
            q = query.query(" select fields(all) from Order limit 1")
        except Exception as e:
            self.assertEqual(e.args[0]['errorCode'],'HTTPs Error: 401')
            utils.printException(e)

    def test_saveDeleteOrg(self):
        restClient.saveOrg_inConfigFile('test1','xxx','yyyy')

        cd = restClient.loadConfigData()
        org = [i for i in cd['orgs'] if (i['name'] == 'test1')][0]
        self.assertTrue(org['name'] == 'test1')
        restClient.deleteOrg_inConfigFile('test1')
        cd = restClient.loadConfigData()
        org = [i for i in cd['orgs'] if (i['name'] == 'test1')]
        self.assertTrue(len(org)==0)
        print()


    def test_connection_error(self):
        restClient.init('DTI')

        while 1==1:
            print('calling')
            res = query.query("select Id from Account limit 10")
            print(f'got response {res}')
            time.sleep(3)


    def select_count(self,objectName):
        q= query.query(f"select count(Id) from {objectName} ")

        print(f'{objectName}   {q["records"][0]["expr0"]}')

            
    def test_permission_error(self):

        url = 'https://nos--nosdev.sandbox.my.site.com/onboarding/'
        token = '00D3O0000004pzC!AQkAQD9oXu2pKay6mhxw5nR.IaEUMBR11v9YtXPb4wahM3t0jqW0YMrxZWF0XQU_eQkmh7r2AecxKNRlCM1iVnHnCC.553bg'
        token_user ='00D3O0000004pzC!AQkAQCxVZDZ0lafKu48TdKODht_iFws3V0xmXppGsaju4It4WjmnXvyY8ni4ixXt3HpFv983PLjE.t.IESLhFA0HVmpdlIBp'
        token_partner = '00D3O0000004pzC!AQEAQOttRfXLK3JV9zzmFKFdwMfbnlFexEItnrVwvmrJHYkVTR3v4gUfOnGhmVapwdMpPOEIaZ83Q4pkBqQ.6bslUQFX8tZh'

        token = token_partner


        restClient.initWithToken('xxx',url=url,token=token)
      #  restClient.init('NOSDEV')

        #q= query.query(f"select fields(all) from Order where Id = '{orderId}'")
    #    q= query.query(f"select fields(all) from Order where Id = '8013O000004IMJ7QAO' limit 1")

        res = query.query("select count() from orderitem")
        self.select_count('Order')


        data = {
            "variables" : {
            "ReservedSchedule" : "",
            "InquiryID" : ""
            },
            "technologyCode" : "FTTHNOS",
            "technology" : "FTTH",
            "scheduleContact" : "",
            "salesChannel" : "TLMK-O",
            "salesAgent" : "fcguedes",
            "resourceAccessPoint" : 10019593336,
            "originCAV" : "81003460-Fernanda Guedes",
            "orderType" : "DESLIGAMENTO",
            "omniInstanceId" : "a3lAU000000EdRJYA0",
            "mainContactPhone" : "920426636",
            "mainContactEmail" : "testingstreamnos+resdvyv@gmail.com",
            "loyaltyPenalty" : "",
            "loyaltyExclusionReason" : "",
            "immediateInactivation" : "",
            "disconnectReason" : "",
            "deactivationDate" : "2024-06-05T00:00:00.000Z",
            "dataframeId" : "6342be89-8b0e-4550-3ede-feac5f9d4fbc",
            "coverageReturnCable" : "true",
            "automaticScheduleMotive" : "SEM EQUIPAMENTOS OBRIGATÓRIOS",
            "automaticSchedule" : True,
            "assetId" : "02iAU000000u6cIYAQ",
            "agentIU" : 81003460.337,
            "agentCompany" : "Select",
            "User" : "fcguedes",
            "UNISkipNotification" : False,
            "Team" : "Supervisão SCFA",
            "ServiceAccount" : "S1000083356",
            "ScheduleComments" : "",
            "Reason" : "Cliente quer desligar",
            "PaperlessProc" : False,
            "OriginatingChannel" : "TLMK-O",
            "NIF" : "180818570",
            "ManualSale" : "",
            "InstallationAddress" : {
            "Street" : "Rua Joaquim Aires Lopes",
            "PostalCode" : "4520-027",
            "Floor" : "2 X",
            "Door" : "267",
            "City" : "Escapães"
            },
            "GlobeProccessId" : "PRC100040383",
            "CustomerInfo" : {
            "Name" : "TESTTEAM DCFIM",
            "NIF" : "180818570",
            "DocId" : "31688006"
            },
            "CoverageVoDFlag" : "true",
            "CoverageHeadendNumber" : "999",
            "CoverageEligibilityStatus" : "A",
            "CoverageDistributionID" : "",
            "CoverageCellId" : "06",
            "CallSysType" : "Parceiros",
            "CallID" : "9nnda.mp3",
            "CAVTeam" : "",
            "CAVNetwork" : "SOHO",
            "CAVChannel" : "TLMK-O",
            "CAV" : "81003460",
            "BillingData" : [ {
            "BICSWIFT" : "BESCPTP0",
            "BillAddressBuilding" : "2 X",
            "BillAddressCity" : "ESCAPÃES",
            "BillAddressCountry" : "Portugal",
            "BillAddressID" : "10019593336",
            "BillAddressName" : "RUA JOAQUIM AIRES LOPES   267",
            "BillAddressState" : "ESCAPÃES",
            "BillAddressZipCode" : "4520-027",
            "BillType" : "Eletrónica",
            "EletronicInvoiceEmail" : "",
            "EletronicInvoiceNumber" : "",
            "Foreign" : False,
            "IBAN" : "PT50000741462274783380154",
            "InvoiceDetail" : "Resumida",
            "PaymentMethod" : "DIRECT_DEBIT"
            } ],
            "AgentEntity" : "200044-Select",
            "AddressName" : "Rua Joaquim Aires Lopes, 267, 2 X, 4520-027 ESCAPÃES"
        }

        options = {
            "isDebug": True,
            "chainable": True,
            "resetCache": False,
            "ignoreCache": True,
            "queueableChainable": False,
            "useQueueableApexRemoting": False
        } 
        
        r = DR_IP.ip(name='MACD_nosTermination',input=data,options=options)

        ff = jsonFile.write('ddd',r)

        input = r['IPResult']['CreateFdo_RADebug']['Input']

        r1 = DR_IP.dr(bundleName='',inputData=input)

        a=1
        
       ## order = query.query(f"select fields(all) from Order where Id='8013O0000053OEgQAM' limit 1")
       ## print(order)

       ## ff = jsonFile.write('ddd',order['records'][0])

      #  q= query.query(f"select fields(all) from vlocity_cmt__CachedAPIResponse__c where Id='a1S3O000004ByFYUA0' limit 100")
        self.select_count('vlocity_cmt__CachedAPIResponse__c')

        self.select_count("Account")
        self.select_count("product2")
        self.select_count("vlocity_cmt__catalogproductrelationship__c")
        self.select_count("vlocity_cmt__CachedAPIResponse__c")
        self.select_count("vlocity_cmt__CachedAPIResponseOffers__c")
        self.select_count("vlocity_cmt__CachedAPIMigrate__c")


        data =  {
            #'vlocity_cmt__CartIdentifier__c':q['records'][0]['vlocity_cmt__CartIdentifier__c']
            'vlocity_cmt__CartIdentifier__c':'ThisIsIt'

        }

        data = {
            # "vlocity_cmt__OrderTotal__c": 0.00,
            # "vlocity_cmt__StatusImageName__c": "Draft",
            "vlocity_cmt__IsActiveOrderVersion__c": False,
            "vlocity_cmt__OrderStatus__c": "Ready To Submit",
            # "NOS_TenMinuteScheduled__c": "2024-02-09T14:52:23.226Z",
            # "vlocity_cmt__EffectiveRecurringTotal__c": 0.00,
            # "OrderNumber": "00220848",
            "vlocity_cmt__IsChangesAllowed__c": True,
            # "vlocity_cmt__OneTimeTotal__c": 0.00,
            "NOS_t_CustomerOldness__c": "NEW",
            "NOS_b_LCETermsAccepted__c": False,
            "NOS_b_FraudAddressFlag__c": False,
            "vlocity_cmt__EffectiveUsageCostTotal__c": 0.00,
            "vlocity_cmt__RequestedStartDate__c": "2024-02-09T15:42:22.000Z",
            "State__c": "Em Carrinho",
            "IsChangeNumber__c": False,
            "Status": "Draft",
            "NOS_b_IsUserAccept__c": False,
            # "IsDeleted": False,
            # "vlocity_cmt__IsValidated__c": False,
            "vlocity_cmt__EffectiveRecurringCostTotal__c": 0.00,
            ##"IsReductionOrder": False,
            # "TotalContractRevenue__c": 0.00,
            "vlocity_cmt__JeopardySafetyIntervalUnit__c": "Seconds",
            "vlocity_cmt__ExternalPricingStatus__c": "Not Ready",
            # "vlocity_cmt__AccountRecordType__c": "Consumer",
            "vlocity_cmt__DefaultCurrencyPaymentMode__c": "Currency",
            "vlocity_cmt__OrderMarginTotal__c": 0.00,
            "NOS_b_CoverageReturnCable__c": False,
            "NOS_b_CoverageVoDFlag__c": False,
            "vlocity_cmt__EffectiveUsagePriceTotal__c": 0.00,
            "vlocity_cmt__EffectiveOneTimeCostTotal__c": 0.00,
            "vlocity_cmt__OneTimeTotal2__c": 0.00,
            "NOS_b_AutomaticScheduling__c": False,
            # "MonthlyContractRevenue__c": 0.00,
            "vlocity_cmt__EffectiveOneTimeLoyaltyTotal__c": 0,
            "OwnerId": "0053O000006cJuJQAU",
            "vlocity_cmt__ForceSupplementals__c": False,
            "RecordTypeId": "0123O000000ZhSrQAK",
            "NOS_t_ValidateSLA__c": True,
            "NOS_t_BusinessScenario__c": "BS_STANDARD_CHANGE",
            "NOS_b_ImmediateInactivation__c": False,
            "vlocity_cmt__RequestDate__c": "2024-02-09T00:00:00.000Z",
            #"NumberOfItemsActivated__c": 0,
            #"SystemModstamp": "2024-02-09T15:42:23.000Z",
            "NOS_b_6ChannelsOffer__c": False,
            "Type": "INSTALAÇÃO",
            "NOS_b_SkipInquiry__c": False,
            "NOS_b_ReversionFlag__c": False,
            #"vlocity_cmt__TotalMonthlyDiscount__c": 0.00,
            "AccountId": "0013O000013YjADQA0",
            "NOS_b_IsBSimulation__c": False,
            "StatusCode": "Draft",
            "Name": "EcommerceOrder",
            "NOS_b_StockValidation__c": True,
            "vlocity_cmt__FulfilmentStatus__c": "Draft",
            "vlocity_cmt__CreatedByAPI__c": False,
            "SkippedNotification__c": False,
            # "MonthlyContractCost__c": 0.00,
            # "vlocity_cmt__TotalOneTimeDiscount__c": 0.00,
            "vlocity_cmt__OriginatingChannel__c": "Call Center",
            "vlocity_cmt__UsageMarginTotal__c": 0.00,
            #"NonRecurringContractRevenue__c": 0.00,
            "vlocity_cmt__DeliveryMethod__c": "In Store",
            # "vlocity_cmt__AccountId__c": "0013O000013YjAD",
            "vlocity_cmt__RecurringMarginTotal__c": 0.00,
            "vlocity_cmt__PriceListId__c": "a4j3O0000000X0zQAE",
            "vlocity_cmt__IsContractRequired__c": False,
            "Activated__c": False,
            "NOS_t_DataIdentify__c": False,
            "vlocity_cmt__IsChangesAccepted__c": False,
            "NOS_b_IsPortfolioChanged__c": False,
            "Pricebook2Id": "01s3O000000ozfFQAQ",
            "NOS_b_InactiveAddressFlag__c": False,
            # "vlocity_cmt__EffectiveOneTimeTotal__c": 0.00,
            "vlocity_cmt__OneTimeMarginTotal__c": 0.00,
            # "NonRecurringContractCost__c": 0.00,
            "vlocity_cmt__RecurringTotal2__c": 0.00,
            # "CommissionableMonthlyMargin__c": 0.00,
            "NOS_b_OccupiedAddressFlag__c": False,
            "vlocity_cmt__CartIdentifier__c": "52a99ef5-aae1-b7e3-8 (16 more) ...",
            # "vlocity_cmt__EffectiveOrderTotal__c": 0.00,
            # "vlocity_cmt__RecurringTotal__c": 0.00,
            # "TotalContractCost__c": 0.00,
            "vlocity_cmt__OneTimeLoyaltyTotal__c": 0,
            "NOS_b_StoreProductsReadyToAssetize__c": False,
            # "vlocity_cmt__JeopardyStatus__c": "Green",
            #"NonRecurringContractMargin__c": 0.00,
            # "vlocity_cmt__Pricebook__c": "Standard Price Book",
            ##"TotalAmount": 0.00,
            # "MonthlyContractMargin__c": 0.00,
            # "NumberOfItemsOpen__c": 0,
            "NOS_b_LoyaltyPenalty__c": False,
            # "TotalContractMargin__c": 0.00,
            "COM_ActivationEventExpired__c": False,
            "NOS_b_OngoingOrders__c": False,
            # "vlocity_cmt__IsPriced__c": False,
            "vlocity_cmt__IsSyncing__c": False,
            "EffectiveDate": "2024-02-09T00:00:00.000Z"
        }
        
        data = {
  "vlocity_cmt__IsActiveOrderVersion__c": False,
  "vlocity_cmt__OrderStatus__c": "Ready To Submit",
  "vlocity_cmt__IsChangesAllowed__c": True,
  "NOS_t_CustomerOldness__c": "NEW",
  "NOS_b_LCETermsAccepted__c": False,
  "NOS_b_FraudAddressFlag__c": False,
  "vlocity_cmt__EffectiveUsageCostTotal__c": 0.00,
  "vlocity_cmt__RequestedStartDate__c": "2024-02-09T15:42:22.000Z",
  "State__c": "Em Carrinho",
  "IsChangeNumber__c": False,
  "Status": "Draft",
  "NOS_b_IsUserAccept__c": False,
  "vlocity_cmt__EffectiveRecurringCostTotal__c": 0.00,
  "vlocity_cmt__JeopardySafetyIntervalUnit__c": "Seconds",
  "vlocity_cmt__ExternalPricingStatus__c": "Not Ready",
  "vlocity_cmt__DefaultCurrencyPaymentMode__c": "Currency",
  "vlocity_cmt__OrderMarginTotal__c": 0.00,
  "NOS_b_CoverageReturnCable__c": False,
  "NOS_b_CoverageVoDFlag__c": False,
  "vlocity_cmt__EffectiveUsagePriceTotal__c": 0.00,
  "vlocity_cmt__EffectiveOneTimeCostTotal__c": 0.00,
  "vlocity_cmt__OneTimeTotal2__c": 0.00,
  "NOS_b_AutomaticScheduling__c": False,
  "vlocity_cmt__EffectiveOneTimeLoyaltyTotal__c": 0,
  "vlocity_cmt__ForceSupplementals__c": False,
  "RecordTypeId": "0123O000000ZhSrQAK",
  "NOS_t_ValidateSLA__c": True,
  "NOS_t_BusinessScenario__c": "BS_STANDARD_CHANGE",
  "NOS_b_ImmediateInactivation__c": False,
  "vlocity_cmt__RequestDate__c": "2024-02-09T00:00:00.000Z",
  "NOS_b_6ChannelsOffer__c": False,
  "Type": "INSTALAÇÃO",
  "NOS_b_SkipInquiry__c": False,
  "NOS_b_ReversionFlag__c": False,
  "AccountId": "0013O00001KxPXnQAN",
  "NOS_b_IsBSimulation__c": False,
 # "StatusCode": "Draft",
  "Name": "EcommerceOrder",
  "NOS_b_StockValidation__c": True,
  "vlocity_cmt__FulfilmentStatus__c": "Draft",
  "vlocity_cmt__CreatedByAPI__c": False,
  "SkippedNotification__c": False,
  "vlocity_cmt__OriginatingChannel__c": "Call Center",
  "vlocity_cmt__UsageMarginTotal__c": 0.00,
  "vlocity_cmt__DeliveryMethod__c": "In Store",
  "vlocity_cmt__RecurringMarginTotal__c": 0.00,
  "vlocity_cmt__PriceListId__c": "a4j3O0000000X0zQAE",
  "vlocity_cmt__IsContractRequired__c": False,
  "Activated__c": False,
  "NOS_t_DataIdentify__c": False,
  "vlocity_cmt__IsChangesAccepted__c": False,
  "NOS_b_IsPortfolioChanged__c": False,
  "Pricebook2Id": "01s3O000000ozfFQAQ",
  "NOS_b_InactiveAddressFlag__c": False,
  "vlocity_cmt__OneTimeMarginTotal__c": 0.00,
  "vlocity_cmt__RecurringTotal2__c": 0.00,
  "NOS_b_OccupiedAddressFlag__c": False,
  "vlocity_cmt__CartIdentifier__c": "This is That",
  "vlocity_cmt__OneTimeLoyaltyTotal__c": 0,
  "NOS_b_StoreProductsReadyToAssetize__c": False,
  "NOS_b_LoyaltyPenalty__c": False,
  "COM_ActivationEventExpired__c": False,
  "NOS_b_OngoingOrders__c": False,
  "vlocity_cmt__IsSyncing__c": False,
  "EffectiveDate": "2024-02-09T00:00:00.000Z"
}


        data = {
            "vlocity_cmt__IsActiveOrderVersion__c": False,
            "vlocity_cmt__OrderStatus__c": "Ready To Submit",
            "vlocity_cmt__IsChangesAllowed__c": True,
            "NOS_t_CustomerOldness__c": "NEW",
            "NOS_b_LCETermsAccepted__c": False,
            "NOS_b_FraudAddressFlag__c": False,
            "vlocity_cmt__EffectiveUsageCostTotal__c": 0.00,
            "vlocity_cmt__RequestedStartDate__c": "2024-03-07T15:42:22.000Z",
            "State__c": "Em Carrinho",
            "IsChangeNumber__c": False,
            "Status": "Draft",
            "NOS_b_IsUserAccept__c": False,
            "vlocity_cmt__EffectiveRecurringCostTotal__c": 0.00,
            "vlocity_cmt__JeopardySafetyIntervalUnit__c": "Seconds",
            "vlocity_cmt__ExternalPricingStatus__c": "Not Ready",
            "vlocity_cmt__DefaultCurrencyPaymentMode__c": "Currency",
            "vlocity_cmt__OrderMarginTotal__c": 0.00,
            "NOS_b_CoverageReturnCable__c": False,
            "NOS_b_CoverageVoDFlag__c": False,
            "vlocity_cmt__EffectiveUsagePriceTotal__c": 0.00,
            "vlocity_cmt__EffectiveOneTimeCostTotal__c": 0.00,
            "vlocity_cmt__OneTimeTotal2__c": 0.00,
            "NOS_b_AutomaticScheduling__c": False,
            "vlocity_cmt__EffectiveOneTimeLoyaltyTotal__c": 0,
            "vlocity_cmt__ForceSupplementals__c": False,
            "RecordTypeId": "0123O000000ZhSrQAK",
            "NOS_t_ValidateSLA__c": True,
            "NOS_t_BusinessScenario__c": "BS_STANDARD_CHANGE",
            "NOS_b_ImmediateInactivation__c": False,
            "vlocity_cmt__RequestDate__c": "2024-03-07T00:00:00.000Z",
            "NOS_b_6ChannelsOffer__c": False,
            "Type": "INSTALAÇÃO",
            "NOS_b_SkipInquiry__c": False,
            "NOS_b_ReversionFlag__c": False,
            "AccountId": "0013O000013YjAD",
            "NOS_b_IsBSimulation__c": False,
            # "StatusCode": "Draft",
            "Name": "EcommerceOrder",
            "NOS_b_StockValidation__c": True,
            "vlocity_cmt__FulfilmentStatus__c": "Draft",
            "vlocity_cmt__CreatedByAPI__c": False,
            "SkippedNotification__c": False,
            "vlocity_cmt__OriginatingChannel__c": "Call Center",
            "vlocity_cmt__UsageMarginTotal__c": 0.00,
            "vlocity_cmt__DeliveryMethod__c": "In Store",
            "vlocity_cmt__RecurringMarginTotal__c": 0.00,
            "vlocity_cmt__PriceListId__c": "a4j3O0000000X0zQAE",
            "vlocity_cmt__IsContractRequired__c": False,
            "Activated__c": False,
            "NOS_t_DataIdentify__c": False,
            "vlocity_cmt__IsChangesAccepted__c": False,
            "NOS_b_IsPortfolioChanged__c": False,
            "Pricebook2Id": "01s3O000000ozfFQAQ",
            "NOS_b_InactiveAddressFlag__c": False,
            "vlocity_cmt__OneTimeMarginTotal__c": 0.00,
            "vlocity_cmt__RecurringTotal2__c": 0.00,
            "NOS_b_OccupiedAddressFlag__c": False,
            "vlocity_cmt__CartIdentifier__c": "0882f140-ad6f-1f54-265b-af3d4809d1ac",
            "vlocity_cmt__OneTimeLoyaltyTotal__c": 0,
            "NOS_b_StoreProductsReadyToAssetize__c": False,
            "NOS_b_LoyaltyPenalty__c": False,
            "COM_ActivationEventExpired__c": False,
            "NOS_b_OngoingOrders__c": False,
            "vlocity_cmt__IsSyncing__c": False,
            "EffectiveDate": "2024-02-09T00:00:00.000Z"
        }   

       # call2 =  Sobjects.update(q['records'][0]['Id'],data,'Order')

        call2 = Sobjects.create('Order',object=data)

        print(call2)
        a=1

    def test_ecomCart(self):
        url = 'https://nos--nosdti.sandbox.my.site.com'
        token = '00D3O0000004pzC!AQkAQHmeh6EDGKY1v2PTfnItN4HNumq_FqZmOM2o1givHqjwWWe3qOKiIpclF8eSNXIX3K7z6Zc30NoNw_FXEiq.utABn8X9'
        token = '00D0Q0000000fNy!AQEAQNJvrPIOvRWnhkSWXTOpWf3M3YwI3dZSur8_ZP4T.C9pFuj4uKI17MVcVNbri9lZTSud0bmwTXz64OBAxbyT3KBnv_P.'
        token = '00D0Q0000000fNy!AQEAQARJzBJR6HS2sM83fE9iDUL7s2UZolUmpzoFY.e5lQBvrInwZcBdq3eUPahIQUeqYr5CzTR_Gv3VQS73cVaC0QoNHJuG'
        orderId=''
        restClient.initWithToken('xxx',url=url,token=token)

        res = query.query('select Id from account limit 1')

        body = {
            "accountId" : "0013O00001KxPXnQAN",
            "cartContextKey" : "efbdf9e5876d9e05bc4beba3b9f2d5f1",
            "catalogCode" : "DC_CAT_WOO_MOBILE",
            "price" : "false",
            "context" : "{\"DIM_PROCESS\":\"SELL\",\"DIM_CHANNEL\":\"UNI\",\"DIM_ADDRESSCOMPETITOR\":\"\",\"DIM_ADDRESSTECH\":\"\",\"DIM_ADDRESSTECHCODE\":\"\",\"DIM_ORDER_TYPE\":\"INSTALAÇÃO\"}",
            "validate" : "false",
            "methodName" : "createEcomCart",
            "apiName" : "CreateEcomCart"
        }
        action = f'/services/apexrest/{restClient.getNamespace()}/v3/carts?price=false&validate=false'

        response = restClient.callAPI(action, method="post", data=body,ts_name=None)

        a=1

    def test_compare_JSON(self):
        dataEx =  {
            "attributes" : {
            "type" : "Order",
            "url" : "/services/data/v60.0/sobjects/Order/8013O0000053GScQAM"
            },
            "LastModifiedDate" : "2024-02-28T12:12:49.000+0000",
            "vlocity_cmt__OrderTotal__c" : 0.00,
            "vlocity_cmt__StatusImageName__c" : "Draft",
            "vlocity_cmt__IsActiveOrderVersion__c" : False,
            "vlocity_cmt__OrderStatus__c" : "Ready To Submit",
            "NOS_TenMinuteScheduled__c" : "2024-02-28T11:22:49.748+0000",
            "vlocity_cmt__EffectiveRecurringTotal__c" : 0.00,
            "OrderNumber" : "00225356",
            "vlocity_cmt__IsChangesAllowed__c" : True,
            "vlocity_cmt__OneTimeTotal__c" : 0.00,
            "NOS_t_CustomerOldness__c" : "NEW",
            "NOS_b_LCETermsAccepted__c" : False,
            "NOS_b_FraudAddressFlag__c" : False,
            "vlocity_cmt__EffectiveUsageCostTotal__c" : 0.00,
            "vlocity_cmt__RequestedStartDate__c" : "2024-02-28T12:12:47.000+0000",
            "State__c" : "Em Carrinho",
            "IsChangeNumber__c" : False,
            "Status" : "Draft",
            "NOS_b_IsUserAccept__c" : False,
            "IsDeleted" : False,
            "vlocity_cmt__IsValidated__c" : False,
            "vlocity_cmt__EffectiveRecurringCostTotal__c" : 0.00,
            "IsReductionOrder" : False,
            "TotalContractRevenue__c" : 0.00,
            "vlocity_cmt__JeopardySafetyIntervalUnit__c" : "Seconds",
            "vlocity_cmt__ExternalPricingStatus__c" : "Not Ready",
            "vlocity_cmt__AccountRecordType__c" : "Consumer",
            "vlocity_cmt__DefaultCurrencyPaymentMode__c" : "Currency",
            "Id" : "8013O0000053GScQAM",
            "vlocity_cmt__OrderMarginTotal__c" : 0.00,
            "NOS_b_CoverageReturnCable__c" : False,
            "NOS_b_CoverageVoDFlag__c" : False,
            "vlocity_cmt__EffectiveUsagePriceTotal__c" : 0.00,
            "vlocity_cmt__EffectiveOneTimeCostTotal__c" : 0.00,
            "vlocity_cmt__OneTimeTotal2__c" : 0.00,
            "NOS_b_AutomaticScheduling__c" : False,
            "MonthlyContractRevenue__c" : 0.00,
            "vlocity_cmt__EffectiveOneTimeLoyaltyTotal__c" : 0,
            "OwnerId" : "0053O000009LB2eQAG",
            "vlocity_cmt__ForceSupplementals__c" : False,
            "RecordTypeId" : "0123O000000ZhSrQAK",
            "NOS_t_ValidateSLA__c" : True,
            "NOS_t_BusinessScenario__c" : "BS_STANDARD_CHANGE",
            "NOS_b_ImmediateInactivation__c" : False,
            "vlocity_cmt__RequestDate__c" : "2024-02-28",
            "NumberOfItemsActivated__c" : 0,
            "SystemModstamp" : "2024-02-28T12:12:49.000+0000",
            "NOS_b_6ChannelsOffer__c" : False,
            "Type" : "INSTALAÇÃO",
            "NOS_b_SkipInquiry__c" : False,
            "NOS_b_ReversionFlag__c" : False,
            "vlocity_cmt__TotalMonthlyDiscount__c" : 0.00,
            "AccountId" : "0013O00001KxPXnQAN",
            "NOS_b_IsBSimulation__c" : False,
            "StatusCode" : "Draft",
            "Name" : "EcommerceOrder",
            "NOS_b_StockValidation__c" : True,
            "vlocity_cmt__FulfilmentStatus__c" : "Draft",
            "CreatedById" : "0053O000009bkctQAA",
            "vlocity_cmt__CreatedByAPI__c" : False,
            "SkippedNotification__c" : False,
            "MonthlyContractCost__c" : 0.00,
            "vlocity_cmt__TotalOneTimeDiscount__c" : 0.00,
            "vlocity_cmt__OriginatingChannel__c" : "Call Center",
            "vlocity_cmt__UsageMarginTotal__c" : 0.00,
            "NonRecurringContractRevenue__c" : 0.00,
            "vlocity_cmt__DeliveryMethod__c" : "In Store",
            "vlocity_cmt__AccountId__c" : "0013O00001KxPXn",
            "vlocity_cmt__RecurringMarginTotal__c" : 0.00,
            "vlocity_cmt__PriceListId__c" : "a4j3O0000000X0zQAE",
            "vlocity_cmt__IsContractRequired__c" : False,
            "Activated__c" : False,
            "NOS_t_DataIdentify__c" : False,
            "vlocity_cmt__IsChangesAccepted__c" : False,
            "NOS_b_IsPortfolioChanged__c" : False,
            "CreatedDate" : "2024-02-28T12:12:49.000+0000",
            "Pricebook2Id" : "01s3O000000ozfFQAQ",
            "NOS_b_InactiveAddressFlag__c" : False,
            "vlocity_cmt__EffectiveOneTimeTotal__c" : 0.00,
            "vlocity_cmt__OneTimeMarginTotal__c" : 0.00,
            "NonRecurringContractCost__c" : 0.00,
            "vlocity_cmt__RecurringTotal2__c" : 0.00,
            "CommissionableMonthlyMargin__c" : 0.00,
            "NOS_b_OccupiedAddressFlag__c" : False,
            "vlocity_cmt__CartIdentifier__c" : "4931ccec-e75c-b9a1-000a-1b93c2c546fa",
            "vlocity_cmt__EffectiveOrderTotal__c" : 0.00,
            "vlocity_cmt__RecurringTotal__c" : 0.00,
            "TotalContractCost__c" : 0.00,
            "vlocity_cmt__OneTimeLoyaltyTotal__c" : 0,
            "NOS_b_StoreProductsReadyToAssetize__c" : False,
            "vlocity_cmt__JeopardyStatus__c" : "Green",
            "NonRecurringContractMargin__c" : 0.00,
            "vlocity_cmt__Pricebook__c" : "Standard Price Book",
            "TotalAmount" : 0.00,
            "MonthlyContractMargin__c" : 0.00,
            "NumberOfItemsOpen__c" : 0,
            "NOS_b_LoyaltyPenalty__c" : False,
            "TotalContractMargin__c" : 0.00,
            "COM_ActivationEventExpired__c" : False,
            "NOS_b_OngoingOrders__c" : False,
            "vlocity_cmt__IsPriced__c" : False,
            "vlocity_cmt__IsSyncing__c" : False,
            "LastModifiedById" : "0053O000009bkctQAA",
            "EffectiveDate" : "2024-02-28"
        }

        dataMe = {
            "attributes" : {
            "type" : "Order",
            "url" : "/services/data/v60.0/sobjects/Order/8013O0000053GdzQAE"
            },
            "LastModifiedDate" : "2024-02-28T15:23:26.000+0000",
            "vlocity_cmt__OrderTotal__c" : 0.00,
            "vlocity_cmt__StatusImageName__c" : "Draft",
            "vlocity_cmt__IsActiveOrderVersion__c" : False,
            "vlocity_cmt__OrderStatus__c" : "Ready To Submit",
            "NOS_TenMinuteScheduled__c" : "2024-02-28T14:33:26.398+0000",
            "vlocity_cmt__EffectiveRecurringTotal__c" : 0.00,
            "OrderNumber" : "00225413",
            "vlocity_cmt__IsChangesAllowed__c" : True,
            "vlocity_cmt__OneTimeTotal__c" : 0.00,
            "NOS_t_CustomerOldness__c" : "NEW",
            "NOS_b_LCETermsAccepted__c" : False,
            "NOS_b_FraudAddressFlag__c" : False,
            "vlocity_cmt__EffectiveUsageCostTotal__c" : 0.00,
            "vlocity_cmt__RequestedStartDate__c" : "2024-02-09T15:42:22.000+0000",
            "State__c" : "Em Carrinho",
            "IsChangeNumber__c" : False,
            "Status" : "Draft",
            "NOS_b_IsUserAccept__c" : False,
            "IsDeleted" : False,
            "vlocity_cmt__IsValidated__c" : False,
            "vlocity_cmt__EffectiveRecurringCostTotal__c" : 0.00,
            "IsReductionOrder" : False,
            "TotalContractRevenue__c" : 0.00,
            "vlocity_cmt__JeopardySafetyIntervalUnit__c" : "Seconds",
            "vlocity_cmt__ExternalPricingStatus__c" : "Not Ready",
            "vlocity_cmt__AccountRecordType__c" : "Consumer",
            "vlocity_cmt__DefaultCurrencyPaymentMode__c" : "Currency",
            "Id" : "8013O0000053GdzQAE",
            "vlocity_cmt__OrderMarginTotal__c" : 0.00,
            "NOS_b_CoverageReturnCable__c" : False,
            "NOS_b_CoverageVoDFlag__c" : False,
            "vlocity_cmt__EffectiveUsagePriceTotal__c" : 0.00,
            "vlocity_cmt__EffectiveOneTimeCostTotal__c" : 0.00,
            "vlocity_cmt__OneTimeTotal2__c" : 0.00,
            "NOS_b_AutomaticScheduling__c" : False,
            "MonthlyContractRevenue__c" : 0.00,
            "vlocity_cmt__EffectiveOneTimeLoyaltyTotal__c" : 0.0,
            "OwnerId" : "0053O000006cJuJQAU",
            "vlocity_cmt__ForceSupplementals__c" : False,
            "RecordTypeId" : "0123O000000ZhSrQAK",
            "NOS_t_ValidateSLA__c" : True,
            "NOS_t_BusinessScenario__c" : "BS_STANDARD_CHANGE",
            "NOS_b_ImmediateInactivation__c" : False,
            "vlocity_cmt__RequestDate__c" : "2024-02-09",
            "NumberOfItemsActivated__c" : 0,
            "SystemModstamp" : "2024-02-28T15:23:26.000+0000",
            "NOS_b_6ChannelsOffer__c" : False,
            "Type" : "INSTALAÇÃO",
            "NOS_b_SkipInquiry__c" : False,
            "NOS_b_ReversionFlag__c" : False,
            "vlocity_cmt__TotalMonthlyDiscount__c" : 0.00,
            "AccountId" : "0013O000013YjADQA0",
            "NOS_b_IsBSimulation__c" : False,
            "StatusCode" : "Draft",
            "Name" : "EcommerceOrder",
            "NOS_b_StockValidation__c" : True,
            "vlocity_cmt__FulfilmentStatus__c" : "Draft",
            "CreatedById" : "0053O000009bkctQAA",
            "vlocity_cmt__CreatedByAPI__c" : False,
            "SkippedNotification__c" : False,
            "MonthlyContractCost__c" : 0.00,
            "vlocity_cmt__TotalOneTimeDiscount__c" : 0.00,
            "vlocity_cmt__OriginatingChannel__c" : "Call Center",
            "vlocity_cmt__UsageMarginTotal__c" : 0.00,
            "NonRecurringContractRevenue__c" : 0.00,
            "vlocity_cmt__DeliveryMethod__c" : "In Store",
            "vlocity_cmt__AccountId__c" : "0013O000013YjAD",
            "vlocity_cmt__RecurringMarginTotal__c" : 0.00,
            "vlocity_cmt__PriceListId__c" : "a4j3O0000000X0zQAE",
            "vlocity_cmt__IsContractRequired__c" : False,
            "Activated__c" : False,
            "NOS_t_DataIdentify__c" : False,
            "vlocity_cmt__IsChangesAccepted__c" : False,
            "NOS_b_IsPortfolioChanged__c" : False,
            "CreatedDate" : "2024-02-28T15:23:26.000+0000",
            "Pricebook2Id" : "01s3O000000ozfFQAQ",
            "NOS_b_InactiveAddressFlag__c" : False,
            "vlocity_cmt__EffectiveOneTimeTotal__c" : 0.00,
            "vlocity_cmt__OneTimeMarginTotal__c" : 0.00,
            "NonRecurringContractCost__c" : 0.00,
            "vlocity_cmt__RecurringTotal2__c" : 0.00,
            "CommissionableMonthlyMargin__c" : 0.00,
            "NOS_b_OccupiedAddressFlag__c" : False,
            "vlocity_cmt__CartIdentifier__c" : "This is That 2",
            "vlocity_cmt__EffectiveOrderTotal__c" : 0.00,
            "vlocity_cmt__RecurringTotal__c" : 0.00,
            "TotalContractCost__c" : 0.00,
            "vlocity_cmt__OneTimeLoyaltyTotal__c" : 0.0,
            "NOS_b_StoreProductsReadyToAssetize__c" : False,
            "vlocity_cmt__JeopardyStatus__c" : "Green",
            "NonRecurringContractMargin__c" : 0.00,
            "vlocity_cmt__Pricebook__c" : "Standard Price Book",
            "TotalAmount" : 0.00,
            "MonthlyContractMargin__c" : 0.00,
            "NumberOfItemsOpen__c" : 0,
            "NOS_b_LoyaltyPenalty__c" : False,
            "TotalContractMargin__c" : 0.00,
            "COM_ActivationEventExpired__c" : False,
            "NOS_b_OngoingOrders__c" : False,
            "vlocity_cmt__IsPriced__c" : False,
            "vlocity_cmt__IsSyncing__c" : False,
            "LastModifiedById" : "0053O000009bkctQAA",
            "EffectiveDate" : "2024-02-09"
        }

        print('Not in dataEx')
        for key in dataMe:
            if key not in dataEx:
                print(key)

            if dataEx[key] != dataMe[key]:
                print(f"{key} {dataEx[key]} {dataMe[key]}")
        
        print('Not in dataMe')
        for key in dataEx:
            if key not in dataMe:
                print(key)


    def test_xxx(self):
        restClient.authenticate('','','barry.brown@sandeshkulkarni-240219-963.demo','test12345',False)