from cmath import log
import logging
import simplejson

ident = -1
treeObjects = []
keyPath = []
def reset():
    global ident,treeObjects
    ident = -1
    treeObjects = []
    keyPath = []

def getChild(json,name):
    for key in json.keys():
        if key == name:
            return json[key]
    return ''

#renaiming and return root Json dict. 
#def setKeyValue(json, matchKey, matchKeyValue,setKey, setKeyValue,logValues=False):
#    sibling = parse(json, matchKey, matchKeyValue,setKey, setKeyValue,logValues)
#    return json

def Id(obj):
    sibbling = getSibling(obj,'Id')
    Id = sibbling['Id']
    if 'value' in Id:
        Id = Id['value']
    return Id

def getSibling(obj, matchKey, matchKeyValue='',logValues=False,multiple=False):
    global treeObjects,keyPath
    reset()
    if isinstance(obj,list)==True:
        rets = []

        for element in obj:
            ret = parse(element, matchKey=matchKey, matchKeyValue=matchKeyValue,logValues=logValues,rets=rets)
            if ret != '':
                if multiple is False:
                    return ret
                rets.append(ret)
        if multiple is False:
            return None
        return rets
    p = parse(obj, matchKey=matchKey, matchKeyValue=matchKeyValue,logValues=logValues)
    treeObjects = treeObjects[0:ident+1]
    keyPath = keyPath[0:ident+1]

    return p

""" def getSibling_atPath(obj,path,field='ProductCode'):
    for p in path.split(':'):
        obj = getSibling(obj,field,p)  
    return obj """

#This is used to get order line items.
def getSiblingWhere_path(obj, matchKey,matchKeyValuePath, whereKey=None,whereValue=None,logValues=False):
    paths = matchKeyValuePath.split(':')

    result = {
        'level':-1,
        'keys':[],
        'objects':[],
        'object':None,
        'matchedObjectList':[]
    }
    for i, path in enumerate(paths):
   # for path in paths:
        index = 0
        if '|' in path:
            index = int(path.split('|')[1])
            path = path.split('|')[0]

        where_Value = whereValue if i == len(paths) - 1 else None

        pathMatchFields = ['records','lineItems','productGroups','result']
        if i == len(paths)-1:
            pathMatchFields.append('childProducts')

        r = getSiblingWhere(obj, matchKey,path, whereKey,where_Value,logValues,onlyOne=False,pathMatchFields=pathMatchFields)

        if len(r['matchedObjectList'])==0:
            return None
        
        result['object'] = r['matchedObjectList'][index]
        result['matchedObjectList'] = r['matchedObjectList']
        result['objects'].extend(r['objects'])

        obj = result['object']
        
    return result

#This is used.
def getSiblingWhere(obj, matchKey,matchKeyValue=None, whereKey=None,whereValue=None,logValues=False,onlyOne=True,pathMatchFields=None):

    result = {
        'level':-1,
        'keys':[],
        'objects':[],
        'object':None,
        'matchedObjectList':[]
    }

    if isinstance(obj,list)==True:
        for element in obj:
            ret = parseWhere(element, matchKey=matchKey,matchKeyValue=matchKeyValue, whereKey=whereKey, whereValue=whereValue,logValues=logValues,result=result,onlyOne=onlyOne,pathMatchFields=pathMatchFields)
            if ret['object'] != None:
                return ret
        return None
    ret = parseWhere(obj, matchKey=matchKey, matchKeyValue=matchKeyValue,whereKey=whereKey, whereValue=whereValue,logValues=logValues,result=result,onlyOne=onlyOne,pathMatchFields=pathMatchFields)
    if ret['level']<0:
        ret['level'] = 0
    ret['keys'] = ret['keys'][0:ret['level']]
    ret['objects'] = ret['objects'][0:ret['level']]

    return ret
#------------------------

def getValue(obj,name):
    value = obj[name]
    if 'value' in obj[name]:
        value = obj[name]['value']  
    return value

#used
def _match_obj(obj,key,matchKey,matchValue,whereKey,whereValue):
    if key != matchKey:
        return None
    
    if matchValue == None and whereKey == None:
        return obj[key]

    if getValue(obj,matchKey)  != matchValue:
        return None
    
    if whereKey == None:
        return obj
    
    if whereKey not in obj:
        return None

    if whereValue == None:
        return obj
    
    if obj[whereKey] not in whereValue.split(':'):
        return None
    
    return obj
             
