import json
from .sfapi import Sobjects, query,restClient,jsonFile,utils,objectUtil,debugLogs,digitalCommerceUtil,VlocityErrorLog,ip_attachments,VlocityTrackingEntry
import logging,time
import simplejson,sys
from operator import itemgetter
from inspect import getmembers, isfunction
import traceback
import colorama
from difflib import SequenceMatcher
from types import SimpleNamespace

#/Users/uormaechea/Documents/Dev/python/incliLib/InCLipkg/incli/logs/07L3O00000E6dDKUAZ.log

varsFile = 'confIcli.json'
vars = None

def readVars(field=None):
    global vars
    vars = jsonFile.read(varsFile)

    if field != None:
        return vars[field]
    return vars

def setVar(name,value):

    vars = jsonFile.read(varsFile)
    vars[name]=value
    jsonFile.write(varsFile,vars)
    print(simplejson.dumps(vars, indent=4))

def getParam(argv,key,i=1,default=None):
    if key not in argv:
        if default != None:
            return default
        return None

    ind = argv.index(key)
    if (ind+i <= (len(argv)-1)):
        arg = argv[ind+i]
        if arg[0] == '-':
            return None
        return arg
    return None

def exists(args,key):
    return True if key in args else False

def isParam(argv,key):
    return True if key in argv else False

def listEnvs():
    cons = restClient.getConfigOrgs()
    cons = sorted(cons,key=itemgetter('name'))
    utils.printFormated(cons,fieldsString='name:isSandBox:instance_url:login.username:login.password:login.bearer')
    env = readVars('environment')
    print(f"Current Environment is {env}")

def _bestMatch(value,vlist):

    matches = []
    for v in vlist:
        s = SequenceMatcher(None, v, value)
      #  print(f"{v} {value} {s.ratio()}")
        if s.ratio() > 0.6:
            matches.append(v)
   # print(matches)
    return matches

def check_modifiers(command,args,modifiers,help=None):
    ars = [c for c in args if c.startswith('-')]
    ars.remove(command)
    if '-u' in ars: ars.remove('-u')
    if '-debug' in ars: ars.remove('-debug')

    for ar in ars:
        if ar not in modifiers:
            matches = _bestMatch(ar,modifiers)
            mstr = f" Did you mean {utils.CYELLOW}{' or '.join(matches)}{utils.CEND} ?" if len(matches)>0 else ''
            print(f"The modifier {utils.CYELLOW}{ar}{utils.CEND} is not valid for command {command}. {mstr}")
            print(f"Valid modifiers are {utils.CGREEN}{' '.join(modifiers)}{utils.CEND}")
            if help != None:
                print(help)
            return False
    return True

def _queryAndPrint(q,fields=None,systemFields=True,nullFields=False):

    res = query.queryRecords(q)
    if fields != None:
        res = utils.deleteNulls(res,systemFields,nullFields)
        if fields=='all':
            utils.printFormated(res)
        else:
            utils.printFormated(res,fields)
    else:
        res = utils.deleteNulls(res,systemFields,nullFields)
        print(simplejson.dumps(res, indent=4))
    
    print()
    print(f"Null values printed-> {nullFields}  systemFields printed--> {systemFields}")

