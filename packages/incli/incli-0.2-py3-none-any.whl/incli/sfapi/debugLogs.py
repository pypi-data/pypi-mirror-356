from . import restClient,query,file,utils,Sobjects,traceFlag,elementParser,debugLogsPrint,tooling

import colorama
import sys,time,os,copy
import ansi2html,re
import threading,traceback
from queue import Queue,Empty
from multiprocessing import Process, Manager

def get_apexLog_records_from_db(logUserId=None,limit=50,whereClause=None):
    where = f" where {whereClause} " if whereClause != None else ''
    where = f" where logUserId='{logUserId}' " if logUserId is not None else where

    call = query.query(f"Select Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier FROM ApexLog  {where} order by LastModifiedDate desc limit {limit}")
    return call

def printLogRecords(loguser=None,limit=50,whereClause=None):
    logUserId = get_loguser_id(loguser) if loguser != None else None
    if loguser != None:
        print(f'Logs for user {loguser}:')
    logs = get_apexLog_records_from_db(logUserId,limit=limit,whereClause=whereClause)
    logs = utils.deleteNulls(logs,systemFields=False)
    logs1 = []
    for log in logs:
        log['LastModifiedDate'] = log['LastModifiedDate'].split('.')[0]
        log['StartTime'] = log['StartTime'].split('.')[0]
        log['LogUserId'] =  f"{log['LogUserId']} ({get_username_and_cache(log['LogUserId'])})"

        logs1.append(log)

    utils.printFormated(logs1,fieldsString="Id:LogUserId:LogLength:DurationMilliseconds:LastModifiedDate:Request:Operation:Application:Status:Location", rename="LogLength%Len:DurationMilliseconds%ms:Application%App")
    return logs


def get_apexLog_record_and_body_from_db(logId,logRecord=None):
    if logRecord == None:
        logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog where Id ='{logId}' limit 1")
        if logRecords == None or len(logRecords)==0:
            utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{logId}> cannot be found in the Server.',other=f"No record in ApexLog with Id {logId}")    
        logRecord = logRecords[0]

    action = f"/services/data/v56.0/sobjects/ApexLog/{logId}/Body/"
    logbody = restClient.callAPI(action)
    return logRecord,logbody

def extract_apexlog_file_header(body):
    def parse_header(pc, line):
        if 'LOGDATA' in line:
            # Clean and split the line while filtering out unnecessary parts
            ch1 = [c.replace('\x1b[0;32m', '').replace('\x1b[0m\x1b[2m', '').replace('\x1b[0m', '') for c in line.split() if c and 'LOGDATA' not in c]

            if ch1[0] == 'Id:':
                pc['header'] = {
                    'Id': ch1[1],
                    'logId': line.split()[1],  # Uses the original line split for logId
                    'LogUserId': ch1[3],
                    'LogUserName': ch1[4].strip('()'),  # Strip parentheses in one go
                    'Request': ch1[6],
                    'Operation': ch1[8],
                    'LogLength': ch1[10],
                    'DurationMilliseconds': ch1[12]
                }
            else:
                pc['header'].update({
                    'StartTime': ch1[1],
                    'Application': ch1[3],
                    'Status': ch1[5],
                    'Location': ch1[7],
                    'RequestIdentifier': ch1[9]
                })

    if not body:
        return None

    lines = body.splitlines()
    try:
        if 'LOGDATA' in lines[0]:
            pc = {}
            parse_header(pc, lines[0])
            parse_header(pc, lines[1])
            return pc.get('header')  # Use .get() to safely retrieve 'header'
        return None
    except Exception as e:
        print(e)  # Print the exception message


def extract_log_filepath(logId):
    return f"{restClient.logFolder()}{logId}.log"


def retrieve_fullBody_from_File_Id(logId):
    return retrieve_fullBody_from_File(extract_log_filepath(logId))

def retrieve_fullBody_from_File(filepath):
    if file.exists(filepath):
        body = file.read(filepath)
        logRecord = extract_apexlog_file_header(body)
        return logRecord,body,filepath

    return None,None,filepath

