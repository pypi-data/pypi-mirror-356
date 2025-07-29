from . import utils,Sobjects

def append_openParsedLines(context,parsedLine):
    context['openParsedLines'].append(parsedLine)

def append_parsedLines(context,parsedLine):
    context['parsedLines'].append(parsedLine) 

def append_openParsedLines_and_increaseIdent(context,obj,increase=True):
    append_openParsedLines(context,obj)
    if increase == True: 
        context['ident'] = context['ident'] + 1

def create_openParsedLine(context,line=None,field=None,value=None,type=None):
    parsedLine = create_parsedLine(context,line,field=field,value=value,type=type)
    append_openParsedLines_and_increaseIdent(context,parsedLine)
    return parsedLine

#@profile
def create_parsedLine(context,line=None,field=None,value=None,type=None):
    parsedLine = create_update_parsedLine(context,line,parsedLineData=None,field=field,value=value,type=type)
    append_parsedLines(context,parsedLine)
    return parsedLine

def close_openParsedLine(context,type,value,key='key',endsWith=None,decrease=True):
    return pop_openParsedLines_and_decreaseIdent_and_updateParsedLine(context,type,value,key,endsWith,decrease)

def pop_openParsedLines_and_decreaseIdent_and_updateParsedLine(context,type,value,key='key',endsWith=None,decrease=True):
    parsedLineData = pop_openParsedLines(context,type=type,key=key,value=value,endsWith=endsWith)
    if parsedLineData != None:
        if decrease == True:   
            context['ident'] = parsedLineData['ident']
        create_update_parsedLine(context,context['line'],parsedLineData=parsedLineData)
    return parsedLineData   

def copy_last_parsedLine(context):
    obj = context['parsedLines'][-1].copy()
    context['parsedLines'].append(obj)
    return obj

def find_in_parsedLines(context,valuesDict):
    '''
    - valuesDict: an object wiht key, value pairs. All value pairs need to match for the search to be succesfull. 
    '''
    for line in reversed(context['parsedLines']):
        for key in valuesDict.keys():
            if key not in line:
                break
            if line[key]!=valuesDict[key]:
                break
        return line
    return None    

def pop_openParsedLines(context,type,value,key='key',endsWith=False):
    openParsedLines = context['openParsedLines']
    try:
        for i,openParsedLine in reversed(list(enumerate(openParsedLines))):
            if openParsedLine['type'] == type:
                if key not in openParsedLine:      
                    continue

                if endsWith == True:
                    if openParsedLine[key].endswith(value) or openParsedLine[key].startswith(value):
                        openParsedLines.pop(i)
                        return openParsedLine    
                else:
                    if openParsedLine[key] == value:
                        openParsedLines.pop(i)
                        return openParsedLine
    except Exception as e:    
        print(e) 

    return None     

