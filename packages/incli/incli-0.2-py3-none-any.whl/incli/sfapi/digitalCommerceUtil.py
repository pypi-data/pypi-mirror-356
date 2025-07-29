from . import restClient, objectUtil,digitalCommerce,utils,thread,query,CPQ
import time
import sys

def _getItemAtPath(obj,path,field='ProductCode'):
    for p in path.split(':'):
        obj = objectUtil.getSibling(obj,field,p)  
    return obj

def updateOfferField(offerDetails,path,field,value,pathField='ProductCode'):
    obj = _getItemAtPath(offerDetails,path,pathField)
    if obj == '':
        raise ValueError(f'Object does not contain element by path {path}')
    if field in obj:
        if 'dataType' in obj and obj['dataType'] == 'number':
            obj[field] = int(value)
        else:    
            obj[field] = value
    else:
        raise ValueError(f'Object does not contain field {field} by path {path}')

    return offerDetails

def updateOfferAttribute(offerDetails,path,AttributeCategory,productAttribute,value):
    obj = _getItemAtPath(offerDetails,path)
    obj = _getItemAtPath(obj,AttributeCategory,field='Code__c')
    obj = _getItemAtPath(obj,productAttribute,field='code')

    obj['userValues'] = value
 
    return offerDetails

def getBasketProductAttributes(basket,path):
    obj = _getItemAtPath(basket,path)
    obj = obj['attributeCategories']

    return obj

def getAction(basket,path,method='addChildBasketAction'):

  #  lpath = path.split(':')
  #  xpath = ":".join(lpath[:-1])
  #  offer = lpath[-1]

    obj,parents = get_ol(basket,path)

  #  obj = _getItemAtPath(basket,xpath)
    if obj == '' or obj == None:
        utils.raiseException('GET_ACTION_ERROR',f"PATH not found {path}.")
    action = _getItemAtPath(obj,method,field='method')

  #  action['params']['offer'] = offer
    action['link'] = f"/services/apexrest/{restClient.getNamespace()}{action['link']}"

    return action

def printCatalogs(catcatalogueCode=None):
    catalogs = digitalCommerce.getCatalogs(catcatalogueCode)
    print()
    print(f'Catalogs in the Org {utils.CGREEN+ restClient._currentConnectionName + utils.CEND}:')
    utils.printFormated(catalogs,"Name:vlocity_cmt__CatalogCode__c:vlocity_cmt__IsActive__c:vlocity_cmt__Description__c",rename="vlocity_cmt__IsActive__c%Active")
    print() 
    return catalogs