def retrieve_logFile_or_fallback_to_db(logId=None,logRecord=None):
    """Gets the log body for the provided logId from file (if exists) otherwise from the Org"""
    if logId==None: logId = logRecord['Id']
    logRecord2,fullBody,filepath = retrieve_fullBody_from_File_Id(logId)

    if fullBody == None:     
       # start_time = time.time()
        try:   

            logRecord, body = get_apexLog_record_and_body_from_db(logId,logRecord=logRecord)
            fullBody = extract_logHeader(logRecord) + body  

        #    print(f"Download time: {time.time() - start_time:.4f} seconds")
        except Exception as e:
            print(str(e))
            if 'error' in e.args[0]:
                if 'cannot be found in the Server' in e.args[0]['error']:
                    fullBody = f"No log record found for Id {logId}"
            else:
                raise e
            
        save_to_store(logId, fullBody)        
       # print(f"Save time: {time.time() - start_time:.4f} seconds  size {len(fullBody)}")
    else:
        logRecord = logRecord2
    return logRecord,fullBody,filepath

def extract_logHeader(logRecord):
    log = logRecord
    username = get_username_and_cache(log['LogUserId'])

    logHeader = f"""{utils.CFAINT}LOGDATA:    Id: {log['Id']}   LogUserId: {log['LogUserId']} {utils.CGREEN}({username}){utils.CEND}{utils.CFAINT}    Request: {log['Request']}  Operation: {utils.CGREEN}{log['Operation']}{utils.CEND}{utils.CFAINT}    lenght: {log['LogLength']}    duration:  {utils.CGREEN}{log['DurationMilliseconds']} {utils.CEND} 
 {utils.CFAINT}LOGDATA:      startTime: {log['StartTime']}    app: {log['Application']}      status: {log['Status']}     location: {log['Location']}     requestIdentifier: {log['RequestIdentifier']}{utils.CEND}
    """     
    return logHeader

def save_to_store(logId,body):
    filepath = extract_log_filepath(logId) #f"{restClient.logFolder()}{logId}.log"
    file.write(filepath,body) 

userCache = {}
def get_username_and_cache(Id):
    username_query = f"select Username from User where Id='{Id}'"
    if username_query not in userCache: userCache[username_query] = query.queryField(username_query) 
    return userCache[username_query]

def do_parse_storage(pc,search_dir=None):  
    if pc['store_logId'] != None:
        pc['filepath'] =  extract_log_filepath(pc['store_logId']) # f"{restClient.logFolder()}{pc['store_logId']}.log"
        do_parse_logId(pc)
        return

    search_dir = search_dir or restClient.logFolder()
    os.chdir(search_dir)

    log_filePaths = sorted(
        (os.path.join(search_dir, f) for f in os.listdir(search_dir) if os.path.isfile(f) and f.lower().endswith('.log')),
        key=os.path.getmtime
    )

    fileNames = [os.path.basename(f) for f in log_filePaths]

    print(f"Files to be parsed in the store {len(log_filePaths)}")
    file_dates = []

    if 1==1:
        print(f"Ordering files by date...")
        total_records = len(log_filePaths)
        num = 0
        for filepath in log_filePaths:
            logRecord,body,x = retrieve_fullBody_from_File(filepath)
            for line in body.splitlines():
                if '|' in line:
                    _time = line.split(' ')[0]
                    file_dates.append({
                        'time':_time,
                        'file':filepath
                    })
                    break

            num = num +1
            sys.stdout.write("\r%d%%" % int(100*num/total_records))
            sys.stdout.flush() 
        newlist = sorted(file_dates, key=lambda d: d['time'])
        sorted_log_file = [d['file'] for d in newlist]


    else:
        sorted_log_file = sorted(fileNames)

    print(f"Ordered.")

    try:
        parse_apexlogs_by_filepaths(pc,filepaths=sorted_log_file,printProgress=True)

    except KeyboardInterrupt:
        print('Interrupted')
    
    print_parsing_results(pc)


def worker_auto_renew_traceFlag(tf):
    try:
        while True:
            print("Updating Trace Flag")
            traceFlag.update_trace_flag_incli(tf['Id'],minutes=5)
            time.sleep(200)
    except Exception as e:
        print(f"InCli no longer in auto, due to exception")
        utils.printException(e)

