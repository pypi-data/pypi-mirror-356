import unittest
##from InCli import InCli
from incli.sfapi import account,restClient,CPQ

class Test_Refresh_cache(unittest.TestCase):
    def test_main(self):
        restClient.init('NOSQSM')
        catalog = "DC_CAT_WOO_MOBILE"
     #   catalog = "test"

        res = restClient.requestWithConnection(f'/services/apexrest/vlocity_cmt/v3/admin/catalogs/{catalog}/catalogprofile')
        print(res['apiResponse']['data']['metrics'])




        rules_lenght = 0
        rules_sets = []
        for key in res['apiResponse']['data']['catalogCodeToRuleAssignments']:
            rules = res['apiResponse']['data']['catalogCodeToRuleAssignments'][key]
            rules_sets.extend(rules)
            rules_lenght = rules_lenght + len(rules)
            a=1

        print(f"Rules length {rules_lenght}")

        ruleset_combinations = []
        if 1==2:
            for rule in rules_sets:
                res = restClient.requestWithConnection(f'/services/apexrest/vlocity_cmt/v3/admin/ruleset/{rule}/rulesetcombinations')
                ruleset_combinations.append(res['apiResponse'])
                a=1




        res = restClient.requestWithConnection(f'/services/apexrest/vlocity_cmt/v3/admin/catalogs/{catalog}/contextdimensions')
        print(f"contextdimensions {len(res['apiResponse'])}")





        offset = 0
        ctxCombos = []
        while offset != -1:
            data = {"catalogCode":"DC_CAT_WOO_MOBILE","dimensions":{},"pagesize":20,"offset":offset,"validate":False}
            res = restClient.requestWithConnection(f'/services/apexrest/vlocity_cmt/v3/admin/catalogs/{catalog}/contextcombinations',method='post',data=data)
            if len(res['apiResponse'])>0:
                ctxCombos.append(res)
                offset = offset + 20

            if len(res['apiResponse'])<20:
                offset = -1

            if len(res['apiResponse'])==0:
                offset = -1         

            a=1

        print(f"ctxCombos {len(ctxCombos)}")




        for ctxCombo in ctxCombos:
            data = {"catalogCode":catalog,"cachekey":ctxCombo['cacheKey']}
            res = restClient.requestWithConnection(f'/services/apexrest/vlocity_cmt/v3/admin/catalogs/{catalog}/contexteligibility',method='post',data=data)
            a=1



        a=1

        
