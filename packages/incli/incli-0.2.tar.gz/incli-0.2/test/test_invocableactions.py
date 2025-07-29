import unittest
from incli.sfapi import restClient,invocableactions
#import traceback
import time
import simplejson
from collections import defaultdict


class Test_InvocableActions(unittest.TestCase):
  def test_actions(self):
    restClient.init('NOSDEV')
    res = invocableactions.listInvocableActions()

    a=1

  def test_vlocity_cmt__CpqCartGetOffersInvocable(self):
      restClient.init('NOSDEV')

      data = {
         'cartId' : '801AU00000oRUejYAG'
      }
      data = {
        "inputs": [
          {
            "cartId": "801AU00000oRUejYAG"
          }
        ]
      }
      #data = {"cartId":"801AU00000oRUejYAG","noFilteredResponse":"false"}
      #data = simplejson.dumps(data)
      #data = [{"cartId":"801AU00000oRUejYAG","isloggedIn":true,"noFilteredResponse":"false"}]
      res = restClient.callAPI(action='/services/data/v63.0/actions/custom/apex/vlocity_cmt__CpqCartGetOffersInvocable',method='post',data=data)

      a=1

  def test_vlocity_cmt__CpqCartItemsInvocable(self):
      restClient.init('NOSDEV')

      data = {
         'cartId' : '801AU00000oRUejYAG'
      }
      data = {
        "inputs": [
          {
            "cartId": "801AU00000oRUejYAG"
          }
        ]
      }
      #data = {"cartId":"801AU00000oRUejYAG","noFilteredResponse":"false"}
      #data = simplejson.dumps(data)
      #data = [{"cartId":"801AU00000oRUejYAG","isloggedIn":true,"noFilteredResponse":"false"}]
      res = restClient.callAPI(action='/services/data/v63.0/actions/custom/apex/vlocity_cmt__CpqCartGetCartItemsInvocable',method='post',data=data)

      a=1