def checkOffers(path=None,quantity=None,catcatalogueCode=None,account=None,basketOps=False,context=None):

    if catcatalogueCode == None:
        catalogs = printCatalogs(catcatalogueCode)
    else:
        catalogs = [{
            'vlocity_cmt__CatalogCode__c':catcatalogueCode,
            'vlocity_cmt__IsActive__c':True
        }]

    catsOffers = []
    numOffersList = []
    print()

    print(utils.CLIGHT_CYAN+"GetOffers per catalog."+utils.CEND)
    getOfferTimes = []
    def getOffersPerCatalog(catalog):

        if catalog['vlocity_cmt__IsActive__c'] == False:
            return 
        try:
            times = {
                'name':catalog['vlocity_cmt__CatalogCode__c'],
                'Error':'',
                "__color__":utils.CEND
            }
            offers = digitalCommerce.getOfferByCatalogue(catalog['vlocity_cmt__CatalogCode__c'],pagesize=400)
            codes = []
            times['elapsed'] = restClient.getLastCallElapsedTime()
            l = len(offers) if offers is not None else 0
            numOffersList.append(l)
            times['# Offers'] = l

        except Exception as e:
            times['elapsed'] = restClient.getLastCallElapsedTime()
            times['Error'] = e.args[0]['error']
            times['__color__'] = utils.CRED
            getOfferTimes.append(times)
            return   

        if offers == None:
            times['Error'] = "Has no offers."
            times['__color__'] = utils.CYELLOW
            getOfferTimes.append(times)
            return 

        catOffers = {
            'catCode':catalog['vlocity_cmt__CatalogCode__c'],
         #   'catId':catalog['Id'],
            'offers':offers,
         #   'relationships':relationships
        }
        catsOffers.append(catOffers)

        if 1==2:
            relationships = query.queryRecords(f"""select vlocity_cmt__SequenceNumber__c,
                                                            vlocity_cmt__EffectiveDate__c,
                                                            Name,
                                                            Id,
                                                            vlocity_cmt__Product2Id__r.Name,
                                                            vlocity_cmt__Product2Id__r.vlocity_cmt__EffectiveDate__c,
                                                            vlocity_cmt__Product2Id__r.ProductCode,
                                                            vlocity_cmt__PromotionId__r.Name,
                                                            vlocity_cmt__PromotionId__r.vlocity_cmt__EffectiveStartDate__c,
                                                            vlocity_cmt__PromotionId__r.vlocity_cmt__Code__c,
                                                            vlocity_cmt__IsActive__c,
                                                            vlocity_cmt__ItemType__c,
                                                            IsDeleted 
                                                            from vlocity_cmt__CatalogProductRelationship__c 
                                                            where vlocity_cmt__CatalogId__c = '{catalog['Id']}' order by vlocity_cmt__SequenceNumber__c limit 200""")
            catOffers['relationships'] = relationship
            catOffers['catId'] = catalog['Id']


        getOfferTimes.append(times)

    thread.processList(getOffersPerCatalog,catalogs,1)
    utils.printFormated(getOfferTimes)
    totalOffers = sum(numOffersList)


    if 1==2:
        for catOffers in catsOffers:
            print()
            print()

            print(utils.CLIGHT_CYAN+ f"Product relationships and offers in the API for catalog {catOffers['catCode']} "+utils.CEND)
            objs = []
            for relationship in catOffers['relationships']:
                    obj = {
                        "seq":relationship['vlocity_cmt__SequenceNumber__c'],
                        "effDate":relationship['vlocity_cmt__EffectiveDate__c'],
                        "Name_Relationship":relationship['Name'],
                        "Id_Relationship":relationship['Id'],
                        "type":relationship['vlocity_cmt__ItemType__c'],
                        "Actv":relationship['vlocity_cmt__IsActive__c'],
                        "Name_prod":relationship['vlocity_cmt__Product2Id__r']['Name'] if relationship['vlocity_cmt__Product2Id__r']!=None else '',
                        "Name_promo":relationship['vlocity_cmt__PromotionId__r']['Name'] if relationship['vlocity_cmt__PromotionId__r']!=None else '',
                        "P_effDate":relationship['vlocity_cmt__Product2Id__r']['vlocity_cmt__EffectiveDate__c'] if relationship['vlocity_cmt__Product2Id__r']!=None else relationship['vlocity_cmt__PromotionId__r']['vlocity_cmt__EffectiveStartDate__c'] if relationship['vlocity_cmt__PromotionId__r']!=None else '',
                        "P_Code":relationship['vlocity_cmt__Product2Id__r']['ProductCode'] if relationship['vlocity_cmt__Product2Id__r']!=None else relationship['vlocity_cmt__PromotionId__r']['vlocity_cmt__Code__c'] if relationship['vlocity_cmt__PromotionId__r']!=None else ''
                    }
                    if 'T' in obj["P_effDate"]:
                        obj["P_effDate"] = obj["P_effDate"].split('T')[0]

                    if obj['type'] == 'Promotion':
                        offer = [ offer for offer in catOffers['offers'] if offer['offerType'] == 'Promotion' and offer['Name']==obj['Name_promo']]
                    if obj['type'] == 'Product':
                        offer = [ offer for offer in catOffers['offers'] if offer['offerType'] == 'Product' and offer['Name']==obj['Name_prod']]
                    if len(offer)>0:
                        obj['Offer Name'] = offer[0]['Name']
                        obj['Offer Code'] = offer[0]['vlocity_cmt__Code__c'] if obj['type'] == 'Promotion' else offer[0]['ProductCode']
                        obj['P_isActive'] = offer[0]['vlocity_cmt__IsActive__c'] if obj['type'] == 'Promotion' else offer[0]['IsActive']
                        obj['isOrderable'] = offer[0]['vlocity_cmt__IsOrderable__c']
                        obj['__color__'] = utils.CEND
                    else:
                        obj['NameP'] = 'No Offer'
                        obj['Code'] = ""
                        obj['PActv'] = ""
                        obj['isOrderable'] = ""     
                        obj['__color__'] = utils.CRED if obj['Actv'] == True else utils.CFAINT 

                    obj['Name_promo'] = f"Promo: {obj['Name_promo']}" if obj['Name_promo']!='' else f"Prod: {obj['Name_prod']}"

                    objs.append(obj)
            utils.printFormated(objs,exclude="Id_Relationship:type:Name_prod")

    print()
    print()

    if basketOps == True:
        print(utils.CLIGHT_CYAN+f"Getting offerDetails, createBasket, createBasket with config per offer. total offers {totalOffers}"+utils.CEND)
    else:        
        print(utils.CLIGHT_CYAN+f"Getting offerDetails. total offers {totalOffers}"+utils.CEND)


    offersList = []

    accountId = None

    if account != None:
        chunks = account.split(':')
        id = query.queryField(f" select Id from Account where {chunks[0]} = '{chunks[1]}'")
        if id==None:
            print(utils.CLIGHT_RED+ f"Cannot find an account where {chunks[0]} = '{chunks[1]}'"+utils.CEND)
        else:
            accountId=id

    for catOffers in catsOffers:
        for offerCount,offer in enumerate(catOffers['offers']):
            _offer = {
                'catalogCode':catOffers['catCode'],
                'offerCode':digitalCommerce.getOfferCode(offer),
                'basketOps':basketOps
            }
            if accountId != None:
                _offer['accountId']=id
            offersList.append(_offer)

    thread.processList(getOfferDetailsAndBaskets,offersList,50)
    newlist = sorted(_theTimes, key=lambda d: f"{d['catalog']}{d['offerCode']}")
    utils.printFormated(newlist)

    utils.printFormated(_errors)

   # for error in _errors:
   #     utils.printException(error)

    print()