def option_readme(args):
    if '-h' in args:
        return
    if '-hu' in args:
        return
    
    colorama.just_fix_windows_console()

    print(f"""
    {utils.CYELLOW}Significant updates:{utils.CEND}
     - Changes in version 0.0.61
       Added {utils.CYELLOW}incli -ipe{utils.CEND} to allow parsing the Integration Procedure Errors.

     - Changes in version 0.0.49
       Added {utils.CYELLOW}-auto{utils.CEND} to the log parsing. This options activates the debug logs automatically for the -loguser especified. If no -loguser is specified it will do it for the user used to authenticate with the org.  
            {utils.CGREEN}incli -logs -u orgAlias -tail -loguser username:onboarding@nosdti-parceiros.cs109.force.com -deletelogs -auto.{utils.CEND}
            This command will start listening for new logs for user onboarding@nosdti-parceiros.cs109.force.com in DTI and parsing them in real time. 
                -auto will activate the debug logs automatically, so the logs are collected without any configuration in Salesforce. 
                -delete will delete the logs from the server as they are parsed. A local copy for the 
            {utils.CGREEN}incli -logs -u orgAlias -tail -deletelogs -auto.{utils.CEND}
            This command will start listening for new logs for the user used to authenticate with the org. -auto and -deletelogs as usual.

            * Replace DTI by the correct alias for the org in your sfdx setup. 

    {utils.CYELLOW}Parsed output fields:{utils.CEND}

     - {utils.CGREEN}time entry{utils.CEND}: The entry time to the event, such as METHOD_ENTRY in the debug log. Helpful to search for the line in the debug log
     - {utils.CGREEN}time exit{utils.CEND}:  The exit time for the event, such as METHOD_EXIT in the debug log. Helpful to search for the line in the debug log
     - {utils.CGREEN}ts{utils.CEND}: an esier to read time entry. Time in miliseconds. 
     - {utils.CGREEN}CPU{utils.CEND}: The Salesforce CPU Time. 
            This field is set when there is a CPU time event in the debug log. This are generated by the system and we have no control when they occur. 
            The parser will also look for DEBUG lines containing the CPU time information. The debug line needs to have the following format: "*** getCpuTime() *** Measured: CPUTime"
                Adding this APEX line in the code will increase the accuracy of CPU Time: {utils.CGREEN}System.debug('*** getCpuTime() *** Measured: ' + Limits.getCpuTime());{utils.CEND}
     - {utils.CGREEN}cpuD{utils.CEND}: The CPU time delta from the previous time the CPU Time was parsed. 
     - {utils.CGREEN}Qt{utils.CEND}: Total queries performed executing the APEX program (user apex + managed pacakes apex). This field accurate. 
     - {utils.CGREEN}Q{utils.CEND}: Total queries performed by the user APEX program. This field is almost accurate. When it is not empty is accurate. {utils.CYELLOW}Requires Apex Profiling = Finest.
     - {utils.CGREEN}Qmp{utils.CEND}: Total queries performed by the managed package. We do not have control when they appear. Only when it is updated is accurate.
     - {utils.CGREEN}Qe{utils.CEND}: Estimate queries performed by the managed package. This is an estimate for the manage package queries. Almost accurate, accurate when Q is not empty.
     - {utils.CGREEN}type{utils.CEND}: Type of log event.
     - {utils.CGREEN}line{utils.CEND}: the line in the APEX program. 
     - {utils.CGREEN}wait{utils.CEND}: time elapsed from the previous event. Typically is the time consumed by the APEX program or managed package between events.  
                In some cases there are 2 values x-y. x is the time to the previous event, y is the time after the event. 
     - {utils.CGREEN}time{utils.CEND}: the time consumed executing the method. 
     - {utils.CGREEN}query{utils.CEND}: the total queries consumed bu the method. 
     - {utils.CGREEN}Call Stack{utils.CEND}:
            Some Call Stack string present a  "for: xRepetitions line_number". 
                - Repetitions: how many times the loop is repeated.
                - line_number: the position in the loop
                When there is a loop:
                    - The {utils.CGREEN}time{utils.CEND} field is the total time consumed by the method in the loop. 
                    - The {utils.CGREEN}wait{utils.CEND} field is the total wait time for the method in the loop. 
    
    Times are rounded to the closest milisecond. 
    - APEX Code = Fine is required to show the call stack with methods
    - APEX Profiling = Finest
    - Database = Info
    - Workflow = Info

    """)

def option_vte(args):
    help = f"""
        {utils.CYELLOW}-vte{utils.CEND}    Lists the latest Vlocity Tracking Entries.   {utils.CGREEN}incli -u orgAlias -vte {utils.CEND}
            {utils.CYELLOW}-limit number{utils.CEND} The number of records to display
        {utils.CYELLOW}-vte a6R7a000001k7t7EAA {utils.CEND} - Displays the JSON for the provided Id.
            {utils.CYELLOW}-fileOutput{utils.CEND} Saves the JSON to a file. """ 
    
    if '-hu' in args: 
        return help

    if '-h' in args: return

    if check_modifiers('-vte',args,["-fileOutput","-limit"],help) == False: return

    connectionInit(args)
    id = getParam(args,'-vte')
    tofile = True if '-fileOutput' in args else False
    limit = getParam(args,'-limit')

    if id != None:
        return VlocityTrackingEntry.query_and_print_error_record(id=id,tofile=tofile)
    limit = 100 if limit == None else limit
    VlocityTrackingEntry.print_error_list(limit=limit)
    
