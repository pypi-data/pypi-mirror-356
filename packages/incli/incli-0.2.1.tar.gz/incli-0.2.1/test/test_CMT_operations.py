import unittest
#from InCli import InCli
from incli.sfapi import restClient,DR_IP,tooling

class Test_CMT_Operations(unittest.TestCase):
    def test_main(self):
        restClient.init('NOSQSM')

        ip_name = 'woo_getOffers'

        code = """
        vlocity_cmt.ScaleCacheService.invalidateCacheValue(new Map<String,String>{'VIPId' => 'woo_getOffersUnai2'});
        vlocity_cmt.IntegrationProcedureService.clearAllCache('woo_getOffersUnai2');
        vlocity_cmt.IntegrationProcedureService.clearMetadataCache('woo_getOffersUnai2');

        """

        res = tooling.executeAnonymous(code=code)

        a=1

    def test_hash(self):
        restClient.init('NOSQSM')

        code = """
        Blob targetBlob = Blob.valueOf('getOffers');
        Blob hash = Crypto.generateDigest('SHA3-256', targetBlob);
        system.debug(EncodingUtil.base64Encode(hash));
        """
        
        res = tooling.executeAnonymous(code=code)

        a=1

        
    def test_getCache(self):
        restClient.init('NOSQSM')

        code = """
                String cachePartitionName = 'vlocity_cmt.VlocityAPIResponse';

                Cache.OrgPartition orgPartition = Cache.Org.getPartition(cachePartitionName);

                if (orgPartition == null) {
                    system.debug('It is null');
                }
                else {
                    for (String key : orgPartition.getKeys())   {
                        system.debug(key);
                        system.debug(JSON.serializePretty(orgPartition.get(key)));

                    }
                }

        """ 
        res = tooling.executeAnonymous(code=code)

    def test_ips(self):
        restClient.init('NOSQSM')

        code = """
            Map<String, Object> competitors = new Map<String, Object>();

            Map<String, Object> input = new Map<String, Object>{
                'channel'=> 'APP2',
                'competitors'=> competitors,
                'isBSimulation'=> false,
                'offer'=> 'Bundle',
                'orderType'=> 'INSTALAÇÃO',
                'process'=> 'SELL',
                'technology'=> 'FTTH',
                'technologyCode'=> 'FTTHNOS'
            };
                
            Map<String, Object> options = new Map<String, Object>{
                'isDebug'=> false,
                'chainable'=> true,
                'resetCache'=> false,
                'ignoreCache'=> false,
                'queueableChainable'=> false,
                'useQueueableApexRemoting'=> false,
                'processName'=>'woo_getOffers'
            };
            
            Map<String, Object> output = new Map<String, Object>();

            CustomIPCalloutQueueable ipCallQueue = new CustomIPCalloutQueueable ();
            Object outputClass = ipCallQueue.invokeMethod('callIPAsync', input, output, options);

        """
        res = tooling.executeAnonymous(code=code)

        a=1

