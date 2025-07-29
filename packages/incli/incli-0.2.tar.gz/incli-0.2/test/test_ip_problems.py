import unittest,time
#from InCli import InCli
from incli.sfapi import restClient,query,Sobjects,DR_IP

#The endpoint used is:
#https://sf-qms.nos.pt/onboarding/services/apexrest/vlocity_cmt/v1/GenericInvoke/vlocity_cmt.IntegrationProcedureService/woo_getOffers

#We use a proxy so the URL may look unfamiliar. It is a pass-through proxy so there is no change in the payload but you can do the same test with the official site URL for Onboarding in our org:
#https://nos--nosqms.sandbox.my.site.com/onboarding/services/apexrest/vlocity_cmt/v1/GenericInvoke/vlocity_cmt.IntegrationProcedureService/woo_getOffers
class Test_IP_problems(unittest.TestCase):
    def call_getOffers(self,technologyCode="FTTHXGSNOS",isBSimulation=False):

        name = "woo_getOffers"
        name = "unai_test40"

        input = {
            "channel": "APP",
            "competitors": {},
            "isBSimulation": True,
            "offer": "Fixed",
            "orderType": "INSTALAÇÃO",
            "process": "SELL",
            "technology": "FTTH",
            "technologyCode": "FTTHXGSNOS"
        }

     #   input = {
     #       "channel": "APP",
     #       "isBSimulation": True,
     #       "orderType": "INSTALAÇÃO",
     #       "technology": "FTTH",
     #       "competitors": {},
     #       "process": "SELL",
     #       "offer": "Bundle",
     #       "technologyCode": "FTTHXGSNOS"
     #   }

     #   input = {}

        options = {
            "isDebug": True,
            "chainable": False,
            "resetCache": False,
            "ignoreCache": False,
            "queueableChainable": False,
            "useQueueableApexRemoting": False
        }
        res = DR_IP.ip(name=name,input=input,options=options)

        print(f" technologyCode: {technologyCode} isBSimulation: {isBSimulation} {restClient.getLastCallElapsedTime()}")

        files = restClient.callSave(f"{technologyCode}{isBSimulation}",logRequest=True,index=-1)

        times = restClient.getLastCallAllTimes()
        print(f" elapsed: {times['elapsed']} delta: {times['delta']} ")
        if 'elapsedTimeCPU' in res['IPResult']:
            print(f" elapsedCPU: {res['IPResult']['elapsedTimeCPU']}  elapsedActual: {res['IPResult']['elapsedTimeActual']}")

        return res


    def test_main(self):
        restClient.init('NOSQSM')
        codes = "FTTHNOS/FTTHXGSNOS/FFTHVOD/FTTHXGSVOD"

        codeCh = codes.split('/')

        a=1

        while a < 1000:
            res = self.call_getOffers(technologyCode=codeCh[0],isBSimulation=True)
    #        time.sleep(5)


        for code in codeCh:
            self.call_getOffers(technologyCode=code,isBSimulation=True)
            self.call_getOffers(technologyCode=code,isBSimulation=False)

        a= 1


    def test_connectionLess(self):

        urlproxy = 'https://sf-qms.nos.pt/onboarding'
        urldirect = "https://nos--nosqms.sandbox.my.site.com/onboarding/"

        restClient.init('ConnectionLess',url=urldirect)

       # self.call_getOffers(technologyCode="",isBSimulation=True)


        #FTTHNOS/FTTHXGSNOS/FFTHVOD/FTTHXGSVOD
        a=1

        while a < 1000:
            res = self.call_getOffers(technologyCode="",isBSimulation=True)
            time.sleep(2)