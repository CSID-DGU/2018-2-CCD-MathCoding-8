# Elasticsearch

## elasticsearch에 logstash를 통해 json 파일 업로드 시키는 방법

1. elasticsearch에서 제공하는 nori_tokenizer를 이용하기 위해 index의 settings을 먼저 설정해준다

PUT index명

{
  "settings": {
    "index": {
      "analysis": {
        "tokenizer": {
          "nori_user_dict": {
            "type": "nori_tokenizer",
            "decompound_mode": "mixed",
            "tokenizer" : "nori_tokenizer"
          }
        },
        "analyzer": {
          "my_analyzer": {
            "type": "custom",
            "tokenizer": "nori_user_dict"
          }
        }
      }
    }
  }
}
