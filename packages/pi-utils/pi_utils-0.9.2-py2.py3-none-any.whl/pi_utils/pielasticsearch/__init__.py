#!/usr/bin/env python3

import elasticsearch
import json
import copy

import inspect

class Pies(elasticsearch.Elasticsearch):

    def pisearch(self, body=None, index=None, doc_type=None, params=None, headers=None, *args, **kargs):
        return self.search(body=body, index=index, doc_type=doc_type, params=params, headers=headers, *args, **kargs)

    """
    一次性返回所有 search
    """
    def pisearch_return_all(self, body=None, index=None, doc_type=None, params=None, headers=None, scroll = '2s', request_timeout=2, *args, **kargs):
        resp = self.search(body = body, index=index, doc_type=doc_type, params=params, headers=headers, scroll = scroll, request_timeout=request_timeout, *args, **kargs)
        ret = copy.deepcopy(resp)
        l = []
        while len(resp['hits']['hits']):
            l = l + resp['hits']['hits']
            resp = self.scroll(
                scroll_id = resp['_scroll_id'],
                scroll = '2s'
            )
        ret['hits']['hits'] = l   
        return ret


    """
    返回一定时间的 search
    """
    def pisearch_time(self, timeStart, timeEnd, is_realtime = None, body=None, index=None, doc_type=None, params=None, headers=None, *args, **kargs):
        match_all = {
           "sort": [
                {
                   "t": {
                       "order": "asc",
                       "unmapped_type": "boolean"
                    }
                }
            ],
           "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                           "match_all": {}
                        },
                        {
                           "range": {
                               "t": {
                                   "gte": timeStart.isoformat('T'),
                                   "lte": timeEnd.isoformat('T')
                                }
                            }
                        }
                   ],
                   "should": [],
                   "must_not": []
               }
            },
        }

        if is_realtime != None:
            match_all['query']['bool']['filter'].append({'match_phrase':{'is_realtime':{'query':is_realtime}}})
        ret = self.search(index = index,body = match_all,*args, **kargs)

        self.last_scroll_id = ret['_scroll_id'] if ('_scroll_id' in ret) else None

        return ret['hits']['hits'], ret['hits']['total']['value'],ret['_scroll_id'] if ('_scroll_id' in ret) else None
        
        
    def search_next(self, scroll_id = None, scroll = '2s'):
        if not scroll_id:
            scroll_id = self.last_scroll_id

        ret = self.scroll(scroll_id = scroll_id, scroll = scroll)

        self.last_scroll_id = ret['_scroll_id'] if ('_scroll_id' in ret) else None
        return ret['hits']['hits'], ret['_scroll_id'] if ('_scroll_id' in ret) else None

    


        

    