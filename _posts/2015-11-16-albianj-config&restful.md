---
layout: post
categories: [Albianj,java]
title: "腾讯文学内容中心分布式统一框架的设计与实现--配置服务与restful"
tags: [ALbianj,java]
---

####配置系统

作为一个IT从业者，当系统发生故障的时候，经常需要我们快速而准确的去排除，
而且一个很重要的前提是不能让现在已经上线的系统停止下来。这就像是一架飞
机正在正常的飞行，突然引擎出现了问题，这时候需要机械师现场排除故障，而
且不能让飞机降落更不能让飞机掉下来。其中的难度当然是可想而知。正是因为
有了这种需求，我们才需要一个可以在系统运行的时候，可以动态改变系统运行
方式的一种方法，而这种方法对于albianj来说，就是内置一个配置系统。

albianj的配置分为两部分，一部分是albianj依赖的xml配置，它主要负责为
albianj的正常运行提供原信息。这部分的配置目前是无法在运行时更改的，如
果要更改必须停止服务。albianj解决xml配置是提供了一个统一的接口：
IAlbianServiceParser。同样，albianj也提供了一个FreeALbianServiceParser
来保证统一性。但是albianj没有提供一个完整的解析xml的算法，而是提供了一
个完整的xml的parser类：AlbianXmlParser。开发者可以自定义自己的xml解析
接口，解析xml的格式。然后通过使用AlbianXmlParser类来完成对于xml的解析。
这部分信息除了本地加载还可以提供远程加载服务，使用远程加载，可以间接的
实现配置重置，但是我们并没有对这个功能加以很多的测试，所以并不推荐使用。  

重点要讲述的另一部分：动态配置。albianj使用数据库作为动态配置的持久化
层，使用albianj提供的缓存系统作为抵挡高并发的解决方案。albianj的动态配
置为树形结构，级数最多支持6级。理论上每个节点都可以有任意数量的子节点，
并且子节点还可以继续派生子节点，每级子节点都可以作为叶子节点存在，作为
叶子结点的值可以是除二进制外的任意类型。

albianj为配置系统的使用提供了各种不同的接口，包括简单运维的接口也一并
提供了。albianj将动态配置的管理分为：初始化，运行中两部分。结束之所以
不加以考虑是因为albianj使用的是主动+被动的缓存策略，放弃了更改通知这一
原先流行，现在已经落后的策略。需要使用albianj的动态配置系统，必须在第
一次使用的时候或者是缓存集体失效的时候初始化缓存，这一步经常被称之为”
充缓存。albianj还为了解决缓存的集体失效问题，对于不同类型的缓存或者对
于不同用处的缓存做了不同的过期时间处理，对于不经常变动的缓存直接进行了
不过期处理。albianj会自动的发现和使用缓存，和开发者无关。

然后，当缓存失效的时候，albianj会自动的去再次从数据库中获取值并且加载
到缓存中。当albianj的动态配置项发生变动的时候，albianj也会主动的去更新
缓存中的配置项，如果此次通知失败，albianj提供了一个可以控制到具体缓存
项的接口，以维护者或者运维人员手工的去更新缓存。

主动缓存和被动缓存的使用使albianj放弃了原始而容易引起不一致性的通知机
制更新配置项的方法。目前的很多项目基本上都是基于zk来进行动态配置项的一
致性管理，但是因为网络的问题或者是环境的问题，zk其实是无法保证一定会更
新到缓存的，一旦无法更新到缓存，那么就会引起配置项的不一致性。也有团队
使用自己的消息队列来完成一致性的管理，鉴于我们以前使用的经验，这也不是
万无一失的，以前在5173的时候，我们就会经常因为动态配置项不一致而重启我
们的服务器，因为除了重新加载一遍所有的配置项，基本上没有什么办法来应对
这个麻烦的异常。  

albianj的动态缓存在数据库中被分成6个表，每个表存储一级节点的值。对于最
后的5，6节点表来说，数据可能会面临好几个级数的增长。这对于使用albianj
的配置系统来说也不是问题。albianj本身自带路由功能，所以可以方便的将数
据量过于庞大的表进行拆分，只是albianj对于动态缓存的策略是使用父节点进
行拆分，所有同一父节点的子节点必须全部存储在一个表中，以方便albianj加
载数据。

因为动态配置项对于整个系统的重要性，我们对于动态配置项表还增加了一定的
记录处理。每个表都增加了lastmodify，lastmender，createtime，author等信
息，以方便查找最后一个更新的人员来问询更改的目的。也为了方便的对于动态
配置进行控制，albianj还为配置节点信息增加了enable的字段，以方便管理人
员快速的开关该配置项；最后，albianj的动态配置项都不会被删除掉，而是由
albianj进行了“软删除”处理，albianj对于动态配置项增加了isdelete项，以方
便此项控制。

为了更好的识别动态项，albianj特意在id生成器中申请了id为00的id作为动态
配置项的id，以方便维护。

####Restful服务

restful是目前为止albianj所支持的最后一个组件。它是我们的内容中心刚刚起
步的时候才被提起，后来慢慢的被使用的越来越多，直到目前，内容中心和我们
内部的一些接口基本上都走了这个内置的restful。

对于restful，albianj开始其实并无多大的需求，腾讯内部有一个微服务的服务器，
使用tcp来完成内部的通讯，同时带有负载均衡等等功能。但是由于这样或者是
那样的原因，使用起来各种的不便，而内容中心的主要职责是提供一致的接
口，所以其实微服务并不太适合网站的开发，而是适合类似于手机或者是内部的
多任务管理的使用场景。而网站，还是restful这种多服务器平行部署比较适合，
一来比较简单，二来维护和扩展也相对方便。

所以albianj设计和实现了restful的服务。restful的内部构建其实很简单，只
要就是一个类似于MVC的模式，而对于restful来说，V只有两种可能的情况：xml
或者是json，所以这部分基本上就相当于省略了。所以对于restful来说，就是
简单的controller和action。albianj基于jetty二次开发了servlet，重新实现
了doget个dopost接口，并且albianj通过kernnel的集成，使用kernnel提供的
service管理功能，将restful的service全部管理了起来。对于每个action，
albianj提供了AlbianRestfulActionAttribute来标识，每个action还提供了一
个verify的接口，以方便对于每个action进行访问的有效性验证。

为了开发者更好的体验，albianj统一了action的函数签名，albianj提供了一个
访问上下文的AlbianRestfulActionContext对象来管理对于action的访问。
action context中包含了当前上下文的resuest、response、sessionid等等信息，
这些信息都是通过jetty或者是客户端提供而得到了。

当restful的接口返回的时候，对于开发者而言也很简单。albianj也对接口的返
回进行了统一。albianj在action context对象中开放了一个result的属性，开
发者只要将返回值正确的设置到这个属性albianj将会自动的进行返回处理，直接
对开发者进行了透明化的隐藏。
