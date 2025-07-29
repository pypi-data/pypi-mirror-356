import unittest
##from InCli import InCli
from incli.sfapi import account,restClient,query,tooling

class Test_Permissions(unittest.TestCase):
    def test_main(self):

        def split_list(input_list, n):
            return [input_list[i:i + n] for i in range(0, len(input_list), n)]
        
        restClient.init('NOSDEV')

        q1 = query.query("SELECT Id, SetupEntityId, Parent.Profile.Name, SetupEntityType FROM SetupEntityAccess WHERE Parent.Profile.Name = 'Onboarding Community Partner'")

        entityTypes = ["ApexClass","CustomEntityDefinition","TabSet","ApexPage","CustomPermission"]
        entities = {}

     #   for entityType in entityTypes:
     #       entities[entityType] = [r['SetupEntityId'] for r in q1['records'] if r['SetupEntityType'] == entityType]

        for r in q1['records']:
            entity = { "Id":r['SetupEntityId'] }
            if r['SetupEntityType'] not in entities:
                entities[r['SetupEntityType']] = {}    
                
            entities[r['SetupEntityType']][entity['Id']] = entity

        ids = list(entities['CustomEntityDefinition'].keys())
        q2 = tooling.query(f"SELECT Id,DeveloperName FROM CustomObject WHERE Id in ({query.IN_clause(ids)}) ")
        for r in q2['records']:
            entities['CustomEntityDefinition'][r['Id']]['entityName'] = r['DeveloperName']

        ids = list(entities['ApexClass'].keys())
        ids_n = split_list(ids,200)
        for id_chunk in ids_n:
            q2 = tooling.query(f"SELECT Id,NamespacePrefix,Name FROM ApexClass WHERE Id in ({query.IN_clause(id_chunk)}) ")
            for r in q2['records']:
                prefix = r['NamespacePrefix'] if r['NamespacePrefix']!=None else ""
                entities['ApexClass'][r['Id']]['entityName'] = prefix + "." + r['Name']

        ids = list(entities['ApexPage'].keys())
        q2 = tooling.query(f"SELECT Id,Name FROM ApexPage WHERE Id in ({query.IN_clause(ids)}) ")
        for r in q2['records']:
            entities['ApexPage'][r['Id']]['entityName'] = r['Name']

        ids = list(entities['TabSet'].keys())
        q2 = query.query(f"SELECT Id,ApplicationId,Name,NamespacePrefix FROM AppMenuItem WHERE ApplicationId in ({query.IN_clause(ids)}) ")
        for r in q2['records']:
            entities['TabSet'][r['ApplicationId']]['entityName'] = r['NamespacePrefix'] + "."+ r['Name'] 




        
