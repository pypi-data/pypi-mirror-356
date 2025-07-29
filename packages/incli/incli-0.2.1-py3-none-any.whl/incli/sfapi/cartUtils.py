from . import jsonFile

def simplifyCart(obj,createFiles=False):
     filex = jsonFile.write('xxxy',obj)

     res1 = keepKeys(obj)
     if createFiles: file1 = jsonFile.write('xxx1',res1)

     res2 = manipulate(obj=res1)
     if createFiles: file2 = jsonFile.write('xxx2',res2)

     res3 = {
          'messages':res2['messages'],
          'lineItems':res2['records']
     }

     if createFiles: file3 = jsonFile.write('xxx3',res3)

     return res3

def removeKeys(obj):
     keys_to_remove = ['previousValue','originalValue','messages','label','hidden','fieldName','editable','dataType','alternateValues','actions']
     keys_to_remove.extend(['readonly','displaySequence','disabled','defaultValue','defaultSelected'])
     keys_to_remove.extend(['isNotTranslatable','cloneable','hidden','hasRules','filterable','required','multiselect','inputType'])

     keys_to_remove_childProduct = ['action','NOS_c_BasePriceRC__c','vlocity_cmt__ProductHierarchyPath__c','vlocity_cmt__BillingAccountId__r','vlocity_cmt__ServiceAccountId__r','parentLineItemId']
     keys_to_remove_childProduct.extend(['Id','itemType','productId','isVirtualItem','productHierarchyPath'])

     if isinstance(obj, dict):
          all_key_to_remove = keys_to_remove
          if (obj.get('itemType') == 'childProduct'):
               all_key_to_remove.extend(keys_to_remove_childProduct)

          return {
               k: removeKeys(v)
               for k, v in obj.items()
               if k not in keys_to_remove
          }
     elif isinstance(obj, list):
          return [removeKeys(item) for item in obj]
     else:
          return obj

def flattenValue(obj):
     for key in obj:
          #print(key)
          if isinstance(obj[key], dict) and 'value' in obj[key]:
               obj[key] = obj[key]['value']

def keepKeys(obj):
     keep_lineItem = ['Id','lineItems','childProducts','productGroups','Name','attributeCategories','promotions']
     keep_productGroup = ['lineItems','childProducts','productGroups','Name']
     keep_childProduct = ['lineItems','childProducts','productGroups','Name']

     keep = None
     if isinstance(obj, dict):
          if (obj.get('itemType') == 'lineItem'): 
               flattenValue(obj)
               extractAttributes(obj)
               keep = keep_lineItem
          if (obj.get('itemType') == 'productGroup'): 
               flattenValue(obj)
               keep = keep_productGroup
          if (obj.get('itemType') == 'childProduct'): 
               flattenValue(obj)
               keep = keep_childProduct

          return {
               k: keepKeys(v)
               for k, v in obj.items()
               if keep == None or len(keep)==0 or k in keep
          }
     elif isinstance(obj, list):
          return [keepKeys(item) for item in obj]
     else:
          return obj
     
def manipulate(obj,pc=[]):
     if isinstance(obj, dict):
          d = {}
          keys = list(obj.keys())
          for k in keys:
               if k in ['lineItems','productGroups','childProducts']:
                    obj[k] = obj[k]['records']

               if k == 'childProducts':
                    a = []
                    for item in obj[k]:
                         a.append(item['Name'])
                    obj[k]=a
               d[k] = manipulate(obj[k],pc)

               if k in ['Name'] and 'productAttributes' not in obj:
                    pc.append(obj['Name'])
                    d['pc'] = ":".join(pc)
          return d
     elif isinstance(obj, list):
          return [manipulate(item,pc) for item in obj]
     else:
          return obj
     
def extractAttributes(lineItem):
    """Extract and format attribute information from lineItems in cart data. 
    Returns a JSON structure with attribute categories, product attributes, possible values, and user values."""
    
    try:        
          result = []
          
          # Process attribute categories
          attribute_categories = lineItem.get("attributeCategories", {}).get("records", [])
          
          for category in attribute_categories:
               category_name = category.get("Name", "unknown")
               category_id = category.get("Id", "unknown")
               
               # Initialize category structure
               newCatefory = {
                    "Name":category_name,
                  #  "categoryId": category_id,
                    "productAttributes": []
               }
               
               # Process product attributes within this category
               product_attributes = category.get("productAttributes", {}).get("records", [])
               
               for attr in product_attributes:
                    attr_name = attr.get("label", attr.get("code", "unknown"))
                    attr_code = attr.get("code", "unknown")
                    attr_id = attr.get("attributeId", "unknown")
                    
                    # Extract possible values from the values array
                    possible_values = []
                    values_array = attr.get("values", [])
                    for value_obj in values_array:
                         # Try different possible value fields
                         value = value_obj.get("label") 
                         if value is not None:
                              possible_values.append(value)
                    
                    # Get user values
                    user_values = attr.get("userValues")
                    
                    newAttribute = {
                         "name":attr_name,
                      #   "attributeId": attr_id,
                      #   "code": attr_code,
                         "userValues": user_values,
                         "dataType": attr.get("dataType", "unknown")#,
                       #  "inputType": attr.get("inputType", "unknown"),
                       #  "required": attr.get("required", False),
                       #  "readonly": attr.get("readonly", False),
                       #  "disabled": attr.get("disabled", False)
                    }
                    if len(possible_values)>0:
                         newAttribute["possibleValues"] = possible_values
                    inputType = attr.get("inputType", "unknown")
                    if inputType == 'checkbox':
                         newAttribute["dataType"] = "boolean"
                    newCatefory["productAttributes"].append(newAttribute)
                    result.append(newCatefory)
        
          lineItem['attributeCategories']=result
        
    except Exception as e:
        print(f"Error extracting attributes: {e}")
        raise
