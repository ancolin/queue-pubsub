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
    