import unittest,hashlib,simplejson
from datetime import datetime
#from InCli import InCli
from incli.sfapi import tooling,restClient,Sobjects,query,jsonFile

class Meta:
    def __init__(self, objName,where,related):
        self.objName = objName
        self.where = where
        self.objectDef = Sobjects.describe(objName)
        self.fields = []
        self.references = []
        self.referencesIndirect = []
        self.fields_def = {}
        self.matchingKeysDefinitions = query.query("select Id,QualifiedApiName,vlocity_cmt__MatchingKeyFields__c,vlocity_cmt__MatchingKeyObject__c,vlocity_cmt__ReturnKeyField__c from vlocity_cmt__drmatchingkey__mdt ")['records']
        self.files = {}
        self.recordTypes = query.query('select Id,Name,DeveloperName, NamespacePrefix, SobjectType  from RecordType ')['records']

        self.related = related
        self.related_objects = [r['object'] for r in self.related if 'file' in r]
        self.related_allobjects = [r['object'] for r in self.related]

        print(self.objName + '-----------------------------------------------------------------')
        for fieldDef in self.objectDef['fields']:
            if fieldDef['name'] in  ['vlocity_cmt__AttributeName__c','vlocity_cmt__AttributeId__c']:
                a=1
            if fieldDef['calculated'] == True:
                print(f"{fieldDef['name']} ->calculated")
                continue
            if fieldDef['name'] in ['CreatedById','CreatedDate','LastModifiedById','LastModifiedDate','LastReferencedDate','LastViewedDate','OwnerId','IsDeleted','SystemModstamp']:
                continue
            print(f"{fieldDef['name']}  {fieldDef['type']}")

            self.fields.append(fieldDef['name']) 
            self.fields_def[fieldDef['name']] = fieldDef
            if fieldDef['type'] == 'reference':
                self.references.append(fieldDef['name'])      
            else:
                if fieldDef['name'].endswith('Id__c'):
                    self.referencesIndirect.append(fieldDef['name'])  

        all_fields_str = ','.join(self.fields)

        if len(self.references)>0:
            for ref in self.references:
                if ref == 'RecordTypeId': continue

                if ref=='vlocity_cmt__PromotionItemId__c':
                    a=1
                matchingFields = self.get_matchingFields(fieldname=ref)
                for matchingField in matchingFields:
                    all_fields_str = all_fields_str + ',' + matchingField

        self.q = f"select {all_fields_str} from {objName}"# where Id = '{Id}'"

        res = query.query(self.q + self.where)
        self.records = res['records']

        if len(self.referencesIndirect)>0:
            for referenceIndirect in self.referencesIndirect:
                matchingFields = self.get_matchingFields(referenceIndirect)
                values = []
                for r in self.records:
                    if r[referenceIndirect] not in values:
                        values.append(r[referenceIndirect])
                if referenceIndirect == 'vlocity_cmt__PriceBookEntryId__c':
                    objectname = 'PricebookEntry'
                if referenceIndirect == 'vlocity_cmt__ObjectId__c':
                    objectname = 'Product2'  #$$$$$$
                if referenceIndirect in ['vlocity_cmt__DefaultPicklistEntryId__c','vlocity_cmt__ImageId__c']:
                    continue
                fls = ['Id']
                desc = Sobjects.describe(objectname)
                validFields = [r['name'] for r in desc['fields']]

                for matchingField in matchingFields:
                    _, fl = matchingField.split('.', 1)
                    if fl.find('.')>0 or fl in validFields:
                        fls.append(fl)
                rr = query.query(f"select {','.join(fls)} from {objectname} where Id in ({query.IN_clause(values)})")
                for record in self.records:
                    value = record[referenceIndirect]
                    rri = [r for r in rr['records'] if r['Id']==value][0]
                    rri['attributes'] = {'type':objectname}
                    record[self.r(referenceIndirect)] = rri
                    a=1
            a=1


    def sortList(self, theList):
        # Split the list into two, sorting each directly
        sorted_vls = sorted(item for item in theList if 'vlocity_cmt' in item)
        sorted_rest = sorted(item for item in theList if 'vlocity_cmt' not in item)
        return sorted_vls + sorted_rest
    
    def ns(self,val):
        return val.replace('vlocity_cmt','%vlocity_namespace%')
    def r(self,val):
        return val.replace('__c','__r')
    def get_matchingFields(self,fieldname,objectname=None):
        print(fieldname)
        if objectname==None:
            field_def = [f for f in self.objectDef['fields'] if f['name'] == fieldname ][0]
            if len(field_def['referenceTo'])==1:
                objectname = field_def['referenceTo'][0]
            else:
                if fieldname == 'vlocity_cmt__PriceBookEntryId__c':
                    objectname = 'PricebookEntry'
                if fieldname == 'vlocity_cmt__ObjectId__c':
                    objectname = self.objName
                else:
                    print('Waht is this')

        mFields = []
        if objectname == None:
            return mFields
        matchingRecord = [r for r in self.matchingKeysDefinitions if r['vlocity_cmt__MatchingKeyObject__c'] == objectname]
        if len(matchingRecord) == 0:
            matchingRecord = [r for r in self.matchingKeysDefinitions if r['vlocity_cmt__MatchingKeyObject__c'] == self.ns(objectname)]

        if len(matchingRecord) == 0:
            return mFields

        fieldname_r = fieldname.replace('__c','__r')

        matchingFields = matchingRecord[0]['vlocity_cmt__MatchingKeyFields__c'].replace('%vlocity_namespace%','vlocity_cmt')
        for matchingField in matchingFields.split(','):
            print(matchingField)
            if matchingField.endswith('Id__c'):  #If matching key is an Id, then we need to get the global key
                matchingFields = self.get_matchingFields(matchingField)
                for match in matchingFields:
                    mFields.append(  f"{fieldname_r}.{match}")
                continue
                #matchingField = matchingField.replace('__c','__r')
                #matchingField = matchingField + '.vlocity_cmt__GlobalKey__c'
            else: 
                if matchingField.endswith('Id'):  #If matching key is an Id, then we need to get the global key
                    objectname2 = matchingField.replace('Id','')
                    matchingFields = self.get_matchingFields(objectname2,objectname=objectname2)
                    for match in matchingFields:
                        mFields.append(  f"{fieldname_r}.{match}")
                    continue
                    #matchingField = matchingField.replace('Id','')
                    #matchingField = matchingField + '.vlocity_cmt__GlobalKey__c'
            mFields.append(  f"{fieldname_r}.{matchingField}")

        print(f"{fieldname}        {mFields}")
        return sorted(mFields)