def option_ipa(args):
    help = f"""
        {utils.CYELLOW}-ipa{utils.CEND}    Lists the latest IP attachments.   {utils.CGREEN}incli -u orgAlias -ipa {utils.CEND}
            {utils.CYELLOW}-limit number{utils.CEND} The number of records to display

            {utils.CYELLOW}-around 2023-03-28T16:25:00{utils.CEND} Will display all the attachments around the datetime provided. 10 minutes before and after the datetime provided. 
            {utils.CYELLOW}-around 2023-03-28T16:25:00 -minutes 25 {utils.CEND} 25 minutes before and after the datetime provided. 

            {utils.CYELLOW}-from 2023-03-28T16:25:00 -to 2023-03-28T18:00:00{utils.CEND} Will display all the attachments between the datetimes provided (from-->to). 

            {utils.CYELLOW}-around 2023-03-28T16:25:00 -contains 8027T000005H16rQAC,"Movel 20GB",coyote23@gmail.com{utils.CEND} Will display all the attachments around the datetime provided containing any of the strings specified (comma separated). 
            {utils.CYELLOW}-from 2023-03-28T16:25:00 -to 2023-03-28T18:00:00 -contains 8027T000005H16rQAC,"Movel 20GB",coyote23@gmail.com{utils.CEND} Will display all the attachments around the datetime provided containing any of the strings specified. 

            -from","2023-03-09T09:19:31","-to","2023-03-11T13:55:00"
        {utils.CYELLOW}-ipa a2J7a000002UakuEAC {utils.CEND} - Displays the attachment for the provided Id.
            {utils.CYELLOW}-fileOutput{utils.CEND} Saves the attachment to a file. """ 
    
    if '-hu' in args: 
        return help
    if '-h' in args: return

    if check_modifiers('-ipa',args,["-fileOutput","-limit","-nf","-from","-to","-around","-minutes","-contains","-orderNumber","-owner"],help) == False: return

    connectionInit(args)
    ipa_id = getParam(args,'-ipa')
    toFile = True if '-fileOutput' in args else False
    limit = getParam(args,'-limit')
    mfrom = getParam(args,'-from')
    mto = getParam(args,'-to')
    maround = getParam(args,'-around')
    minutes = getParam(args,'-minutes')
    contains = getParam(args,'-contains')
    orderNumber = getParam(args,'-orderNumber')
    owner = getParam(args,'-owner')


    nf = True if '-nf' in args else False

    if ipa_id != None:
        return ip_attachments.print_attachments(Id=ipa_id,toFile=toFile)

    if mfrom == None and mto == None and maround==None:    
        limit = 100 if limit == None else limit

    if orderNumber != None:
        order = query.query(f"select fields(all) from order where OrderNumber='{orderNumber}' limit 1")
        account = query.query(f"select fields(all) from account where Id='{order['records'][0]['AccountId']}' limit 1")
        contains_lst = []
        contains_lst.append(order['records'][0]['Id'])
        contains_lst.append(account['records'][0]['vlocity_cmt__PrimaryContactId__c'])
        contains_lst.append(account['records'][0]['NOS_t_IdConta__c'])
        contains_lst.append(account['records'][0]['ID_Conta__c'])
        contains_lst.append(order['records'][0]['OwnerId'])

        contains_lst.append(account['records'][0]['Name'])
        contains = ','.join(contains_lst)

        maround = order['records'][0]['CreatedDate'].split('.')[0]
        print(maround)
        print(contains)

        minutes = 30
        limit = None

    if maround != None:
        if minutes != None: minutes = int(minutes)
        if minutes == None: minutes = 10
        mfrom,mto = utils.datetimestr_around(maround,minutes=minutes)        

    ip_attachments.print_attachments(limit=limit,only_not_finished=nf,date1=mfrom,date2=mto,contains=contains,ownerF=owner)

def option_ipe(args):
    help = f"""
        {utils.CYELLOW}-ipe{utils.CEND} displays the last 50 errors. 
            {utils.CYELLOW}-limit number{utils.CEND} The number of records to display
            {utils.CYELLOW}-last number{utils.CEND} Shows the error Json for the last number of records
            {utils.CYELLOW}-where {utils.CEND} Where clause

        {utils.CYELLOW}-ipe errorId{utils.CEND} Shows the error JSON for the provided Id
            {utils.CYELLOW}-fileOutput{utils.CEND} Saves the error to a file. """ 

    if '-hu' in args:
        return help

    if '-h' in args: return

    if check_modifiers('-ipe',args,["-fileOutput","-limit","-last","-where","-contains","-owner"],help) == False: return

    connectionInit(args)
    toFile = True if '-fileOutput' in args else False
    limit = getParam(args,'-limit')
    last = getParam(args,'-last')
    ipe_id = getParam(args,'-ipe')
    where = getParam(args,'-where')
    contains = getParam(args,'-contains')
    ownerF = getParam(args,'-owner')

    if ipe_id != None:
        return VlocityErrorLog.query_and_print_error_record(ipe_id,tofile=toFile)

    if last != None:
        return VlocityErrorLog.print_error_records(last)

    return VlocityErrorLog.print_error_list(where=where,limit=limit,contains=contains,ownerF=ownerF)

