import unittest
from incli.sfapi import restClient,query,utils

class Test_Omniscripts(unittest.TestCase):
    def test_omnis(self):
        restClient.init('NOSDEV')

        instanceID = 'a3l3O000000ER5YQAW'
        omniId = 'a3m3O000000KXurQAG'
        instanceID = 'a3l3O000000ER5iQAG'
        new = 'a3m3O000000KXvLQAW'
        res = query.query(f"select fields(all) from vlocity_cmt__OmniScriptInstance__c where Id = '{instanceID}' limit 100")

        res2 = query.query(f"select fields(all) from vlocity_cmt__OmniScriptInstance__c where vlocity_cmt__OmniScriptId__c = '{omniId}' limit 100")

        res3 = query.query(f"select fields(all) from vlocity_cmt__OmniScript__c limit 1")
        omnis = query.query(f"select fields(all) from vlocity_cmt__OmniScript__c where vlocity_cmt__Type__c = 'unai' and vlocity_cmt__SubType__c = 'test' limit 100")

        omnis_sorted = sorted(omnis['records'], key=lambda x: x['vlocity_cmt__Version__c'])

        results = []
        for omni in omnis_sorted:
            instances = query.query(f"select fields(all) from vlocity_cmt__OmniScriptInstance__c where vlocity_cmt__OmniScriptId__c = '{omni['Id']}' limit 100")
            for instance in instances['records']:
                result = {
                    'version': instance['vlocity_cmt__OmniScriptVersion__c'],
                    'Id' : instance['Id'],
                    'status': instance['vlocity_cmt__Status__c']
                }
                results.append(result)

                attachement = query.query(f"select fields(all) from attachment where parentId = '{instance['Id']}' and Name = 'OmniScriptFullJSON.json' limit 200")

                for attach in attachement['records']:
                    print(attach['Name'])
                    body = restClient.requestWithConnection(action=attach['Body'])  

                print()

        utils.printFormated(results)
        print()