def worker_deleteRecords(delete_queue):
    def divide_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
        
    while True:
        logId = delete_queue.get()

        logIds = [logId]
        while True:
            try:
                logId = delete_queue.get_nowait()  # Non-blocking
                logIds.append(logId)
            except Empty:
                break

        try :
            Sobjects.delete('ApexLog',logIds)
            # logIdsList= list(divide_chunks(logIds,200))
            # for l in logIdsList:
            #     res = Sobjects.deleteMultiple('ApexLog',l)

           # print(f"Deleted record {logId}")
            delete_queue.task_done()
        except utils.InCliError as e:
            if e.args[0]['errorCode'] != 'NO_LOG':
                utils.printException(e)
        except Exception as e:
            print(logId)
            print(e)

def worker_read_logBody_from_org(q):
    while True:
        try:
           # Id = q.get()
            r = q.get()
            retrieve_logFile_or_fallback_to_db(logRecord=r)
          #  print(f"     Read body for Id {Id}")
        #     Sobjects.delete('apexlog',Id)
            q.task_done()
        except Exception as e:
            print(e)

def start_download_worker_threads(pc,threads):
    pc['downloadBody_queue'] = Queue(maxsize=0)
    threads = 10
    for x in range(0,threads):
        threading.Thread(target=worker_read_logBody_from_org,args=(pc['downloadBody_queue'],), daemon=True).start()

def start_delete_worker_threads(pc,threads):
    pc['delete_queue'] = Queue(maxsize=0)
    for x in range(0,threads):
        threading.Thread(target=worker_deleteRecords,args=(pc['delete_queue'],), daemon=True).start()

def do_parse_tail(pc):
    timefield = "LastModifiedDate"

    logRecords = query.queryRecords(f"Select fields(all) FROM ApexLog order by {timefield} desc limit 1")
    recordTime = logRecords[0].get(timefield) if logRecords else '2000-12-12T17:19:35.000Z'
    lastRecordTime = f"{recordTime.split('.')[0]}Z"

    if pc.get('all') == True:
        lastRecordTime = '2000-12-12T17:19:35Z'

    if  pc.get('loguser')!=None and  pc.get('loguser').lower() == 'InCliELKIT'.lower():
        pc['isELK'] = True

   # InCliUser = 'InCliELKIT'.lower()
   # is_cli_user = pc.get('loguser').lower() == InCliUser if pc.get('loguser')!=None else False

    if pc.get('isELK') == True:
   # if is_cli_user:
        logUserId = 'InCliELKIT'