def option_q(args):
    help = f"""
        {utils.CYELLOW}-q "select..."{utils.CEND} query to execute. System Fields, such as LastModifiedDate, and null fields are not returned. 
            {utils.CYELLOW}-null{utils.CEND} - will print fields with null values
            {utils.CYELLOW}-system{utils.CEND} - will print the system fields
            {utils.CYELLOW}-all{utils.CEND} - will print both nulls and system fields
            {utils.CYELLOW}-fields "a:b:c:..."{utils.CEND} --> print in table format the specified fields.
            {utils.CYELLOW}-fields all{utils.CEND} --> print in table format"""
    
    if '-hu' in args:
        return help

    if '-h' in args: return

    if check_modifiers('-q',args,["-fields","-null","-system","-all"],help) == False: return

    q = getParam(args,'-q')

    fields = getParam(args,'-fields') if '-fields' in args else None    
    nullFields = True if '-null' in args else False
    systemFields = True if '-system' in args else False
    all = True if '-all' in args else False
    if all == True:
        nullFields = True
        systemFields = True

    connectionInit(args)

    _queryAndPrint(q,fields=fields,systemFields=systemFields,nullFields=nullFields)

def option_cc(args):
    colorama.just_fix_windows_console()
    help = f"""
        {utils.CYELLOW}-cc{utils.CEND}       {utils.CGREEN}incli -u orgAlias -cc {utils.CEND}
            Checks the catalogs. Gets all catalogs, does a getOffers, getOfferDetails. Performs basketwithoutconfig and basket with config, if -basket is set. 
            {utils.CYELLOW}-code{utils.CEND} - Catalogue Code. does it for a single catalog. 
            {utils.CYELLOW}-list{utils.CEND} - List all the catalogues. 
            {utils.CYELLOW}-basket{utils.CEND} - Performs basket operations. """ 
    if '-hu' in args:
        return help

    if '-h' in args: return

    if check_modifiers('-cc',args,["-code","-list","-basket","-account","-guest","-context"],help) == False: return

    connectionInit(args)

   # path = getParam(args,'-checkCatalogs')
   # quantity = getParam(args,'-checkCatalogs',2)
    catcatalogueCode = getParam(args,'-code')
    list = True if '-list' in args else False
    basketOps = True if '-basket' in args else False

    account = getParam(args,'-account')
    context = getParam(args,'-context')

    if list == True:
        digitalCommerceUtil.printCatalogs()
        return

    digitalCommerceUtil.checkOffers(catcatalogueCode=catcatalogueCode,account=account,basketOps=basketOps)

    print()

def option_d(args):
    help = f"""
        {utils.CYELLOW}-d objectName{utils.CEND} --> Describe an object
            {utils.CYELLOW}-d objectName:fieldName{utils.CEND} --> describe a field in the object"""
    if '-hu' in args:
        return help    

    if '-h' in args: return

    if check_modifiers('-d',args,[""],help) == False: return

    connectionInit(args)

    objectField = getParam(args,'-d')
    if objectField == None:
        print(help)
        return

    ofs = objectField.split(':')

    sObjectName = ofs[0]
    fieldName = ofs[1] if len(ofs) > 1 else None

    res = Sobjects.describe(sObjectName)
    if fieldName == None:
        print(simplejson.dumps(res['fields'], indent=4))
    else:
        sibbling = objectUtil.getSiblingWhere(res['fields'],'name',fieldName)['object']

        print(simplejson.dumps(sibbling, indent=4))

