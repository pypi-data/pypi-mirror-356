from . import Sobjects,query

def get_orphans():
    def print_orphans(q,name):
        res = query.query(q)
        print(f"{name}  {res['records'][0]['expr0']}")

    print_orphans("select count(Id)  from VOMAudit__c  where OrchestrationItemId__c = null and OrderId__c = null",'VOMAudit__c')
    print_orphans("select count(Id)  from vlocity_cmt__FulfilmentRequest__c  where vlocity_cmt__OrderId__c = null ",'vlocity_cmt__FulfilmentRequest__c')
    print_orphans("select count(Id)  from vlocity_cmt__FulfilmentRequestLine__c  where vlocity_cmt__FulfilmentRequestID__c   = null ",'vlocity_cmt__FulfilmentRequestLine__c')
    print_orphans("select count(Id)  from vlocity_cmt__FulfilmentRequestLine__c  where vlocity_cmt__FulfilmentRequestID__r.Id   = null ",'vlocity_cmt__FulfilmentRequestLine__c')
    print_orphans("select count(Id)  from vlocity_cmt__FulfilmentRequestLine__c  where vlocity_cmt__FulfilmentRequestID__r.vlocity_cmt__OrderId__c   = null",'vlocity_cmt__FulfilmentRequestLine__c')
    print_orphans("select count(Id) from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c  where vlocity_cmt__SourceOrderItemId__c = null  and vlocity_cmt__SourceFulfilmentRequestLineId__c = null","vlocity_cmt__FulfilmentRequestLineDecompRelationship__c")
    print_orphans("select count(Id) from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c  where vlocity_cmt__SourceOrderItemId__c = null  and vlocity_cmt__SourceFulfilmentRequestLineId__r.vlocity_cmt__FulfilmentRequestID__c = null","vlocity_cmt__FulfilmentRequestLineDecompRelationship__c")
    print_orphans("select count(Id) from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c  where vlocity_cmt__SourceOrderItemId__c = null  and vlocity_cmt__SourceFulfilmentRequestLineId__r.vlocity_cmt__FulfilmentRequestID__r.vlocity_cmt__OrderId__c = null","vlocity_cmt__FulfilmentRequestLineDecompRelationship__c")
    a=1
    print_orphans("select count(Id) from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = null","vlocity_cmt__OrchestrationPlan__c")
    print_orphans("select count(Id) from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c = null","vlocity_cmt__OrchestrationItem__c")

    a=1
def clean_orphans():

   # Sobjects.delete_query("select Id from vlocity_cmt__FulfilmentRequestDecompRelationship__c where vlocity_cmt__SourceFulfilmentRequestId__r.vlocity_cmt__OrderId__c = null ")
    Sobjects.delete_query("select Id from vlocity_cmt__FulfilmentRequestLine__c  where vlocity_cmt__FulfilmentRequestID__c   = null ")
    Sobjects.delete_query("select Id from vlocity_cmt__FulfilmentRequest__c   where vlocity_cmt__OrderId__c    = null ")

    Sobjects.delete_query("select Id from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c    where    vlocity_cmt__DestinationFulfilmentRequestLineId__c    = null ")
    Sobjects.delete_query("select Id from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c    where    vlocity_cmt__SourceFulfilmentRequestLineId__c    = null and vlocity_cmt__SourceOrderItemId__c = null ")

    Sobjects.delete_query("select Id from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c = null")
    Sobjects.delete_query("select Id from vlocity_cmt__OrchestrationDependency__c  where vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c   = null")
    Sobjects.delete_query("select Id from vlocity_cmt__OrchestrationDependency__c   where vlocity_cmt__OrchestrationItemId__c = null or vlocity_cmt__DependsOnItemId__c = null")
    Sobjects.delete_query("select Id from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c  = null")
    Sobjects.delete_query("select Id from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = null")

    Sobjects.delete_query("SELECT Id from vlocity_cmt__InventoryItemDecompositionRelationship__c  where vlocity_cmt__SourceAssetId__c = null")
    Sobjects.delete_query("SELECT Id from vlocity_cmt__InventoryItem__c  where vlocity_cmt__AccountId__c = null")

    Sobjects.delete_query("SELECT Id, OrchestrationItemId__c from VOMAudit__c  where OrchestrationItemId__c=null ")

