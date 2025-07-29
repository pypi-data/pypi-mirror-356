import unittest,sys,simplejson
from incli.sfapi import restClient,query,utils,file_csv


class Test_Query(unittest.TestCase):
    def test_query1(self):
        restClient.init('DEVNOSCAT2')
        res = query.query("SELECT Id,Name FROM vlocity_cmt__DRBUNDLE__C ")

        output = []

        for rec in res['records']:
            res2 = query.query(f"SELECT count(Id) FROM vlocity_cmt__DRMapItem__c where name = '{rec['Name']}' ")
            out = {
                'Name':rec['Name'],
                'size:':res2['records'][0]['expr0']
            }
            output.append(out)
            print(".")
            
        utils.printFormated(output)

        print()

    def test_query2(self):
        restClient.init('NOSDEV')
        orderId_error = '8013O000004yyhsQAA'
        orderId_works = '8013O000004yyz8QAA'
        orderId = orderId_error
      #  orderId = orderId_works
        res = query.query(f"SELECT fields(all)  FROM vlocity_cmt__OrderPriceAdjustment__c where vlocity_cmt__OrderId__c  = '{orderId}' limit 200 ")

        for r in res['records']:
            res2 = query.query(f"select Id from orderItem where Id = '{r['vlocity_cmt__OrderItemId__c']}'")
            print(f"{r['vlocity_cmt__OrderItemId__c']}      {len(res2['records'])}")

            a=1

        a=1