def option_l(args):
    help = f"""
        {utils.CYELLOW}-l{utils.CEND} --> current org limits consuptions. """
    if '-hu' in args:
        return help

    if '-h' in args: return
    
    if check_modifiers('-l',args,[""],help) == False: return

    connectionInit(args)
    action = '/services/data/v51.0/limits'
    res = restClient.callAPI(action)
    restClient.checkError()
    records = []
    for key in res.keys():
        record = {
            'Limit':key,
            'Max':res[key]['Max'],
            'Remaining':res[key]['Remaining'],
        }
        record['Percent Remaining'] =  100 *(res[key]['Remaining']/res[key]['Max']) if res[key]['Max']>0 else 0
        record['__color__'] = ''

        if record['Max'] != 0:
            if record['Percent Remaining']<50:
                record['__color__'] = utils.CYELLOW
            if record['Percent Remaining']<25:
                record['__color__'] = utils.CYELLOW
        records.append(record)

    utils.printFormated(records)

def option_o(args):
    help = f"""
        {utils.CYELLOW}-o{utils.CEND} --> List all Objects
            {utils.CYELLOW}-name objectName{utils.CEND}  --> get one row from the object
            {utils.CYELLOW}-name objectName:Id{utils.CEND} --> get the row especified by the Id
            {utils.CYELLOW}-like name{utils.CEND} --> where the Name contains the substring name"""
    if '-hu' in args:
        return help

    if '-h' in args: return
      
    if check_modifiers('-o',args,["-like","-count","-name","-limit"],help) == False: return

    connectionInit(args)

    if '-name' in args:
        obj = getParam(args,'-name')
        limit = getParam(args,'-limit') if '-limit' in args else None    
        l = limit if limit != None else 1
        chunks = obj.split(':')

        if len(chunks) == 1:
            q = f"select fields(all) from {chunks[0]} limit {l}"
        else:
            q = f"select fields(all) from {chunks[0]} where Id='{chunks[1]}'"

        print('pre q:'+q)
        _queryAndPrint(q,systemFields=True,nullFields=True)
        return
        
    like = getParam(args,'-like') if '-like' in args else None    
    count = True if '-count' in args else False   

    objs = Sobjects.listObjects()
    if like is not None:
        if ':' not in like:
            like = f"name:{like}"        
        ls = like.split(':')
        outs = []
        for obj in objs:
      #      print(f"{str(ls[1])} . {str(obj[ls[0]])}")
            if str(ls[1]).lower() in str(obj[ls[0]]).lower():
                outs.append(obj) 
    else:
        outs = objs

    if count==True:
        for out in outs:
            if out['queryable'] == True:
                print("Quering objects row count.")
                print("", end=".")          
                try:
                    c = query.query(f" select count(Id) from {out['name']}",raiseEx=True)
                    out['count'] = c['records'][0]['expr0']
                except Exception as e:
                    out['count'] = 'E'
            else:
                out['count'] = '-'
    
    #print(simplejson.dumps(objs, indent=4))
    utils.printFormated(outs,'name:label:associateParentEntity:associateParentEntity:queryable:count')

def xx_option_default(args):
    help = f"""
        {utils.CYELLOW}-default  {utils.CEND}  --> displays the current default values. 
        {utils.CYELLOW}-default:set key value{utils.CEND} --> defaults the specified key-value. When set as default, if the command does not include the parameter it will pick the default value
        {utils.CYELLOW}-default:del key  {utils.CEND}  --> deletes the default
            {utils.CYELLOW}Defaultable u{utils.CEND}: Can be set to a default value --> {utils.CGREEN}incli -default:set u collote@acme.com {utils.CEND} or {utils.CGREEN}incli -default:set u orgAlias {utils.CEND} 
            {utils.CYELLOW}Defaultable loguser{utils.CEND}: Can be set to default. {utils.CGREEN}incli -default:set loguser "Alias:TheCollote"{utils.CEND}"""

    if '-hu' in args: return

    if '-h' in args:
        return help   

    if "-default:del" in args:
        key = getParam(args,'-default:del',i=1)
        if key == None:
            restClient.glog().info(f'Key not found in the provided arguments. {args}')
            return 
        restClient.delConfigVar(key)
        return

    if "-default:set" in args: 
        key = getParam(args,'-default:set',i=1)
        if key == None:
            print(f"{utils.CLIGHT_PURPLE}Parameter to set not specified.{utils.CEND}")
            print(f"{utils.CYELLOW}-default:set key value {utils.CEND}" )
            return        
        value = getParam(args,'-default:set',i=2)
        if value == None:
            print(f"{utils.CLIGHT_PURPLE}Value to set not specified.{utils.CEND}")
            print(f"{utils.CYELLOW}-default:set key value {utils.CEND}" )
            return        
        if key == None or value==None:
            print(help)
            return

        restClient.setConfigVar(key,value)
        print(f"Default value for {key} is {utils.CYELLOW}{value}{utils.CEND}")

    if "-default" in args: 
        key = 'u' 
        value =restClient.getConfigVar(key)
        if value == None: value = 'Not set'
        print(f"Default value for {key} is {utils.CYELLOW}{value}{utils.CEND}")

        key = 'loguser' 
        value =restClient.getConfigVar(key)
        if value == None: value = 'Not set'
        print(f"Default value for {key} is {utils.CYELLOW}{value}{utils.CEND}")

        help = """
        -history"""
        return help