#        incli_debuglevel_ids = traceFlag.get_InCli_debuglevelIds()
        pc.update({
            'auto': False,
            'output_format': 'JSON',
            'printNum': False,
            'deleteLogs':True
        })
    else:
        pc['printNum'] = True
        if (pc.get('deleteLogs') or pc.get('auto')) and pc['loguser'] is None:
            pc['loguser'] = f"username:{pc['connection']['Username']}"
        logUserId = get_loguser_id(pc['loguser']) if pc.get('loguser') else None

    if pc.get('deleteLogs')==True:       
        start_delete_worker_threads(pc,1)
        print(f"ApexLog records for {pc['loguser']} {logUserId} will be automatically deleted.")

    if pc.get('auto') == True:
        tf = traceFlag.set_incli_traceFlag_for_user(f"Id:{logUserId}",pc['debug_level'])
        print(f"TraceFlag for user {pc['loguser']} {logUserId} set to Auto. Debug Level InCli{pc['debug_level']}.")

        utils.printFormated(tf,fieldsString="ApexCode,ApexProfiling,Callout,Database,LogType,System,Validation,Visualforce,Workflow",separator=',')
        threading.Thread(target=worker_auto_renew_traceFlag,args=(tf,), daemon=True).start()

    if 1==1:
        start_download_worker_threads(pc,10)

    try:
        waitingForRecords = False
        procesed = []
        greaterThanLastTime = True

        while (True):
            if greaterThanLastTime:    
                where = f" {timefield} > {lastRecordTime} "
            else:          
                where = f" {timefield} >= {lastRecordTime} "
            where = f" {pc['whereClause']} and {where}" if pc['whereClause'] is not None else where

            if logUserId is not None:
                if pc.get('isELK') == True:
                    serverTime = restClient.get_serverTime()
                    res1 = tooling.query(f"""SELECT Id, StartDate, ExpirationDate,TracedEntity.Name,TracedEntityId,  DebugLevel.DeveloperName 
                                    FROM TraceFlag 
                                    WHERE StartDate <= {serverTime} AND ExpirationDate >= {serverTime} """)

                    pc['ELK_listen'] = [r['TracedEntityId'] for r in res1['records'] if r['DebugLevel']['DeveloperName'] == 'InCliELKIT']
                    other = [r['TracedEntityId'] for r in res1['records'] if r['DebugLevel']['DeveloperName'] != 'InCliELKIT']
                    pc['ELK_delete'] = [entityId for entityId in pc.get('ELK_listen') if entityId not in other]

                    if len(pc['ELK_listen']) == 0:
                        time.sleep(5)
                        continue
                    
                 #   incli_user_ids = traceFlag.get_InCli_usersIds(incli_debuglevel_ids)
                    where = f" logUserId in ({query.IN_clause(pc['ELK_listen'])}) and {where} "
                else:
                    where = f" logUserId='{logUserId}'and {where} "

            fields = "Id,LogUserId,LogLength,LastModifiedDate,Request,Operation,Application,Status,DurationMilliseconds,StartTime,Location,RequestIdentifier,SystemModstamp"
            logRecords = query.queryRecords(f"Select {fields} FROM ApexLog where {where} order by {timefield} asc")
            if len(logRecords) > 0:
                waitingForRecords = False

                logRecords_not_processed = [r for r in logRecords if r['Id'] not in procesed]

                if pc.get('parseSmallFiles')==False:
                    records1 = []
                    for r in logRecords_not_processed:
                        if  r['LogLength']>200: 
                            records1.append(r)
                        else:
                            if pc.get('deleteLogs') == True:
                                pc['delete_queue'].put(r['Id'])
                    logRecords_not_processed = records1

                if len(logRecords_not_processed) == 0:
                    greaterThanLastTime = True
                    continue     
                
                greaterThanLastTime = False
                ids_not_processed = [r['Id'] for r in logRecords_not_processed]
                procesed.extend(ids_not_processed)

                for r in logRecords_not_processed:
                    pc['downloadBody_queue'].put( (r) )

                parse_apexlogs_tail(logIds=ids_not_processed,pc=pc,raiseKeyBoardInterrupt=True,raise_no_log=False)

                lastRecordTime = logRecords[-1][timefield].split('.')[0] + "Z"

            elif  waitingForRecords == False:
                print()
                print(f"waiting for debug logs for user {pc['loguser']}")  if pc['loguser'] != None  else print(f"waiting for debug logs ")
                waitingForRecords = True

            if pc.get('isELK') == True:
                time.sleep(10)
            else:
                time.sleep(2)

    except KeyboardInterrupt as e:
        print()
        print_parsing_results(pc)
        print("Terminating -tail..., cleaning up")
        parse_apexlogs_from_org_terminate()
        if pc['auto']:
            print(f"Stopping -auto. Deleting InCli traceflag for user { pc['loguser']}")
    
        if pc.get('auto') == True:
            traceFlag.delete_trace_Flag(tf['Id'])

        print('Terminated')
        return
    
