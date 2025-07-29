from . import restClient,CPQ,account,timeStats,objectUtil,utils
import copy

def create_cart_with_promotion(cartName,accountName,pricelistName,promoName,ts:timeStats=None):
    cartId = CPQ.getCartId(f"name:{cartName}")
    if cartId != None:
        CPQ.deleteCart(cartId)

    accountId = account.createAccount_Id(f'Name:{accountName}',recordTypeName='Consumer')
    cartId = CPQ.createCart(accountF= accountId, pricelistF=f'Name:{pricelistName}',name=cartName,checkExists=True)
    if ts!=None: ts.time('createCart')

    promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)

    res = CPQ.postCartsPromoItems_api(cartId,promo['Id'])
    print(restClient.getLastCallElapsedTime())

    all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c',price=False,validate=False,includeAttachment=False)
    print(restClient.getLastCallElapsedTime())

def cartItems_getObjAndParent(cartItems,pcPath,itemType='childProduct'):
    obj,parents = get_ol(cartItems,pcPath,itemType) #item type is not set... not sure why
    if obj == None: utils.raiseException('Item not found',f"{itemType} with product code {pcPath} cannot be found")

    cartItem = obj
    position = len(parents) - 2
    parentRecord = parents[position]

    return cartItem,parentRecord

def post_cart_item(cartId,cartItems,pcPath,itemType='childProduct',path=None,noResponseNeeded=False,price=False,validate=False):
    cloned_items = copy.deepcopy(cartItems)

  #  obj,parents = get_ol(cloned_items,productCode)
  #  if obj == None: utils.raiseException('Item not found',f"{itemType} with product code {productCode} cannot be found")

  #  item = obj
  #  position = len(parents) - 2
  #  parentRecord = parents[position]

    item,parentRecord = cartItems_getObjAndParent(cloned_items,pcPath,itemType)

    #if path == None: path = productCode

    priceBookEntryId = item['Id']['value']
    #parentId = parentRecord['parentLineItemId'] if parentRecord.get('parentLineItemId') != None  else parentRecord['Id']['value']
    #parentHierarchyPath = parentRecord['productHierarchyPath']

   # call = CPQ.addItemstoCart_api(cartId,priceBookEntryId,parentRecord=parentRecord,parentId=parentId,parentHierarchyPath=parentHierarchyPath,noResponseNeeded=noResponseNeeded,price=price,validate=validate)
    call = CPQ.addItemstoCart_api(cartId,priceBookEntryId,parentRecord=parentRecord,noResponseNeeded=noResponseNeeded,price=price,validate=validate)

    return call

def update_field(cartId,items,productCode,updateDic=None,attributesDic=None,price=False,validate=False):
    item,parents = get_ol(items,productCode)
    if item == None: utils.raiseException('Item not found',f"With product code {productCode} cannot be found")

    obj = {}
    obj['vlocity_cmt__LineNumber__c'] = item['vlocity_cmt__LineNumber__c']
    obj['vlocity_cmt__RootItemId__c'] = item['vlocity_cmt__RootItemId__c']
    obj['vlocity_cmt__Action__c'] = item['vlocity_cmt__Action__c']
    obj['vlocity_cmt__AssetReferenceId__c'] = item['vlocity_cmt__AssetReferenceId__c']
    obj['Id'] = item['Id']

    if updateDic != None:
        obj.update(updateDic)
        
    if attributesDic != None:
        obj['attributeCategories'] = item['attributeCategories']
        for key in attributesDic.keys():
            sp = key.split(':')
            att = objectUtil.getSibling(obj,sp[0],sp[1])
            att['userValues']=attributesDic[key]

    items = {"records":[obj]}
    call = CPQ.updateCartItem_api(cartId,items,price=price,validate=validate)
    return call

def delete_cart_item(cartId,items,productCode,price=False,validate=False):
    obj,parents = get_ol(items,productCode,itemType='lineItem')
    if obj == None: utils.raiseException('Item not found',f" with product code {productCode} cannot be found")

    item = obj
    itemIds = item['Id']['value']

    if len(parents) > 2:
        position = len(parents) - 2
        parentRecord = parents[position]

        parentRecord2 = {}
        parentRecord2['Id'] = parentRecord['Id']['value']
        parentRecord2['productId'] = parentRecord['productId']
        parentRecord2['productHierarchyPath'] = parentRecord['productHierarchyPath']
        parentRecord2['itemType'] = parentRecord['itemType']
        parentRecord2['parentLineItemId'] = parentRecord['parentLineItemId'] if 'parentLineItemId' in parentRecord else parentRecord['Id']['value']

    else:
        parentRecord2 = None # is a root item

    call = CPQ.deleteCartItems_api(cartId,itemIds=[itemIds],parentRecord=parentRecord2,price=price,validate=validate) 

    return call