def option_logs(args):
    help = f"""
    LOG records
        {utils.CYELLOW}-logs{utils.CEND} --> lists log records in the org. Default 50 lines.  {utils.CGREEN}incli -u orgAlias -logs {utils.CEND} 
            {utils.CYELLOW}-auto{utils.CEND}, refreshes the view every couple of seconds.     {utils.CGREEN}incli -u orgAlias -logs -auto {utils.CEND}  
            {utils.CYELLOW}-limit X{utils.CEND}, where X specifies the number of logs to list. Default 50 max 50K {utils.CGREEN}incli -u orgAlias -logs -auto -limit 10{utils.CEND}
    
    LOG Parsing
        Common modifiers:
            {utils.CYELLOW}-debuglevel {utils.CEND} values {utils.CGREEN}XXS, XS, S, M, L{utils.CEND}. Logs file size.   
                    {utils.CGREEN}XXS{utils.CEND} --> ApexCode: debug   Database: info. displays basic information and it is fast. 
                    {utils.CGREEN}M (default){utils.CEND} adds the stack trace, is the default. 
                    {utils.CGREEN}L{utils.CEND} can help detecting if there is an exception in the manage package.
                         {utils.CYELLOW}-var{utils.CEND} outputs variable assigments
            {utils.CYELLOW}-allLimits{utils.CEND} displays all limits (SQOL rows...) as columns. 
            {utils.CYELLOW}-limitinfo {utils.CEND}--> prints out the log line when the limits (CPU, SOQL) are parsed as rows.    
            {utils.CYELLOW}-fileOutput {utils.CEND}--> creates 2 files for the parsed logs, txt and html format. 
            {utils.CYELLOW}-level {utils.CEND}--> outputs parsed lines up to the specified level. 

        {utils.CYELLOW}-logs {utils.CGREEN}Id{utils.CEND} --> parse the log with the provided Id. No modifiers. {utils.CGREEN}incli -u orgAlias -logs 07L0Q00000N5sMkUAJ"{utils.CEND}

        {utils.CYELLOW}-logs -inputfile {utils.CEND}--> parses the file provided in the inputfile. {utils.CGREEN}incli -logs -inputfile "path to file/xxxx.log"{utils.CEND} 

        {utils.CYELLOW}-logs -store {utils.CEND}--> parses the files saved locally in order of creation(download) {utils.CGREEN}incli -logs -store {utils.CEND} 
            {utils.CYELLOW}-error {utils.CEND}--> parses the files saved locally and displays only the ones with errors. {utils.CGREEN}incli -logs -store -error {utils.CEND} 

        {utils.CYELLOW}-logs -folder {utils.CGREEN}path {utils.CEND}--> parses the files saved locally in order of creation(download) {utils.CGREEN}incli -logs -folder /a/b/.../ {utils.CEND} 

        {utils.CYELLOW}-logs -last {utils.CGREEN}X {utils.CEND}--> parses the last X logs. X as number. {utils.CGREEN}incli -u orgAlias -logs -last 10{utils.CEND}. Parses the last 10 logs in the org.
            {utils.CYELLOW}-loguser {utils.CGREEN}field:value{utils.CEND}, filter the logs for the specified user. The user can be specified by any field in the User Object. 
                {utils.CGREEN}-loguser Id:0053O000000IHneQAG, -loguser "name:Onboarding Site Guest User", -loguser Alias:John.Doe, -loguser FirstName:Onboarding, -loguser ProfileId:00e3O000000IHneQAG{utils.CEND}
            {utils.CYELLOW}-where {utils.CGREEN}X {utils.CEND}--> the where clause for a query on the ApexLog object.  
                {utils.CGREEN}incli -logs -loguser Alias:John.Doe -where="Status<>'Success" -last 10" {utils.CEND} --> parses the last 10 logs for user John.Doe where the status is not Success

        {utils.CYELLOW}-logs -tail {utils.CEND}--> activelly parsers new debug logs as they are created.
            {utils.CYELLOW}-deletelogs {utils.CEND}--> as log files are processed, they are deleted from the server. The local copy remains. if -loguser is not provided it will default to your User.
            {utils.CYELLOW}-auto {utils.CEND}--> automaticallyu configures the collection of logs for -loguser. If no -loguser provided defaults to your user. 
            {utils.CYELLOW}-loguser {utils.CGREEN}field:value{utils.CEND}, filter the logs for the specified user. The user can be specified by any field in the User Object. 
                {utils.CGREEN}incli -u orgAlias -logs -tail -loguser username:user@acme.com -deletelogs -auto.{utils.CEND} This command will listen to the logs for the loguser specified and delete the logs from the org as they are parsed (local copy is kept)
 """
        
    if '-hu' in args: return

    if '-h' in args:
        return help

    if check_modifiers('-logs',args,["-last","-tail","-store","-deletelogs","-limit","-limitinfo","-auto","-folder","-level","-loguser","-where","-inputfile","-fileOutput","-error","-parseSmallFiles","-allLimits","-debuglevel","-var","-downloadOnly","-all","-fullsoql","-callstack","-search","-noMethod","-noMP","-filter"],help) == False: return

    #if logId == None and last== None and inputfile==None and tail == False and store==False and is_folder==False:

    parseContext = {
        'logId' :       getParam(args,'-logs') ,
        'filepath':     getParam(args,'-inputfile') ,
        'printLimits':  isParam(args,'-limitinfo') ,
        'lastN':        getParam(args,'-last')  ,
        'loguser':      getParam(args,'-loguser') ,
        'level':        getParam(args,'-level'),
        'callstack':    getParam(args,'-callstack'),
        'search':    getParam(args,'-search'),
        'whereClause':  getParam(args,'-where') ,
        'writeToFile':  exists(args,"-fileOutput") ,
        'tail':         exists(args,"-tail"),
        'deleteLogs':   exists(args,"-deletelogs"),
        'parseStore':   exists(args,"-store"),
        'print_only_errors':exists(args,"-error"),
        'operation':    None,
        'auto':         exists(args,"-auto"),
        'store_logId':  getParam(args,'-store') ,
        'search_dir':   getParam(args,'-folder')  ,
        "parseSmallFiles":     exists(args,"-parseSmallFiles"),
        "output_format":'STDOUT',
        "allLimits":    exists(args,"-allLimits"),
        'debug_level':  getParam(args,'-debuglevel') ,
        "var":          exists(args,"-var"),
        "var_limit":    getParam(args,'-var') ,
        "downloadOnly": exists(args,"-downloadOnly"),
        "all":          exists(args,"-all"),
        "full_soql":    exists(args,"-fullsoql"),
        "is_folder":    exists(args,"-folder"),
        "noMethod":     exists(args,"-noMethod"),
        "noMP":         exists(args,"-noMP"),
        "limit":        getParam(args,'-limit',default=50),
        'logToStore':   True,
        'processRepetition':True,
        "filter":    getParam(args,'-filter') 

       # 'full_soql':    False
    }

    pc = SimpleNamespace(**parseContext)

    if pc.debug_level == None: 
        pc.debug_level = 'M'
    else: 
        if pc.debug_level not in ['S','L','M','XS','XXS']: 
            print('debuglevel must be set to XXS, XS, S, M or L. Deafulting to M')
            pc.debug_level = 'M'

    if pc.var == True:
        if pc.var_limit == None: pc.var = -1
        else: pc.var = int(pc.var_limit)
    else:
        pc.var = None

    pp = pc.__dict__
    if all(parseContext[v] is None or parseContext[v] is False for v in ["logId", "lastN", "filepath", "tail", "parseStore", "is_folder"]):
        connectionInit(args)

        try:
            if pc.auto:
                while True:
                    debugLogs.printLogRecords(loguser=pc.loguser,limit=pc.limit,whereClause=pc.whereClause)
                    time.sleep(5)
            if not pc.auto:
                return debugLogs.printLogRecords(loguser=pc.loguser,limit=pc.limit,whereClause=pc.whereClause)
            
        except Exception as e:
            raise e

    if pc.tail:
        connection = connectionInit(args)
        pc.connection = connection
        return debugLogs.do_parse_tail(pc.__dict__)

    elif pc.parseStore:
        return debugLogs.do_parse_storage(pc.__dict__)

    elif pc.is_folder:
        return debugLogs.do_parse_storage(pc.__dict__,search_dir=pc.search_dir)

    elif pc.filepath != None:
        return debugLogs.do_parse_from_file(pc.__dict__)

    elif pc.logId != None:  #check if already downloaded        
        connectionInit(args)
        return debugLogs.do_parse_logId(pc.__dict__)

    else:
        connectionInit(args)
        return debugLogs.do_parse_logs_lastN(pc.__dict__)