def test_delete_Account_and_All(name):

    Sobjects.delete_query(f"SELECT Id FROM order WHERE Account.name = '{name}' ",size=1)

    res = query.query(f"select fields(all) from order where Account.name = '{name}' limit 100")

    for r in res['records']:
        data =  {
            'Status':'In Progress'
        }
        Sobjects.update(r['Id'],data=data,sobjectname='Order')

    Sobjects.delete_query(f"SELECT Id FROM order WHERE Account.name = '{name}' ",size=1)
    #deletes
    #Order Applied Promotion Affected Items
    #Order Pricing
    #Order
    #Applied Promotions
    #Order Applied Promotions

    Sobjects.delete_query(f"SELECT Id FROM Account WHERE name = '{name}' ",size=1)
    #Deletes
    #Account
    #Parties    

   # clean_orphans()

def delete_decompostion_plan(orderId):
    data = {
        'vlocity_cmt__FulfilmentStatus__c':'Draft',
        'Status':'Draft'
    }
    Sobjects.update(orderId,data,'Order')
    Sobjects.delete_query(f"select Id from vlocity_cmt__FulfilmentRequestDecompRelationship__c where vlocity_cmt__SourceOrderId__c  = '{orderId}'")
    Sobjects.delete_query(f"select Id from vlocity_cmt__FulfilmentRequest__c where vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.delete_query(f"select Id  from vlocity_cmt__OrchestrationDependency__c where vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.delete_query(f"select Id from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.delete_query(f"select Id from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.delete_query(f"select Id from vlocity_cmt__FulfilmentRequestLineSourceRootOrderItem__c  where vlocity_cmt__RootOrderItemId__r.OrderId = '{orderId}' ")

def get_all(accountName):

    def print_q(q):
        res = query.query(q)
        print(len(res['records']))
        ids = [r['Id'] for r in res['records']]
        return ids

    accountId = print_q(f"SELECT Id FROM account WHERE name = '{accountName}' ")
    print(accountId)
    orderIds = print_q(f"select Id from order where Account.name = '{accountName}' ")
    orderItemIds = print_q(f"select Id from orderitem where OrderId in ({query.IN_clause(orderIds)})  ")
    assetIds = print_q(f"select Id from Asset where Account.name = '{accountName}' ")

    frs = print_q(f"select Id from vlocity_cmt__FulfilmentRequest__c where vlocity_cmt__OrderId__c in ({query.IN_clause(orderIds)})  ")
    frls = print_q(f"select Id from vlocity_cmt__FulfilmentRequestLine__c where vlocity_cmt__FulfilmentRequestID__c in ({query.IN_clause(frs)})  ")

    frldr = print_q(f"select Id from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c  where vlocity_cmt__SourceOrderItemId__c in ({query.IN_clause(orderItemIds)})  or vlocity_cmt__SourceFulfilmentRequestLineId__c in ({query.IN_clause(frls)})")

    orchPlanIds = print_q(f"select Id from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c in ({query.IN_clause(orderIds)})  ")
    orchItemIds = print_q(f"select Id from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c in ({query.IN_clause(orchPlanIds)})  ")

    orchItemSourcesIds = print_q(f"select Id from vlocity_cmt__OrchestrationItemSource__c  where vlocity_cmt__OrchestrationItemId__c in ({query.IN_clause(orchItemIds)})  or vlocity_cmt__SourceFulfilmentRequestLineId__c in ({query.IN_clause(frls)})")
    orchItemDepIds = print_q(f"select Id from vlocity_cmt__OrchestrationDependency__c where vlocity_cmt__OrchestrationItemId__c in ({query.IN_clause(orchItemIds)})  ")

    inventoryIds = print_q(f"select Id from vlocity_cmt__InventoryItem__c where vlocity_cmt__AccountId__c in ({query.IN_clause(accountId)})  ")

    vomAuditIds = print_q(f"select Id from VOMAudit__c where OrchestrationItemId__c in ({query.IN_clause(orchItemIds)}) or  OrderId__c in ({query.IN_clause(orderIds)})")

    a=1
