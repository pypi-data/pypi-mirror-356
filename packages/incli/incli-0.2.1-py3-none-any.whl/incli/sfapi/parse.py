import re

products = []
promotions = []
def Product2(line):
    if 'Adding to File' in line:
        if '>> Product2' in line:
            print(line)
            pattern = r"Product2/([0-9a-f\-]+) - ([\w\-]+)"


            match = re.search(pattern, line)

            if match:
                prod = {
                    'name':match.group(2),
                    'Id':match.group(1),
                    'lines':[]
                }
                products.append(prod)
                find_all_lines(prod)
            else:
                print(line)
                print("No match found.")

        if '>> Promotion' in line:
            print(line)
            pattern = r"Promotion/([0-9a-f\-]+) - ([\w\-]+)"


            match = re.search(pattern, line)

            if match:
                prod = {
                    'name':match.group(2),
                    'Id':match.group(1),
                    'lines':[]
                }
                promotions.append(prod)
                find_all_lines(prod)
            else:
                print(line)
                print("No match found.")

def find_all_lines(obj):
    with open('/Users/uormaechea/Downloads/ouutput2.txt', 'r') as file:
        for line in file:
            if obj['Id'] in line:
                obj['lines'].append(line)

def process():
    with open('/Users/uormaechea/Downloads/ouutput2.txt', 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Print each line
         #   print(line, end='')
            line = line.replace('\x1b[0m','')
            line = line.replace('\x1b[32m','')
            line = line.replace('\x1b[36m','')

       #     print(line)
       #     for car in line:
       #         print(car)
            Product2(line)

def find_lines(Id):
    with open('/Users/uormaechea/temp/DebugLogs_18Nov/vbtlog.txt', 'r') as file:
        # Iterate through each line in the file
        for line in file:
            if Id in line:
                print(line)

def processEx():
    process()

    for prod in products:
        if len(prod['lines'])>4:
            a=1
    for prod in promotions:
        if len(prod['lines'])>4:
            a=1
        if '36d10ada-ce65-1950-8077-e0c3fae6b1cf' == prod['Id']:
            a=1
    
if __name__ == '__main__':
    print('-------------------------------------------------------------------------------------------------------------------')
    find_lines('633c96e4-66e1-d5a5-a8e3-d45bdf7fe21c')