def option_h(args,type="-h"):

    module = __import__('incli')

    funcs = getmembers(sys.modules[__name__], isfunction)
    functions = [func[0] for func in funcs if func[0].startswith('option_')]

    for f in functions:
        if f == 'option_h':      
            continue
        args = type
        p = eval(f'{f}(args)')
        if p != None: print(p)

    print()
    print()

def option_hu(args):
    if '-h' in args:
        help = f"""
        {utils.CYELLOW}-hu{utils.CEND} --> additional help for utilities. """
        return help    

    option_h(args,"-hu")

def connectionInit(argsIn):

    guest_url = getParam(argsIn,'-guest') 

    if guest_url!=None:
        return restClient.initWithToken('GUEST',url=guest_url)

    userName_or_ofgAlias = getParam(argsIn,'-u') 
    return restClient.init(userName_or_ofgAlias)

def checkVersion():
    try:
        from importlib import metadata
    except ImportError:
        import importlib_metadata as metadata

    fileversion = metadata.version("incli")

    try:
        restClient.init('ConnectionLess')
       # restClient.glog().info("Checking version")
        res = restClient.requestRaw(url='https://pypi.org/pypi/incli/json')
        if res == 'No Response':
            print("No connection.")
            return
        version = res['info']['version']

        if version != fileversion:
            print()
            print(f"Version {fileversion}. {colorama.Fore.WHITE+colorama.Back.RED}Version {version} is available --> pip install incli --upgrade{utils.CEND}")
        else:
            print()
            print(f"{utils.CFAINT}incli version {fileversion} {utils.CEND}")
    except Exception as e:
        print(e)

