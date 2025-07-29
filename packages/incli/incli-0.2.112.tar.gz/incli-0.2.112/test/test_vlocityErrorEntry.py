import unittest,simplejson,sys
from incli import incli
from incli.sfapi import VlocityErrorLog,restClient,VlocityTrackingEntry,query,utils,jsonFile
from operator import itemgetter

class Test_VlocityErrorEntry(unittest.TestCase):

    def test_get_errors(self):
        restClient.init('NOSPRD')

        VlocityErrorLog.get_errors()

        print()

    def test_get_errors(self):
        restClient.init('NOSPRD')

        VlocityErrorLog.get_errors()

        print()
    def test_print_errors_orderNum(self):
        restClient.init('NOSPRD')

        orderNums = [
            '00300871',
            '00300083',
            '00300052',
            '00298441',
            '00303789',
            '00303731',
            '00303549',
            '00303520',
            '00303458',
            '00303477',
            '00302987',
            '00303406',
            '00303322',
            '00302681',
            '00302623'
        ]

        original_stdout = sys.stdout
        _filename = f"vte_output.txt"
        with open(_filename, 'w') as f:
            sys.stdout = f 
            for orderNumber in orderNums:
                VlocityTrackingEntry.print_error_list(orderNumber=orderNumber)
                print()
            sys.stdout = original_stdout 
            print()
            print(f"   File {_filename} created.")

        print()
    def test_get_error_ip(self):
        restClient.init('NOSDEV')

        Id = 'a6K3O000000FHuqUAG'

        q = f"select fields(all) from vlocity_cmt__VlocityErrorLogEntry__c where Id='{Id}' limit 10"

        res = query.query(q)


        out=[]
        for record in res['records']:
            data = record['vlocity_cmt__InputData__c']
            datas = simplejson.loads(data)

            theFile =jsonFile.write('TheIPError_1',datas)
            
            out.append(datas)
            print(datas['ErrorMessage__c'])


      #  file_csv.write('VlocityErrorLogEntry_1',out)

        print()

        
    def test_getTrackingEntries(self):
        restClient.init('DEVNOSCAT4')

        #q = 'select vlocity_cmt__VlocityInteractionToken__c from vlocity_cmt__VlocityTrackingEntry__c order by SystemModstamp desc limit 1'
        
        q = "select fields(all) from vlocity_cmt__VlocityTrackingEntry__c order where Id = 'a6R3O000000JFBTUA4' limit 1"

        call = query.query(q)

        data_str = call['records'][0]['vlocity_cmt__Data__c']

        data = simplejson.loads(data_str)

        a=1

    def test_getTrackingEntries2(self):
        restClient.init('DEVNOSCAT4')

        #q = 'select vlocity_cmt__VlocityInteractionToken__c from vlocity_cmt__VlocityTrackingEntry__c order by SystemModstamp desc limit 1'

        id = 'd540f937-f362-4c4f-afdf-d44114c1c90e'
        id = '389390cd-2b54-4f03-956f-ce2a0dfc3461'

        
       # q = "select fields(all) from vlocity_cmt__VlocityTrackingEntry__c order where SalesforceSessionToken__c = 'a4fb3ca067acda62c91c34e8c59eeac4ce21109a77dc5f0baa142546cb172e370da8423cab594794e25de33946c057b72abfb588c864e9907be000450158ec0c' limit 200"
        q = f"select fields(all) from vlocity_cmt__VlocityTrackingEntry__c order where vlocity_cmt__VlocityInteractionToken__c = '{id}' or ParentInteractionToken__c ='{id}'limit 200"

        call = query.query(q)

        for r in call['records']:
            data = simplejson.loads(r['vlocity_cmt__Data__c'])
            r['TS'] = data['Timestamp']
            r['ElementType']=data['ElementType'] if 'ElementType' in data else ''
            r['ElementName']=data['ElementName'] if 'ElementName' in data else ''
            r['ElapsedTime']=data['ElapsedTime'] if 'ElapsedTime' in data else ''
            r['ActionTargetType']=data['ActionTargetType'] if 'ActionTargetType' in data else ''
            r['ActionTargetName']=data['ActionTargetName'] if 'ActionTargetName' in data else ''
            r['IntegrationProcedureKey']=data['IntegrationProcedureKey'] if 'IntegrationProcedureKey' in data else ''
            r['data'] = data
            r['ElementName']=f"{data['ClassName']}-{data['TrackingEvent']}" if 'ClassName' in data else r['ElementName']
            r['Request'] = True if 'Request' in data and data['Request'] != None else False

        sorted_list = sorted(call['records'], key=itemgetter('TS'))

        for r in sorted_list:
            data = simplejson.loads(r['vlocity_cmt__Data__c'])
        #    print(f"{r['TS']} {r['vlocity_cmt__TrackingService__c']}  {r['vlocity_cmt__VlocityInteractionToken__c']}   {r['ParentInteractionToken__c']}    {r['vlocity_cmt__TrackingCategory__c']}  {r['ElementType']}  {r['ElementName']}   {r['ActionTargetName']}")


        utils.printFormated(sorted_list,"TS:Name:ElapsedTime:vlocity_cmt__TrackingService__c:vlocity_cmt__VlocityInteractionToken__c:ParentInteractionToken__c:vlocity_cmt__TrackingCategory__c:ElementType:ElementName:ActionTargetName:Request",rename='vlocity_cmt__TrackingService__c%TrackingService:vlocity_cmt__TrackingCategory__c%TrackingCategory:vlocity_cmt__VlocityInteractionToken__c%InterationToken')
        a=1
#data['SalesforceSessionToken']

#14ca1649f9cfd6e813194c01890ce0c68098c5f7a9257fea6c6337c25f166b380be8aed0e943ef94ba3aad26c494c88178e798f931b7c4408225e56cb69a8f12