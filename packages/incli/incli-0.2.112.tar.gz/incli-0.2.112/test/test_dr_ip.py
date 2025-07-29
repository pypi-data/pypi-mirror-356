import unittest,simplejson
#from InCli import InCli
from incli.sfapi import file,DR_IP,restClient,query,utils,thread,jsonFile,file_csv,tooling

class Test_DR_IP(unittest.TestCase):
    options = {
        "isDebug": False,
        "chainable": True,
        "resetCache": False,
        "ignoreCache": True,
        "queueableChainable": False,
        "useQueueableApexRemoting": False
    }     
    def test_IP(self):
        #restClient.init('DTI')
        restClient.init('NOSDEV')

        
        call = DR_IP.ip("custom_GetTrialPromos",input={},options=self.options)
        lc = restClient.lastCall()

        print()

    def test_IP_test(self):
        restClient.init('NOSDEV')

        input = {
            "cartId": "8013O0000053k5yQAA"
        }


        
        call = DR_IP.ip("unai_chainableIpsTest",input=input,options=self.options)

        print()

    def test_get_remote_class_1(self):

        restClient.init('NOSDEV')

        res = query.query("select fields(all) from account limit 1")
        account = res['records'][0]

        accounts = []
        for i in range(1000):
            account = {
                "Name":f'Test{i}',
                "BillingPostalCode":"121212",
                "DoorNumber__c":'12'
            }
            accounts.append(account)

        #del account['IsDeleted']
        #del account['MasterRecordId']

        input = {
            'data':accounts,
            'objectName':'Account',
            'simulate':'YES'
        }

        res=DR_IP.remoteClass('CreateHierarchy','saveRecords',input,{})
        print(restClient.getLastCallElapsedTime())
        print(res)

        print()

    key ='d18120d8-9217-43f9-72b5-9fce1b3cdcd8'
    def test_attachment(self):
        restClient.init('DTI')

        q = f"select fields(all) from vlocity_cmt__DRBulkData__c where vlocity_cmt__GlobalKey__c = '{self.key}' limit 20"
        call0 = query.query(q)
        print(call0)
        
        q2 = f"select fields(all) from Attachment where ParentId ='{call0['records'][0]['Id']}' limit 10"
        call2 = query.query(q2)
        print(call2['records'][0]['Id'])
        attachmentId = call2['records'][0]['Id']
     #   attachmentId = '00P0Q00000JWEzGUAX'
        action = call2['records'][0]['Body']
        call = restClient.requestWithConnection(action=action)

        filepath = restClient.callSave("AttachementX123")

        print()

    def test_finish_call(self):
        restClient.init('NOSPRD')
        input = "{}"

        options1 = self.options.copy()
        options1['vlcIPData'] = 'fcf963ae-d9a7-751f-6632-19753dd995XX'

        call = DR_IP.ip("MACD_ichangeOrderProcessAsynch",input=input,options=options1)

        print()

    def test_dr_bundle(self):
        restClient.init('DTI')

        q = "SELECT Name, Id, LastModifiedDate, LastModifiedBy.Name, CreatedDate, CreatedBy.Name, vlocity_cmt__Type__c, vlocity_cmt__InputType__c, vlocity_cmt__OutputType__c, vlocity_cmt__Description__c, LastModifiedById FROM vlocity_cmt__DRBundle__c USING SCOPE Everything WHERE vlocity_cmt__Type__c != 'Migration' AND  vlocity_cmt__Type__c != 'Export (Component)' ORDER BY Name"

        q = "SELECT Name, Id, LastModifiedDate, LastModifiedBy.Name, CreatedDate, CreatedBy.Name, vlocity_cmt__Type__c, vlocity_cmt__InputType__c, vlocity_cmt__OutputType__c, vlocity_cmt__Description__c, LastModifiedById FROM vlocity_cmt__DRBundle__c ORDER BY Name"

        res = query.query(q)
        
        out = []
        for record in res['records']:
            o = {
                "Name":record['Name'],
                "type":record['vlocity_cmt__Type__c']

            }
            out.append(o)
        utils.printFormated(out)
        print()

    def test_get_remote_class(self):

        restClient.init('NOSQSM')
        inp = {
            'orderId':"8013O000003keqvQAA"
        }
        res=DR_IP.remoteClass('CPQUtils','find',inp,{})
        print(restClient.getLastCallElapsedTime())
        print(res)

        print()

    def test_get_remote_class_queryHelper(self):

        restClient.init('mpomigra')
        inp = {
            'orderId':"8013O000003keqvQAA"
        }
        res=DR_IP.remoteClass('QueryHelper','query',inp,{})
        print(restClient.getLastCallElapsedTime())
        print(res)

        print()