class Test_VBT_like2(unittest.TestCase):
    def sortList(self, theList):
        # Split the list into two, sorting each directly
        sorted_vls = sorted(item for item in theList if 'vlocity_cmt' in item)
        sorted_rest = sorted(item for item in theList if 'vlocity_cmt' not in item)

        # Return the concatenated sorted lists
        return sorted_vls + sorted_rest

    def getValue(self, val, f_def):
        if val is None:
            return ""

        if f_def['type'] == 'datetime':
            dt = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f%z')
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        if f_def['soapType'] == 'xsd:double':
            return int(val) if val == int(val) else val
        
        if f_def['name'] == 'vlocity_cmt__AttributeDefaultValues__c':
            my_dict = simplejson.loads(val)
            sorted_keys = sorted(my_dict.keys())
            sorted_dict = {key: my_dict[key] for key in sorted_keys}

            return sorted_dict

        def sort_dict_keys(obj):
            if isinstance(obj, dict):
                # Sort the dictionary keys alphabetically
                sorted_obj = {k: sort_dict_keys(v) for k, v in sorted(obj.items())}
                return sorted_obj
            elif isinstance(obj, list):
                # If the object is a list, recursively sort any dictionaries within the list
                return [sort_dict_keys(item) for item in obj]
            else:
                # If it's not a dict or list, return it as is (base case)
                return obj
        if f_def['name'] == 'vlocity_cmt__AttributeMetadata__c':
            return sort_dict_keys(simplejson.loads(val))
        
        if f_def['name'] == 'vlocity_cmt__ValidValuesData__c':
            return sort_dict_keys(simplejson.loads(val))
        
        return val

    def serialize_record(self,m,objectRecord):
        def ns(val):
            return val.replace('vlocity_cmt','%vlocity_namespace%')
        
        def get_matchingFields(fieldname,objectDef):
            field_def = [f for f in objectDef['fields'] if f['name'] == fieldname ][0]

            mFields = []
            if len(field_def['referenceTo'])==1:
                referenceTo = field_def['referenceTo'][0]
                referenceTo_ns = referenceTo.replace('vlocity_cmt','%vlocity_namespace%')

                matchingRecord = [r for r in self.matchingKeysDefinitions if r['vlocity_cmt__MatchingKeyObject__c'] == referenceTo]
                if len(matchingRecord) == 0:
                    matchingRecord = [r for r in self.matchingKeysDefinitions if r['vlocity_cmt__MatchingKeyObject__c'] == referenceTo_ns]

                if len(matchingRecord) == 0:
                    return mFields

                fieldname_r = fieldname.replace('__c','__r')

                matchingFields = matchingRecord[0]['vlocity_cmt__MatchingKeyFields__c'].replace('%vlocity_namespace%','vlocity_cmt')
                for matchingField in matchingFields.split(','):
                    print(matchingField)
                    if matchingField.endswith('Id__c'):
                        matchingField = matchingField.replace('__c','__r')
                        matchingField = matchingField + '.vlocity_cmt__GlobalKey__c'
                    mFields.append(  f"{fieldname_r}.{matchingField}")
            else:
                print('Waht is this')
            
            print(f"{fieldname}        {mFields}")
            return mFields
        

        output = {}


        if m.objName not in m.related_objects:
            for item in m.related_objects:
                m.fields.append(item)

        sorted_fields = self.sortList(m.fields)
        VlocityRecordSObjectType = ''
        for fieldName in sorted_fields:
            if fieldName in ['Id'] : continue
            print(fieldName)
            field_ns = fieldName.replace('vlocity_cmt','%vlocity_namespace%')

            if fieldName != m.objName and fieldName in m.related_objects:
                related_object_cfg = [r for r in m.related if r['object'] == fieldName][0]
                related_object_def = Sobjects.describe(related_object_cfg['object'])
                q_field =None
                if 'whereField' in related_object_cfg:
                    q_field = related_object_cfg['whereField']
                else:
                    for rel_field in related_object_def['fields']:
                        for ref2 in rel_field['referenceTo']:
                            if ref2 == m.objName:
                                q_field = rel_field['name']
                where = f" where {q_field} = '{objectRecord['Id']}'"
                m_rel = Meta(related_object_cfg['object'],where=where,related=m.related)

                if (len(m_rel.records)>0):
                    all_outputs = []
                    if fieldName == 'vlocity_cmt__PromotionItem__c':
                        m_rel.records = sorted(m_rel.records, key=lambda recx: str(recx['vlocity_cmt__GlobalGroupKey__c'])) 
                    for record in m_rel.records:
                        all_outputs.append( self.serialize_record(m_rel,record) )
                    output[ns(related_object_cfg['object'])] = related_object_cfg['file'].replace('xxxx',objectRecord[related_object_cfg['xxxx']]).replace(' ','-')
                    m.files[output[ns(related_object_cfg['object'])]] = all_outputs

                  #  aaa = jsonFile.write(output[ns(related_object_cfg['object'])],all_outputs)
                continue

            field_def = m.fields_def[fieldName]

            VlocityRecordSObjectType = m.objName
            if fieldName == 'RecordTypeId':
                #recType = [r for r in m.objectDef['recordTypeInfos'] if r['recordTypeId'] == objectRecord['RecordTypeId']][0]
                # entitydef = [r for r in self.EntityDefinitions['records'] if recType['developerName'] == r['DeveloperName']][0]
                # VlocityRecordSObjectType = entitydef['QualifiedApiName']

                recType = [r for r in m.recordTypes  if r['Id'] == objectRecord['RecordTypeId']][0]
                a=1
                locityRecordSObjectType = recType['SobjectType']
                RecordTypeId = {
                    "DeveloperName": recType['DeveloperName'],
                    "SobjectType": ns(recType['SobjectType']),
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"RecordType/{ns(recType['SobjectType'])}/{recType['DeveloperName']}",
                    "VlocityRecordSObjectType": "RecordType"
                }
                output['RecordTypeId'] = RecordTypeId

                continue

            if fieldName.endswith('Id__c'):
                if fieldName in m.referencesIndirect:
                    matchFields = m.get_matchingFields(fieldname=fieldName)
                    a=1
                if objectRecord[fieldName] == None:
                    output[field_ns] = ""
                else:
                    fieldName_r = fieldName.replace('__c','__r')
                    tt = {
                    }
                    objectType = objectRecord[fieldName_r]['attributes']['type']
                    objectType_ns = objectType.replace('vlocity_cmt','%vlocity_namespace%')

                   # for key in objectRecord[fieldName_r]:
                    matchFields = self.sortList( m.get_matchingFields(fieldname=fieldName))
                    for matchfield in  matchFields:
                        try:
                            ombject_r,mfield = matchfield.split('.',1)
                            if '.' in mfield:
                                a1,a2 = mfield.split('.')
                                tt[ns(mfield)] = self.getValue(objectRecord[ombject_r][a1][a2],field_def)
                            else:
                                tt[ns(mfield)] = self.getValue(objectRecord[ombject_r][mfield],field_def)
                        except Exception as e:
                            print(e)

                    vlocityXsourcekey = 'VlocityRecordSourceKey'
                    vlocityXsourcekey_field = 'VlocityLookupRecordSourceKey'
                    vlocityDataPackType = 'VlocityLookupMatchingKeyObject'

                    field_obj = fieldName.replace('Id','')
                    if (field_obj in m.related_allobjects):
                        vlocityXsourcekey = 'VlocityMatchingRecordSourceKey'
                        vlocityXsourcekey_field = 'VlocityMatchingRecordSourceKey'
                        vlocityDataPackType = 'VlocityMatchingKeyObject'

                    tt["VlocityDataPackType"] = vlocityDataPackType

                    if fieldName in m.referencesIndirect:
                        tt[vlocityXsourcekey_field] = f"{vlocityXsourcekey}:{objectRecord[ombject_r]['Id']}"
                    else:
                        val = tt[ns(mfield)]
                        if len(matchFields) > 1:
                            val = "GeneratedXXXX"

                        tt[vlocityXsourcekey_field] = f"{objectType_ns}/{val}"

                    tt["VlocityRecordSObjectType"] = objectType_ns

                    output[field_ns] = tt
                continue

            output[field_ns] = self.getValue(objectRecord[fieldName],field_def)

        output["VlocityDataPackType"]= "SObject"
        output["VlocityRecordSObjectType"]= ns(VlocityRecordSObjectType)
        output["VlocityRecordSourceKey"]= f'{output["VlocityRecordSObjectType"]}/{output["%vlocity_namespace%__GlobalKey__c"]}'

        return output

    def test_describe(self):

        restClient.init('mpomigra250')

        self.prefix_dic = {}
        self.EntityDefinitions = query.query("SELECT DurableId, QualifiedApiName, KeyPrefix,DeveloperName FROM EntityDefinition where QualifiedApiName like 'vlocity_cmt__%' limit 2000")

        for rec in self.EntityDefinitions['records']:
            self.prefix_dic[rec['KeyPrefix']] = rec


        self.matchingKeysDefinitions = query.query("select Id,QualifiedApiName,vlocity_cmt__MatchingKeyFields__c,vlocity_cmt__MatchingKeyObject__c,vlocity_cmt__ReturnKeyField__c from vlocity_cmt__drmatchingkey__mdt ")['records']

        #select fields(all) from vlocity_cmt__DRMapItem__c where Name = 'Promotion Migration' AND vlocity_cmt__IsDisabled__c  = false ORDER BY vlocity_cmt__DomainObjectCreationOrder__c  limit 200
        related = {
            'vlocity_cmt__Promotion__c':[
                {
                    'object':'vlocity_cmt__Promotion__c'
                },
                {
                    'object':'vlocity_cmt__PriceListEntry__c',
                    'file':'xxxx_PriceListEntries.json',
                    'xxxx':'vlocity_cmt__Code__c'
                },
                {
                    'object':'vlocity_cmt__PromotionItem__c',
                    'file':'xxxx_PromotionItems.json',
                    'xxxx':'vlocity_cmt__Code__c'
                }
            ],
            'Product2':[
                {
                    'object':'Product2'
                },                
                {
                    'object':'vlocity_cmt__ProductChildItem__c',
                    'file':'xxxx_ProductChildItems.json',
                    'xxxx':'ProductCode'
                },
                {
                    'object':'vlocity_cmt__AttributeAssignment__c',
                    'file':'xxxx_AttributeAssignments.json',
                    'xxxx':'ProductCode',
                    'whereField':'vlocity_cmt__ObjectId__c'
                }
            ]
        }

        if 1==2:
            objName = 'vlocity_cmt__Promotion__c'
            code = 'PROMO_NOS_PREMIUM_TV_001' 
            code = 'PROMO_NOS_INST_001'
            directory = 'TEST5'

            Id = query.query(f"select Id from vlocity_cmt__Promotion__c where vlocity_cmt__Code__c = '{code}'")['records'][0]['Id']

        if 1==1:
            objName = 'Product2'
            code = 'T_BSCS_RFS_NOS_BILLING_DISC_4460'
            directory = 'TEST_Prod1'

            Id = query.query(f"select Id from product2 where ProductCode = '{code}'")['records'][0]['Id']

        m = Meta(objName,where=f" where Id = '{Id}' " , related= related[objName])

        res = query.query(m.q + f" where Id = '{Id}' ")

        output = self.serialize_record(m,m.records[0])

      #  output = self.serialize_object(objName,promoId)


        dir = f'{directory}/{objName}/{output["%vlocity_namespace%__GlobalKey__c"]}'

        aaa = jsonFile.write(f'{dir}/{code}_DataPack.json',output)
        for file in m.files:
            aaa = jsonFile.write(f'{dir}/{file}',m.files[file])


        print(output)
        a=1

    def test_getAttachment(self):
        restClient.init('DTI')

       # res = Sobjects.get_attachment('00P0Q00000MPx20UAD')

        res = Sobjects.get_attachment_Id('m090Q00000006neQAA')

        a=1


#Exception while parsing for logI 07LAU00000Ad9EA2AZ 