def parse_apexlogs_tail(pc,logIds=None,raiseKeyBoardInterrupt=False,printProgress=False,threads=10,raise_no_log=True):
    if 'total_parsed'       not in pc:   pc['total_parsed'] = 0
    if 'parsed_Id_status'   not in pc:   pc['parsed_Id_status'] = []
    if 'errors' not in pc:   pc['errors'] = []
    if 'downloadBody_queue'  not in pc:   pc['downloadBody_queue'] = None
            
    num = 0
    items = logIds
    if 'downloadOnly' in pc and pc['downloadOnly'] == True:
        return

    for num,item in enumerate(items):
        if printProgress:
            sys.stdout.write("\r%d%%" % int(100*num/len(items)))
        try:
            if logIds!= None:
                parsed={ 'logId':item, 'status':'ok' }
                pc['logId'] = item
                pc['filepath'] = None
            else:
                parsed={ 'file':os.path.basename(item), 'status':'ok' }
                pc['filepath'] = item  
                pc['logId'] = parsed['file'].split('.')[0]
            
            pc['parsed_Id_status'].append(parsed)

            filepath = wait_4_logFile(pc['logId'])
            if filepath == None:
                continue
            pc['logRecord'],pc['body'],pc['filepath'] = retrieve_fullBody_from_File(filepath) 

            if pc.get('delete_queue')!= None:
                if pc.get('isELK'):
                    if pc['logRecord']['LogUserId'] in pc.get('ELK_delete'):            
                        pc['delete_queue'].put(pc['logId'])
                if pc.get('isELK') != True:
                    pc['delete_queue'].put(pc['logId'])

            if pc['body'] == None :   
                utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
            if len(pc['body'])==0:    
                utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')
            if 'No log record found for Id' in pc['body']:
                print(f"{pc['body']} as it was already deleted by another process.")
                continue

            if pc.get('logRecord') != None:
                if 'logId' not in parsed : 
                    parsed['logId'] = pc['logRecord']['Id']
                    parsed['timeStamp'] = pc['logRecord']['StartTime']

            parse = True
            if pc['filter'] != None:
                if pc['filter'] not in pc['body']:
                    parse = False

            if parse == True:
                parse_apexlog_body(pc)
                debugLogsPrint.print_parsed_lines_to_output(pc)

                if 'printNum' in pc and pc['printNum']:    print( pc['total_parsed']+num+1)
                if 'logRecord' in pc:
                    if pc['logRecord'] == None: parsed['timeStamp'] = 'No log record'
                    else:
                        parsed['timeStamp'] = pc['logRecord']['StartTime']
                        if parsed['timeStamp'] == None: parsed['timeStamp'] = 'No time stamp'
                else:
                    parsed['timeStamp'] = ''
                if pc['context']['exception'] == True:    
                    parsed['status'] = pc['context']['exception_msg'][0:200]

            
        except KeyboardInterrupt:
            if raiseKeyBoardInterrupt:        raise
            break
        except utils.InCliError as e:
            parsed['status'] = f"Parse error: {e.args[0]['errorCode']}  "
            utils.printException(e)
            pc['errors'].append(e)
        except Exception as e:
            e1 = utils.exception_2_InCliException(e)
            parsed['status'] = f"{e1.args[0]['errorCode']}: {e1.args[0]['error']}"
        #    if 'header' in pc:
        #        if 'logId' not in parsed : 
        #            parsed['logId'] = pc['header']['Id']
        #            parsed['timeStamp'] = pc['header']['startTime']
            pc['errors'].append(e1)
            print(traceback.format_exc())

    pc['total_parsed'] = pc['total_parsed'] + num + 1
    
def wait_4_logFile(logId):
    file_path = extract_log_filepath(logId)

    counter = 0
    while not os.path.exists(file_path):
       # print(f"Waiting for {file_path} to be downloaded...")
        time.sleep(0.2)  
        counter = counter +1
        if counter > 100:
            return None
    return file_path

def do_parse_logs_lastN(pc):
    whereClause = pc['whereClause']
    loguser = pc['loguser']
    lastN = pc['lastN']
    pc['printNum'] = True

    if loguser ==None:
        loguser = restClient.getConfigVar('loguser')

    if loguser == None:
        print(f"{utils.CYELLOW}Getting logs for all users.{utils.CEND}")
    else:
        print(f"{utils.CYELLOW}Getting logs for {loguser}.{utils.CEND}")

    where = f" where {whereClause} " if whereClause is not None else ''
    where = f" where logUserId='{get_loguser_id(loguser)}' " if loguser is not None else where

    if lastN == None: lastN = 1
    q = f"Select Id FROM ApexLog {where} order by LastModifiedDate desc limit {lastN}"
    logIds = query.queryFieldList(q)
    if logIds == None or len(logIds)==0:   utils.raiseException(errorCode='NO_LOG',error=f'No logs can be found. ',other=q)

    parse_apexlogs_from_org_lastN(pc,logIds=logIds)

    print_parsing_results(pc)

def do_parse_from_file(parseContext):

    if file.exists(parseContext['filepath']) == False:
        utils.raiseException(errorCode='NO_LOG',error=f'The requested file <{parseContext["filepath"]}> cannot be found in the Server.',other="No file ")
    else:
        parseContext['logRecord'],parseContext['body'],parseContext['filepath'] = retrieve_fullBody_from_File(parseContext['filepath'])

  #  parseContext['body'] = file.read(parseContext['filepath'])
    parseContext['operation'] = 'parsefile'
 #   name = os.path.basename(parseContext['filepath']).split('.')[0]
 #   parseContext['logId']=name
    name = os.path.basename(parseContext['filepath'])
    parseContext['logId'] = name.split('.')[0]
    context =  parse_apexlog_body(parseContext)
    debugLogsPrint.print_parsed_lines_to_output(parseContext)
    return context

