import unittest,hashlib
from datetime import datetime
#from InCli import InCli
from incli.sfapi import account,restClient,CPQ,query,jsonFile

class Test_VBT_like(unittest.TestCase):

    def feelTheFields(self,js,record):
        for field in js:
            if field in ['VlocityDataPackType','VlocityRecordSObjectType']:
                continue
            field_vlo = field.replace('%vlocity_namespace%','vlocity_cmt')
            if type(js[field]) is dict:
                print(js[field])
                field_vlo_r = field_vlo.replace('__c','__r')

                for field_in in js[field]:
                    field_in_vlo = field_in.replace('%vlocity_namespace%','vlocity_cmt')

                    if field_vlo_r == 'RecordTypeId':
                        field_vlo_r = 'RecordType'

                    if field_in_vlo in record[field_vlo_r]:
                        js[field][field_in] = record[field_vlo_r][field_in_vlo]
                continue

            if field_vlo in record:
                js[field] = record[field_vlo]
            else:
                js[field] = 'XXXXXXXXXXXXXXXXXXXXXX'

        a=1
    def generate_fixed_length_string(self,input_string, length=10):
        # Generate a SHA-256 hash of the input string
        hash_object = hashlib.sha256(input_string.encode())
        
        # Convert the hash to a hexadecimal string
        hex_dig = hash_object.hexdigest()
        
        # Return the first `length` characters of the hash
        return hex_dig[:length]
                
    def createPromo(self,code):
        res = query.query(f"select fields(all),vlocity_cmt__PriceListId__r.vlocity_cmt__Code__c,RecordType.DeveloperName, RecordType.SobjectType  from vlocity_cmt__Promotion__c where vlocity_cmt__Code__c ='{code}' limit 1")

        promo = res['records'][0]

        promoJson = {
            "%vlocity_namespace%__AppliesToAllItems__c": promo['vlocity_cmt__AppliesToAllItems__c'],
            "%vlocity_namespace%__BenefitTimePlanId__c": promo['vlocity_cmt__BenefitTimePlanId__c'],
            "%vlocity_namespace%__BenefitTimePolicyId__c": promo['vlocity_cmt__BenefitTimePolicyId__c'],
            "%vlocity_namespace%__CannotBeCombined__c": promo['vlocity_cmt__CannotBeCombined__c'],
            "%vlocity_namespace%__Code__c": promo['vlocity_cmt__Code__c'],
            "%vlocity_namespace%__CpqEngineHints__c": promo['vlocity_cmt__CpqEngineHints__c'],
            "%vlocity_namespace%__Description__c": promo['vlocity_cmt__Description__c'],
            "%vlocity_namespace%__DiscountType__c": promo['vlocity_cmt__DiscountType__c'],
            "%vlocity_namespace%__DurationTimePlanId__c": promo['vlocity_cmt__DurationTimePlanId__c'],
            "%vlocity_namespace%__DurationTimePolicyId__c": promo['vlocity_cmt__DurationTimePolicyId__c'],
            "%vlocity_namespace%__DurationUnitOfMeasure__c": promo['vlocity_cmt__DurationUnitOfMeasure__c'],
            "%vlocity_namespace%__Duration__c": promo['vlocity_cmt__Duration__c'],
            "%vlocity_namespace%__EffectiveEndDate__c": promo['vlocity_cmt__EffectiveEndDate__c'],
            "%vlocity_namespace%__EffectiveStartDate__c": promo['vlocity_cmt__EffectiveStartDate__c'],
            "%vlocity_namespace%__EnableAutoAddProducts__c": promo['vlocity_cmt__EnableAutoAddProducts__c'],
            "%vlocity_namespace%__EnableAutoApplyPromotion__c": promo['vlocity_cmt__EnableAutoApplyPromotion__c'],
            "%vlocity_namespace%__FollowOnPromotionId__c": promo['vlocity_cmt__FollowOnPromotionId__c'],
            "%vlocity_namespace%__GlobalKey__c": promo['vlocity_cmt__GlobalKey__c'],
            "%vlocity_namespace%__IsActive__c": promo['vlocity_cmt__IsActive__c'],
            "%vlocity_namespace%__IsLimitedQuantity__c": promo['vlocity_cmt__IsLimitedQuantity__c'],
            "%vlocity_namespace%__IsOrderable__c": promo['vlocity_cmt__IsOrderable__c'],
            "%vlocity_namespace%__PriceListEntry__c": f"{code}_PriceListEntries.json",
            "%vlocity_namespace%__PriceListId__c": {
                "%vlocity_namespace%__Code__c": promo['vlocity_cmt__PriceListId__r']['vlocity_cmt__Code__c'],
                "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                "VlocityLookupRecordSourceKey": f"%vlocity_namespace%__PriceList__c/{promo['vlocity_cmt__PriceListId__r']['vlocity_cmt__Code__c']}",
                "VlocityRecordSObjectType": "%vlocity_namespace%__PriceList__c"
            },
            "%vlocity_namespace%__PromotionItem__c": f"{code}_PromotionItems.json",
            "%vlocity_namespace%__Quantity__c": promo['vlocity_cmt__Quantity__c'],
            "%vlocity_namespace%__RankOrder__c": promo['vlocity_cmt__RankOrder__c'],
            "%vlocity_namespace%__RedeemableCode__c": promo['vlocity_cmt__RedeemableCode__c'],
            "%vlocity_namespace%__ServiceContinuation__c": promo['vlocity_cmt__ServiceContinuation__c'],
            "NOS_b_ImpactLoyalty__c": promo['NOS_b_ImpactLoyalty__c'],
            "NOS_c_LoyaltyAmount__c": promo['NOS_c_LoyaltyAmount__c'],
            "NOS_c_OperationalLoyalty__c": promo['NOS_c_OperationalLoyalty__c'],
            "NOS_c_VariableLoyalty__c": promo['NOS_c_VariableLoyalty__c'],
            "NOS_d_SellingEndDate__c": promo['NOS_d_SellingEndDate__c'],
            "NOS_l_RootPromotion__c": promo['NOS_l_RootPromotion__c'],
            "NOS_n_LoyaltyPeriod__c": promo['NOS_n_LoyaltyPeriod__c'],
            "NOS_n_PromotionalItem__c": promo['NOS_n_PromotionalItem__c'],
            "NOS_t_CommercialName__c": promo['NOS_t_CommercialName__c'],
            "NOS_t_Fallback__c": promo['NOS_t_Fallback__c'],
            "NOS_t_Family__c": promo['NOS_t_Family__c'],
            "NOS_t_Type__c": promo['NOS_t_Type__c'],
            "Name": promo['Name'],
            "RecordTypeId": {
                "DeveloperName": promo['RecordType']['DeveloperName'],
                "SobjectType": "%vlocity_namespace%__Promotion__c",
                "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                "VlocityLookupRecordSourceKey": f"RecordType/%vlocity_namespace%__Promotion__c/{promo['RecordType']['DeveloperName']}",
                "VlocityRecordSObjectType": "RecordType"
            },
            "VlocityDataPackType": "SObject",
            "VlocityRecordSObjectType": "%vlocity_namespace%__Promotion__c",
            "VlocityRecordSourceKey": f"%vlocity_namespace%__Promotion__c/{promo['vlocity_cmt__GlobalKey__c']}"
        }

   #     self.feelTheFields(promoJson,promo)

        return promoJson

    def convertTimeStamp(self,timestamp):
        if timestamp == "" or timestamp == None:
            return ""
        dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def emptyStr4None(self,ste):
        if ste == None:
            return ""
        return ste

    def create_PLE(self,code):
        def emptyStrifNone(value):
            if value == None:
                return ""
            return value

        res = query.query(f"""SELECT id,
                          name,vlocity_cmt__basepricelistid__c,vlocity_cmt__displaytext__c,vlocity_cmt__effectivefromdate__c,vlocity_cmt__effectiveuntildate__c,vlocity_cmt__globalkey__c,vlocity_cmt__isactive__c,vlocity_cmt__isbaseprice__c,vlocity_cmt__isoverride__c,vlocity_cmt__isvirtualprice__c,vlocity_cmt__offerid__c,vlocity_cmt__pricelistname__c,vlocity_cmt__pricingelementamount__c,vlocity_cmt__pricingelementglobalkey__c,vlocity_cmt__pricingelementid__c,vlocity_cmt__pricingmatrixbindingdata__c,vlocity_cmt__productid__c,vlocity_cmt__promotionid__c,vlocity_cmt__promotionitemid__c,vlocity_cmt__rulesdescription__c,vlocity_cmt__timeplanid__c,vlocity_cmt__timepolicyid__c,vlocity_cmt__pricebookentryid__c,
                          vlocity_cmt__OfferId__r.vlocity_cmt__GlobalKey__c,
                          vlocity_cmt__PriceListId__r.vlocity_cmt__Code__c,
                          vlocity_cmt__PricingElementId__r.vlocity_cmt__GlobalKey__c,
                          vlocity_cmt__ProductId__r.vlocity_cmt__GlobalKey__c,
                          vlocity_cmt__PromotionItemId__r.vlocity_cmt__OfferId__r.vlocity_cmt__GlobalKey__c,
                          vlocity_cmt__PromotionItemId__r.vlocity_cmt__ProductId__r.vlocity_cmt__GlobalKey__c,
                          vlocity_cmt__PromotionItemId__r.vlocity_cmt__PromotionId__r.vlocity_cmt__GlobalKey__c,
                          vlocity_cmt__PriceListId__r.vlocity_cmt__Pricebook2Id__c, 
                          vlocity_cmt__PriceListId__r.vlocity_cmt__Pricebook2Id__r.name,
                          vlocity_cmt__PromotionId__r.vlocity_cmt__GlobalKey__c

                FROM vlocity_cmt__PriceListEntry__c WHERE (vlocity_cmt__PromotionId__r.vlocity_cmt__Code__c = '{code}') """)

        allPLEs = []
        for ple in res['records']:
            pleJson =     {
                "%vlocity_namespace%__BasePriceListId__c": emptyStrifNone( ple['vlocity_cmt__BasePriceListId__c']),
                "%vlocity_namespace%__DisplayText__c": ple['vlocity_cmt__DisplayText__c'],
                "%vlocity_namespace%__EffectiveFromDate__c": self.convertTimeStamp(ple['vlocity_cmt__EffectiveFromDate__c']),
                "%vlocity_namespace%__EffectiveUntilDate__c": self.convertTimeStamp(ple['vlocity_cmt__EffectiveUntilDate__c']),
                "%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__GlobalKey__c'],
                "%vlocity_namespace%__IsActive__c": ple['vlocity_cmt__IsActive__c'],
                "%vlocity_namespace%__IsBasePrice__c": ple['vlocity_cmt__IsBasePrice__c'],
                "%vlocity_namespace%__IsOverride__c": ple['vlocity_cmt__IsOverride__c'],
                "%vlocity_namespace%__IsVirtualPrice__c": ple['vlocity_cmt__IsVirtualPrice__c'],
                "%vlocity_namespace%__OfferId__c": {
                    "%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__OfferId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"Product2/{ple['vlocity_cmt__OfferId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "Product2"
                },
                "%vlocity_namespace%__PriceBookEntryId__c": {
                    "Pricebook2.Name": ple['vlocity_cmt__PriceListId__r']['vlocity_cmt__Pricebook2Id__r']['Name'],
                    "Product2.%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"VlocityRecordSourceKey:{ple['vlocity_cmt__PriceBookEntryId__c']}",
                    "VlocityRecordSObjectType": "PricebookEntry"
                },
                "%vlocity_namespace%__PriceListId__c": {
                    "%vlocity_namespace%__Code__c": ple['vlocity_cmt__PriceListId__r']['vlocity_cmt__Code__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"%vlocity_namespace%__PriceList__c/{ple['vlocity_cmt__PriceListId__r']['vlocity_cmt__Code__c']}",
                    "VlocityRecordSObjectType": "%vlocity_namespace%__PriceList__c"
                },
                "%vlocity_namespace%__PriceListName__c": ple['vlocity_cmt__PriceListName__c'],
                "%vlocity_namespace%__PricingElementAmount__c": ple['vlocity_cmt__PricingElementAmount__c'] if ple['vlocity_cmt__PricingElementAmount__c']!= 0.0 else 0,
                "%vlocity_namespace%__PricingElementGlobalKey__c": ple['vlocity_cmt__PricingElementGlobalKey__c'],
                "%vlocity_namespace%__PricingElementId__c": {
                    "%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__PricingElementId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"%vlocity_namespace%__PricingElement__c/{ple['vlocity_cmt__PricingElementId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "%vlocity_namespace%__PricingElement__c"
                },
                "%vlocity_namespace%__PricingMatrixBindingData__c": emptyStrifNone(ple['vlocity_cmt__PricingMatrixBindingData__c']),
                "%vlocity_namespace%__ProductId__c": {
                    "%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"Product2/{ple['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "Product2"
                },
                "%vlocity_namespace%__PromotionId__c": {
                    "%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__PromotionId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityMatchingKeyObject",
                    "VlocityMatchingRecordSourceKey": f"%vlocity_namespace%__Promotion__c/{ple['vlocity_cmt__PromotionId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "%vlocity_namespace%__Promotion__c"
                },
                "%vlocity_namespace%__PromotionItemId__c": {
                    "%vlocity_namespace%__OfferId__r.%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__PromotionItemId__r']['vlocity_cmt__OfferId__r']['vlocity_cmt__GlobalKey__c'],
                    "%vlocity_namespace%__ProductId__r.%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__PromotionItemId__r']['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c'],
                    "%vlocity_namespace%__PromotionId__r.%vlocity_namespace%__GlobalKey__c": ple['vlocity_cmt__PromotionItemId__r']['vlocity_cmt__PromotionId__r']['vlocity_cmt__GlobalKey__c'],
                    "NOS_t_MatchingKey__c": "",
                    "VlocityDataPackType": "VlocityMatchingKeyObject",
                    "VlocityMatchingRecordSourceKey": f"%vlocity_namespace%__PromotionItem__c/Generated-{self.generate_fixed_length_string(ple['vlocity_cmt__PromotionItemId__c'])}",
                    "VlocityRecordSObjectType": "%vlocity_namespace%__PromotionItem__c"
                },
                "%vlocity_namespace%__RulesDescription__c": emptyStrifNone(ple['vlocity_cmt__RulesDescription__c']),
                "%vlocity_namespace%__TimePlanId__c": emptyStrifNone(ple['vlocity_cmt__TimePlanId__c']),
                "%vlocity_namespace%__TimePolicyId__c": emptyStrifNone(ple['vlocity_cmt__TimePolicyId__c']),
                "Name": ple['Name'],
                "VlocityDataPackType": "SObject",
                "VlocityRecordSObjectType": "%vlocity_namespace%__PriceListEntry__c",
                "VlocityRecordSourceKey": f"%vlocity_namespace%__PriceListEntry__c/{ple['Name']}"
            }

            allPLEs.append(pleJson)

        return allPLEs
        
    def create_PromoItems(self,code):
        res = query.query(f"""SELECT id,
                         vlocity_cmt__ActionType__c,
                         vlocity_cmt__CardinalityCheckScope__c,
                         vlocity_cmt__CatalogCategoryId__c,
                         vlocity_cmt__ContextEntityFilterId__c,
                         vlocity_cmt__ContextProductId__c,
                         vlocity_cmt__Description__c,
                         vlocity_cmt__EffectiveFromDate__c,
                         vlocity_cmt__EffectiveUntilDate__c,
                         vlocity_cmt__GlobalGroupKey__c,
                         vlocity_cmt__GlobalKey__c,
                         vlocity_cmt__IsActive__c,
                         vlocity_cmt__IsUndoable__c,
                         vlocity_cmt__MaxQuantity__c,
                         vlocity_cmt__MinQuantity__c,
                         vlocity_cmt__Quantity__c,
                         Name,
                         vlocity_cmt__OfferProductGroupKey__c,
                         vlocity_cmt__ProductHierarchyGlobalKeyPath__c,
                         vlocity_cmt__ProductHierarchyGroupKeyPath__c,
                         vlocity_cmt__ProductHierarchyPath__c,
                         vlocity_cmt__UndoableMessage__c,
                         vlocity_cmt__UpdateScope__c,
                         NOS_t_MatchingKey__c,
                         vlocity_cmt__OfferId__r.vlocity_cmt__GlobalKey__c,
                         vlocity_cmt__ProductId__r.vlocity_cmt__GlobalKey__c,
                         vlocity_cmt__PromotionId__r.vlocity_cmt__GlobalKey__c
                FROM vlocity_cmt__PromotionItem__c WHERE (vlocity_cmt__PromotionId__r.vlocity_cmt__Code__c = '{code}')  """)

        allPI = []
        for pi in res['records']:
            piJson =         {
                "%vlocity_namespace%__ActionType__c": pi['vlocity_cmt__ActionType__c'],
                "%vlocity_namespace%__CardinalityCheckScope__c": self.emptyStr4None(pi['vlocity_cmt__CardinalityCheckScope__c']),
                "%vlocity_namespace%__CatalogCategoryId__c": self.emptyStr4None(pi['vlocity_cmt__CatalogCategoryId__c']),
                "%vlocity_namespace%__ContextEntityFilterId__c": self.emptyStr4None(pi['vlocity_cmt__ContextEntityFilterId__c']),
                "%vlocity_namespace%__ContextProductId__c": self.emptyStr4None(pi['vlocity_cmt__ContextProductId__c']),
                "%vlocity_namespace%__Description__c": self.emptyStr4None(pi['vlocity_cmt__Description__c']),
                "%vlocity_namespace%__EffectiveFromDate__c": self.convertTimeStamp(pi['vlocity_cmt__EffectiveFromDate__c']),
                "%vlocity_namespace%__EffectiveUntilDate__c": self.convertTimeStamp(pi['vlocity_cmt__EffectiveUntilDate__c']),
                "%vlocity_namespace%__GlobalGroupKey__c": pi['vlocity_cmt__GlobalGroupKey__c'],
                "%vlocity_namespace%__GlobalKey__c":self.emptyStr4None(pi['vlocity_cmt__GlobalKey__c']),
                "%vlocity_namespace%__IsActive__c": pi['vlocity_cmt__IsActive__c'],
                "%vlocity_namespace%__IsUndoable__c": pi['vlocity_cmt__IsUndoable__c'],
                "%vlocity_namespace%__MaxQuantity__c": int(pi['vlocity_cmt__MaxQuantity__c']),
                "%vlocity_namespace%__MinQuantity__c": int(pi['vlocity_cmt__MinQuantity__c']),
                "%vlocity_namespace%__OfferId__c": {
                    "%vlocity_namespace%__GlobalKey__c": pi['vlocity_cmt__OfferId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"Product2/{pi['vlocity_cmt__OfferId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "Product2"
                },
                "%vlocity_namespace%__OfferId__r.%vlocity_namespace%__GlobalKey__c": pi['vlocity_cmt__OfferId__r']['vlocity_cmt__GlobalKey__c'],
                "%vlocity_namespace%__OfferProductGroupKey__c": pi['vlocity_cmt__OfferProductGroupKey__c'],
                "%vlocity_namespace%__ProductHierarchyGlobalKeyPath__c": self.emptyStr4None(pi['vlocity_cmt__ProductHierarchyGlobalKeyPath__c']),
                "%vlocity_namespace%__ProductHierarchyGroupKeyPath__c": self.emptyStr4None(pi['vlocity_cmt__ProductHierarchyGroupKeyPath__c']),
                "%vlocity_namespace%__ProductHierarchyPath__c": self.emptyStr4None(pi['vlocity_cmt__ProductHierarchyPath__c']),
                "%vlocity_namespace%__ProductId__c": {
                    "%vlocity_namespace%__GlobalKey__c": pi['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityLookupMatchingKeyObject",
                    "VlocityLookupRecordSourceKey": f"Product2/{pi['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "Product2"
                },
                "%vlocity_namespace%__ProductId__r.%vlocity_namespace%__GlobalKey__c": pi['vlocity_cmt__ProductId__r']['vlocity_cmt__GlobalKey__c'],
                "%vlocity_namespace%__PromotionId__c": {
                    "%vlocity_namespace%__GlobalKey__c": pi['vlocity_cmt__PromotionId__r']['vlocity_cmt__GlobalKey__c'],
                    "VlocityDataPackType": "VlocityMatchingKeyObject",
                    "VlocityMatchingRecordSourceKey": f"%vlocity_namespace%__Promotion__c/{pi['vlocity_cmt__PromotionId__r']['vlocity_cmt__GlobalKey__c']}",
                    "VlocityRecordSObjectType": "%vlocity_namespace%__Promotion__c"
                },
                "%vlocity_namespace%__PromotionId__r.%vlocity_namespace%__GlobalKey__c": pi['vlocity_cmt__PromotionId__r']['vlocity_cmt__GlobalKey__c'],
                "%vlocity_namespace%__Quantity__c": int(pi['vlocity_cmt__Quantity__c']),
                "%vlocity_namespace%__UndoableMessage__c": self.emptyStr4None(pi['vlocity_cmt__UndoableMessage__c']),
                "%vlocity_namespace%__UpdateScope__c": pi['vlocity_cmt__UpdateScope__c'],
                "NOS_t_MatchingKey__c": self.emptyStr4None(pi['NOS_t_MatchingKey__c']),
                "Name": pi['Name'],
                "VlocityDataPackType": "SObject",
                "VlocityRecordSObjectType": "%vlocity_namespace%__PromotionItem__c",
                "VlocityRecordSourceKey": f"%vlocity_namespace%__PromotionItem__c/Generated-{self.generate_fixed_length_string(pi['Id'])}"
            }

            allPI.append(piJson)

        return allPI

    def test_main(self):

        restClient.init('mpomigra250')

        code = 'PROMO_NOS_INST_001'
       # code = 'PROMO_NOS_COMP_SERVICE_115'

        promo = self.createPromo(code)
        ples = self.create_PLE(code)
        pis = self.create_PromoItems(code)

        dir = f'TEST3/Promotion/{promo["%vlocity_namespace%__GlobalKey__c"]}'

        aaa = jsonFile.write(f'{dir}/{code}_DataPack.json',promo)
        aaa = jsonFile.write(f'{dir}/{code}_PriceListEntries.json',ples)
        aaa = jsonFile.write(f'{dir}/{code}_PromotionItems.json',pis)

        print()


        