#@profile
def create_update_parsedLine(context,loglineStr=None,parsedLineData=None,field=None,value=None,type=None):
    """
    Creates or updates parsedLineData by parsing information from the given context and loglineStr.
    
    Args:
     - context (dict).
     - loglineStr (str, optional): A string that represents the current line being processed. If not provided, it is
                            taken from context['line'].
     - parsedLineData (dict, optional): A dictionary to be updated. If None, a new dictionary is created.
     - field (str, optional): A specific field in parsedLineData to be updated with a given value.
     - value (any, optional): The value to assign to the field in parsedLineData, if the field is provided.
     - type (str, optional): The type of the object being created or updated (used during object initialization).

    Functionality:
    - If parsedLineData is not provided, it initializes a new dictionary with basic fields like 'type', 'ident', and 'Id'.
    - Appends the loglineStr, total queries, and time (from chunks) to corresponding lists in the parsedLineData dictionary.
    - Extracts the index of the last element from each key in context['LU'] and stores it in parsedLineData['limitsIndexes'].
    - Attempts to extract and append a timestamp from the chunks; if this fails, defaults to 0.
    - If field and value are provided, directly updates the parsedLineData with the field-value pair.
    - Handles setting and calculating elapsed time based on timestamps and context['timeZero'].
    
    Returns:
    - The updated or newly created parsedLineData dictionary.
    """
    def append_to_list(obj,listFieldName,newValue):
        obj.setdefault(listFieldName, []).append(newValue)

        #if listFieldName in obj:
        #    obj[listFieldName].append(newValue)
        #else:
        #    obj[listFieldName] = [newValue]

    loglineStr = loglineStr or context.get('line')
    chunks = context.get('chunks', [])
    
    if parsedLineData == None:
        parsedLineData = {
            'type' : type,
            'ident' : context['ident'],
            'exception' :False,
            'lines':[],
            'totalQueries':[],
            'time':[],
            'limitsIndexes':[],
            'timeStamp':[]
        }
        if len(chunks)>3:  
            parsedLineData['Id'] = chunks[3]

    #append_to_list(parsedLineData,'lines',loglineStr)
    parsedLineData['lines'].append(loglineStr)
    #append_to_list(parsedLineData,'totalQueries',context['totalQueries'])
    parsedLineData['totalQueries'].append(context['totalQueries'])
    #append_to_list(parsedLineData,'time',chunks[0].split(' ')[0])
    #parsedLineData['time'].append(chunks[0].split(' ')[0])
    #parsedLineData['time'].append(chunks[0][:11])

    chunk0s = chunks[0].split(' ')
    #parsedLineData['time'].append(chunks[0][:chunks[0].find(' ')])
    parsedLineData['time'].append(chunk0s[0])


    limitsIndexes = {}
    for key in context['LU'].keys():
        limitsIndexes[key] = len(context['LU'][key])-1

    #append_to_list(parsedLineData,'limitsIndexes',limitsIndexes)
    parsedLineData['limitsIndexes'].append(limitsIndexes)

    #timestamp = int(chunks[0].split('(')[1].split(')')[0]) if len(chunks) > 1 else 0
    timestamp = int(chunk0s[1][1:-1]) if len(chunks) > 1 else 0

    #append_to_list(parsedLineData, 'timeStamp', timestamp)
    parsedLineData['timeStamp'].append(timestamp)

    if field is not None:  
        parsedLineData[field] =  value 

    if context['timeZero'] == 0:  
        context['timeZero'] = parsedLineData['timeStamp'][0]

    parsedLineData['elapsedTime'] = parsedLineData['timeStamp'][0] #- _context['timeZero']

    return parsedLineData

#@profile
def find_in_openParsedLines(context, field, value, endsWith=False, delete=True, startsWith=False):
    openParsedLines = context.get('openParsedLines', [])
    
    for i in range(len(openParsedLines) - 1, -1, -1):
        openParsedLine = openParsedLines[i]

        if field in openParsedLine:
            field_value = openParsedLine[field]

            if (startsWith and field_value.startswith(value)) or \
               (endsWith and field_value.endswith(value)) or \
               (not startsWith and not endsWith and field_value == value):

                if delete:
                    del openParsedLines[i]  

                return openParsedLine
    
    return None  

def find_in_openParsedLines2(context,field,value,endsWith=False,delete=True,startsWith=False):
    try:
        openParsedLines = context['openParsedLines']
        for i,openParsedLine in reversed(list(enumerate(openParsedLines))):
            if field in openParsedLine:
                field_value = openParsedLine[field]
                
                if (startsWith and field_value.startswith(value)) or \
                   (endsWith and field_value.endswith(value)) or \
                   (field_value == value):
                    
                    if delete:
                        openParsedLines.pop(i)
                    return openParsedLine
                
    except Exception as e:
        print(e) 
    return None

def is_in_operation(context,text,contains=False):
    if context['chunks_lenght']<2: 
        return False
    if contains and text in context['chunks'][1]: 
        return True
    elif context['chunks'][1] == text: 
        return True
    return False

def create_limits_obj():
  limit = {
    'SOQL queries': {'v': 0},
    'query rows': {'v': 0},
    'SOSL queries': {'v': 0},
    'DML statements': {'v': 0},
    'Publish Immediate DML': {'v': 0},
    'DML rows': {'v': 0},
    'CPU time': {'v': 0},
    'heap size': {'v': 0},
    'callouts': {'v': 0},
    'Email Invocations': {'v': 0},
    'future calls': {'v': 0},
    'queueable jobs added to the queue': {'v': 0},
    'Mobile Apex push calls': {'v': 0}
  }
  return limit