def do_parse_logId(parseContext):
    set_apexlog_body_in_pc(parseContext)
    context =  parse_apexlog_body(parseContext)
    debugLogsPrint.print_parsed_lines_to_output(parseContext)

    return context

def parse_apexlogs_by_filepaths(pc,filepaths,raiseKeyBoardInterrupt=False,printProgress=False,raise_no_log=True):

    if 'total_parsed'       not in pc:   pc['total_parsed'] = 0
    if 'parsed_Id_status'   not in pc:   pc['parsed_Id_status'] = []
    if 'errors' not in pc:   pc['errors'] = []
    if 'downloadBody_queue'  not in pc:   pc['downloadBody_queue'] = None

    num = 0

    for num,item in enumerate(filepaths):
        if printProgress:
            sys.stdout.write("\r%d%%" % int(100*num/len(filepaths)))
        try:
            parsed={ 'file':os.path.basename(item), 'status':'ok' }
            pc['filepath'] = item  
            pc['logId'] = parsed['file'].split('.')[0]
            
            pc['parsed_Id_status'].append(parsed)
            
            if file.exists(item):
                pc['filepath'] = item
                pc['logRecord'],pc['body'],filename = retrieve_fullBody_from_File(pc['filepath'])
            else:
                utils.raiseException(errorCode='NO_LOG',error=f'The requested file <{filename}> cannot be found. ')
            if pc['body'] == None :   utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
            if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')

            if pc.get('logRecord') != None:
                if 'logId' not in parsed : 
                    parsed['logId'] = pc['logRecord']['Id']
                    parsed['timeStamp'] = pc['logRecord']['StartTime']

            parse_apexlog_body(pc)
            debugLogsPrint.print_parsed_lines_to_output(pc)

            if pc.get('printNum'):    
                print( pc['total_parsed']+num+1)
            if 'logRecord' in pc:
                if pc['logRecord'] == None: parsed['timeStamp'] = 'No log record'
                else:
                    parsed['timeStamp'] = pc['logRecord']['StartTime']
                    if parsed['timeStamp'] == None: parsed['timeStamp'] = 'No time stamp'
            else:
                parsed['timeStamp'] = ''
            if pc['context']['exception'] == True:    
                parsed['status'] = pc['context']['exception_msg'][0:200]

        except KeyboardInterrupt:
            if raiseKeyBoardInterrupt:        raise
            break
        except utils.InCliError as e:
            parsed['status'] = f"Parse error: {e.args[0]['errorCode']}  "
            utils.printException(e)
            pc['errors'].append(e)
        except Exception as e:
            e1 = utils.exception_2_InCliException(e)
            parsed['status'] = f"{e1.args[0]['errorCode']}: {e1.args[0]['error']}"
        #    if 'header' in pc:
        #        if 'logId' not in parsed : 
        #            parsed['logId'] = pc['header']['Id']
        #            parsed['timeStamp'] = pc['header']['startTime']
            pc['errors'].append(e1)
            print(traceback.format_exc())

    pc['total_parsed'] = pc['total_parsed'] + num + 1

def print_results(result_dict,pc):
    counter = 0

    while True:
        while counter not in result_dict:
            time.sleep(0.1)  # Wait until the result is available

        Id = result_dict[counter]

        print(f"Result for ID {counter}: {Id}")

        try:
            if Id == None:
                continue
            pc['logId'] = Id
            pc['filepath'] = None

            set_apexlog_body_in_pc(pc)
            parse_apexlog_body(pc)
            debugLogsPrint.print_parsed_lines_to_output(pc)

        except Exception as e:
            print(e)
        
        counter = counter + 1 

downloadBody_queue = None
print_process = None

def parse_apexlogs_from_org_terminate():
    global downloadBody_queue,print_process
  #  if downloadBody_queue!= None:
  #      downloadBody_queue.put((None,0))
    if print_process!= None:
        print("Terminating printer process")
        print_process.terminate()
        print_process.join()


