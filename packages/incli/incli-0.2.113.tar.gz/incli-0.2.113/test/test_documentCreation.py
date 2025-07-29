import unittest
from incli.sfapi import restClient,DR_IP

class Test_DocumentCreation(unittest.TestCase):
    def test_doc1(self):
        restClient.init('NOSDEV')

        inputdata = {
            "inputData": {
                "Application": "APP NOS",
                "TVExtra": {
                    "TVExtraName": "Não aplicável"
                },
                "VFItems": {
                    "VFName": "Não aplicável"
                },
                "IFItems": {
                    "IFName": "Não aplicável"
                },
                "IF_OtherPricingEquipments": True,
                "ShippingEquipments": "Cartão SIM",
                "BillingPaymentMethod": "Débito Direto",
                "ShippingAddressPostalCode": None,
                "CustomerNIF": "103867848",
                "BillingInvoiceDispatch": "Eletrónica",
                "ShippingAddressStreet": None,
                "CustomerName": "TESTTEAM MRC VOUCHER",
                "IF_IdDataAccept": False,
                "TVItems": {
                    "Channels": None,
                    "TVName": "Inclui 80 canais TV e 20 canais de radio - nos.pt/lista-canais",
                    "TVNameSMS": "Inclui 80 canais TV e 20 canais de radio"
                },
                "BillingAddressStreet": "RUA DAS TORRES SN 3 RÉS DO CHÃO   LJ",
                "IF_UsageDataAccept": True,
                "ShippingAddressCity": None,
                "ExtraIFItems": [],
                "ServiceAccountId": "S1000099047",
                "IFSpeed": "Não aplicável",
                "ExtraTVItems": [
                    {
                        "ExtraTVService": "1 Sport TV Premium HD €27,99"
                    }
                ],
                "IF_OldSatelliteEquipment": False,
                "PricingEquipment": [
                    {
                        "PricingEquipmentPrice": "€3,65",
                        "PricingEquipmentBasePrice": "€3,65",
                        "PricingEquipmentName": "1 Box 1.0 HD"
                    }
                ],
                "EffTotalPackNRC": "€0,00",
                "IMItems": [
                    {
                        "IMName": "Não aplicável"
                    }
                ],
                "BillingAccountNumber": "1.60113091",
                "ShippingAddressFloor": None,
                "DocumentReleaseMonthNo": 1,
                "VMItems": [
                    {
                        "VMName": "Inclui 1 cartão WTF, com 3.500 min, 3.500 SMS e 20GB dados (em roaming 16,17GB)."
                    },
                    {
                        "VMName": "Inclui 1 cartão À medida, com 200 min/SMS e 100MB de dados."
                    }
                ],
                "OfferName": "NOS TV Max",
                "AgentCompany": "200000-CATVP-TV CABO PORTUGAL,",
                "ShippingTime": None,
                "LoyaltyAmount": "€180,00",
                "TotalBenefits": "€180,00",
                "PreviousValue": "-",
                "ScheduleContact": None,
                "DocumentReleaseDate": "20 Janeiro 2025",
                "NewCartPrice": "€73,03",
                "NotificationLoyalty": "€7,50 durante 24 meses = €180,00.",
                "ShippingContact": None,
                "IF_ValueAddedServicesAccept": True,
                "PricingServices": [
                    {
                        "PricingServicesPrice": "€27,99",
                        "PricingServicesBasePrice": "€27,99",
                        "PricingServicesName": "1 Sport TV Premium HD"
                    }
                ],
                "InstallAddressStreet": "Rua das Torres",
                "CustomerNumber": "C1000098933",
                "VMPolicies": "Consulte as Políticas de Utilização Responsável e as condições detalhadas em nos.pt/polRoaming",
                "OrderType": "ALTERAÇÃO",
                "DiscountNRC": "€0,00",
                "VFExtra": [
                    {
                        "VFExtraName": "Não aplicável"
                    }
                ],
                "ServiceAccountSFId": "a3lAU000000trIDYAY",
                "CustomerContact": "927602912",
                "IF_SGPSAccept": True,
                "ExtraEquipment": [
                    {
                        "ExtraEquipmentName": "1 Box 1.0 HD"
                    }
                ],
                "OtherEquipLabel": "Equipamentos",
                "BillingInvoiceType": "Resumida",
                "IF_OtherPricingServices": True,
                "AccountId": "C1000098933",
                "ExtraVMItems": [],
                "LoyaltyPromotionExtraMessage": "[1]Se esgotar plafond de net, será ativado automaticamente um pacote de 200MB/ €2,99 (máx. 5), válido até ao fim do mês. Pode gerir os dados na app, área cliente, linha apoio ou loja NOS. Se não pretende esta funcionalidade,ligue 931699000 ou 16990.",
                "Sysdate": "20-01-2025",
                "AgentCode": "71005102",
                "ExtraEquipItems": [
                    {
                        "ExtraEquipService": "1 Box 1.0 HD €3,65"
                    }
                ],
                "IF_FISDocGeneration": True,
                "IF_B2C_Customer": True,
                "ExtraIMItems": [],
                "IF_OldCableEquipment": False,
                "LoyaltyPeriod": 24,
                "IMExtra": [
                    {
                        "IMExtraName": "Não aplicável"
                    }
                ],
                "InstallAddressFloor": "Rés do Chão   LJ",
                "VMExtra": [
                    {
                        "VMExtraName": "Não aplicável"
                    }
                ],
                "CustomerEmail": "testingstreamnos+wwlxdgh@gmail.com",
                "ShippingPersonToContact": None,
                "InstallAddressPostalCode": "7595-124",
                "VMSpeed": "WTF: 500 Mbps/50 Mbps,À medida: 40 Mbps/20 Mbps",
                "InstallAddressDoor": "SN 3",
                "BillingAddressCity": "TORRÃO",
                "CustomerDocId": "30212410",
                "OtherServicesLabel": "Outros Serviços",
                "LoyaltyPeriodDesc": "24 meses",
                "IF_NewNetEquipment": False,
                "ExtraCharges": [
                    {
                        "ExtraChargesName": "Não aplicável"
                    }
                ],
                "MrcExtraInfo": "Os valores apresentados incluem o IVA à taxa legal em vigor",
                "SaleConfirmationTextFooter": "20/01/202509:35:57 CATVP-TV CABO PORTUGAL, S.A. 71005102-Alberto Rodriguez PRC100050440",
                "ServiceAccountNumber": "S1000099047",
                "BundlePrice": "€41,39",
                "NewCartBasePrice": "€73,03",
                "PersonId": "P118873005",
                "ExtraVFItems": [],
                "NotificationMessages": [
                    {
                        "MarketingMessage": "Preço especial (inc. desconto de €1) mediante fatura eletrónica e débito direto ativos."
                    }
                ],
                "BillingAddressPostalCode": "7595-124",
                "IF_OldNetEquipment": False,
                "BillingContactEmail": "testingstreamnos+wwlxdgh@gmail.com/927602912",
                "RequestId": "a3lAU000000jcIrYAI",
                "IF_NewCableEquipment": False,
                "DocumentReleaseDay": 20,
                "AgentName": "Alberto Rodriguez",
                "OmniProcessId": "a3lAU000000jcIrYAI",
                "BundleBasePrice": "€41,39",
                "NetExtraInfo": "As velocidades podem variar em função de diversos fatores que não dependem do controlo da NOS. Informação sobre fatores influenciadores em nos.pt/vel",
                "IF_NewSatelliteEquipment": False,
                "DocumentReleaseYear": 2025,
                "ShippingAddressDoor": None,
                "InstallAddressCity": "Torrão",
                "PreviousValueText": "-",
                "BillingIBAN": "PT75003506516741496986791"
            }
        }


        res = DR_IP.ip(name='unai_GenerateCustomerDocumentation',input=inputdata)

        for document in res['IPResult']['documents']:
            if document['type'] == 'FISDocument':
                data = {
                    "jobId": document['jobId']
                }
                res2 = DR_IP.ip(name='DocumentService_GetDocument',input=data)
                

        a=1




       