def append_limits(context,package,limitsObj):
    if package not in context['LU']:
        context['LU'][package] = []
    context['LU'][package].append(limitsObj)

def clone_and_appendLimit(context,limit,value,package='(default)'):
    if package not in context['LU']:
        context['LU'][package] = []
    if len(context['LU'][package])>0:
        limitsObj = context['LU'][package][-1].copy()
    else:
        limitsObj = {
            'SOQL queries': {'v': 0},
            'query rows': {'v': 0},
            'SOSL queries': {'v': 0},
            'DML statements': {'v': 0},
            'Publish Immediate DML': {'v': 0},
            'DML rows': {'v': 0},
            'CPU time': {'v': 0},
            'heap size': {'v': 0},
            'callouts': {'v': 0},
            'Email Invocations': {'v': 0},
            'future calls': {'v': 0},
            'queueable jobs added to the queue': {'v': 0},
            'Mobile Apex push calls': {'v': 0}
        }
    limitsObj[limit] = {'v':value}
    append_limits(context,package,limitsObj)

def parseWfRule(pc):
  #  line = context['line']
    context = pc['context']
    chunks = context['chunks'] 

    if is_in_operation(context,'WF_RULE_EVAL',contains=True):
        if 'BEGIN' in chunks[1]:
            create_openParsedLine(context,field='output',value='Workflow',type='RULE_EVAL')
            return True

        if 'END' in chunks[1]:
            close_openParsedLine(context,type='RULE_EVAL',key='output',value='Workflow')
            return True

    if is_in_operation(context,'WF_CRITERIA',contains=True):
        if 'BEGIN' in chunks[1]:
            parsedLine = create_openParsedLine(context,type='WF_CRITERIA')

            colon_split=chunks[2].split(':')
            colon_space = colon_split[1].strip().split(' ')
            parsedLine['ObjectName'] = colon_split[0][1:]
            parsedLine['RecordName'] = colon_space[0]
            if len(colon_space)>1:
                parsedLine['RecordID'] = colon_space[1]
            else:
                parsedLine['RecordID'] = ""

            parsedLine['rulename'] = chunks[3]
            parsedLine['rulenameId'] = chunks[4]
            parsedLine['output'] = parsedLine['rulename']

            return True

        if 'END' in chunks[1]:
            parsedLine =close_openParsedLine(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
            parsedLine['result'] = chunks[2]
            parsedLine['output'] = f"{parsedLine['ObjectName']}: {parsedLine['rulename']} --> {parsedLine['result']}"
            return True
  
    if is_in_operation(context,'WF_RULE_NOT_EVALUATED'):
        parsedLine = close_openParsedLine(context,type='WF_CRITERIA',key='type',value='WF_CRITERIA')   
        parsedLine['output'] = f"{parsedLine['rulename']} --> Rule Not Evaluated"
        return True

    if is_in_operation(context,'WF_ACTION'):
        parsedLine = find_in_openParsedLines(context,'output','Workflow',delete=False)
        parsedLine['action'] = chunks[2]
        return True

def parseExceptionThrown(pc):
    context = pc['context']
    chunks = context['chunks']

    if is_in_operation(context,'EXCEPTION_THROWN'):
        parsedLine = create_parsedLine(context,type='EXCEPTION',field='output',value=chunks[3])
        context['exception'] = True
        context['exception_msg'] = parsedLine['output']
        context['file_exception'] = True

        if context['line_index'] != len(context['lines'])-1:
            next = 1
            nextline = context['lines'][context['line_index']+next]
            while '|' not in nextline and context['line_index']+next != len(context['lines'])-1:
                if nextline != '':
                    parsedLine = copy_last_parsedLine(context)
                    parsedLine['output'] = nextline
                next = next + 1
                nextline = context['lines'][context['line_index']+next]
        return True

    if is_in_operation(context,'FATAL_ERROR'):
        obj = create_parsedLine(context,type='EXCEPTION',field='output',value=chunks[2])
        context['exception'] = True
        context['exception_msg'] = obj['output']

        context['file_exception'] = True
        next = 1
        nextline = context['lines'][context['line_index']+next]
        while '|' not in nextline:
            if nextline != '':
                parsedLine = copy_last_parsedLine(context)
                parsedLine['output'] = nextline
            next = next + 1
            nextlineIndex = context['line_index']+next
            if nextlineIndex >= len(context['lines']):
                break
            else:
                nextline = context['lines'][nextlineIndex]
        return True

    return False

def parseUserDebug(pc):
    context = pc['context']
    chunks = context['chunks']

    if is_in_operation(context,'USER_DEBUG'):
        parsedLine = create_parsedLine(context,type='DEBUG')
        parsedLine.update({
            'timeStamp': parsedLine['timeStamp'] + [parsedLine['timeStamp'][0]],
            'type': 'DEBUG',
            'subType': chunks[3],
            'output': chunks[4]
        })
        if parsedLine['subType'] == 'ERROR':
            context['exception'] = True
            context['exception_msg'] = parsedLine['output']

        parsedLine['apexline'] = chunks[2][1:-1]

        line_index = context['line_index']
        lines = context['lines']
        if line_index < len(lines) - 1:
            next = 1
            nextline = lines[line_index + next]
            while '|' not in nextline:
                parsedNextLine = copy_last_parsedLine(context)
                parsedNextLine['output'] = nextline
                next += 1
                if line_index + next >= len(lines):
                    break
                nextline = lines[line_index + next]

        if  parsedLine['output'].startswith('*** '):
            def add_to_LU(string,limit):
                if parsedLine['output'].startswith(string):
                    chs = chunks[4].split(':')[1].strip().split(' ')
                    clone_and_appendLimit(context,limit,chs[0])
                    parsedLine['isLimitInfo'] = True
                    return True
                return False

            metrics = [
                ('*** getCpuTime()', 'CPU time'),
                ('*** getQueries()', 'SOQL queries'),
                ('*** getQueryRows()', 'query rows'),
                ('*** getDmlStatements()', 'DML statements'),
                ('*** getDmlRows()', 'DML rows'),
                ('*** getHeapSize()', 'heap size')
            ]

            for metric, description in metrics:
                if add_to_LU(metric, description):
                    return True

        if 'Usage report.' in parsedLine['output']:
            heapSize = chunks[4].split(':')[3].strip()
            clone_and_appendLimit(context,'heap size',heapSize)
            cpuTime = chunks[4].split(':')[1].split(';')[0].strip()
            clone_and_appendLimit(context,'CPU time',cpuTime)
            parsedLine['isLimitInfo'] = True

            return True

        if  parsedLine['output'].startswith('CPU Time:'):
            chs = chunks[4].split(' ')
            clone_and_appendLimit(context,'CPU time',chs[2])
            parsedLine['isLimitInfo'] = True

        if parsedLine['output'].startswith('CPQCustomHookImplementation'):
            if parsedLine['output'].endswith('PreInvoke'):
                context['CPQCustomHookImplementation'] = 'Started'
            if parsedLine['output'].endswith('PostInvoke'):
                context['CPQCustomHookImplementation'] = 'Finished'

        return True

    return False

def parse_limit_usage(pc):
    context = pc['context']
    chunks = context['chunks']   

    if is_in_operation(context,'CUMULATIVE_LIMIT_USAGE') or is_in_operation(context,'CUMULATIVE_LIMIT_USAGE_END'):
        context['TESTING_LIMITS'] = False

    if is_in_operation(context,'TESTING_LIMITS'):
        context['TESTING_LIMITS'] = True

    if is_in_operation(context,'LIMIT_USAGE_FOR_NS'):
        if 'TESTING_LIMITS' in context and context['TESTING_LIMITS'] == True: 
            return
        package = chunks[2]
        next = 1
        nextline = context['lines'][context['line_index']+next]
        limits = {}
        while '|' not in nextline:
            if 'out of' in nextline:
                sp1 = nextline.split(':')
                limit = sp1[0].strip()
                if 'Number of' in limit: limit = limit.split('Number of ')[1]
                else: limit = limit.split('Maximum ')[1]
                sp2 = sp1[1].strip().split(' ')

                limits[limit] = {'v':int(sp2[0]),'m':int(sp2[3])}
            next = next + 1
            nextline = context['lines'][context['line_index']+next]

        if limits['heap size']['v'] == 0:
            if 'LU' in context:
                if package in context['LU']:
                    limits['heap size']['v'] = context['LU'][package][-1]['heap size']['v']

        append_limits(context,package,limits)
        return True

def parseLimits(pc):
    context = pc['context']
    chunks = context['chunks'] 

    if is_in_operation(context,'LIMIT_USAGE'):
        if chunks[3] == 'SOQL':
            clone_and_appendLimit(context,'SOQL queries',chunks[4])
            return True
        if chunks[3] == 'SOQL_ROWS':
            clone_and_appendLimit(context,'query rows',chunks[4])

        return True


def parseSOQL(pc):
  #  line = context['line']
    context = pc['context']
    chunks = context['chunks']

    if is_in_operation(context,'SOQL_EXECUTE_BEGIN'):
        obj = create_openParsedLine(context,type="SOQL")
        obj['query'] = chunks[4]

        next_line_index = context['line_index']+1
        if next_line_index<len(context['lines']):
            try:
                nextline = context['lines'][next_line_index]

            except Exception as e:
                print(e)
            while '|' not in nextline:
                obj['query'] = obj['query'] +' ' + nextline.strip()
                next_line_index = next_line_index + 1 
                nextline = context['lines'][next_line_index]

        obj['object'] = obj['query'].lower().split(' from ')[1].strip().split(' ')[0]
        obj['apexline'] = chunks[2][1:-1]

        soql = obj['query'].lower()
        ch_so = obj['query'].split("'")
        if len(ch_so)>1:
            posibles = ch_so[1::2]

            ids = [posible for posible in posibles if Sobjects.checkId(posible) ]
            idss = set(ids)
            if len(idss)>0:
                obj['where_ids'] = ",".join(idss)


        obj['for_update'] = ' for update' in soql

        if 'where' in soql:
            soql = soql.split('where')[0]
        _from = soql.split(' from ')[-1].strip()
        _from = _from.split(' ')[0]

        obj['from'] = _from
        obj['output'] = f"Select: {obj['from']} --> No SOQL_EXECUTE_END found"

      #  append_openOpenParsedLines_append_parsedLines_increaseIdent(context,obj,increase=False)
        return True

    if context['chunks_lenght']>1 and chunks[1] == 'SOQL_EXECUTE_END':
        context['totalQueries'] = context['totalQueries'] + 1
        obj = close_openParsedLine(context,type="SOQL",key='type',value='SOQL',decrease=True)
        obj['rows'] = chunks[3].split(':')[1]

        if pc['full_soql']:
          #  query = obj['query']
          #  query = query.replace(' from ',' FROM ')
          #  query = query.replace(' From ',' FROM ')
          #  qs = query.split(' FROM ')
          #  print(qs)
          #  query = f"{qs[0]}{utils.CYELLOW} FROM {utils.CEND}{qs[1]}"
            obj['output'] = f"{obj['query']} --> {utils.CYELLOW}{obj['rows']}{utils.CEND}"
        else:
            for_uptate = "for update" if obj['for_update'] else ""
            ids = f"w:{obj['where_ids']}" if 'where_ids' in obj else ""

            if context['output_format']=='JSON':
                obj['output'] = f"Select {for_uptate}: {obj['from']} --> {obj['rows']} rows {ids}"
            else:
                obj['output'] = f"Select {for_uptate}: {obj['from']} --> {obj['rows']} rows {utils.CFAINT}{utils.CYELLOW}{ids}{utils.CEND}"

        return True

    return False

#@profile
def parseMethod_entry(pc):
    context = pc['context']
    chunks = context['chunks'] 

    if len(chunks)<4:
        print(context['line'])
        return

    method = chunks[3] if len(chunks) == 4 else chunks[4]

    if pc.get('noMP') == True and method.startswith(('vlocity_cmt.','System.','Database.')):
        return True

    if '(' in method:
        method = method.split('(')[0]

    parsedLineData = create_parsedLine(context, type='METHOD')
    parsedLineData.update({
        'method': method,
        'apexline': chunks[2][1:-1] if chunks[2] != '[EXTERNAL]' else 'EX',
        'output': method
    })

    if '.getInstance' in parsedLineData['method']:
        pass
    else:
        append_openParsedLines_and_increaseIdent(context,parsedLineData)

#@profile
def parseMethod_exit(pc):
    context = pc['context']

    chunks = context['chunks'] 

    if len(chunks)<4:
        print(context['line'])
        return

    method = chunks[3] if len(chunks) == 4 else chunks[4]

    if pc.get('noMP') == True and method.startswith(('vlocity_cmt.','System.','Database.')):
        return True

    if '(' in method:
        method = method.split('(')[0]

    parsedLineData = find_in_openParsedLines(context,'method',method)
    apexline = chunks[2][1:-1]

    if parsedLineData == None:
        parsedLineData = find_in_openParsedLines(context,'method',f"{method}",endsWith=True)
        if parsedLineData != None and apexline != parsedLineData['apexline']:
            parsedLineData == None

    if parsedLineData == None:
        parsedLineData = find_in_openParsedLines(context,'method',f"{method}",startsWith=True)
        if parsedLineData != None and apexline != parsedLineData['apexline']:
            parsedLineData == None

    if parsedLineData is not None:
        context['ident'] = parsedLineData['ident']
        create_update_parsedLine(context,parsedLineData=parsedLineData)
    else:
        parsedLineData = create_parsedLine(context, type='NO_ENTRY')
        parsedLineData.update({
            'method': chunks[-1],
            'apexline': chunks[2][1:-1] if chunks[2] != '[EXTERNAL]' else 'EX'
        })

    if 'method' in parsedLineData:
        parsedLineData['output']=parsedLineData['method']
    else:
        parsedLineData['output']=parsedLineData['Id']

def parseMethod(pc):
    context = pc['context']

   # line = context['line']
    chunks = context['chunks'] 
    #if context['chunks_lenght']>1 and 'METHOD_' in  chunks[1]:
    if 1==1:
        if len(chunks)<4:
            print(context['line'])
            return

        operation = chunks[1]
        method = chunks[3] if len(chunks) == 4 else chunks[4]

        if pc.get('noMP') == True and method.startswith(('vlocity_cmt.','System.','Database.')):
            return True

        if '(' in method:
            method = method.split('(')[0]

        if 'ENTRY' in operation:
            parsedLineData = create_parsedLine(context, type='METHOD')
            parsedLineData.update({
                'method': method,
                'apexline': chunks[2][1:-1] if chunks[2] != '[EXTERNAL]' else 'EX',
                'output': method
            })

            if '.getInstance' in parsedLineData['method']:
                pass
            else:
                append_openParsedLines_and_increaseIdent(context,parsedLineData)
            return True

        else:
            parsedLineData = find_in_openParsedLines(context,'method',method)
            apexline = chunks[2][1:-1]

            if parsedLineData == None:
                parsedLineData = find_in_openParsedLines(context,'method',f"{method}",endsWith=True)
                if parsedLineData != None and apexline != parsedLineData['apexline']:
                    parsedLineData == None

            if parsedLineData == None:
                parsedLineData = find_in_openParsedLines(context,'method',f"{method}",startsWith=True)
                if parsedLineData != None and apexline != parsedLineData['apexline']:
                    parsedLineData == None

            if parsedLineData is not None:
                context['ident'] = parsedLineData['ident']
                create_update_parsedLine(context,parsedLineData=parsedLineData)
            else:
                parsedLineData = create_parsedLine(context, type='NO_ENTRY')
                parsedLineData.update({
                    'method': chunks[-1],
                    'apexline': chunks[2][1:-1] if chunks[2] != '[EXTERNAL]' else 'EX'
                })

            if 'method' in parsedLineData:
                parsedLineData['output']=parsedLineData['method']
            else:
                parsedLineData['output']=parsedLineData['Id']
            return True
    else:
        a=1
    return False

def parseVariableAssigment(pc):
    context = pc['context']
    limit = pc['var']
    chunks = context['chunks'] 

   # if is_in_operation(context,'VARIABLE_ASSIGNMENT'):
    if 1==1:
        if len(chunks) >= 5:
            if 'ExecutionException' in chunks[4] or 'ExecutionException' in chunks[4]:
                parsedLine = create_parsedLine(context, type='VAR_ASSIGN')
                parsedLine.update({
                    'type': 'VAR_ASSIGN',
                    'subType': 'EXCEPTION',
                    'output': chunks[4],
                    'apexline': 'EX' if chunks[2] == '[EXTERNAL]' else chunks[2][1:-1]
                })

                next = 1
                nextline = context['lines'][context['line_index']+next]
                while ('VARIABLE_ASSIGNMENT' in nextline or '[EXTERNAL]' in nextline) and 'HEAP_ALLOCATE' not in nextline:
                    chunks = nextline.split('|')
                    parsedLine = create_parsedLine(context, line=nextline, type='VAR_ASSIGN')
                    parsedLine.update({
                        'type':'VAR_ASSIGN',
                        'subType': 'EXCEPTION',
                        'output':chunks[4] if chunks[4] else "NOP",
                        'apexline': chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
                    })
                    next = next + 1
                    nextline = context['lines'][context['line_index']+next]
                return True
            
        if (limit!=None):
            if chunks[3] != 'this': 
                parsedLine = create_parsedLine(context, type='VAR')
                parsedLine.update({
                    'type': 'VAR',
                    'subType': 'VAR',
                    'output': f"{chunks[3]} = {chunks[4]}",
                    'apexline': chunks[2][1:-1]
                })

                if limit != -1:
                    parsedLine['output'] = parsedLine['output'] [0:limit]

        return True
    return False

def parseDML(pc):
    context = pc['context']

  #  line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'DML_BEGIN'):
        parsedLine = create_openParsedLine(context, type="DML")
        parsedLine.update({
            'OP': chunks[3],
            'Type': chunks[4],
            'Id': chunks[2],
            'Rows': chunks[5],
            'apexline': chunks[2][1:-1],
            'output': f"{chunks[3]} {chunks[4]} --> {chunks[5]}"
        })

        return True

    if is_in_operation(context,'DML_END'):
        close_openParsedLine(context,'DML',key='Id',value=chunks[2])
        return True

    return False

def parseVariableScope(pc):
    context = pc['context']
    chunks = context['chunks']

    if '[1]' != chunks[2] or '.' not in chunks[4]:
        return

    #if is_in_operation(context,'VARIABLE_SCOPE_BEGIN'):
    parsedLine = create_parsedLine(context,type='VSB')
    parsedLine['output'] = chunks[4]
    return True

def executeAnonymous(pc):
    context = pc['context']

    if context['line'].startswith('Execute Anonymous'):
        parsedLine = create_parsedLine(context,type='EA')
        parsedLine['output'] = context['line'].split(':')[1]
        return True

def parseCallOutResponse(pc):
    context = pc['context']

    line = context['line']
    chunks = context['chunks']

    if is_in_operation(context,'CALLOUT_RESPONSE'):
        parsedLine = create_parsedLine(context,line,type='CALLOUT')
        parsedLine['apexline'] = chunks[2][1:-1]
        parsedLine['output'] = chunks[3]
        return True

    return False

def parseConstructor(pc):
    context = pc['context']
    chunks = context['chunks']

    if is_in_operation(context,'CONSTRUCTOR_ENTRY'):
        if pc.get('noMP') == True and 'vlocity_cmt.' in chunks[5]:
            return True
        parsedLine = create_openParsedLine(context,field='output',value=chunks[5],type='CONSTRUCTOR')
        parsedLine['apexline'] = chunks[2][1:-1] if chunks[2]!='[EXTERNAL]' else 'EX'
        return True

    if is_in_operation(context,'CONSTRUCTOR_EXIT'):
        if pc.get('noMP') == True and 'vlocity_cmt.' in chunks[5]:
            return True
        close_openParsedLine(context,type='CONSTRUCTOR',key='output',value=chunks[5])
        return True

    return False

def parseCodeUnitStarted(pc):
    context = pc['context']
    chunks = context['chunks']

    parsedLine = create_openParsedLine(context,type='CODE_UNIT')
    parsedLine['output'] = chunks[4] if len(chunks)>4 else chunks[3]

def parseCodeUnitFinished(pc):
    context = pc['context']
    chunks = context['chunks']

    close_openParsedLine(context,'CODE_UNIT',key='output',value=chunks[2])

def parseCodeUnit(pc):
    context = pc['context']
    chunks = context['chunks']

    if is_in_operation(context,'CODE_UNIT_STARTED'):
        parsedLine = create_openParsedLine(context,type='CODE_UNIT')
        parsedLine['output'] = chunks[4] if len(chunks)>4 else chunks[3]
        return True

    if is_in_operation(context,'CODE_UNIT_FINISHED'):
        close_openParsedLine(context,'CODE_UNIT',key='output',value=chunks[2])
        return True

    return False

def parseNamedCredentials(pc):
    context = pc['context']
    chunks = context['chunks']

    if is_in_operation(context,'NAMED_CREDENTIAL_REQUEST'):
        create_openParsedLine(context,field='output',value=chunks[2],type='NAMED_CRD')
        return True

    if is_in_operation(context,'NAMED_CREDENTIAL_RESPONSE'):
        close_openParsedLine(context,type='NAMED_CRD',key='type',value='NAMED_CRD')
        return True

    return False

def parseFlow(pc):
    context = pc['context']
    chunks = context['chunks']
    debugList = context['parsedLines']

    if is_in_operation(context,'FLOW_START_INTERVIEW_BEGIN'):
        parsedLine = create_openParsedLine(context, type='FLOW_START_INTERVIEW')
        parsedLine.update({
            'interviewId': chunks[2],
            'Name': chunks[3],
            'output': chunks[3]
        })
        return True

    if is_in_operation(context,'FLOW_START_INTERVIEW_END'):
        interviewId = chunks[2]
        close_openParsedLine(context,'FLOW_START_INTERVIEW',key='interviewId',value=interviewId)
        return True

    if is_in_operation(context,'FLOW_ELEMENT_ERROR'):
        parsedLine = create_update_parsedLine(context, type='FLOW_ELEMENT_ERROR')
        parsedLine.update({
            'message': chunks[2],
            'elementType': chunks[3] if len(chunks) > 3 else '',
            'elementName': chunks[4] if len(chunks) > 4 else ''
        })
        parsedLine['output'] = utils.CRED + f"{chunks[2]} in {parsedLine['elementType']}:{parsedLine['elementName']}" + utils.CEND
        #THIS IS NOT CORRECT
        debugList.append(parsedLine)
        context['exception'] = True
        context['exception_msg'] = parsedLine['output']
        return True
    
    if is_in_operation(context,'FLOW_ELEMENT_BEGIN'):
        parsedLine = create_openParsedLine(context, type='FLOW_ELEMENT')
        parsedLine.update({
            'interviewId': chunks[2],
            'elementType': chunks[3],
            'elementName': chunks[4],
            'output': f"{chunks[3]}-{chunks[4]}"
        })
        return True

    if is_in_operation(context,'FLOW_ELEMENT_END'):
        interviewId = chunks[2]
        close_openParsedLine(context,'FLOW_ELEMENT',key='interviewId',value=interviewId)

    if is_in_operation(context,'FLOW_RULE_DETAIL'):
        values = {
            'type':'FLOW_ELEMENT',
            'elementType':'FlowDecision',
            'interviewId':chunks[2],
            'elementName':chunks[3]
        }
        parsedLine = find_in_parsedLines(context, values)
        parsedLine.update({
            'ruleName': chunks[3],
            'result': chunks[4],
            'output': f"{parsedLine['elementType']}-{parsedLine['elementName']} -- {chunks[3]}->{chunks[4]}"
        })

        return True

    return False

def parseUserInfo(pc):
    context = pc['context']

    if is_in_operation(context,'USER_INFO'):
        create_parsedLine(context,context['line'],field='output',value=context['chunks'][4],type='USER_INFO')
        return True
    return False

def appendEnd(pc):
    context = pc['context']


    #in case there is no line parsed
    if context['parsedLines'][-1]['type'] == 'LOGDATA':
        return
    for line in reversed(context['lines']):
        if '|' in line:
            break

    if 'CPQCustomHookImplementation' in context and  context['CPQCustomHookImplementation'] == 'Started':
        parsedLine = create_parsedLine(context,line,type='EXCEPTION',field='output',value="CPQCustomHookImplementation did not finish")
        context['exception'] = True
        context['exception_msg'] = parsedLine['output']

        context['file_exception'] = True
        
    lastline = line
    parsedLine = create_update_parsedLine(context,lastline,type="END")
    parsedLine['output'] = 'Final Limits'
    context['parsedLines'].append(parsedLine)