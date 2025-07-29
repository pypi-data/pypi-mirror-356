import unittest
#from InCli import InCli
from incli.sfapi import restClient,query,Sobjects,CPQ,OM,DR_IP,jsonFile

class Test_OM(unittest.TestCase):
    def test_main(self):
        restClient.init('NOSDEV')

        orchestrationPlanId = 'a453O000000FBKLQA4'
        orderId = '8013O000003mfcPQAQ'

        finished = False
        while finished == False:
            q_plan = f"select fields(all) from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}'  limit 100"

            res = query.query(q_plan)

            if res['records'][0]['vlocity_cmt__State__c'] == 'Completed':
                finished = True
                continue

            orchestrationPlanId = res['records'][0]['Id']

            q = f"select fields(all) from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c = '{orchestrationPlanId}'  limit 200"

            res2 = query.query(q)

            active = [r for r in res2['records'] if r['vlocity_cmt__State__c'] in ['Fatally Failed']]
            for r in active:
                print(f"{r['Name']} {r['vlocity_cmt__State__c']}")
                data = {
                    'vlocity_cmt__State__c':'Completed'
                }
                rr = Sobjects.update(r['Id'],data,sobjectname='vlocity_cmt__OrchestrationItem__c')
                a=1
            

        a=1

    def test_clean_plan(self):
        restClient.init('NOSQSM')
        orderId = '801AU00000TUb36YAD'

        res = OM.delete_orchestration_plan_and_decomposition(orderId)

        a=1
        
    def test_cancel_unfreeze(self):
        restClient.init('qmscopy')

        orderId = '801AP00000lcVe4YAE'

        call2 = CPQ.unfreezeOrder(orderId)

        a=1