def _main(argsIn):

    if "-debug" in argsIn:    restClient.setLoggingLevel(level=logging.DEBUG)
    else:  restClient.setLoggingLevel(logging.INFO)

    restClient.glog().debug("In debug mode")
    checkVersion()
    
    colorama.just_fix_windows_console()

    if '-h' in argsIn:
#        {utils.CYELLOW}-readme{utils.CEND} --> new functionality added and some example. 
        help = f"""
        {utils.CYELLOW}-u{utils.CEND} --> username or org alias to be used to log into the org. Used in most commands. {utils.CGREEN}incli -u collote@acme.com ... {utils.CEND} or {utils.CGREEN}incli -u orgAlias... {utils.CEND} """
        print(help)

    funcs = getmembers(sys.modules[__name__], isfunction)
    functions = [func[0] for func in funcs if func[0].startswith('option_')]

    args = []
    for argv in argsIn:
        if argv == '|':     break
        args.append(argv)

    for arg in args:
        ar = arg.split(':')[0][1:]
        ar = f"option_{ar}"
        if ar in functions:
            res = None
            res = eval(f'{ar}(args)')
            if '-h' not in argsIn:
                return res

    if '-h' in argsIn:
        print()
        print(utils.CBOLD+"SFDX Commands:"+utils.CEND)
        print("incli connects to the orgs as authorized in SFDX. Some useful commands are:")
        print()
        print(f" - {utils.CYELLOW}sf org list --all --verbose {utils.CEND}--> to list all authorized Orgs and Connection Status")
        print(f" - {utils.CYELLOW}sf org login web -r 'Instance URL' -a 'Alias' {utils.CEND}--> to re-authorize")
        print()
        return

    commands = [f"-{fu.split('_')[1]}" for fu in functions]
    print("Command is not valid.")
    print(f"Valid commands are {utils.CGREEN}{' '.join(commands)}{utils.CEND}")
    print(f"Try {utils.CGREEN}incli -h{utils.CEND} or {utils.CGREEN}incli -hu{utils.CEND} for more information.")

def main():
    argsIn = sys.argv

    try:
        _main(argsIn)

    except KeyboardInterrupt as e:
        print()
        print("ate ja")
    except Exception as e:
        colorama.just_fix_windows_console()

        utils.printException(e)
       # print(traceback.format_exc())

        if "-debug" in sys.argv:
            print(traceback.format_exc())

    print()
if __name__ == '__main__':
    main()

