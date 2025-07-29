import unittest
from incli.sfapi import restClient,CPQ,account,Sobjects,utils,query,jsonFile,debugLogs
import traceback,simplejson,os


class Test_Stuff(unittest.TestCase):

  def test_PromotionErrors(self):
    restClient.init("DTI")
    fileName = '/Users/uormaechea/Downloads/vbtlogtestwithjobinbetweenpacksretrys.txt'
    Id = ''

    promotions = []

    with open(fileName, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            if 'Error >> Promotion' in line:
                Id = line.split('/')[1].split(' ')[0]
                if Id not in promotions:
                   promotions.append(Id)

    for promo in promotions:
      print('----------------------------------------------------------------------------------------')
      print(f"Promotions: {promo}")
      with open(fileName, 'r') as file:
         for line in file:
            if promo in line:
               print(line)
               if "Error" in line:
                  vlocity_cmt__GlobalKey__c = line.split("vlocity_cmt__GlobalKey__c=")[1].split(' ')[0]
                  vlocity_cmt__IsOverride__c = line.split("vlocity_cmt__IsOverride__c=")[1].split(' ')[0]
                  vlocity_cmt__OverrideContext__c = line.split("vlocity_cmt__OverrideContext__c=")[1].split(' ')[0]
                  vlocity_cmt__ObjectId__c = line.split("vlocity_cmt__ObjectId__c=")[1].split(' ')[0]
                  vlocity_cmt__Code__c = line.split("vlocity_cmt__Code__c=")[1].split(' ')[0]

                  res = query.query(f"select fields(all),vlocity_cmt__AttributeId__r.vlocity_cmt__Code__c from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__GlobalKey__c = '{vlocity_cmt__GlobalKey__c}' limit 1")

                  if (res['totalSize']==0):
                     print(f"vlocity_cmt__AttributeAssignment__c does not exist with global key {vlocity_cmt__GlobalKey__c}")
                  else:
                     print(f"{vlocity_cmt__GlobalKey__c}  {vlocity_cmt__IsOverride__c}  ---- {res['records'][0]['vlocity_cmt__IsOverride__c']}    {vlocity_cmt__OverrideContext__c}-{res['records'][0]['vlocity_cmt__OverrideContext__c']}    {vlocity_cmt__ObjectId__c}--{res['records'][0]['vlocity_cmt__ObjectId__c']}    {vlocity_cmt__Code__c}--{res['records'][0]['vlocity_cmt__AttributeId__r']['vlocity_cmt__Code__c']}")
                  a=1
            #    print(res)
      print('----------------------------------------------------------------------------------------')

  def convert_to_json(self,file_path):
      with open(file_path, 'r') as file:
          try:
              json_data = simplejson.load(file)
              return json_data
          except simplejson.JSONDecodeError as e:
              print(f"Error decoding JSON in file {file_path}: {e}")
              return None
        
  def process_directory(self,input_directory):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if "OverrideDefinitions" in file:
                file_path = os.path.join(root, file)
                json_data = self.convert_to_json(file_path)
                if json_data is not None:
                    for js in json_data:
                      if "%vlocity_namespace%__OverridingAttributeAssignmentId__c" in js:
                        oa = js["%vlocity_namespace%__OverridingAttributeAssignmentId__c"]
                        
                        if oa['%vlocity_namespace%__IsOverride__c'] == True:
                           if oa['%vlocity_namespace%__OverrideContext__c'] == None:  
                              print(f"{file_path.split('/')[-1]}  -->  {oa['%vlocity_namespace%__AttributeId__r.%vlocity_namespace%__Code__c']}")
 #                             print(simplejson.dumps(json_data, indent=2))
 #                             print()
                        else:
                           if oa['%vlocity_namespace%__OverrideContext__c'] != None:   
                              print('This should not be')

  def test_check_allFolders(self):
    input_directory = "/Users/uormaechea/temp/DebugLogs_18Nov/salesforce-TesteDeployDTI/sourcecode/vlocity/Promotion"
    self.process_directory(input_directory)  

  def test_check_Padrao(self):
    input_directory = "/Users/uormaechea/temp/DebugLogs_18Nov/salesforce-TesteDeployDTI/sourcecode/vlocity/Product2"
    with open('Padrao', 'w') as filep:

      for root, dirs, files in os.walk(input_directory):
          for file in files:
            if 'DataPack' in file:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as _file:
                    try:
                        file_contents = _file.read()
                        if 'PricebookEntry/Pricebook2' in file_contents:
                          if 'Catálogo de preços padrão' in file_contents:
                            s = f"******** Padrao --> {file}" + '\n'
                          else:
                            s= f"-------         --> {file}" + '\n'
                          filep.write(s)
                        else:
                           a=1
                    except simplejson.JSONDecodeError as e:
                        print(f"Error  {file_path}: {e}")
                        return None
                a=1
  def test_in_all(self):
    a=1

  def test_check_in_all_files(self):
    input_directory = "/Users/uormaechea/temp/salesforce-rs.devcatsb3.dti-sourcecode-vlocity/sourcecode/vlocity"

    infile = []
    for root, dirs, files in os.walk(input_directory):
      for file in files:
        if 'WOO' in file:
           continue
   #     print(file)
        name = "_".join(file.split('_')[0:-1])
        file_path = os.path.join(root, file)
        with open(file_path, 'r') as _file:
          try:
            file_contents = _file.read()
            if 'IsOverride__c": true' in file_contents:
              if name not in infile:
                infile.append(name)
                print(name)
                a=1
          except Exception as e:
             print(e)
       
  def test_check_OverrideContext_as(self):
    input_directory = "/Users/uormaechea/temp/salesforce-RS.P102529.CATALOG.2023.R43.FIXVBTISSUES2-sourcecode-vlocity/sourcecode/vlocity/Product2"

    infile = []
 #   with open('AttibuteAssig_git', 'w') as filep:
    with open('ProdOverrides_git', 'w') as filep:

      for root, dirs, files in os.walk(input_directory):
          product_globalKey = root.split('/')[-1]
          for file in files:
            if '_OverrideDefinitionsxxx' in file:
                product_name = file.split('_OverrideDefinitions')[0]
                file_path = os.path.join(root, file)
                json_data = self.convert_to_json(file_path)
                for js in json_data:
                  if '%vlocity_namespace%__OverriddenAttributeAssignmentId__c' in js:
                    oaa = js['%vlocity_namespace%__OverriddenAttributeAssignmentId__c']
                    if oaa['%vlocity_namespace%__IsOverride__c'] == True:
                      if oaa['%vlocity_namespace%__OverrideContext__c'] == None:
                        a=1
                  if '%vlocity_namespace%__OverridingAttributeAssignmentId__c' in js:
                    oaa = js['%vlocity_namespace%__OverridingAttributeAssignmentId__c']
                    if oaa['%vlocity_namespace%__IsOverride__c'] == True:
                      if oaa['%vlocity_namespace%__OverrideContext__c'] == None:
                        variable = product_name
                        if variable not in infile:
                          filep.write(variable + '\n')
                          infile.append(variable)
                        
            if 'AttributeAssignment' in file:
                product_name = file.split('_AttributeAssignment')[0]

                file_path = os.path.join(root, file)
                json_data = self.convert_to_json(file_path)

                l = len(json_data) 
                c = 0
                for js in json_data:
                  if js['%vlocity_namespace%__IsOverride__c'] == True:
                    c=c+1
                    if js['%vlocity_namespace%__OverrideContext__c'] == '':

                      variable = product_globalKey
                      variable = product_name
                      if variable not in infile:
                        filep.write(variable + '\n')
                        infile.append(variable)
                        filep.write(file + '\n')

                    else:
                      a=1
             #   print(f"{file}  {l}  {c}")

    q = None
    for inf in infile:
        if q == None:
           q = f"'{inf}'"
        else:
           q = f"{q},'{inf}'"

    print(q)    


  def test_check_OverrideContext_promo(self):
    input_directory = "/Users/uormaechea/temp/DebugLogs_18Nov/salesforce-TesteDeployDTI_2/sourcecode/vlocity/Promotion"

    infile = []
    with open('OverrideDef_git', 'w') as filep:
      for root, dirs, files in os.walk(input_directory):
          promo_globalKey = root.split('/')[-1]

          product_globalKey = root.split('/')[-1]
          for file in files:
            if 'OverrideDefinitions' in file:
              product_name = file.split('_OverrideDefinitions')[0]

            #  variable = product_globalKey
              variable = product_name

              if 'WOO' in product_name:
                 continue

              if variable not in infile:
                filep.write(variable + '\n')
                infile.append(variable)
                      #filep.write(file + '\n')

             #   print(f"{file}  {l}  {c}")


                a=1
  def test_checkAll_inGIT(self):
      input_directory = "/Users/uormaechea/temp/DebugLogs_18Nov/salesforce-TesteDeployDTI_2/sourcecode/vlocity/"

      no_product_folders = []

      done_products = []

      promos_directory = input_directory + "Promotion/"
      products_directory = input_directory + "Product2/"
      for root, dirs, files in os.walk(promos_directory):
        for dir in dirs:
          promo_directory = promos_directory + dir
          print(promo_directory + '--------------------------------------------------------------------------------------------------------')
          for root2, dirs2, files2 in os.walk(promo_directory):
            for _file in files2:
              if 'PromotionItems' in _file:
                file_path = os.path.join(promo_directory, _file)
                with open(file_path, 'r') as file:
                  try:
                      json_data = simplejson.load(file)
                      for js in json_data:
                        name = json_data[0]['%vlocity_namespace%__ProductId__c']['%vlocity_namespace%__GlobalKey__c']

                        self.check_product(products_directory,name,done_products=done_products)
                            

                  except Exception as e:
                      print(f"Error decoding JSON in file {file_path}: {e}")
                      return None                
          a=1

  def check_product(self,product2_dir,product_globalKey,hier='',done_products=[]):
    print(hier)
    prod_file_dir = product2_dir + product_globalKey

    if product_globalKey in done_products:
      return
    
    if product_globalKey == '85abeb1b-8cfe-a36d-458c-4e377cbf17a7':
       a=1
  
    if os.path.exists(prod_file_dir):
      print(f'    Product2 Exists  --> {product_globalKey}')

      for root, dirs, files in os.walk(prod_file_dir):
        for _file in files:
          if 'ProductChildItems' in _file:
              file_path = os.path.join(prod_file_dir, _file)
              with open(file_path,'r') as prod_file:
                json_data = simplejson.load(prod_file)
                for js in json_data:
                  if '%vlocity_namespace%__ChildProductId__c' in js and js['%vlocity_namespace%__ChildProductId__c'] != '':
                    childName = js['%vlocity_namespace%__ChildProductId__c']['%vlocity_namespace%__GlobalKey__c']
                    self.check_product(product2_dir,childName,hier+':'+childName)
                  else:
                      continue
      done_products.append(product_globalKey)                

    else:
      if name not in no_product_folders:
        no_product_folders.append(name)
        print(f'Does not exist --> {name}')
  def test_checkPRoducts(self):
     
    restClient.init('DEVNOSCAT3')
    res = query.query(f"select fields(all) from  vlocity_cmt__AttributeAssignment__c where vlocity_cmt__IsOverride__c = true and vlocity_cmt__OverrideContext__c =null  limit 100")

    for r in res['records']:
      prodId = r['vlocity_cmt__ObjectId__c']   
      res2 = query.query(f"select fields(all) from product2 where Id = '{prodId}'") 
      print(f"{res2['records'][0]['Name']}   {res2['records'][0]['vlocity_cmt__GlobalKey__c']}  {res2['records'][0]['ProductCode']}")
      a=1

  def test_find_in_folders(self):
     
    input_directory = "/Users/uormaechea/temp/salesforce-RS.PROJ.DTI-sourcecode-vlocity/sourcecode/vlocity"

    search = '2118f9-a03f21-d02d10-f7a363-ed0036268'
   # search = '5c78c150-d765-3300-d054-8dd441d9eaa7'
    search = 'Campanha Bilhete Anual Sport TV Premium'
    search = 'Campanha Bilhete Anual Sport TV Premium HD Multiscreen'
  #  search = 'f5dd576d-12e8-026f-0d14-fd064f3636b3'

    for root, dirs, files in os.walk(input_directory):        
      for _file in files:
        file_path = os.path.join(root, _file)
        with open(file_path, 'r') as _file:
          try:
            file_contents = _file.read()
            if search in file_contents:
              print(file_path)
          except Exception as e:
            #print(e)
            a=1           