_theTimes = []
_errors = []
_error_index = 0

#codes --> {'catalogCode': 'DC_CAT_WOO_FIXED_TV_MOBILE', 'offerCode': 'C_WOO_FIXED_TV_INTERNET_MOBILE', 'basketOps': True}
def getOfferDetailsAndBaskets(codes):
    global _error_index,_errors
    try:
        offerCode = codes['offerCode']
        catalogCode = codes['catalogCode']
        times = {
            'catalog':catalogCode,
            'offerCode':offerCode,
            'details':'',
            'createBasket':'',
            'afterConfig':'',
            '__color__':utils.CEND,
            "error":''
        }

        current_op = 'details'
        details = digitalCommerce.getOfferDetails(catalogCode,offerCode)
        times['details'] = restClient.getLastCallElapsedTime()
      #  times['detailsKey'] = details['contextKey'] +':'+details['result']['offerDetails']['offer']['Name']

        if codes['basketOps'] == True:
            current_op = 'createBasket'

            basket = digitalCommerce.createBasket(catalogCode,offerCode)
            times['createBasket'] = restClient.getLastCallElapsedTime()
            times['createBasketKey'] = basket['cartContextKey']

            if details['result']['offerDetails']['offer']['offerType'] == 'Promotion':
                try:
                    offerDetails = updateOfferField(details,'ATT_NOS_OTT_SUBSCRIPTION_ID','values',123456,'code')
                except Exception as e:
                    if e.args[0] == 'Object does not contain element by path ATT_NOS_OTT_SUBSCRIPTION_ID':
                        offerDetails = updateOfferField(details,'ATT_NOS_PRICE_CONDITIONS','values','PRICE_COND_003','code')
                    else:
                        raise
            else:
                offerDetails = updateOfferField(details,'0001','Quantity',4,'lineNumber')

            current_op = 'afterConfig'

            basket2 = digitalCommerce.createBasketAfterConfig(catalogCode,offerDetails)
            times['afterConfig'] = restClient.getLastCallElapsedTime()
            times['afterConfigKey'] = basket2['cartContextKey'] 
            if 'promotions' in basket2['result']['records'][0] and len(basket2['result']['records'][0]['promotions']['records'])>0:
                times['afterConfigKey'] = times['afterConfigKey'] + ' : ' + basket2['result']['records'][0]['promotions']['records'][0]['vlocity_cmt__Code__c']

        if 'accountId' in codes and 1==2:
            times['cart']=''
            current_op = 'cart'

            cart = digitalCommerce.createCart(codes['accountId'],catalogCode,basket2['cartContextKey'],createAsset=False)
            times['cart']=restClient.getLastCallElapsedTime()

            times['delete']=''
            current_op = 'delete'

            delete = CPQ.deleteCart(cart['orderId'])
            times['delete']=restClient.getLastCallElapsedTime()

            print()

    except Exception as e:
        if len(e.args)> 0  and 'error' in e.args[0]:

            error_in_list = [err for err in _errors if err['errorCode'] == e.args[0]['errorCode'] and err['error'] == e.args[0]['error']]

            if len(error_in_list) == 0:
                _error = {
                    'index': _error_index,
                    'errorCode': e.args[0]['errorCode'],
                    'error': e.args[0]['error']
                }
                _error_index = _error_index + 1
                _errors.append(_error)
            else:
                _error = error_in_list[0]

   #         times['error']=_error['errorCode']
            times[current_op] = f"Error-{_error['index']}" #e.args[0]['error']


        else:
            times['error']=f"{e}"


        times['__color__'] = utils.CLIGHT_RED

    _theTimes.append(times)

