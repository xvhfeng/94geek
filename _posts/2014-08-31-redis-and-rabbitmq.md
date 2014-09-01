---
layout: post
categories: [arch]
title: "redis vs rabbitmq相关功能介绍和测试"
tags: [arch]
---
####摘要
近日，一py找到我，让我帮忙做一些redis和rabbitmq的功能和性能测试。他们在做项目
的时候要使用到消息队列，以完成25000个节点的数据推送并发，并且需要在接到数据后
，一部分数据在短时间内（最多可能是3s内）必须处理完毕，并且产生后续动作。所以这
一块对于性能的要求相当的高。目前来看，实际情况是我那py那里人手不够，所以在选型
的时候首先要满足尽量少的工作量，换而言之，就是他们最好找一个大而全，并且还能保
证效率的message queue。市面上mq的玩意不少，但是貌似能大规模使用的，并且达到一
定效率的倒是并不多。所以我推荐了2款：redis和rabbitmq。总体上，这两款也算是使用
较多的典型代表了。  
redis，效率强大，mq的功能并不是太完善。并且很多的功能（比如ack）等都需要自己写
代码来使用"贴膏药"的方式弥补；  
rabbitmq，工业级标准的代表，但是一提到工业级基本上就是代表了坑爹。性能肯定是无
法和redis相比，但是强大在功能完善，连RPC都自带了。汗颜......。所以基本上这款是
我py最上心的（PS：人少活多，当然选型的时候选功能多的，自己可以少干很多活。）。  
![redis-vs-rabbitmq](/img/redis-vs-rabbitmq/total.jpg)

<!-- more -->
####redis功能介绍

####rabbitmq功能介绍

####message queue测试结果

####赠品--高可用环境搭建

