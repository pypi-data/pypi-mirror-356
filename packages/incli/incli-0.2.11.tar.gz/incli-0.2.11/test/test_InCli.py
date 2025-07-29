from incli import incli
from incli.sfapi import utils,query,restClient,file
import sys, os,simplejson
#python3 -m unittest

import unittest
#from InCli import InCli
#from incli.sfapi import restClient
import traceback,time

#/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg
# python3 -m build
#python3 -m twine upload --repository pypi dist/InCli-0.0.29*

class Test_Main(unittest.TestCase):

    def test_q(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_q_System(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-system"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_q_nulls(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-null"])       
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2) 
    def test_q_all(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 1","-all"])   
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_q_fields_all(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select fields(all) from Order limit 10","-fields","AccountId"])  
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_q_fields_all(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select AccountId,Pricebook2Id,OrderNumber,TotalContractCost__c,State__c from Order limit 50","-fields","all"])  
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
  
    def test_q_complexfields_all(self):
        try:
            incli._main(["-u","NOSDEV","-q", "select Id,vlocity_cmt__BillingAccountId__c,vlocity_cmt__LineNumber__c,vlocity_cmt__ServiceAccountId__c,vlocity_cmt__Product2Id__r.productCode from orderitem where OrderId='8013O000003ivMKQAY' order by vlocity_cmt__LineNumber__c","-fields","all"])  
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

  
    def test_o(self):
        try:
            incli._main(["-u","uormaechea.devnoscat2@nos.pt","-o"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_o_name(self):
        try:
            incli._main(["-u","uormaechea.devnoscat4@nos.pt","-o","-name","order"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_o_name_limit(self):
        try:
            incli._main(["-u","uormaechea.devnoscat4@nos.pt","-o","-name","order","-limit","10"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_o_like(self):
        try:
            incli._main(["-u","uormaechea.devnoscat2@nos.pt","-o","-like","XOM"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_h(self):
        try:
            incli._main(["-h"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_hu(self):
        try:
            incli._main(["-hu"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc(self):
        try:
            incli._main(["-u","NOSDEV","-cc"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)


    def test_cc_guest(self):
        try:
            incli._main(["-u","DTI","-cc","-basket","-guest",'https://nos--nosdti.sandbox.my.site.com/onboarding',"-code","DC_CAT_DEEPLINK"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_guest_context(self):
        try:
            context = {"DIM_PROCESS":"SELL","DIM_CHANNEL":"APP","DIM_ADDRESSCOMPETITOR":"","DIM_ADDRESSTECH":"","DIM_ADDRESSTECHCODE":"","DIM_ORDER_TYPE":"INSTALAÇÃO"}

            incli._main(["-u","DTI","-cc","-basket","-guest",'https://nos--nosdti.sandbox.my.site.com/onboarding',"-code","DC_CAT_DEEPLINK","-context",simplejson.dumps(context)])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_guest_AccountId(self):
        try:
            incli._main(["-u","NOSDEV","-cc","-basket","-guest",'https://nos--nosdti.sandbox.my.site.com/onboarding',"-code","DC_CAT_WOO_MOBILE","-account","name:unaiTest4"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_no_u(self):
        try:
            incli._main(["-cc"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)


    def test_cc_basket(self):
        try:
            incli._main(["-u","NOSDEV","-cc","-basket"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_cc_basket_code(self):
        try:
            incli._main(["-u","DEVNOSCAT4","-cc","-code","DC_CAT_WOO_MOBILE","-basket"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_cc_list(self):
        try:
            incli._main(["-u","NOSDEV","-cc","-list"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_code(self):
        try:
            incli._main(["-u","NOSDEV","-cc","-code","DC_CAT_DEEPLINK"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_cc_account(self):
        try:
            incli._main(["-u","NOSDEV","-cc","-account","name:unaiTest4","-code","DC_CAT_MPO_CHILD_003"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs(self):
        try:
            incli._main(["-u","NOSDEV","-logs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_LEVEL(self):
        try:
            incli._main(["-u","NOSDEV","-logs",'-tail',"-auto","-debuglevel","M"])
            print(traceback.format_exc())
        except Exception as e:
            utils.printException(e)
            self.assertTrue(1==2)


    def test_logs_option_all(self):
        try:
            incli._main(["-u","NOSDEV","-logs","-auto","-tail","-all","-loguser","username:autoproc@00d3o0000004pzcuaq"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_where(self):
        try:
            incli._main(["-u","NOSDEV","-logs","-where","adaasdasd='asasd'"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_store(self):
        try:
            incli._main(["-logs","-store"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_store_id(self):
        try:
            incli._main(["-logs","-store","07L0Q00000N7AHsUAN"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_store_error(self):
        try:
            incli._main(["-u","NOSDEV","-logs","-store","-error"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_user_ELK(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-tail","-loguser","InCliELKIT","-deletelogs"])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_user(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-loguser","Alias:ana.r"])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_query(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-where","Operation='Batch Apex'","-last","10"])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_userDefault_loguser(self):
        try:
            incli._main(["-default:set","loguser","Alias:ana.r"])
            incli._main(["-u","NOSDEV","-logs"])
            incli._main(["-default:del","loguser"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_userWrong(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-loguser","username:uormaechea_nosdev@nos.pt"])
        except Exception as e:
            print(e.args[0]['error'])
            self.assertTrue(e.args[0]['error']=='User with field Alias:xxxx does not exist in the User Object.')
            utils.printException(e)

    def test_logs_limit(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-limit","200"])
            self.assertTrue(len(res)==2)
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_all(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-tail","-auto","-deletelogs","-all"])
            if len(res)>0:
                self.assertTrue(res[0]['Id']!=None)
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
  

    def test_logs_all2(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f'/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07LAU00000Dk2ZM2AZ.log','-all'])
            if len(res)>0:
                self.assertTrue(res[0]['Id']!=None)
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_level(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f'/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07LAU00000Dk2ZM2AZ.log','-level','5'])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_callStack(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f'/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07LAU00000Dk1AM2AZ.log','-callstack','14856586030'])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_search(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f'/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07LAU00000DkFJA2A3.log','-search','findBy'])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_logs_noMethod(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f'/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07LAU00000DkFJA2A3.log','-noMethod'])
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_ID_2(self):
        try:
            id = '07L3O00000Dic7oUAB'
           # id = '07L7a00000TOMLDEA5'
            env = 'NOSDEV'
            #id = None

            if id == None:
                restClient.init(env)
                id = query.queryField("Select Id FROM ApexLog order by StartTime desc limit 1")
            incli._main(["-u",env,"-logs",id])

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_limitinfo(self):
        try:
           # id = '07L3O00000Dh69HUAR'
            id = None

            if id == None:
                restClient.init('NOSDEV')
                id = query.queryField("Select Id FROM ApexLog order by StartTime desc limit 1")
            incli._main(["-u","NOSDEV","-logs",id])
            incli._main(["-u","NOSDEV","-logs",id,"-limitinfo"])

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_log_IDflow(self): #flow
        try:
            incli._main(["-u","NOSDEV","-logs","-inputfile","/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/flowAndWF.log"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

#07L3O00000Dy7SAUAZ
    def test_log_ID(self):
        try:
            incli._main(["-u","NOSDEV","-logs","07LAU00000GpuIY2AZ"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def test_log_ID_wrong(self):
        try:
            incli._main(["-u","DEVNOSCAT4","-logs","xxx"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def test_log_ID_limitsInfo(self):
        try:
            incli._main(["-u","NOSDEV","-logs","07L3O00000DxlaLUAR","-limitinfo"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())
    def test_log_ID_to_file(self):
        try:
            incli._main(["-u","NOSQSM","-logs","07L7a00000VBNh9EAH","-fileOutput","-allLimits"])
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def test_log_folder(self):
        try:
            res = incli._main(["-logs","-folder",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/InCli/logs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_folder_file(self):
        try:
            res = incli._main(["-logs","-folder",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/InCli/logs1","-fileOutput"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_folder_Id(self):
        try:
            res = incli._main(["-logs","-folder",f"/Users/uormaechea/Downloads/logs_SF"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    
    def test_log_file(self):
        try:
            res = incli._main(["-logs","-inputfile",f'/Users/uormaechea/Downloads/07LAP00000GLU2I2AX.log'])

        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
          #  self.assertTrue(1==2)

    def test_logs_file_var(self):
        try:
            res = incli._main(["-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/InCli/logs/07L3O00000GpY1eUAF.log","-var"])
            if len(res)>0:
                self.assertTrue(res[0]['Id']!=None)
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2) 
    def test_log_file_allLimits(self):
        try:
            res = incli._main(["-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07L3O00000EmvvzUAB.log","-allLimits"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_to_file(self):
        try:
            res = incli._main(["-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/incli/logs/07L3O00000EmvvzUAB.log","-fileOutput"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_id(self):
        try:
            id = '07L0Q00000N5yVKUAZ'
            res = incli._main(["-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/.InCli/logs/{id}.log"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_set_id(self):
        try:
            id = '07L3O00000DwvxvUAB'
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/.InCli/logs/{id}.log"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_test_folder(self):
        try:
            id = '07L3O00000EBQ6MUAX'
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/InCli/logs/{id}.log"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_to_file(self):
        try:
            if 1==2:
                restClient.init('DTI')
                html_name = f"{restClient.logFolder()}07L3O00000Dgt4sUAB.html"
                txt_name = f"{restClient.logFolder()}07L3O00000Dgt4sUAB.html"

                if file.exists(html_name):
                    file.delete(html_name)
                if file.exists(txt_name):
                    file.delete(txt_name)
                self.assertTrue(file.exists(html_name)==False)
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/InCli/logs/07L3N00000IuugrUAB.log","-var","-fileOutput"])
            self.assertTrue(file.exists(html_name)==True)
            self.assertTrue(file.exists(txt_name)==True)

            html = file.read(f"{restClient.logFolder()}07L3O00000Dgt4sUAB.html")
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_2(self):
        try:
            incli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/07L3O00000DgwlbUAB.log"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_file_exception_wf(self):
        try:
            res = incli._main(["-u","NOSDEV","-logs","-inputfile",f"/Users/uormaechea/Documents/Dev/python/InCliLib/InCLipkg/test/files/ExceptionThrown.log"])
            self.assertTrue(res['exception']==True)
            last = res['debugList'][-1]
            self.assertTrue(last['cmtSOQLQueries'][0] == '43')
         #   self.assertTrue(last['CPUTime'][0] == '13363')
            self.assertTrue(res['file_exception']==True)
            
            print()
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_last(self):
        try:
            incli._main(["-u","DTI","-logs","-last","100"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_tail_loguser_guest_auto_delete(self):
        try:
            incli._main(["-u","NOSDEV","-logs","-tail","-auto","-deletelogs","-allLimits"])

          #  incli._main(["-u","DTI","-logs","-tail","-auto","-deletelogs","-downloadOnly"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_last_loguser(self):
        try:
            incli._main(["-u","NOSQSM","-logs","-last","2","-loguser","username:uormaechea@nos.pt"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_tail_auto_loguser_new(self):
        try:
            incli._main(["-u","NOSDEV","-logs","-tail","-auto","-loguser","username:pvg@optimus.force.com.nosdev"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_log_tail_auto(self):
        try:
            #return
            incli._main(["-u","mpomigra250","-logs","-tail","-auto"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)  

    def test_log_tail_auto_delete(self):
        try:
            #return
            incli._main(["-u","dbl48","-logs","-tail","-deletelogs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)  

    def test_log_tail_auto_delete_INCLI_LOG_USER(self):
        try:
            #return
            incli._main(["-u","NOSDEV","-logs","-tail","-auto","-deletelogs","-loguser","InCliELKIT"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)  

    def test_log_tail_auto_delete_filter(self):
        try:
            #return
            #incli._main(["-u","NOSDEV","-logs","-tail","-auto","-deletelogs","-filter","801AU00000N9ZhHYAV"])

            incli._main(["-u","NOSDEV","-logs","-tail","-auto","-deletelogs","-debuglevel","XXS","-filter","801AU00000N9ZhHYAV"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)  

    def test_log_tail_auto_delete_level(self):
        try:
            #return
            incli._main(["-u","NOSDEV","-logs","-tail","-auto","-deletelogs","-debuglevel","XXS"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)  

    def test_log_tail(self):
        try:
            #return
            incli._main(["-u","NOSDEV","-logs","-tail"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)   
    def test_log_tail_delete_guest(self):
        try:
            #return
            incli._main(["-u","NOSQSM","-logs","-tail","-deletelogs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)     

    def test_log_tail_delete(self):
        try:
            #return
            incli._main(["-u","NOSDEV","-logs","-tail","-deletelogs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)     

    def test_log_tail_delete_parseSmallFiles(self):
        try:
            #return
            incli._main(["-u","DEVNOSCAT4","-logs","-tail","-deletelogs","-parseSmallFiles"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)    

    def test_log_tail_where(self):
        try:
            return

            incli._main(["-u","NOSDEV","-logs","-tail","-where","LogLength>3000"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)    
    def test_log_tailx(self):
        try:
            restClient.init('NOSDEV')
            logRecords = query.queryRecords("Select fields(all) FROM ApexLog order by StartTime desc limit 1")
            time = logRecords[0]['StartTime']
            timez = time.split('.')[0] + "Z"
            while (True):
                logRecords = query.queryRecords(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog where StartTime > {timez} order by StartTime asc ")

                if len(logRecords) > 0:
                    print()
                    for record in logRecords:
                        print(f"{record['StartTime']}  {record['Operation']}")
                        time = record['StartTime']
                        timez = time.split('.')[0] + "Z"
                        
                time.sleep(5)
            print()

          #  incli._main(["-u","NOSDEV","-logs","-last","10"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_default(self):
        try:
            incli._main(["-default:set","u"])
            incli._main(["-default:set","u","NOSDEV"])
            incli._main(["-default:get","u"])        
            res = incli._main(["-logs","-last","1"])
            incli._main(["-default:del","u"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_default_get(self):
        try:
            incli._main(["-default:get"])        
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_default_weird(self):
        try:
            incli._main(["-h:","InCli","-default:set","u","NOSDEV"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_d(self):
        try:
            incli._main(["-u","NOSDEV","-d"])
            incli._main(["-u","NOSDEV","-d","Order"])
            incli._main(["-u","NOSDEV","-d","Order:Status"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_l(self):
        try:
            incli._main(["-u","NOSPRD","-l"])
            incli._main(["-u","DEVNOSCAT2","-l"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_l_no_U(self):
        try:
            incli._main(["-l"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_checkVersion(self):
        incli.checkVersion()
        print()

    def test_ipe(self):
        try:
            #incli._main(["-u","NOSQSM","-ipe","-where","vlocity_cmt__SourceName__c like '%orta%'","-contains","PP00034719","-limit","5000"])

            incli._main(["-u","NOSQSM","-ipe","-debug"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipe_owner(self):
        try:
            #incli._main(["-u","NOSQSM","-ipe","-where","vlocity_cmt__SourceName__c like '%orta%'","-contains","PP00034719","-limit","5000"])

            incli._main(["-u","NOSPRD","-ipe","-owner","Id:005cy000000RZEbAAO"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipe_id(self):
        try:
            incli._main(["-u","NOSPRD","-ipe","a6K7T000001dk4PUAQ"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipe_id_tofile(self):
        try:
            incli._main(["-u","NOSDEV","-ipe","a6K3O000000FJ5WUAW","-fileOutput"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)
    def test_ipe_last(self):
        try:
            incli._main(["-u","NOSPRD","-ipe","-last","100"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa(self):
        try:
            incli._main(["-u","NOSDEV","-ipa"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)


    def test_ipa_owner(self):
        try:
            incli._main(["-u","NOSPRD","-ipa","-owner","Id:0057T000000XH6JQAW"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa_dates(self):
        try:
            incli._main(["-u","NOSPRD","-ipa","-from","2024-11-26T01:00:00","-to","2024-11-26T02:00:00"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa_around(self):
        try:
            incli._main(["-u","NOSPRD","-ipa","-around","2023-03-28T16:25:00"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa_contains(self):
        try:
            incli._main(["-u","NOSPRD","-ipa","-around","2023-03-14T11:24:07","-contains","a3l7T000001RbofQAC,Marco"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)          

    def test_ipa_limit(self):
        try:
            incli._main(["-u","NOSPRD","-ipa","-limit","25"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa_orderNumber(self):
        try:
            incli._main(["-u","NOSPRD","-ipa","-orderNumber","00300083"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa_id(self):
        try:
            incli._main(["-u","NOSQSM","-ipa","a2J7a000002mqCxEAI"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_ipa_id_toFile(self):
        try:
            incli._main(["-u","NOSQSM","-ipa","a2J7a000002mqCxEAI","-fileOutput"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_vte(self):
        try:
            incli._main(["-u","NOSDEV","-vte"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_vte_id(self):
        try:
            incli._main(["-u","NOSDEV","-vte","a6a3O000000FFkYQAW"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_vte_id_file(self):
        try:
            incli._main(["-u","NOSDEV","-vte","a6a3O000000FFkYQAW","-fileOutput"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_vte_wrong_command(self):
        try:
            incli._main(["-u","NOSDEV","-xxx","a6a3O000000FFkYQAW","-fileOutput"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)

    def test_vte_wrong_modifier(self):
        try:
            incli._main(["-u","NOSDEV","-logs","a6a3O000000FFkYQAW","-dellogs"])
        except Exception as e:
            utils.printException(e)
            print(traceback.format_exc())
            self.assertTrue(1==2)