def create_cart_with_offer(accountname,cartName,offerName,create=False,pricelistF='Name:B2C Price List',price=False,validate=False,timeStats=None):

    cartId = CPQ.getCartId(f"name:{cartName}")
    if cartId != None:
        if create == True:
            CPQ.deleteCart(cartId)

 #   accountF = f'Name:{accountname}'
 #   accountId = account.create_Id(accountname,recordTypeName='Consumer')
    accountId = account.create_Id(accountname)

    inputFields = {
        'NOS_t_CoverageTechnology__c':'FTTH'
    }

    inputFields = None
    cartId = CPQ.createCart(accountF= accountId, pricelistF=pricelistF,name=cartName,checkExists=True,inputFields=inputFields)
    if timeStats != None:  timeStats.time('createCart')

    return add_offer_to_cart(cartId,offerName,pricelistF,price,validate)

def add_offer_to_cart(cartId,offerName,pricelistF='Name:B2C Price List',price=False,validate=False,timeStats=None):
    offer = CPQ.getCartProducts(cartId,query=offerName,onlyOne=True)
    if timeStats != None:  
        timeStats.field('product',offerName)
        timeStats.time('getCartProducts')

    items = CPQ.addItemstoCart(cartId,productCode=offer['ProductCode']['value'],pricelistF=pricelistF,price=price,validate=validate)

    counters = cart_stats(items)
    if timeStats != None:  timeStats.time('addItemstoCart',extend_obj=counters)

    return cartId,items

def create_cart_with_promo(accountname,cartName,promoName,create=False,pricelistF='Name:B2C Price List',price=False,validate=False,timeStats=None,inputFields=None):

    cartId = CPQ.getCartId(f"name:{cartName}")
    if cartId != None:
        if create == True:
            CPQ.deleteCart(cartId)

    accountId = account.create_Id(accountname,recordTypeName='Consumer')
    cartId = CPQ.createCart(accountF= accountId, pricelistF=pricelistF,name=cartName,checkExists=True,inputFields=inputFields)
    if timeStats != None:  timeStats.time('createCart')

    promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)
    if timeStats != None:  timeStats.time('getCartPromotions')

    if promo == None:
        utils.raiseException('NO_PROMO',f"promo with name {promoName} cannot be found.")

    print(f'Adding promo to cart {promoName}')
    res = CPQ.postCartsPromoItems_api(cartId,promo['Id'],price=price,validate=validate)
    if timeStats != None:  
        timeStats.field('product',promoName)
        timeStats.time('postCartsPromoItems')

    return cartId,res['actions']['rootitemadded']['client']

def _contextLineItemIds(obj,ids=[]):
    if 'lineItems' in obj:
        for li in obj['lineItems']['records']:
            ids.append(li['Id']['value'])
            _contextLineItemIds(li,ids)
    if 'productGroups' in obj:
        for pg in obj['productGroups']['records']:
            _contextLineItemIds(pg,ids)

def getlineItemIds(items,productCode):
    """Get the id for the product and all the sibblings."""
    obj,parents = get_ol(items,productCode,itemType='lineItem')
    if obj == None: utils.raiseException('Item not found',f" with product code {productCode} cannot be found")

    contextLineItemIds = []
    _contextLineItemIds(obj,contextLineItemIds)

    contextLineItemIds.append(obj['Id']['value'])
    return contextLineItemIds

def post_promo_item(cartId,items,productCode,promotionName=None,promotionId=None,price=True,validate=True,contextLineItemIds=None):
    """
    provide promotionName or promotionId. if both promotionId takes precedence. 
    """
    obj,parents = get_ol(items,productCode,itemType='lineItem')
    #if obj == None: utils.raiseException('Item not found',f" with product code {productCode} cannot be found")

    #contextLineItemIds = []
    #_contextLineItemIds(obj,contextLineItemIds)

    #contextLineItemIds.append(obj['Id']['value'])

    if contextLineItemIds == None:
        contextLineItemIds = getlineItemIds(items,productCode)

    done = False
    position = len(parents) - 2
    while done == False:
        parentRecord = parents[position]
        if 'promotions' not in parentRecord:
            position = position - 2
        else:
            done = True

    if promotionId == None:
        for promo in parentRecord['promotions']['records']:
            if promo['Name'] == promotionName:
                promotionId = promo['Id']

    call = CPQ.postCartsPromoItems_api(cartId, promotionId,price=price,validate=validate,contextLineItemIds=contextLineItemIds)

    return call

def clone_lineItem(cartId,items,path,price=False,validate=False,reduced=True):
    obj,parents = get_ol(items,path,itemType='lineItem')
    if obj == None: utils.raiseException('Item not found',f"Cannot Clone. Item not found {path} ")

    itemId = obj['Id']['value']

    call = CPQ.clone_item_api(cartId,itemId,price=price,validate=validate,reduced=reduced)

    return call

