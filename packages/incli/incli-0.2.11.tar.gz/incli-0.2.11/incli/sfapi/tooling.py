from . import restClient,Sobjects,utils,thread,query as SQOL
import simplejson


v = 'v51.0'
def query(q):
    action = f"/services/data/{v}/tooling/query/?q={q}"
    call = restClient.callAPI(action)
    checkError()
    for r in call['records']: r.pop('attributes')

    return call

def query_threaded(q,values,search="$$$",raiseEx=True,th=10):
    result = []

    def do_work(value):
        q1 = q.replace(search,value)
        res = query(q1)
        return res

    def on_done(res,result):
        result.append(res['records'][0])

    thread.execute_threaded(values,result,do_work,on_done,threads=th)

    return result

def get(sobject,id):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}/{id}"
    call = restClient.callAPI(action)
    return call

def checkError():
    call = restClient.lastCall()['response']
    if 'serverResponse' in call:
        sr = call.split('serverResponse:')[1]
        srj = simplejson.loads(str(sr))
        utils.raiseException(srj[0]['errorCode'],srj[0]['message'])  

def post(sobject,data):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}"
    call = restClient.callAPI(action,method='post',data=data)
    checkError()
    return call

def delete(sobject,id):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}/{id}"
    call = restClient.callAPI(action,method='delete')
    checkError()
    return call

def patch(sobject,id,data):
    action = f"/services/data/{v}/tooling/sobjects/{sobject}/{id}"
    call = restClient.callAPI(action,method='patch',data=data)
    checkError()
    return call

def IdF(object,fieldF,multiple=False):
    chunks = fieldF.split(":")
    if len(chunks)<2:
        utils.raiseException("fieldF error",f"Not a valid fieldF name:value  {fieldF}")
    q = f"select id from {object} where {chunks[0]} = '{chunks[1]}'"
    call = query(q)   
    if len(call['records']) == 0:
        return None
    if multiple:
        return call['records']
    return call['records'][0]['Id']

def describe(sobject):
    action =f"/services/data/{v}/tooling/sobjects/{sobject}/describe/"
    call = restClient.callAPI(action)
    utils.printFormated(call['fields'],"label:name:type")

    print()
    

def queryTraceFlg(q):
    q = "select id, TracedEntityId,logtype, startdate, expirationdate, debuglevelid, debuglevel.apexcode, debuglevel.visualforce from TraceFlag limit 10"
    call = query(q)
    print()
    
def completions():
    action =f"/services/data/{v}/tooling/completions?type=apex"

    allheaders = {
        'Content-type': 'application/json',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br'
        ,'Accept':'application/json'
    }
    call = restClient.callAPI(action,headers=allheaders)
    filename = restClient.callSave("completions.json")
    print()

    'serverResponse: [{"message":"Invalid Accept header */*. Must be one of the following values: [com.force.swag.rest.format.FormatImpl@fd630a47, com.force.swag.rest.format.FormatImpl@b5980ad8]","errorCode":"INVALID_TYPE"}]'

def executeAnonymous(code=None):
    if code == None:
        code ="Delete [select Id from vlocity_cmt__SyncDeltaObject__c LIMIT 10000];"
  #  code = """
  #  Map<String, Object> input = new Map<String, Object>{'methodName' => 'refreshBatchJobLists'};
  #  vlocity_cmt.TelcoAdminConsoleController controllerClass = new vlocity_cmt.TelcoAdminConsoleController();
  #  controllerClass.setParameters(JSON.serialize(input));
  #  System.debug(controllerClass.invokeMethod());
  #  """
    action =f"/services/data/{v}/tooling/executeAnonymous?anonymousBody={code}"
    call = restClient.callAPI(action)
    return call

# https://blog.bessereau.eu/assets/pdfs/api_tooling.pdf
def ApexExecutionOverlayAction_class(className,username,actionScript,line,IsDumpingHeap=False):

    if actionScript == None:
        actionScriptType = 'None'
    classId = SQOL.queryField(f"select Id from ApexClass where name = '{className}'")
    userId = SQOL.queryField(f"select Id from User where username = '{username}'")

    action =f"/services/data/{v}/tooling/sobjects/ApexExecutionOverlayAction"

    data = {
        "ActionScript" : actionScript,
        "ActionScriptType" : actionScriptType,
        "ExecutableEntityId" : classId,
        "IsDumpingHeap" : IsDumpingHeap,
        "Iteration" : "1",
        "Line" : line,
        "ScopeId" : userId
    }

    res = restClient.callAPI(action,method='post',data=data)

    print(res)

