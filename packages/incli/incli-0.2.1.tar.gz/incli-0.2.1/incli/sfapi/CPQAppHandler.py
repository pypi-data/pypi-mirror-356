from . import restClient
import simplejson as json

def checkError(call,raiseEx=True):
  if 'messages' in call:
    if len(call['messages']) > 0:
      if 'code' in call['messages'][0]:
        msg = call['messages'][0] 
        message = f"Code:{msg['code']}  {msg['severity']}  {msg['message']}"
        if msg['message'] == 'No Results Found.':
            return None
        if raiseEx == True and msg['severity'] == 'ERROR':
          raise ValueError(message)
  return call

def call(method,data,options=None):
  action = f'/services/apexrest/vlocity_cmt/v1/GenericInvoke/vlocity_cmt.CPQAppHandler/{method}'
  _data = {
      "sMethodName":method,
      "sClassName":"vlocity_cmt.CPQAppHandler"
      }

  if isinstance(data, str):
    _data['input'] =  data
  else:
     _data['input'] =  json.dumps(data)

  if options == None:  
    _data['options'] = json.dumps( {
      "preTransformBundle":"",
      "postTransformBundle":"",
      "useQueueableApexRemoting":False,
      "ignoreCache":False,
      "vlcClass":"vlocity_cmt.CPQAppHandler",
      "useContinuation":False
      } )
  else:
    _data['options'] =  json.dumps(options)
  call = restClient.callAPI(action=action,data=_data,method='post')
  return call

def getCartsItems(cartId):
    method = 'getCartsItems'

    data = {
        "cartId":cartId,
        "fields":"vlocity_cmt__BillingAccountId__c,vlocity_cmt__ServiceAccountId__c,Quantity,vlocity_cmt__RecurringTotal__c,vlocity_cmt__OneTimeTotal__c,vlocity_cmt__OneTimeManualDiscount__c,vlocity_cmt__RecurringManualDiscount__c,vlocity_cmt__ProvisioningStatus__c,vlocity_cmt__RecurringCharge__c,vlocity_cmt__OneTimeCharge__c,ListPrice,vlocity_cmt__ParentItemId__c,vlocity_cmt__BillingAccountId__r.Name,vlocity_cmt__ServiceAccountId__r.Name,vlocity_cmt__PremisesId__r.Name,vlocity_cmt__InCartQuantityMap__c,vlocity_cmt__EffectiveQuantity__c",
        "pagesize":"10",
        "price":False,
        "priceDetailsFields":"vlocity_cmt__OneTimeCharge__c,vlocity_cmt__OneTimeManualDiscount__c,vlocity_cmt__OneTimeCalculatedPrice__c,vlocity_cmt__OneTimeTotal__c,vlocity_cmt__RecurringCharge__c,vlocity_cmt__RecurringCalculatedPrice__c,vlocity_cmt__RecurringTotal__c,vlocity_cmt__OneTimeLoyaltyPrice__c,vlocity_cmt__UsageUnitPrice__c,vlocity_cmt__UsagePriceTotal__c",
        "validate":False,
        "lastRecordId":""
    }
    
    return call(method,data)