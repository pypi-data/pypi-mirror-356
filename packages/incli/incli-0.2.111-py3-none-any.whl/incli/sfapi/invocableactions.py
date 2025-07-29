from . import restClient


def getInvocableActions(type):
     return restClient.callAPI(action=f'/services/data/v63.0/actions/{type}')
def getInvocableActionsStandard():
     return getInvocableActions('standard')
def getInvocableActionsCustom():
     return getInvocableActions('custom')    
def listInvocableActions():
     print('STANDARD')
     res = getInvocableActions('standard')
     for action in res['actions']:
          print(f"{action['name']:40}  {action['label']:20} {action['type']:20} ")
     print('CUSTOM')
     res = getInvocableActions('custom')
     for key in res.keys():
          print(f"{key:40}  {res[key]} ")
          res1 = restClient.callAPI(res[key])
          for action in res1['actions']:
               print(f"   {action['name']:40}  {action['label']:20} {action['type']:20}  {action['url']} ")