def parse_apexlogs_from_org_lastN(pc,logIds=None,raiseKeyBoardInterrupt=False,threads=10,raise_no_log=True):
    global downloadBody_queue,print_process
    def read_logBody_from_org(id_queue, result_dict,deleteLogs):
      while True:
        try:
            id_data = id_queue.get()  # Get the next id and its position
            if id_data is None:  # None is the signal to stop the worker
                break
            Id, position = id_data                
            retrieve_logFile_or_fallback_to_db(logId=Id)
            #json_data = getJSON(id_)  # Simulate downloading the JSON data
            if deleteLogs == True:
                delete_log_from_org(Id)
            result_dict[position] = Id  # Store the result by position
            id_queue.task_done()  # Indicate the task is done
        except Exception as e:
            print(e)
            result_dict[position] = None  # Store the result by position


    if downloadBody_queue == None:
        downloadBody_queue = Queue(maxsize=0)
        manager = Manager()
        result_dict = manager.dict()
        pc['log_counter'] = 0

        #threads = 1
        for x in range(0,threads):
            threading.Thread(target=read_logBody_from_org,args=(downloadBody_queue,result_dict,pc['deleteLogs']), daemon=True).start()

        pc_copy = copy.deepcopy(pc)
        print_process = Process(target=print_results, args=(result_dict,pc_copy,))
        print_process.start()

    for logid in logIds:
        downloadBody_queue.put( (logid, pc['log_counter']) )
        pc['log_counter'] = pc['log_counter'] + 1

    if pc.get('downloadOnly') == True:
        return      
    
  #  print_process.join()

def delete_log_from_org(logId):
    return Sobjects.delete('apexlog',logId)

def print_parsing_results(pc):
    print()

    if 'parsed_Id_status' not in pc:
        print("No files parsed.")
        return 
    parsed = pc['parsed_Id_status']
    errors = pc['errors']

    print(f"{pc['total_parsed']} logs parsed")
   # print(parsed)
    parsed = [par for par in parsed if par['status']!='ok']

    if len(parsed) == 0:  print("No errors.")
    if len(parsed)>0:
        utils.printFormated(parsed,fieldsString='timeStamp:logId:status')
     #   errors = list({error.args[0] for error in errors})
        errors = list({error.args[0]['errorCode']:error for error in errors}.values())

        for error in errors:    utils.printException(error)  

def get_loguser_id(loguser):
    id = Sobjects.IdF('User',loguser)
    return id if id!= None else utils.raiseException('QUERY',f"User with field {loguser} does not exist in the User Object.") 

def set_apexlog_body_in_pc(pc):
    """if pc['filepath'] defined, reads from the file specified. Otherwiese logId needs to be set. 
    """

    filename = None
    if pc.get('filepath') != None:
        filename = pc['filepath']
    else:
        filename = extract_log_filepath(pc['logId']) #f"{restClient.logFolder()}{pc['logId']}.log"

    if file.exists(filename):
        pc['filepath'] = filename
        pc['logRecord'],pc['body'],x = retrieve_fullBody_from_File(pc['filepath'])
    else:
        pc['logRecord'],pc['body'],pc['filepath'] = retrieve_logFile_or_fallback_to_db(logId=pc['logId'])
    if pc['body'] == None :   utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
    if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')




def createContext(pc):

    lines = pc['body'].splitlines()
    context = {
        'totalQueries' : 0,
        'timeZero':0,
        'ident':0,
        "exception":False,
        'LU':{}
    }
    context['totalQueries'] = 0
    context['timeZero'] = 0
    context['ident'] = 0
    context['exception'] = False
    context['file_exception'] = False
    context['previousIsLimit'] = False
    context['firstLineIn'] = True
    context['firstLineOut'] = True

    context['parsedLines'] = []
    context['openParsedLines'] = []

    context['lines'] = lines

    return context

frequency = {}

