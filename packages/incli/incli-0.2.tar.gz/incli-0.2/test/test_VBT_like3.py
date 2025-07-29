import unittest,hashlib,simplejson
from datetime import datetime
#from InCli import InCli
from incli.sfapi import tooling,restClient,Sobjects,query,jsonFile

class Test_VBT_like3(unittest.TestCase):
    def test_serialize_record(self):
        sampleFile = '/Users/uormaechea/temp/salesforce-qms/sourcecode/vlocity/Product2/0a8dfbcb-ea51-eab7-3086-9ffb6c0830c3/C_CORP_ESCRITORIO_IP_DataPack.json'

        sample = jsonFile.read(sampleFile)

        for key in sample.keys():
            print(key)

        a=1
      