def cart_stats(items):
    def _add_to_counter(counters,field,value=1):
        if field not in counters: counters[field] = 0
        counters[field] = counters[field] + value

    def _parse_order_line(ol,counters):
        _add_to_counter(counters,ol['itemType'])
        if 'action' in ol: 
            _add_to_counter(counters,ol['action'])

        if 'attributeCategories' in ol and ol['attributeCategories'] != None : #CPQ Next puts attributeCategories = None for itemType = ProductGroup
            if 'records' in ol['attributeCategories']:  #CPQ Next. if total size = 0 there are no records. 
                for ar in ol['attributeCategories']['records']:
                    _add_to_counter(counters,f"{ol['itemType']}_att",len(ar['productAttributes']['records']))
            
        ol_types = ['lineItems','childProducts','productGroups']

        for ol_type in ol_types:
            if ol_type in ol:
                for r in ol[ol_type]['records']:
                    _parse_order_line(r,counters)
    
    counters = {} 
    if 'records' not in items: return counters  #cart is empty
    for r in items['records']:
        _parse_order_line(r,counters)

    return counters

def get_ol(items,path,itemType=None):
    """Returns the object and the parents."""

    onlyOne=False

    siblings = objectUtil.getSiblingWhere_path(items,matchKey='ProductCode',matchKeyValuePath=path,whereKey='itemType',whereValue=itemType)

    if siblings == None: return None, None
    return siblings['object'],siblings['objects']
    print()

def cart_products_hierarchy(items):
    def _add_to_counter(counters,field,value=1):
        if field not in counters: counters[field] = 0
        counters[field] = counters[field] + value

    def _parse_order_line(ol,counters,padding=''):
        _add_to_counter(counters,ol['itemType'])
        if 'action' in ol: 
            _add_to_counter(counters,ol['action'])


        if 'ProductCode' in ol:
            promos =''
            if 'promotions' in ol:
                promos = " --- Promo:"
                for p in ol['promotions']['records']:
                    promos = promos + " "+p['Name']

            if 'value' in ol['ProductCode']: print(padding+ol['ProductCode']['value'] + promos )
            else: print(padding+ol['ProductCode'] + promos)
        if 'attributeCategories' in ol:
            for ar in ol['attributeCategories']['records']:
                _add_to_counter(counters,f"{ol['itemType']}_att",ar['productAttributes']['totalSize'])
            
        ol_types = ['lineItems','childProducts','productGroups']

        for ol_type in ol_types:
            if ol_type in ol:
                for r in ol[ol_type]['records']:
                    _parse_order_line(r,counters,padding=padding+'  ')
    
    counters = {} 
    if 'records' not in items: return counters  #cart is empty
    for r in items['records']:
        _parse_order_line(r,counters)

    return counters

def sort_cartItems(cartItems,deleteFields = None):
    if 'messages' in cartItems:
        cartItems['messages'] = sorted(cartItems['messages'], key=lambda p: p["message"])
    if 'records' not in cartItems:
        return cartItems
    records = cartItems['records']
    if len(records) == 0:
        return cartItems
    itemType = records[0]['itemType']

    sorted_records = records
    if len(records)>1:
        if itemType == 'lineItem':
            sorted_records = sorted(records, key=lambda p: p["vlocity_cmt__LineNumber__c"]["value"])
        if itemType == 'productGroup':
            sorted_records = sorted(records, key=lambda p: p["ProductCode"]["value"])
        if itemType == 'childProduct':
            sorted_records = sorted(records, key=lambda p: p["productHierarchyPath"])

    cartItems['records'] = sorted_records

    item_types = ['lineItems','childProducts','productGroups']

    if len(sorted_records)>0:
        newRecords = []
        for record in sorted_records:
            if deleteFields != None:
                for deleteField in deleteFields:
                    if deleteField in record:
                        record.pop(deleteField,None)

            if 'vlocity_cmt__BillingAccountId__c' in record:
                record['vlocity_cmt__BillingAccountId__c']['actions'] = {}
            if 'vlocity_cmt__ServiceAccountId__c' in record:
                record['vlocity_cmt__ServiceAccountId__c']['actions'] = {}
            if 'productHierarchyPath' in record:
                if record['productHierarchyPath'] == "01tAU00000CBTMOYA5":
                    a=1
            for item_type in item_types:
                if item_type in record:
                    sort_cartItems(record[item_type],deleteFields=deleteFields)
            if 'productHierarchyPath' in record:
                if record['productHierarchyPath'] == "01tAU00000CBTMOYA5":
                    a=1
            remaining_keys = {k: v for k, v in record.items() if k not in item_types}
            ordered_keys = {k: record[k] for k in item_types if k in record}
            #if len(ordered_keys)>0:
            sorted_remaining_keys = dict(sorted(remaining_keys.items()))
            newRecord = {**sorted_remaining_keys, **ordered_keys}
            newRecords.append(newRecord)
        
        cartItems['records'] = newRecords

    a=1

    return cartItems