def parse_apexlog_body(pc):
    if pc['body'] == None :  utils.raiseException(errorCode='NO_LOG',error=f'The requested log <{pc["logId"]}> cannot be found. ')
    if len(pc['body'])==0:    utils.raiseException(errorCode='NO_LOG',error=f'The body for the requested log <{pc["logId"]}> is empty. ')


    exclude_list1 = ['SYSTEM_MODE_ENTER','SYSTEM_MODE_EXIT','HEAP_ALLOCATE','STATEMENT_EXECUTE','VARIABLE_SCOPE_XXXX_BEGIN','HEAP_ALLOCATE','SYSTEM_METHOD_ENTRY','SYSTEM_METHOD_EXIT','SOQL_EXECUTE_EXPLAIN','ENTERING_MANAGED_PKG','SYSTEM_CONSTRUCTOR_ENTRY','SYSTEM_CONSTRUCTOR_EXIT']
    exclude_list2 = ['VALIDATION_RULE','VALIDATION_FORMULA','VALIDATION_PASS','WF_RULE_FILTER','WF_RULE_EVAL_VALUE','STATIC_VARIABLE_LIST','FLOW_CREATE_INTERVIEW_BEGIN','FLOW_CREATE_INTERVIEW_END','TOTAL_EMAIL_RECIPIENTS_QUEUED','CUMULATIVE_PROFILING_BEGIN','CUMULATIVE_PROFILING','CUMULATIVE_PROFILING_END','EXECUTION_STARTED','EXECUTION_FINISHED']

    if 'noMethod' in pc and  pc['noMethod'] == True:
        exclude_list1.append('METHOD_ENTRY')
        exclude_list1.append('METHOD_EXIT')
        exclude_list1.append('CONSTRUCTOR_ENTRY')
        exclude_list1.append('CONSTRUCTOR_EXIT')
        exclude_list1.append('VARIABLE_SCOPE_BEGIN')
        exclude_list1.append('WF_CRITERIA_BEGIN')
        exclude_list1.append('WF_CRITERIA_END')

    try:
        context = createContext(pc)
        context['output_format'] = pc['output_format']
        pc['context'] = context

        parsers = [
         #   elementParser.parseVariableAssigment,
         #   elementParser.parseMethod,
            elementParser.parseSOQL,
            elementParser.parse_limit_usage,
            elementParser.parseLimits,
            elementParser.parseUserDebug,
            elementParser.parseUserInfo,
            elementParser.parseExceptionThrown,
            elementParser.parseDML,
         #   elementParser.parseConstructor,
         #   elementParser.parseCodeUnit,
            elementParser.parseNamedCredentials,
            elementParser.parseCallOutResponse,
          #  elementParser.parseVariableScope,
            elementParser.parseWfRule,
            elementParser.parseFlow
        ]

        parser_map = {
            "METHOD_ENTRY": elementParser.parseMethod_entry,
            "METHOD_EXIT": elementParser.parseMethod_exit,
            "CONSTRUCTOR_ENTRY":elementParser.parseConstructor,
            "CONSTRUCTOR_EXIT":elementParser.parseConstructor,
            "VARIABLE_ASSIGNMENT":elementParser.parseVariableAssigment,
            "VARIABLE_SCOPE_BEGIN":elementParser.parseVariableScope,
            'CODE_UNIT_STARTED':elementParser.parseCodeUnitStarted,
            'CODE_UNIT_FINISHED':elementParser.parseCodeUnitFinished
        }

        for num,line in enumerate(context['lines']):
            if line == '':
                continue
            if context['firstLineIn'] == True:
                if 'APEX_CODE' in line:
                    context['firstLineIn'] = False
                    levels = line.strip().split(' ')[1].replace(',','=').replace(';','  ')
                    levels = f"{utils.CFAINT}{levels}{utils.CEND}"
                    obj = {  'type':'LOGDATA', 'output':levels  }
                    context['parsedLines'].append(obj)

                    continue      
                else:
                    obj = {    'type':'LOGDATA',   'output':line  }
                    context['parsedLines'].append(obj)
                    continue

            chunks = line.split('|')
            if len(chunks)<2:
                if line.startswith('Execute Anonymous'):
                    context['line'] = line
                    context['chunks'] = chunks
                    elementParser.executeAnonymous(pc)
                continue
            if len(chunks[0])<10:
                continue
            if len(chunks[1])>30:
                continue

            context['chunks'] = chunks
            operation = chunks[1]

            if operation in exclude_list1: continue
            if operation in exclude_list2 : continue

            context['chunks_lenght'] = len(chunks)
            context['line'] = line
            context['line_index'] = num

            if operation in parser_map:
                parser_map[operation](pc)

            else:    
                #print(operation)
                for parser in parsers:
                    if parser(pc):
                        continue
            
        if len(context['openParsedLines']) > 0:
            a=1
        elementParser.appendEnd(pc)

        return context

    except KeyboardInterrupt as e:
        print(f"Parsing for logI {pc['logId']} interrupted.")
        raise e
    except Exception as e:
        print(f"Exception while parsing for logI {pc['logId']} ")
        raise e