def ApexExecutionOverlayAction_heap(className,line,username=None,deletePrevious=True):

    if deletePrevious:
        res = query(f"select Id from ApexExecutionOverlayAction where ExecutableEntity.Name = '{className}'")
        for rec in res['records']:
            delete('ApexExecutionOverlayAction',rec['Id'])
            
    classId = SQOL.queryField(f"select Id from ApexClass where name = '{className}'")

    action =f"/services/data/{v}/tooling/sobjects/ApexExecutionOverlayAction"

    data = {
        "ActionScript" : None,
        "ActionScriptType" : 'None',
        "ExecutableEntityId" : classId,
        "IsDumpingHeap" : True,
        "Iteration" : "1",
        "Line" : line
    }
    if username!= None:
        data['ScopeId'] = SQOL.queryField(f"select Id from User where username = '{username}'")

    res = restClient.callAPI(action,method='post',data=data)

    print(res)

def ApexExecutionOverlayResult_Heap(className):
    res = query(f"select Id,ClassName,CreatedDate from ApexExecutionOverlayResult where ClassName ='{className}' order by CreatedDate desc")

    if len(res['records'])==0:
        print('ApexExecutionOverlayResult record not found')
        return

    action = f"/services/data/v51.0/tooling/sobjects/ApexExecutionOverlayResult/{res['records'][0]['Id']}"

    res2 = restClient.callAPI(action,method='get')

    print(res2['OverlayResultLength'])
    total = 0
    for r in res2['HeapDump']['extents']:
        print('-------------------------------------------------------------------------------')
        print(f" {r['typeName']}  {r['collectionType']}  {r['totalSize']}")
        total = total + int(r['totalSize'])
 #       if r['typeName']=='vlocity_cmt.XOMObjectDescriber.FieldMetadata':
        if 1==1:
            for extent in r['extent']:
                print(f"                  {extent['address']}     {extent['size']}")
                if extent['symbols']==None:
                    if 'entry' in extent['value']:
                        entry = extent['value']['entry']
                        for en in entry:
                            print(f"                                    {en['keyDisplayValue']}     {en['value']['value']}")
                    else:
                        print(f"           {extent['size']}                  value {extent['value']['value']}")
                    a=1
                    continue
                if 'symbols' in extent and extent['symbols']!=None:
                    for symbols in extent['symbols']:
                        if 'entry' in extent['value']:
                            for entry_r in extent['value']['entry']:
                                print(f"                            {entry_r['keyDisplayValue']}     {entry_r['value']['value']}")
                                
                        else:
                            print(f"            {extent['size']}       {symbols}   {extent['value']['value']}")
                else:
                        print(f"             {extent['size']}      No symbols")

    print(total)
    a=1

def ApexExecutionOverlayResult_class2(className,username,actionScript,line,IsDumpingHeap=False):

    if actionScript == None:
        actionScriptType = 'None'
    classId = SQOL.queryField(f"select Id from ApexClass where name = '{className}'")
    userId = SQOL.queryField(f"select Id from User where username = '{username}'")

    action =f"/services/data/{v}/tooling/sobjects/ApexExecutionOverlayResult"

    data = {
        "ActionScript" : actionScript,
        "ActionScriptType":'None',
    #    "ActionScriptType" : "Apex",
    #    "ExecutableEntityId" : classId,
        "IsDumpingHeap" : IsDumpingHeap,
        "Iteration" : "1",
        "Line" : line,
        "UserId" : userId
    }

    data = {}
    res = restClient.callAPI(action,method='get',data=data)

    ID = '07n3O00000097lWQAQ'
    action = f'/services/data/v51.0/tooling/sobjects/ApexExecutionOverlayResult/{ID}'

    res2 = restClient.callAPI(action,method='get')

    action = '/services/data/v51.0/tooling/sobjects/ApexExecutionOverlayResult/describe'
    res3 = restClient.callAPI(action,method='get')


    print(res)
#select ExecutableEntityId,Id,ExecutableEntityName,IsDeleted,IsDumpingHeap,Iteration,Line,ScopeId,ExecutableEntity.name,ActionScript  from ApexExecutionOverlayAction 