#SELECT ID, NAME, vlocity_cmt__PRODUCT2ID__R.ID, vlocity_cmt__PRODUCT2ID__R.NAME, vlocity_cmt__PRODUCT2ID__R.vlocity_cmt__ISNOTASSETIZABLE__C, VLOCITY_CMT__BILLINGACCOUNTID__C, VLOCITY_CMT__SERVICEACCOUNTID__C, VLOCITY_CMT__ATTRIBUTESELECTEDVALUES__C, VLOCITY_CMT__ATTRIBUTESMARKUPDATA__C, VLOCITY_CMT__LINENUMBER__C, VLOCITY_CMT__ACTION__C, TOLABEL(vlocity_cmt__ACTION__C) ACTION__C__TRANSLATED, VLOCITY_CMT__SUBACTION__C, TOLABEL(vlocity_cmt__SUBACTION__C) SUBACTION__C__TRANSLATED, VLOCITY_CMT__SUPPLEMENTALACTION__C, TOLABEL(vlocity_cmt__SUPPLEMENTALACTION__C) SUPPLEMENTALACTION__C__TRANSLATED, VLOCITY_CMT__SUPERSEDEDFRLINEID__C, vlocity_cmt__SUPERSEDEDFRLINEID__R.vlocity_cmt__FULFILMENTREQUESTID__C, vlocity_cmt__SUPERSEDEDFRLINEID__R.vlocity_cmt__FIRSTVERSIONFRLINEID__C, VLOCITY_CMT__FIRSTVERSIONFRLINEID__C, vlocity_cmt__FIRSTVERSIONFRLINEID__R.vlocity_cmt__FULFILMENTREQUESTID__C, VLOCITY_CMT__MAINORDERITEMID__C, vlocity_cmt__MAINORDERITEMID__R.vlocity_cmt__FIRSTVERSIONFRLINEID__C, VLOCITY_CMT__ISPONRREACHED__C, VLOCITY_CMT__ISREADYFORACTIVATION__C, VLOCITY_CMT__ISORCHESTRATIONITEMSINFINALSTATE__C, VLOCITY_CMT__ISCHANGESALLOWED__C, VLOCITY_CMT__INVENTORYITEMID__C, VLOCITY_CMT__ITEMNUMBER__C, VLOCITY_CMT__EXPECTEDCOMPLETIONDATE__C, (SELECT ID,NAME, vlocity_cmt__SOURCEORDERITEMID__C, vlocity_cmt__SOURCEORDERITEMID__R.PRODUCT2.ID, vlocity_cmt__SOURCEORDERITEMID__R.PRODUCT2.NAME, vlocity_cmt__SOURCEFULFILMENTREQUESTLINEID__C, vlocity_cmt__SOURCEFULFILMENTREQUESTLINEID__R.vlocity_cmt__PRODUCT2ID__R.ID, vlocity_cmt__SOURCEFULFILMENTREQUESTLINEID__R.vlocity_cmt__PRODUCT2ID__R.NAME, vlocity_cmt__ISCONDITIONFAILED__C, vlocity_cmt__DECOMPOSITIONRELATIONSHIPMETADATA__C FROM vlocity_cmt__SOURCEDECOMPOSITIONRELATIONSHIPS__R), VLOCITY_CMT__FULFILMENTREQUESTID__C, vlocity_cmt__FULFILMENTREQUESTID__R.vlocity_cmt__FIRSTVERSIONFRID__C, vlocity_cmt__FULFILMENTREQUESTID__R.vlocity_cmt__ORDERID__C, VLOCITY_CMT__FULFILMENTSTATUS__C, TOLABEL(vlocity_cmt__FULFILMENTSTATUS__C) FULFILMENTSTATUS__C__TRANSLATED, (SELECT vlocity_cmt__FULFILMENTREQUESTLINEID__C, vlocity_cmt__ROOTORDERITEMID__C       FROM vlocity_cmt__SOURCEROOTORDERITEMS__R), VLOCITY_CMT__INVENTORYITEMID__R.ID, VLOCITY_CMT__INVENTORYITEMID__R.NAME, VLOCITY_CMT__INVENTORYITEMID__R.vlocity_cmt__ACCOUNTID__C, VLOCITY_CMT__INVENTORYITEMID__R.vlocity_cmt__LINENUMBER__C, VLOCITY_CMT__INVENTORYITEMID__R.vlocity_cmt__PRODUCTID__C, VLOCITY_CMT__INVENTORYITEMID__R.VLOCITY_CMT__PRODUCTID__R.NAME, VLOCITY_CMT__INVENTORYITEMID__R.VLOCITY_CMT__PROVISIONINGSTATUS__C, VLOCITY_CMT__INVENTORYITEMID__R.VLOCITY_CMT__BILLINGACCOUNTID__C, VLOCITY_CMT__INVENTORYITEMID__R.VLOCITY_CMT__SERVICEACCOUNTID__C, VLOCITY_CMT__INVENTORYITEMID__R.VLOCITY_CMT__ATTRIBUTESELECTEDVALUES__C, VLOCITY_CMT__INVENTORYITEMID__R.VLOCITY_CMT__QUALIFICATIONEXPIRATIONDATE__C, VLOCITY_CMT__INVENTORYITEMID__R.RECORDTYPEID FROM vlocity_cmt__FulfilmentRequestLine__c WHERE  vlocity_cmt__FulfilmentRequestID__r.VLOCITY_CMT__OrderId__c = '801AP00000lCgBsYAK' order by VLOCITY_CMT__LineNumber__c


    def test_cancel_amend(self):
        restClient.init('DEVNOSCAT3')

        supplementalOrder = '8013O0000053DKdQAM'
        amendedOrder = '8013O0000053DKdQAM'

        call1 = CPQ.cancelOrder(supplementalOrder)
        call2 = CPQ.unfreezeOrder(amendedOrder)

        a=1

    def test_submitCancelOrder(self):
        restClient.init('DEVNOSCAT3')

        supplementalOrder = '8013N000007pZhWQAU'
        orderId = '8013N000007pZhHQAU'

        call1 = CPQ.submitCancelOrder(orderId,supplementalOrder)

        a=1

    def test_amend_order(self):

        restClient.init('NOSDEV')
        cartId ='8013O0000053Z3jQAE'
        call1 = CPQ.preValidate(cartId)
        f1 = jsonFile.write('sss',call1)
        call2 = CPQ.createSupplementalOrder(cartId)
    #    call2 = CPQ.unfreezeOrder(cartId)

        a=1
        

    def test_decompose(self):
        restClient.init('NOSDEV')

        cartId = '8013O000004xlFMQAY'

        res = OM.decomposeAndCreatePlan(cartId)

        res = OM.viewDecomposedOrder(cartId)

    def test_get_frl_for_order(self):
        restClient.init('NOSDEV')

        orderId = ''
        data = {
            "Order": {
                "COMOrderId": "8013O000004zYh7QAE",
                "ProvisioningSubscriberId": 50014846,
                "eTrackingId": "8013O000004zYh7QAE|2599637|5898533",
                "Items": [
                    {
                        "Id": "oEDkNIg75",
                        "Attribute": [
                            {
                                "Code": "ATT_DC_ASSET_ID",
                                "Value": 200177592
                            }
                        ]
                    },
                    {
                        "Id": "nCIVJIaFZ",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177676
                        }
                    },
                    {
                        "Id": "BW1VqfKUh",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177675
                        }
                    },
                    {
                        "Id": "g3qHgqRxk",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177534
                        }
                    },
                    {
                        "Id": "jllayH1jL",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177565
                        }
                    },
                    {
                        "Id": "vwavOOLGk",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177635
                        }
                    },
                    {
                        "Id": "2g3f00p8y",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177539
                        }
                    },
                    {
                        "Id": "p6jPEo6dx",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177554
                        }
                    },
                    {
                        "Id": "A7YwvyCBU",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177537
                        }
                    },
                    {
                        "Id": "nrvRGFfbP",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177563
                        }
                    },
                    {
                        "Id": "wX8GcqjZC",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 200177609
                        }
                    }
                ],
                "ExternalSOMOrderId": "a6u3O000005c86aQAA",
                "TaskId": "a433O000000RAn3QAG",
                "Account": {
                    "EntityID": 0
                },
                "Status": "Completed"
            }
        }
        orchestrationItemId = 'a433O000000RAn3QAG'

        res0 = query.query(f"SELECT Id, vlocity_cmt__OrderItemId__c, Name, vlocity_cmt__State__c, vlocity_cmt__OrchestrationItemType__c, vlocity_cmt__OrderItemId__r.orderId, vlocity_cmt__ExecutionLog__c, vlocity_cmt__ErrorQueueId__c, vlocity_cmt__ManualQueueId__c, vlocity_cmt__OrderItemId__r.vlocity_cmt__ServiceAccountId__c, vlocity_cmt__OrderItemId__r.vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c, vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c, vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.NOS_t_CoverageTechnology__c, vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.Type, vlocity_cmt__FulfilmentRequestLineId__r.vlocity_cmt__ServiceAccountId__r.NOS_t_IdConta__c, vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.NOS_t_ChangeType__c FROM vlocity_cmt__OrchestrationItem__c WHERE Id = '{orchestrationItemId}'")

        somOrderId= data['Order']['ExternalSOMOrderId']
        som = query.query(f"SELECT  SOMOrderId__c, SOMOrderId__r.COMOrderId__r.Type, SOMOrderId__r.SOMType__c, SOMOrderId__r.COMOrderId__r.VOM_Order_Context__c FROM SOMOrderItem__c WHERE SOMOrderId__c = '{somOrderId}' LIMIT 1")

        res1 = query.query(f"select Id from vlocity_cmt__FulfilmentRequest__c where vlocity_cmt__OrderId__c   = '8013O000004zYh7QAE' ")

        ids = [r['Id'] for r in res1['records']]

        res2 = query.query(f"select Id,vlocity_cmt__JSONAttribute__c from vlocity_cmt__FulfilmentRequestLine__c where vlocity_cmt__FulfilmentRequestID__c  in ({query.IN_clause(ids)}) ")

        for r in res2['records']:
            if 'oEDkNIg75' in r['vlocity_cmt__JSONAttribute__c']:
                print('------------------------------')
        a=1
  
    def test_billing_info(self):
        restClient.init('NOSDEV')
        orderId = '8013O000004zq8NQAQ'
        
        action = f"/services/apexrest/BillingCommercialGroupListener/a433O000002zgVjQAI"

        data = {
            "Order" : {
                "OrderItem" : [ {
                "Attribute" : [ {
                    "Value" : "1728487",
                    "Code" : "ATT_DC_COMMERCIAL_GROUP"
                } ],
                "ItemInternalID" : "QhrzUhRAh"
                } ],
                "Status" : "",
                "eTrackingId" : "47160864"
            }
        }
        res = restClient.callAPI(action,method='post',data= data)

        print(res)
        print()
        a=1

  
    def test_heap_om_problem(self):
        restClient.init('NOSDEV')

        data = {
           "Order": {
                "COMOrderId": "8013O000004zq8NQAQ",
                "eTrackingId": "8013O000004zq8NQAQ|2601288|5906764",
                "ProvisioningSubscriberId": 123,
                "Items": [
                    {
                        "Id": "VtJOl6q9Q",
                        "ActivationDate": "2024-02-20 17:07:28",
                        "GuidingId": "",
                        "Attribute": [
                            {
                                "Code": "ATT_DC_ASSET_ID",
                                "Value": 111
                            }
                        ]
                    },
                    {
                        "Id": "ZrVwlr7SJ",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 121
                        }
                    },
                    {
                        "Id": "QBBKJxUBo",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 222
                        }
                    },
                    {
                        "Id": "kRSgRyUKd",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 333
                        }
                    },
                    {
                        "Id": "s9T3X668a",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 444
                        }
                    },
                    {
                        "Id": "jX0AMCMJZ",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 555
                        }
                    },
                    {
                        "Id": "pfYOf8IPt",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 666
                        }
                    },
                    {
                        "Id": "bbmJxuscZ",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 777
                        }
                    },
                    {
                        "Id": "JWxNCZ3b7",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 888
                        }
                    },
                    {
                        "Id": "UsQqVPXb5",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 999
                        }
                    },
                    {
                        "Id": "J4k3kFje8",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 123
                        }
                    },
                    {
                        "Id": "CBtR4Lf8q",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 232
                        }
                    },
                    {
                        "Id": "ssL4TEO4D",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 343
                        }
                    },
                    {
                        "Id": "AT7HTgIce",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 545
                        }
                    },
                    {
                        "Id": "GThqAF08s",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 656
                        }
                    },
                    {
                        "Id": "VDW6BMNuz",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 767
                        }
                    },
                    {
                        "Id": "FUBlxCWwm",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 878
                        }
                    },
                    {
                        "Id": "tEDHCGXnM",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 989
                        }
                    },
                    {
                        "Id": "QgDXqZkFm",
                        "ActivationDate": "2024-02-20 17:09:12",
                        "GuidingId": "",
                        "Attribute": {
                            "Code": "ATT_DC_ASSET_ID",
                            "Value": 789
                        }
                    }
                ],
                "ExternalSOMOrderId": "a6u3O000005cpxyQAA",
                "TaskId": "a433O000000RShHQAW",
                "Account": {
                    "EntityID": 0
                },
                "Status": "Completed"
            }
        }
       # action = "/services/apexrest/XOrderAsyncListener2/a433O000000RAn3QAG"
        action = "/services/apexrest/XOrderAsyncListener/a433O000000RAn3QAG"
     #   action = "/services/apexrest/SOMOrderAsyncListener/a433O000000RAn3QAG"
        action = "/services/apexrest/UnaiSOMOrderAsyncListenerB2C/a433O000000RShHQAW"

        res = restClient.requestWithConnection(action=action,method='post',data=data)

        print(res)

        a= 1

        #idSet:[ "a363O00000043pVQAQ", "a363O00000043pYQAQ", "a363O00000043pZQAQ", "a363O00000043pfQAA", "a363O00000043pnQAA", "a363O00000043pvQAA", "a363O00000043q0QAA", "a363O00000043qAQAQ", "a363O00000043qYQAQ" ]
        #idSet:[ "a363O00000043qnQAA", "a363O00000043qqQAA", "a363O00000043qrQAA", "a363O00000043qyQAA", "a363O00000043rrQAA", "a363O00000043rvQAA", "a363O00000043rxQAA", "a363O00000043rzQAA", "a363O00000043s1QAA", "a363O00000043s2QAA" ]
        #idSet:[ "a363O00000043s4QAA", "a363O00000043s6QAA", "a363O00000043s7QAA", "a363O00000043sAQAQ", "a363O00000043sDQAQ", "a363O00000043sEQAQ", "a363O00000043sHQAQ", "a363O00000043sKQAQ", "a363O00000043sMQAQ", "a363O00000043sNQAQ", "a363O00000043sOQAQ", "a363O00000043sSQAQ", "a363O00000043sTQAQ", "a363O00000043sXQAQ", "a363O00000043sZQAQ", "a363O00000043sbQAA", "a363O00000043shQAA", "a363O00000043skQAA", "a363O00000043snQAA" ]
        #idSet:[ ]  220-250
        #idSet:[ ]

    def test_attributes(self):
        restClient.init('NOSDEV')

        data = {
            'attributeCodeValueList':[ {
                "Value" : "OMEGA",
                "Code" : "ATT_DC_RELATED_SYSTEM"
                }, {
                "Value" : "PROVISIONING",
                "Code" : "ATT_DC_ROLE"
                }],
            'Id':'a363O00000043pVQAQ',
            'Ids':[ "a363O00000043pTQAQ", "a363O00000043pUQAQ", "a363O00000043pVQAQ", "a363O00000043pWQAQ", "a363O00000043pXQAQ", "a363O00000043pYQAQ", "a363O00000043pZQAQ", "a363O00000043paQAA", "a363O00000043pbQAA", "a363O00000043pcQAA", "a363O00000043pdQAA", "a363O00000043peQAA", "a363O00000043pfQAA", "a363O00000043pgQAA", "a363O00000043phQAA", "a363O00000043piQAA", "a363O00000043pjQAA", "a363O00000043pkQAA", "a363O00000043plQAA", "a363O00000043pmQAA", "a363O00000043pnQAA", "a363O00000043poQAA", "a363O00000043ppQAA", "a363O00000043pqQAA", "a363O00000043prQAA", "a363O00000043psQAA", "a363O00000043ptQAA", "a363O00000043puQAA", "a363O00000043pvQAA", "a363O00000043pwQAA", "a363O00000043pxQAA", "a363O00000043pyQAA", "a363O00000043pzQAA", "a363O00000043q0QAA", "a363O00000043q1QAA", "a363O00000043q2QAA", "a363O00000043q3QAA", "a363O00000043q4QAA", "a363O00000043q5QAA", "a363O00000043q6QAA", "a363O00000043q7QAA", "a363O00000043q8QAA", "a363O00000043q9QAA", "a363O00000043qAQAQ", "a363O00000043qBQAQ", "a363O00000043qCQAQ", "a363O00000043qDQAQ", "a363O00000043qEQAQ", "a363O00000043qFQAQ", "a363O00000043qGQAQ", "a363O00000043qHQAQ", "a363O00000043qIQAQ", "a363O00000043qJQAQ", "a363O00000043qKQAQ", "a363O00000043qLQAQ", "a363O00000043qMQAQ", "a363O00000043qNQAQ", "a363O00000043qOQAQ", "a363O00000043qPQAQ", "a363O00000043qQQAQ", "a363O00000043qRQAQ", "a363O00000043qSQAQ", "a363O00000043qTQAQ", "a363O00000043qUQAQ", "a363O00000043qVQAQ", "a363O00000043qWQAQ", "a363O00000043qXQAQ", "a363O00000043qYQAQ", "a363O00000043qZQAQ", "a363O00000043qaQAA", "a363O00000043qbQAA", "a363O00000043qcQAA", "a363O00000043qdQAA", "a363O00000043qeQAA", "a363O00000043qfQAA", "a363O00000043qgQAA", "a363O00000043qhQAA", "a363O00000043qiQAA", "a363O00000043qjQAA", "a363O00000043qkQAA", "a363O00000043qlQAA", "a363O00000043qmQAA", "a363O00000043qnQAA", "a363O00000043qoQAA", "a363O00000043qpQAA", "a363O00000043qqQAA", "a363O00000043qrQAA", "a363O00000043qsQAA", "a363O00000043qtQAA", "a363O00000043quQAA", "a363O00000043qvQAA", "a363O00000043qwQAA", "a363O00000043qxQAA", "a363O00000043qyQAA", "a363O00000043qzQAA", "a363O00000043r0QAA", "a363O00000043r1QAA", "a363O00000043r2QAA", "a363O00000043r3QAA", "a363O00000043r4QAA", "a363O00000043r5QAA", "a363O00000043r6QAA", "a363O00000043r7QAA", "a363O00000043r8QAA", "a363O00000043r9QAA", "a363O00000043rAQAQ", "a363O00000043rBQAQ", "a363O00000043rCQAQ", "a363O00000043rDQAQ", "a363O00000043rEQAQ", "a363O00000043rFQAQ", "a363O00000043rGQAQ", "a363O00000043rHQAQ", "a363O00000043rIQAQ", "a363O00000043rJQAQ", "a363O00000043rKQAQ", "a363O00000043rLQAQ", "a363O00000043rMQAQ", "a363O00000043rNQAQ", "a363O00000043rOQAQ", "a363O00000043rPQAQ", "a363O00000043rQQAQ", "a363O00000043rRQAQ", "a363O00000043rSQAQ", "a363O00000043rTQAQ", "a363O00000043rUQAQ", "a363O00000043rVQAQ", "a363O00000043rWQAQ", "a363O00000043rXQAQ", "a363O00000043rYQAQ", "a363O00000043rZQAQ", "a363O00000043raQAA", "a363O00000043rbQAA", "a363O00000043rcQAA", "a363O00000043rdQAA", "a363O00000043reQAA", "a363O00000043rfQAA", "a363O00000043rgQAA", "a363O00000043rhQAA", "a363O00000043riQAA", "a363O00000043rjQAA", "a363O00000043rkQAA", "a363O00000043rlQAA", "a363O00000043rmQAA", "a363O00000043rnQAA", "a363O00000043roQAA", "a363O00000043rpQAA", "a363O00000043rqQAA", "a363O00000043rrQAA", "a363O00000043rsQAA", "a363O00000043rtQAA", "a363O00000043ruQAA", "a363O00000043rvQAA", "a363O00000043rwQAA", "a363O00000043rxQAA", "a363O00000043ryQAA", "a363O00000043rzQAA", "a363O00000043s0QAA", "a363O00000043s1QAA", "a363O00000043s2QAA", "a363O00000043s3QAA", "a363O00000043s4QAA", "a363O00000043s5QAA", "a363O00000043s6QAA", "a363O00000043s7QAA", "a363O00000043s8QAA", "a363O00000043s9QAA", "a363O00000043sAQAQ", "a363O00000043sBQAQ", "a363O00000043sCQAQ", "a363O00000043sDQAQ", "a363O00000043sEQAQ", "a363O00000043sFQAQ", "a363O00000043sGQAQ", "a363O00000043sHQAQ", "a363O00000043sIQAQ", "a363O00000043sJQAQ", "a363O00000043sKQAQ", "a363O00000043sLQAQ", "a363O00000043sMQAQ", "a363O00000043sNQAQ", "a363O00000043sOQAQ", "a363O00000043sPQAQ", "a363O00000043sQQAQ", "a363O00000043sRQAQ", "a363O00000043sSQAQ", "a363O00000043sTQAQ", "a363O00000043sUQAQ", "a363O00000043sVQAQ", "a363O00000043sWQAQ", "a363O00000043sXQAQ", "a363O00000043sYQAQ", "a363O00000043sZQAQ", "a363O00000043saQAA", "a363O00000043sbQAA", "a363O00000043scQAA", "a363O00000043sdQAA", "a363O00000043seQAA", "a363O00000043sfQAA", "a363O00000043sgQAA", "a363O00000043shQAA", "a363O00000043siQAA", "a363O00000043sjQAA", "a363O00000043skQAA", "a363O00000043slQAA", "a363O00000043smQAA", "a363O00000043snQAA", "a363O00000043soQAA", "8023O000008pb4DQAQ", "8023O000008pb48QAA", "8023O000008pb4NQAQ", "8023O000008pb4cQAA", "8023O000008pb4dQAA", "8023O000008pb4XQAQ", "8023O000008pb4IQAQ", "8023O000008pb4JQAQ", "8023O000008pb4KQAQ", "8023O000008pb4LQAQ", "8023O000008pb41QAA", "8023O000008pb42QAA", "8023O000008pb43QAA", "8023O000008pb44QAA", "8023O000008pb45QAA", "8023O000008pb46QAA", "8023O000008pb47QAA", "8023O000008pb3pQAA", "8023O000008pb3qQAA", "8023O000008pb3rQAA", "8023O000008pb3sQAA", "8023O000008pb3tQAA", "8023O000008pb3uQAA", "8023O000008pb3vQAA", "8023O000008pb3wQAA", "8023O000008pb3xQAA", "8023O000008pb3yQAA", "8023O000008pb3zQAA", "8023O000008pb40QAA", "8023O000008pb3GQAQ", "8023O000008pb3HQAQ", "8023O000008pb3IQAQ", "8023O000008pb3JQAQ", "8023O000008pb3KQAQ", "8023O000008pb3LQAQ", "8023O000008pb3MQAQ", "8023O000008pb3NQAQ", "8023O000008pb3OQAQ", "8023O000008pb3PQAQ", "8023O000008pb3QQAQ", "8023O000008pb3RQAQ", "8023O000008pb3SQAQ", "8023O000008pb3TQAQ", "8023O000008pb3UQAQ", "8023O000008pb3VQAQ", "8023O000008pb3WQAQ", "8023O000008pb3XQAQ", "8023O000008pb3YQAQ", "8023O000008pb3ZQAQ", "8023O000008pb3aQAA", "8023O000008pb3bQAA", "8023O000008pb3cQAA", "8023O000008pb3dQAA", "8023O000008pb3eQAA", "8023O000008pb3fQAA", "8023O000008pb3gQAA", "8023O000008pb3hQAA", "8023O000008pb3iQAA", "8023O000008pb3jQAA", "8023O000008pb3kQAA", "8023O000008pb3lQAA", "8023O000008pb3mQAA", "8023O000008pb3nQAA", "8023O000008pb3oQAA", "8023O000008pb4SQAQ", "8023O000008pb4TQAQ", "8023O000008pb4UQAQ", "8023O000008pb4VQAQ" ]
        }

        res = DR_IP.remoteClass('SystemHelper','attributes',data)

        a=1

    def test_getStats(self):
        restClient.init('DEVNOSCAT3')

        orderId = '8013N000006K1J5QAK'

        res = query.query(f"select Id,vlocity_cmt__AttributeSelectedValues__c, vlocity_cmt__JSONAttribute__c, vlocity_cmt__AttributesMarkupData__c  from vlocity_cmt__FulfilmentRequestLine__c where vlocity_cmt__FulfilmentRequestID__r.vlocity_cmt__OrderId__c = '{orderId}' ")

        print(f"Number of FRLs: {len(res['records'])}")

        totalSelected = 0
        totalJSON = 0
        max = 0
        l = 0
        maxj =0
        lj = 0
        for r in res['records']:
            l = len(r['vlocity_cmt__AttributeSelectedValues__c']) if r['vlocity_cmt__AttributeSelectedValues__c'] != None else 0
            lj = len(r['vlocity_cmt__JSONAttribute__c']) if r['vlocity_cmt__JSONAttribute__c'] != None else 0

            totalSelected = totalSelected + l
            totalJSON = totalJSON + lj

            if l>max: max = l
            if lj>max: maxj = lj

        print(f"vlocity_cmt__AttributeSelectedValues__c  size: {totalSelected}    max:{max}")
        print(f"vlocity_cmt__JSONAttribute__c  size: {totalJSON}    max:{maxj}")

        a=1
