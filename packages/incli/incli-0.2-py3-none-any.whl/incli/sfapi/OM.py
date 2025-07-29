from . import query,Sobjects,restClient,utils
import time

def complete_orchestration_plan(orderId):

    finished = False
    naps_conter = 0
    max_naps = 5
    while finished == False:
        q_plan = f"select fields(all) from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}'  limit 100"

        res = query.query(q_plan)

        if len(res['records']) == 0:
            print('There is no Orchestation plan')
            utils.raiseException('NO_PLAN',f'There is no orchestration plan for order {orderId}')


        if res['records'][0]['vlocity_cmt__State__c'] == 'Completed':
            finished = True
            continue

        orchestrationPlanId = res['records'][0]['Id']

        q = f"select fields(all) from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c = '{orchestrationPlanId}'  limit 200"

        res2 = query.query(q)

        active = [r for r in res2['records'] if r['vlocity_cmt__State__c'] in ['Fatally Failed',"Failed","Ready","Running"]]
        if len(active) == 0:
            time.sleep(5)
            naps_conter = naps_conter + 1
            if naps_conter >max_naps:
                finished = True
                continue
        else:
            naps_conter = 0
        for r in active:
            try:
                print(f"{r['Id']}   {r['Name']} {r['vlocity_cmt__State__c']}   ")
                data = {
                    'vlocity_cmt__State__c':'Completed'
                }
                rr = Sobjects.update(r['Id'],data,sobjectname='vlocity_cmt__OrchestrationItem__c')
            except Exception as e:
                print(e)
                time.sleep(10)  #This is to avoid shti.

        
def waitfor_orchestration_plan(orderId):
    q_plan = f"select fields(all) from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}'  limit 100"

    finished = False
    iterations = 0
    while finished == False and iterations<10:
        res = query.query(q_plan)
        iterations = iterations + 1 

        if len(res['records']) == 0:
            time.sleep(10)
        else:
            finished = True
            
# https://help.salesforce.com/s/articleView?id=ind.v_dev_t_vlocity_order_management_rest_apis_666373.htm&type=5
 
def delete_orchestration_plan_and_decomposition(orderId):
    data = {
        'vlocity_cmt__FulfilmentStatus__c':'Draft',
        'Status':'Draft'
    }
    Sobjects.update(orderId,data,'Order')
    Sobjects.deleteMultiple_query(f"select Id from vlocity_cmt__FulfilmentRequestDecompRelationship__c where vlocity_cmt__SourceOrderId__c  = '{orderId}'")
    Sobjects.deleteMultiple_query(f"select Id from vlocity_cmt__FulfilmentRequest__c where vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.deleteMultiple_query(f"select Id  from vlocity_cmt__OrchestrationDependency__c where vlocity_cmt__OrchestrationItemId__r.vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.deleteMultiple_query(f"select Id from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.deleteMultiple_query(f"select Id from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}' ")
    Sobjects.deleteMultiple_query(f"select Id from vlocity_cmt__FulfilmentRequestLineSourceRootOrderItem__c  where vlocity_cmt__RootOrderItemId__r.OrderId = '{orderId}' ")

def isDecomposed(orderId):
    action = f'/services/apexrest/ordermanagement/v1/orders/{orderId}/decompose'

    action = f"/services/apexrest/vlocity_cmt/Decomposition/isSfdcDecomposedOrder?orderId={orderId}"

    res = restClient.callAPI(action=action,method='get')

    return res

    
def decomposeAndCreatePlan(orderId):
    action = f"/services/apexrest/vlocity_cmt/Decomposition/decomposeAndCreatePlan?orderId={orderId}"
    res = restClient.callAPI(action=action,method='post')

    return res

def decompose(orderId):
    action = f"/services/apexrest/vlocity_cmt/Decomposition/decompose?orderId={orderId}"
    res = restClient.callAPI(action=action,method='post')

    return res

def viewDecomposedOrder(orderId):
    action = f"/services/apexrest/vlocity_cmt/Decomposition/viewDecomposedOrder?orderId={orderId}"
    res = restClient.callAPI(action=action,method='get')

    return res

def viewDecomposedOrder(orderId):
    action = f"/services/apexrest/vlocity_cmt/Decomposition/viewDecomposedOrder?orderId={orderId}"
    res = restClient.callAPI(action=action,method='get')

    return res