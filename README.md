# required interpreter
Python 3.6
# Overview
* Publisher
    * Queue を作る人
* Store
    * Queue を蓄える人
* Subscriber
    * Queue をもらう人
# Queue
## Required
* order
    * Type: String
    * Store が Queue を push する際にキーとして使用する
    * Subscriber が Queue を pop する際にキーとして使用する
* receipt
    * Type: Dictionary
    * Store が Queue を push する際に値として使用する
    * Subscriber がジョブを判断するために使用する
    * receipt の内容は Publisher と Subscriber 次第とする
# Run
## store
1. boot store api
`docker-compose up -d store`
1. push queue
`curl -X POST -d '{"order": "some order", "receipt": {"something":"something"}}' http://{{store}}`
1. pop queue
`curl -X GET http://{{store}}?order=some order&limit=1`
## sample publisher with HTTP Request
`docker-compose run --rm publisher`
## sample subscriber with HTTP Request
`docker-compose run --rm subscriber`