#set selecte key where keyvalue is matchKeyValue and return jsonDic 
# if set Key provided, will replace the setKeyValue
def parseWhere(obj,result,matchKey='', matchKeyValue=None,whereKey=None, whereValue=None,logValues=False,onlyOne=True,_level=-1,_objects=[],pathMatchFields=None):
    """
    Recursively traverses a nested data structure (such as a dictionary or list) to find and return an object that satisfies specific criteria. 
    if matchKeyValue = None, if the obj contains the matchKey is a match. 
    if whereValue = None, if the obj contains the whereKey is a match. 
    """
    #result['level']=result['level']+1
    _level += 1
    if len(_objects) > _level:
        _objects[_level] = obj
    else:
        _objects.append(obj)

    if len(_objects) > _level:
        _objects = _objects[0:_level+1]

    if isinstance(obj, (list)):
        a=1

    if not isinstance(obj, (dict, list)):
        result['object'] = None
        return result

    if matchKey not in pathMatchFields: pathMatchFields.append(matchKey) 
    
    matchedObjectList = []

    for key in obj.keys():
        if key not in pathMatchFields: 
            continue

        match = _match_obj(obj,key,matchKey,matchKeyValue,whereKey,whereValue)
        if match!= None:
            result.update({'object': match, 'level': _level, 'objects': _objects})
            return result       

        child = obj[key]
        if isinstance(child,dict):
            ret = parseWhere(child,result,matchKey, matchKeyValue,whereKey,whereValue,logValues,onlyOne=onlyOne,_level=_level,pathMatchFields=pathMatchFields)
            if ret['object'] != None:  
                return ret

        if isinstance(child,list):
            for item in child:
                ret = parseWhere(item, result,matchKey,matchKeyValue,whereKey,whereValue,logValues,onlyOne=onlyOne,_level=_level,pathMatchFields=pathMatchFields)
                if ret.get('object') is not None:
                    if onlyOne:
                        return ret
                    matchedObjectList.append(ret['object'])    

    if len(matchedObjectList)>0:
        result['matchedObjectList'] = matchedObjectList
        return result

    result['object'] = None
    return result

def parse(json, matchKey='', matchKeyValue='',setKey='', setKeyValue='',logValues=False,rets=None):
    global ident,treeObjects
    ident=ident+1
    treeObjects.insert(ident, json)
#    print(ident)


    if isinstance(json,dict)==False and isinstance(json,list)==False:
        return ''  #continue

    for key in json.keys():
        keyPath.insert(ident,key)
        if key == 'PricebookEntry':
            continue

        if key == 'ProductCode' and logValues == True:
            printIdent(f'{key}  {json[key]}')

        if key == matchKey:
            if matchKeyValue == '':
                return json
            value = getValue(json,matchKey) 

         #   printIdent(f'{key}  {value}')

            if value == matchKeyValue:
                if setKey!='':
                    if setKeyValue == None:
                        return json[setKey]
                    if json[setKey] != None and type(json[setKey]) is dict and 'value' in json[setKey]:
                        json[setKey]['value'] = setKeyValue
                    else:
                        json[setKey] = setKeyValue
           #     ident = ident-1

                return json 

        if isinstance(json[key],dict):
            ret = parse(json[key],matchKey, matchKeyValue,setKey,setKeyValue)
          #  ident = ident-1

            if ret != '':
                return ret if rets is None else rets.append(json)

        if isinstance(json[key],list):
            for l in json[key]:
                ret = parse(l,matchKey,matchKeyValue,setKey,setKeyValue)
            #    ident = ident-1
  
                if ret != '':
                    return ret if rets is None else rets.append(json)
    ident = ident-1

    return ''

#set selecte key where keyvalue is matchKeyValue and return jsonDic 
# if set Key provided, will replace the setKeyValue
""" def parseEx(json, matchKey='', matchKeyValue='',setKey='', setKeyValue='',logValues=False,retObjects=[]):
    global ident
    ident=ident+1
  
    if isinstance(json,dict)==False and isinstance(json,list)==False:
        return ''  #continue

    for key in json.keys():
        if key == 'PricebookEntry':
            continue

        if key == 'ProductCode' and logValues == True:
            printIdent(f'{key}  {json[key]}')

        if key == matchKey:
            value = json[matchKey]
            if 'value' in json[matchKey]:
                value = json[matchKey]['value']
            if value == matchKeyValue:
                if setKey!='':
                    if setKeyValue == None:
                        return json[setKey]
                    if json[setKey] != None and type(json[setKey]) is dict and 'value' in json[setKey]:
                        json[setKey]['value'] = setKeyValue
                    else:
                        json[setKey] = setKeyValue
                #return json     
                retObjects.append(json[matchKey])

        if isinstance(json[key],dict):
            ret = parse(json[key],matchKey, matchKeyValue,setKey,setKeyValue,retObjects)
            if ret != '':
                retObjects.append(ret)
                #return ret
            ident = ident-1

        if isinstance(json[key],list):
            for l in json[key]:
                ret = parse(l,matchKey,matchKeyValue,setKey,setKeyValue,retObjects)
                if ret != '':
                    retObjects.append(json)
                    #return ret
                ident = ident-1
    return retObjects
 """

#used
def getField(obj,path,separator=':'):
    """
    Get field in object for a path. 
    - path: the path
    - separator: for the path. a:b:c by default. 
    """
    paths = path.split(separator)
    _obj = obj
    for p in paths:
        if p in _obj:
            _obj = _obj[p]
        else:
            return None
    return _obj

def printIdent(string):
    global ident
    str = ''
    for x in range(ident):
        str = str + ' '
    print(str + string)


def replace_everywhere_in_obj(obj,find,replace):
    strAll = simplejson.dumps(obj)
    stItems2 = strAll.replace(find,replace)
    return simplejson.loads(stItems2)


