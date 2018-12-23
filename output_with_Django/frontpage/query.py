from elasticsearch import Elasticsearch
es_client = Elasticsearch("localhost:9200")

# 일반 쿼리문
def query(user_input):
    result = es_client.search(index='nnn',
                              doc_type='disease',
                              body={
                                  "query": {
                                      "multi_match": {
                                          "query": user_input,
                                          "fields": ["diseaseko^3", "treatment", "symptom^2","synonym^0.25"],
                                          "type": "best_fields",
                                          "fuzziness": "auto",
                                          "minimum_should_match": 2
                                      }
                                  },
                                  "highlight": {
                                      "fragment_size": 2000,
                                      "number_of_fragments": 0,
                                      "fields": [
                                          # {"diseaseko": {}},
                                          {"symptom": {}}
                                      ]
                                  }
                              },
                              size = 100)
    return result

# 링크 쿼리문
def link_query(input_link):
    result = es_client.search(index='nnn',
                              doc_type='disease',
                              body={
                                  "query": {
                                      "match": {
                                          "diseaseko": {
                                              "query": input_link,
                                              "fuzziness": "auto",
                                              "minimum_should_match": 2
                                          }
                                      }
                                  }
                              },
                              size = 1)
    return result

# 검색결과 내 재검색 쿼리
def re_query(old,new):
    new_result = es_client.search(index='nnn',
                                  doc_type='disease',
                                  body={
                                      "query": {
                                          "bool": {
                                              "must": {
                                                  "multi_match": {
                                                      "query": old,
                                                      "fields": ["diseaseko^3", "treatment", "symptom^2","synonym^0.25"],
                                                      "type": "best_fields",
                                                      "fuzziness": "auto",
                                                      "minimum_should_match": 2
                                                  }
                                              },
                                              "filter": {
                                                  "match": {
                                                      "symptom": {
                                                          "query": new,
                                                          "fuzziness": "auto",
                                                          "minimum_should_match": 2
                                                      }
                                                  }
                                              }
                                          }
                                      }
                                      ,
                                      "highlight": {
                                          "fragment_size": 2000,
                                          "number_of_fragments": 0,
                                          "fields": [
                                              # {"diseaseko": {}},
                                              {"symptom": {}}
                                          ]
                                      }
                                  },
                                  size=100)
    return new_result