############################################################################################################
    def bestMach(self,log,ip_definitions):
        possible_ips = []

        sequenceExecute = log['vlcDebug']['executionSequence']
        sequence = [key[0:-6] for key in log.keys() if key.endswith('Status') and type(log[key]) is bool]
     #   for key in sequence:
     #       if key not in log:
     #           sequence.remove(key)

        for ip_definition in ip_definitions:
            if ip_definition['vlocity_cmt__ProcedureKey__c'] == 'iUse_submitResumeOrder':
                a=1
            score = 0

            executed = ""
            for ip_step in ip_definition['steps']:
                ex = "1" if ip_step['name'] in sequence else "0"
                if ex == "0" and ip_step['executionConditionalFormula'] != "": ex = 'C'
                if ex == "0" and ip_step['loop_element'] == True: ex = 'L' 
                executed = f"{executed}{ex}"

            missed = []
            for seq in sequence:
                if seq not in ip_definition['steps_names']:
                    executed = f"{executed}*"
                    missed.append(seq)
            score = executed.count('1')

            if score>0:
                ip = {
                    'name':ip_definition['vlocity_cmt__ProcedureKey__c'],
                    'score':score,
                    'ip_steps':len(ip_definition['steps']),
                    'size':len(sequence),
                    'execured':executed,
                    'ip_stesps':ip_definition['steps'],
                    'debug_steps':sequence,
                    'missed':missed
                }
                possible_ips.append(ip)
        
        possible_ips_sorted = sorted(possible_ips, key=lambda d: d['score'])
        possible_ips_sorted.reverse()

        return possible_ips_sorted

    def findMatch(self,log,ip_definitions):
        possible_ips = []

        sequenceExecute = log['vlcDebug']['executionSequence']
        sequence = [key[0:-6] for key in log.keys() if key.endswith('Status') and type(log[key]) is bool]
        if sorted(sequence) == sorted(sequenceExecute):
            a=1
        else:
            a=1

        for ip_definition in ip_definitions:           
            if len(sequence) > len(ip_definition['steps_names']):  continue

            if ip_definition['vlocity_cmt__ProcedureKey__c'] == 'woo_getBundleNBOOffer':
                a=1          
            found = True
            for step in sequence:
                if step not in ip_definition['steps_names']: 
                    found = False
                    break
            if found: 
                posible = {
                    'ip':ip_definition['vlocity_cmt__ProcedureKey__c'],
                    'executed':"",
                    'ip_steps':ip_definition['steps_names'],
                    'debug_steps':sequence,
                    'missing':[]
                }
                for ip_step in ip_definition['steps']:
                    ex = "1" if ip_step['name'] in sequence or ip_step['name'] in sequenceExecute else "0"
                    if '0' not in posible['executed']:
                        if ex == "0" and ip_step['executionConditionalFormula'] != "": 
                            ex = 'C'
                        if ex == "0" and ip_step['loop_element'] == True: ex = 'L'
                    if ex == '0': posible['missing'].append(ip_step)

                    posible['executed'] = f"{posible['executed']}{ex}"
                if '1' not in posible['executed']: continue
                if posible['executed'][0]=='0': 
                    continue
                if '01' in posible['executed']:
                    continue
                possible_ips.append(posible)

        return possible_ips

    def test_find_stooped_VIPs_threaded(self):
        restClient.init('NOSPRD')


        if 1==2:
            q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null order by Id desc limit 200"
            bulk_data_records = query.query(q0)

            bulk_ids = [record['Id'] for record in bulk_data_records['records']]

            q = f"select ID,Body,ParentId,LastModifiedDate from Attachment where ParentId in ({query.IN_clause(bulk_ids)})"
            q = f"select fields(all) from Attachment where ParentId in ({query.IN_clause(bulk_ids)}) limit 200"

            attachments = query.query(q,base64=True)

            for attachment in attachments['records']:
                attachment['vlocity_cmt__GlobalKey__c'] = [bdr['vlocity_cmt__GlobalKey__c'] for bdr in bulk_data_records['records'] if bdr['Id']==attachment['ParentId']][0]

            jsonFile.write('attachments_123',attachments)
            
        else:
            attachments = jsonFile.read('attachments_123')

        self.process_attachements_threaded(attachments)

    def test_process_one(self):
        restClient.init('DTI')

        bulkDataId = 'a2J0Q000001Qim1UAC'
        q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where Id='{bulkDataId}'"
        bulk_data_records = query.query(q0)

        q = f"select fields(all) from Attachment where ParentId = '{bulkDataId}' limit 1"
        attachments = query.query_base64(q)

        for attachment in attachments['records']:
            attachment['vlocity_cmt__GlobalKey__c'] = [bdr['vlocity_cmt__GlobalKey__c'] for bdr in bulk_data_records['records'] if bdr['Id']==attachment['ParentId']][0]

        self.process_attachements_threaded(attachments)

        
    def test_print_attachments(self):
        restClient.init('NOSQSM')
        date1 = "2023-02-24"


        q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null and LastModifiedDate>{date1}T00:00:00.00Z "
        bulk_data_records = query.query(q0)

        q = f"select ID,Body,ParentId,LastModifiedDate from Attachment where ParentId in (select Id from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null and LastModifiedDate>{date1}T00:00:00.00Z)"

        attachments = query.query(q,base64=True)   

        for attachment in attachments['records']:
            attachment['vlocity_cmt__GlobalKey__c'] = [bdr['vlocity_cmt__GlobalKey__c'] for bdr in bulk_data_records['records'] if bdr['Id']==attachment['ParentId']][0]
            attachment['log'] = restClient.requestWithConnection(action=attachment['Body'])
            if 'UpdateOrderStatusToPaid_RA' in attachment['log']:
       #     if 'GetOrderServiceAccount_DEA' in attachment['log']:

                print(attachment['log']['OrderDetailsNode']['OrderNumber'])
                json_formatted_str = simplejson.dumps(attachment['log'], indent=2, ensure_ascii=False)

                print(json_formatted_str)
        print()

    def test_date(self):
        restClient.init('NOSPRD')
        date1 = "2023-01-01"
        date2 = "2023-02-01"


        q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null and LastModifiedDate>{date1}T00:00:00.00Z and LastModifiedDate<{date2}T00:00:00.00Z"
        bulk_data_records = query.query(q0)

        q = f"select ID,Body,ParentId,LastModifiedDate from Attachment where ParentId in (select Id from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null and LastModifiedDate>{date1}T00:00:00.00Z and LastModifiedDate<{date2}T00:00:00.00Z)"

        attachments = query.query(q,base64=True)

        for attachment in attachments['records']:
            attachment['vlocity_cmt__GlobalKey__c'] = [bdr['vlocity_cmt__GlobalKey__c'] for bdr in bulk_data_records['records'] if bdr['Id']==attachment['ParentId']][0]

        self.process_attachements_threaded(attachments)


        print()



    num_threads=15
    def process_attachements_threaded(self,attachments):
        ip_definitions = self.get_IP_definitions()

        result = []

        def do_work(attachment):
            attachment['log'] = restClient.requestWithConnection(action=attachment['Body'])
            return attachment

        def on_done(attachment,result):
            log = attachment['log']
            if 'vlcDebug' in log:
                possible_ips =self.findMatch(log,ip_definitions)
                if len(possible_ips) >0:  attachment['possible'] = possible_ips
                else: attachment['best_match'] = self.bestMach(log,ip_definitions)
                result.append(attachment)

        thread.execute_threaded(attachments['records'],result,do_work,on_done,threads=self.num_threads)

        found = [attachment for attachment in attachments['records'] if 'possible' in attachment]
        best_match = [attachment for attachment in attachments['records'] if 'best_match' in attachment]

        newlist = sorted(found, key=lambda d: d['LastModifiedDate']) 

        print_list = []
        for record in newlist:
            for pos in record['possible']:
                p = {
                    'LastModifiedDate':record['LastModifiedDate'][0:19],
                    'Id':record['Id'],
                    'ParentId':record['ParentId'],
                    'vlocity_cmt__GlobalKey__c':record['vlocity_cmt__GlobalKey__c'],
                    'IP':pos['ip'],
                    'debug':pos['executed'],
                    'missing':",".join([f"{rec['name']}-[{rec['type']}]" for rec in pos['missing']])
                }
                print_list.append(p)


        file_csv.write('Attachment_records_Jan',print_list)
        utils.printFormated(print_list)

        print()


    def test_find_stooped_VIPs(self):
        restClient.init('NOSQSM')

        q0 = f"select Id,vlocity_cmt__GlobalKey__c from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null"
        bulk_data_records = query.query(q0)
        bdrs={}
        for bdr in bulk_data_records['records']: bdrs[bdr['Id']] = bdr['vlocity_cmt__GlobalKey__c']
        print(len(bdrs))

        q = f"select ID,Body,ParentId from Attachment where ParentId in (select Id from  vlocity_cmt__DRBulkData__c where vlocity_cmt__DRBundleName__c = 'None Specified' and vlocity_cmt__AsyncApexJobId__c = null and vlocity_cmt__GlobalKey__c != null)"

        attachments = query.query(q,base64=True)

        for attachment in attachments['records']:
            attachment['vlocity_cmt__GlobalKey__c'] = bdrs[attachment['ParentId']]

        ip_definitions = self.get_IP_definitions()

        ip_definitions_woo = [ip_definition for ip_definition in ip_definitions if ip_definition['vlocity_cmt__ProcedureKey__c'].startswith('woo_')]

        for ip_definition_woo in ip_definitions_woo:
            ip_definition_woo['steps'] = set(ip_definition_woo['steps'])
        for attachment in attachments['records']:
            log = restClient.requestWithConnection(action=attachment['Body'])
            possible_ips = []

            if 'vlcDebug' in log:
                sequence = log['vlcDebug']['executionSequence']
                possible_ips =self.findMatch(sequence,ip_definitions_woo)
                if len(possible_ips) >0:
                    bulk_data_record = [record for record in bulk_data_records['records'] if record['Id']==attachment['ParentId']][0].copy()
                    bulk_data_record['possible'] = possible_ips
                    utils.printFormated(bulk_data_record)
            #    else:
            #        posibles = self.bestMach(sequence,ip_definitions)
           #         utils.printFormated(posibles)

    def get_IP_definitions(self):
        q = f"""select 
                    Id,
                    vlocity_cmt__Content__c,
                    vlocity_cmt__OmniScriptId__r.name,
                    vlocity_cmt__OmniScriptId__r.vlocity_cmt__ProcedureKey__c 
                    from vlocity_cmt__OmniScriptDefinition__c 
                    where vlocity_cmt__OmniScriptId__c in (select Id from vlocity_cmt__OmniScript__c where vlocity_cmt__OmniProcessType__c = 'Integration Procedure' and vlocity_cmt__IsActive__c = TRUE) """

        res = query.query(q)

        ip_definitions = []

        for record in res['records']:
            ip_definition = {
                'vlocity_cmt__ProcedureKey__c': record['vlocity_cmt__OmniScriptId__r']['vlocity_cmt__ProcedureKey__c'],
                'Name':                         record['vlocity_cmt__OmniScriptId__r']['Name'],
                'steps':                        [],
                'steps_names':[]
            }
            if ip_definition['vlocity_cmt__ProcedureKey__c'] == 'MACD_ichangeOrderProcessAsynch':
                a=1
            ip_definitions.append(ip_definition)
            content = simplejson.loads(record['vlocity_cmt__Content__c'])

            def getChildStep(child,parent_conditional='',parent_loop=False):
                if 'installCoverageEligibility' == child['name']:
                    a=1
                step = {
                    'name':child['name'],
                    'label':child['propSetMap']['label'] if 'label' in child['propSetMap'] else '',
                    'executionConditionalFormula':child['propSetMap']['executionConditionalFormula'] if 'executionConditionalFormula' in child['propSetMap'] else '',
                    'chainOnStep':child['propSetMap']['chainOnStep'] if 'chainOnStep' in child['propSetMap'] else False,
                    'indexInParent':child['indexInParent'],
                    'type':child['type'],
                    'loop_element':parent_loop
                }    
                if parent_conditional != '':
                    step['executionConditionalFormula'] = f"{step['executionConditionalFormula']} - {parent_conditional}"

                if child['type'] == 'Loop Block':
                    step['loop_element'] = True

                return step

            def addChildren(child,parent_conditional='',parent_loop=False):
                step = getChildStep(child,parent_conditional,parent_loop)
                ip_definition['steps'].append(step)
                ip_definition['steps_names'].append(step['name'])

                if 'children' in child and len(child['children'])>0:
                    for child1 in child['children']:
                        if 'eleArray' in child1:
                            for eleChild in child1['eleArray']:
                                parent_loop = True if child['type'] == 'Loop Block' or parent_loop == True  else False
                                addChildren(eleChild,parent_conditional=step['executionConditionalFormula'],parent_loop=parent_loop)
                        else:
                            a=1

            for child in content['children']:
                addChildren(child)

        return ip_definitions


    def test_nos_ipqueue(self):
        restClient.init('NOSQSM')

        data = jsonFile.read('/Users/uormaechea/Documents/Dev/python/InCliLib/ppp.json')

        if 'input' not in data:
            data = {
                'input':data,
                  "options": {
                        "chainable": True,
                        "postTransformBundle": "",
                        "preTransformBundle": "",
                        "processName": "MACD_ichangeOrderProcessAsynch",
                        "useQueueableApexRemoting": False,
                        "ignoreCache": False,
                        "vlcClass": "CustomIPCalloutQueueable",
                        "useContinuation": False,
                        "isDebug": True
                    }
            }

        call = DR_IP.ip('MACD_ichangeOrderProcessAsynch',data['input'],data['options'])

        a=1

    def test_IP_call(self):
        restClient.init('NOSDEV')


        data = {
            "technologyCode": "HFC",
            "technology": "HFC",
            "servicePointNumber": "3103012709",
            "processId": "a3lAU0000015n2jYAA",
            "orderType": "ALTERAÇÃO NÚMERO MÓVEL",
            "childServiceAccount": "001AU00000km9yCYAQ",
            "changeType": "",
            "assetServiceAccount": "001AU00000kmZiqYAE",
            "assetList": [
                "02iAU000007tpHBYAY",
                "02iAU000007tpHUYAY",
                "02iAU000007tpHJYAY",
                "02iAU000007tpHCYAY",
                "02iAU000007tpHMYAY",
                "02iAU000007tpHfYAI",
                "02iAU000007tpHbYAI",
                "02iAU000007tpHXYAY",
                "02iAU000007tpHnYAI",
                "02iAU000007tpHrYAI",
                "02iAU000007tpHjYAI",
                "02iAU000007tpHPYAY",
                "02iAU000007tpHvYAI",
                "02iAU000007tpI5YAI",
                "02iAU000007tpI0YAI",
                "02iAU000007tpIAYAY",
                "02iAU000007tpHNYAY",
                "02iAU000007tpHVYAY",
                "02iAU000007tpHKYAY",
                "02iAU000007tpHtYAI",
                "02iAU000007tpIDYAY",
                "02iAU000007tpI8YAI",
                "02iAU000007tpHSYAY",
                "02iAU000007tpHZYAY",
                "02iAU000007tpI3YAI",
                "02iAU000007tpHdYAI",
                "02iAU000007tpHhYAI",
                "02iAU000007tpHlYAI",
                "02iAU000007tpHyYAI",
                "02iAU000007tpHpYAI",
                "02iAU000007tpHEYAY",
                "02iAU000007tpHGYAY",
                "02iAU000007tpHHYAY",
                "02iAU000007tpHFYAY",
                "02iAU000007tpHIYAY",
                "02iAU000007tpI1YAI",
                "02iAU000007tpI6YAI",
                "02iAU000007tpHYYAY",
                "02iAU000007tpHoYAI",
                "02iAU000007tpHQYAY",
                "02iAU000007tpHcYAI",
                "02iAU000007tpHsYAI",
                "02iAU000007tpIBYAY",
                "02iAU000007tpHgYAI",
                "02iAU000007tpHwYAI",
                "02iAU000007tpHkYAI",
                "02iAU000007tpI4YAI",
                "02iAU000007tpI9YAI",
                "02iAU000007tpHTYAY",
                "02iAU000007tpIEYAY",
                "02iAU000007tpHzYAI",
                "02iAU000007tpHLYAY",
                "02iAU000007tpHiYAI",
                "02iAU000007tpHeYAI",
                "02iAU000007tpHaYAI",
                "02iAU000007tpHuYAI",
                "02iAU000007tpHqYAI",
                "02iAU000007tpHmYAI",
                "02iAU000007tpHDYAY",
                "02iAU000007tpHOYAY",
                "02iAU000007tpHWYAY",
                "02iAU000007tpICYAY",
                "02iAU000007tpI7YAI",
                "02iAU000007tpHxYAI",
                "02iAU000007tpHRYAY",
                "02iAU000007tpI2YAI"
            ],
            "assetId": "02iAU000007tpHBYAY",
            "assetBillingAccount": "001AU00000kbBzjYAE",
            "accountId": "001AU00000kaxa9YAA",
            "Username": "fmrodrigues",
            "ProductCode": "C_NOS_MSISDN",
            "OldDN": 960384871,
            "NewDN": "931001564",
            "NIF": "149158114",
            "Mobile": 923652313,
            "IU": "",
            "Email": "ouqyabur@email.com",
            "CAVTeam": "",
            "CAVNetwork": "",
            "CAVChannel": "",
            "CAV": "",
            "AgentTeam": "Supervisão SCFA",
            "AccountNumber": "C1000105251"
            }

        options = {
            "isDebug": True,
            "chainable": False,
            "resetCache": False,
            "ignoreCache": True,
            "queueableChainable": True,
            "useQueueableApexRemoting": False
        }           
    
        call = DR_IP.ip('unai_creationOrderIChangeNu',data,options)

        print(restClient.getLastCallElapsedTime())

        a=1

    def test_LWCPrep(self):
        restClient.init('NOSQSM')
        action = '/services/apexrest/omniout/guest/v1/GenericInvoke/BusinessProcessDisplayController/LWCPrep'
        data = {
            "sClassName":"Vlocity LWCPrep",
            "config":"{\"IsActiveOmniscript\":{\"scriptId\":\"a3e7a000000MB31AAG\"}}"
            }
        for x in range(0,20):
            call = restClient.requestWithConnection(action=action,data=data,method='post')
            print(restClient.getLastCallElapsedTime())

        return call
    
    def test_LWCPrep2(self):
        restClient.init('ConnectionLess')
        action = '/services/apexrest/omniout/guest/v1/GenericInvoke/BusinessProcessDisplayController/LWCPrep'

        urlproxy = 'https://sf-qms.nos.pt/onboarding'
        urldirect = "https://nos--nosqms.sandbox.my.site.com/onboarding/"

        url = urldirect

        times =[]
        data = {
            "sClassName":"Vlocity LWCPrep",
            "config":"{\"IsActiveOmniscript\":{\"scriptId\":\"a3e7a000000MB31AAG\"}}"
            }
        for x in range(0,50):
            call = restClient.requestRaw(url=url,action=action,data=data,method='post')
            time = restClient.getLastCallElapsedTime()
            print(time)
            times.append(time)

        total = sum(times)
        count = len(times)
        average = total / count     

        print('Average:')
        print(average)

   # https://sf-qms.nos.pt/onboarding/services/apexrest/omniout/guest/v1/GenericInvoke/BusinessProcessDisplayController/LWCPrep'

    def test_dr_getAsset(self):
        restClient.init('NOSDEV')

        name = 'filipeGetAssetList'
       # name = 'GetAssetList'
        data = {"assetId": "02i3O00000F3qHMQAZ"}
        call = DR_IP.dr(name,data)

        print(call)

        a=1

    def test_dr_getAsset2(self):
        restClient.init('NOSQSM')

        data = {"assetId": "02i7a00000TMXGcAAP"}
        call = DR_IP.dr('GetAssetList',data)

        a=1

    def test_call_chainable_ip(self):
        restClient.init('NOSPRD')

        input = "{\"AddressName\":\"Rua Actor António Silva, Edifício Metropolis - Teste, 5   Vlocity Lógico 12, 1600-404 LISBOA\",\"BillingData\":[{\"PaymentMethod\":\"Outros\",\"InvoiceDetail\":\"Resumida\",\"IBAN\":\"\",\"Foreign\":false,\"EletronicInvoiceNumber\":\"\",\"EletronicInvoiceEmail\":\"\",\"BillType\":\"Eletrónica\",\"BillAddressZipCode\":\"1600-404\",\"BillAddressState\":\"LISBOA\",\"BillAddressName\":\"RUA ACTOR ANTÓNIO SILVA   EDIFÍCIO METROPOLIS\",\"BillAddressID\":\"8004202708\",\"BillAddressCountry\":\"Portugal\",\"BillAddressCity\":\"LISBOA\",\"BillAddressBuilding\":\"P 5. G-C\",\"BICSWIFT\":\"\"}],\"CoverageCellId\":\"01\",\"CoverageDistributionID\":\"\",\"CoverageEligibilityStatus\":\"A\",\"CoverageHeadendNumber\":\"101\",\"CoverageVoDFlag\":\"true\",\"CustomerInfo\":{\"DocId\":\"13506208\",\"NIF\":\"265641861\",\"Name\":\"TESTE I BUY 105\"},\"GlobeProccessId\":\"PRC100001902\",\"InstallationAddress\":{\"City\":\"Lisboa\",\"Door\":\"Edifício Metropolis - Teste\",\"Floor\":\"5   Vlocity Lógico 12\",\"PostalCode\":\"1600-404\",\"Street\":\"Rua Actor António Silva\"},\"ManualSale\":\"\",\"NIF\":\"265641861\",\"OriginatingChannel\":\"TLMK-I\",\"PaperlessProc\":false,\"Reason\":\"Cliente quer desligar\",\"ScheduleComments\":\"\",\"ServiceAccount\":\"S990434870\",\"Team\":\"Qualidade e Projetos\",\"UNISkipNotification\":false,\"User\":\"utvteac\",\"agentEntity\":\"200000-CATVP-TV CABO PORTUGAL,\",\"agentIU\":\"\",\"assetId\":\"02i7T00000Gl6DmQAJ\",\"automaticSchedule\":true,\"automaticScheduleMotive\":\"SEM EQUIPAMENTOS OBRIGATÓRIOS\",\"coverageReturnCable\":\"true\",\"dataframeId\":\"9b017036-f5b0-afa7-9f51-fdf00233d76f\",\"deactivationDate\":\"2024-01-19T00:00:00.000Z\",\"disconnectReason\":\"\",\"immediateInactivation\":\"\",\"loyaltyExclusionReason\":\"\",\"loyaltyPenalty\":613.33,\"mainContactEmail\":\"marta.i.lapa@nos.pt\",\"mainContactPhone\":\"931018282\",\"omniInstanceId\":\"a3l7T000002xr3nQAA\",\"orderType\":\"DESLIGAMENTO\",\"originCAV\":\"\",\"resourceAccessPoint\":10012911668,\"salesAgent\":\"utvteac\",\"salesChannel\":\"TLMK-I\",\"scheduleContact\":\"\",\"technology\":\"FTTH\",\"technologyCode\":\"FTTHNOS\",\"variables\":{\"InquiryID\":\"\",\"ReservedSchedule\":\"\"}}"

        options = "{\"postTransformBundle\":\"\",\"preTransformBundle\":\"\",\"processName\":\"MACD_nosTerminationUnai\",\"useQueueableApexRemoting\":false,\"ignoreCache\":false,\"vlcClass\":\"CustomIPCalloutQueueable\",\"useContinuation\":false}"

        name = 'CustomIPCalloutQueueable'
        method  = 'callIPAsync'
        res = DR_IP.remoteClass(name,method,input,options)

        a=1
    def test_submit_order_unai(self):
        restClient.init('NOSDEV')

        orderId = '8013O0000053v3OQAQ'  
        input = {
            "ContextId":orderId,
            "cartId":orderId,
            "orderId":orderId,
            "skipCheckoutValidation":"false"
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":True, "useQueueableApexRemoting":False}

        res = DR_IP.ip('nos_SplitSubmitOrder',input,options)

        a = 1

    def test_submit_orderr(self):
        restClient.init('NOSPRD')

        orderId = '8017T0000062hTsQAI'
        input = {
            "ContextId":orderId
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":True, "useQueueableApexRemoting":False}

        res = DR_IP.ip('nosIN_clause_SubmitOrder',input,options)

        a = 1

    def test_queueableChainable(self):

        restClient.init('NOSDEV')

        input = {
            "orderId":"801AU00000LL1yPYAT",
            "cartId":"801AU00000LL1yPYAT",
            "ContextId":"801AU00000LL1yPYAT",
            "skipCheckoutValidation":"false"
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":True, "useQueueableApexRemoting":False}
        options = { "queueableChainable":"true"}

        res = DR_IP.ip('nos_SubmitOrder_unai',input,options)     

        a=1

    def test_queueableChainable_chain(self):

        restClient.init('NOSDEV')

        input = {
            "orderId":"801AU00000LNGkjYAH",
            "cartId":"801AU00000LNGkjYAH",
            "ContextId":"801AU00000LNGkjYAH",
            "skipCheckoutValidation":"false"
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":True, "useQueueableApexRemoting":False,"vlcIPData":"9209d7cb-9236-2780-485d-9a842999e28a"}
       # options = { "queueableChainable":True, "vlcIPData":"9209d7cb-9236-2780-485d-9a842999e28a"}
       # options = {}

        res = DR_IP.ip('nos_SubmitOrder_unai',input,options)     

        a=1

    def test_queueable_manyqueries(self):

        restClient.init('DEVNOSCAT3')

        orderId = '8010Q000003PqNfQAK'
        input = {
            "cartId":orderId
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":True, "useQueueableApexRemoting":False}
       # options = {}

      #  res = DR_IP.ip_headers_testing('unaiTest_manyQueries',input,options)     
        res = DR_IP.ip_headers_testing('unaiTest_simpleIP',input,options)     

        res2 = DR_IP.ip('unaiTest_simpleIP',input,options)     

        a=1

    def test_dunning_order(self):
        #Change the step between SD and SR
        #Last SR

        restClient.init('NOSDEV')

        data = {
            "BillingAccount": "1.60104681",
            "DunningID": "DNN07810042024160418000000141359000000",
            "Step": "SD"
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":False, "useQueueableApexRemoting":False}
       
    #    res = DR_IP.ip('om_DunningSD_SR',data,options)    
        res = DR_IP.ip('unai_UnaiDunningSD_SR',data,options)    

        a=1 

    def test_100K(self):
        #Change the step between SD and SR
        #Last SR

        restClient.init('NOSDEV')

        data = {
            "trialPromoCode": "",
            "technologyCode": "FTTHNOS",
            "technology": "FTTH",
            "process": "SELL",
            "plumeProductCode": "",
            "orderType": "INSTALAÇÃO",
            "offerCode": "PROMO_WOO_FIXED_INTERNET_MOBILE_24_MONTHS_014",
            "competitors": {
                "Competitor": [
                    {
                        "Name": "W ESPECIAL"
                    }
                ]
            },
            "channel": "APP",
            "catalogCode": "DC_CAT_WOO_FIXED_INTERNET_MOBILE",
            "IsEsim_CBX": True
        }

        options = {"isDebug":True, "chainable":True, "resetCache":True, "ignoreCache":True, "queueableChainable":False, "useQueueableApexRemoting":False}
       
        res = DR_IP.ip('woo_createBasketWithPromosAndConfig',data,options)    

        a=1 



    def test_dunning_order_HD(self):
        #Change the step between SD and SR
        #Last SR

        restClient.init('NOSDEV')

        data = {
            "BillingAccount": "1.60104681",
            "DunningID": "DNN07810042024160418000000141359000000",
            "Step": "HR"
        }

        options = {"isDebug":False, "chainable":False, "resetCache":False, "ignoreCache":True, "queueableChainable":False, "useQueueableApexRemoting":False}
       
    #    res = DR_IP.ip('om_DunningSD_SR',data,options)    
        res = DR_IP.ip('om_DunningHD_Hr',data,options)    

        a=1 

    def test_ipcallqueue_chainableIpsTest(self):
        restClient.init('NOSDEV')

        code = """
            Map<String, Object> competitors = new Map<String, Object>();

            Map<String, Object> input = new Map<String, Object>{
                'cartId'=> '8013O0000053k5yQAA'
            };
                
            Map<String, Object> options = new Map<String, Object>{
                'isDebug'=> false,
                'chainable'=> true,
                'resetCache'=> false,
                'ignoreCache'=> false,
                'queueableChainable'=> false,
                'useQueueableApexRemoting'=> false,
                'processName'=>'woo_getOffers'
            };
            
            Map<String, Object> output = new Map<String, Object>();

            ipcallQueue ipc = new ipcallQueue();
            ipc.ipName = 'unai_chainableIpsTest';
            ipc.input = input;
            ipc.options = options;
            
            System.enqueueJob(ipc);

        """
        res = tooling.executeAnonymous(code=code)

        a=1