def get_ol(items,path,itemType=None):
    """Returns the object and the parents."""

    onlyOne=False

    siblings = objectUtil.getSiblingWhere_path(items,selectKey='ProductCode',selectKeyValuePath=path,whereKey='itemType',whereValue=itemType)

    if siblings == None: return None, None
    return siblings['object'],siblings['objects']
    print()

def get_basket_lines(basket):

    def get_value(item,field):
        if 'value' in item[field]:
            return item[field]['value']
        else:
            return item[field]
    def get_itemFields(item):
        fields = {}

        field_names = ['name','ProductCode','SpecificationType','Quantity','vlocity_cmt__Action__c','vlocity_cmt__EffectiveOneTimeTotal__c','vlocity_cmt__EffectiveRecurringTotal__c']

        for f_n in field_names:
            fields[f_n] = get_value(item,f_n)

        return fields
    
    def get_attributes(item):
        if 'attributeCategories' in item:
            attCats = {}
            for ac in item['attributeCategories']['records']:
              #  attCats[ac['Name']] = {}
                attCats[ac['Code__c']] = {}

                if 'productAttributes' in ac:
                    for pa in ac['productAttributes']['records']:
                       # attCats[ac['Name']][pa['label']] = pa['userValues']
                        attCats[ac['Code__c']][pa['code']] = pa['userValues']

            return attCats
        return None

    def parse_item(item,itemType):
        fields = None
        if itemType == 'lineItem':
            fields = get_itemFields(item)
            attrs = get_attributes(item)
            fields['Attributes'] = attrs
            print(fields)
        else:
            fields = {
                'name':item['name']
            }
        fields['itemType'] = item['itemType']

        itemTypes = ['lineItem','productGroup','childProduct']

        for _itemType in itemTypes:
            _itemTypes = f"{_itemType}s"
            if _itemTypes in item:
                if 'children' not in fields: fields['children'] = []
                for record in item[_itemTypes]['records']:
                    child = parse_item(record,_itemType)       
                    if 'ProductCode' in child or 'children' in child: 
                        fields['children'].append(child)      

        return fields
    
    if 'result' in basket:
        basket = basket['result']
    
    for record in basket['records']:
        pp = parse_item(record,'lineItem')

        print(pp)


def parse_basket(basket):
    def get_value(item,field):
        if field not in item:
            return None
        if type(item[field]) is dict:
       # if 'value' in item[field]:
            return item[field]['value']
        else:
            return item[field]
    def parse_item(item,itemType,parsed):
        fields = get_itemFields(item)

        fields['itemType'] = item['itemType']
      #  print(fields)
        parsed.append(fields)
        fields['childItems'] = 0

        itemTypes = ['lineItem','productGroup','childProduct']

        for _itemType in itemTypes:
            _itemTypes = f"{_itemType}s"
            if _itemTypes in item:
                for record in item[_itemTypes]['records']:
                    child = parse_item(record,_itemType,parsed)     
                    if child['itemType']  == 'lineItem':
                        fields['childItems'] = fields['childItems'] +1 
          #          if 'ProductCode' in child or 'children' in child: 
          #              fields['children'].append(child)      

        return fields

    def get_itemFields(item):
        fields = {}

        field_names = ['name','ProductCode','SpecificationType','Quantity','vlocity_cmt__Action__c','minQuantity','maxQuantity','groupMinQuantity','groupMaxQuantity']

        for f_n in field_names:
            fields[f_n] = get_value(item,f_n)

        return fields
    
    if 'result' in basket:
        basket = basket['result']

    for record in basket['records']:
        parsed =[]
        pp = parse_item(record,'lineItem',parsed)

        for p in parsed:
            p['x'] = ''
            if p['Quantity'] != None:
                if p['Quantity'] < p['minQuantity']:
                    p['x'] = 'Add'
                if p['Quantity'] > p['maxQuantity']:
                    p['x'] = 'Sub'    
            if p['childItems'] < p['groupMinQuantity']:
                p['x'] = 'Add_Child'   
            if p['childItems'] > p['groupMaxQuantity']:
                p['x'] = 'Sub_Child'                 

        utils.printFormated(parsed,rename='vlocity_cmt__Action__c%Action:SpecificationType%spec')

      #  print(pp)