---
layout: post
categories: [c,arch]
title: "YDB的内核的模块化设计"
tags: [c,arch]
---
####摘要  
![car](/img/module/1.jpg)
    <br />
ydb是一个公司使用的分布式文件系统，如果有需要，也可以拿来当k-v的storage来使用
。ydb主要应对的一个使用场景就是我们的章节存储，还有的一个可能就是图片的存储。
这些都是典型的k-v模型。  
那么，ydb就很明确了，首先它需要一个服务器端，用来存储k-v结构，然后把key返回给
client，再由client存储到db中；在需要的时候，通过key，就可以从ydb中得到key相应
的value，并且还能对value做相应的更改和删除等操作。  
既然是典型的C-S模型，那么对于Server来说，他需要解决几个问题：网络的交互、内部
job的状态dispatch，disk-io的操作。其中，网络的交互和disk-io都是典型的blacking
操作，需要我们另外想办法解决。  

<!-- more -->
####设计
根据摘要的描述，我们容易的得到ydb的内部其实分成了几个部分：网络，dio，notify。
这3部分相互之间的协作构成了我们整个系统。鉴于这3个部分的共性：它们基本上都是
listen message，然后deal message，最后再把处理完的message dispatch到它的下游（
或者上游）。那么我们就能从这3部分的特性中提炼出来一个大家都拥有的概念，在ydb中
，我们把它称之为module。在ydb中，我们把module定义在spx中，spx_module就是模块的
定义。  
在每一个module中，我们使用到了多线程，即每一个module包含了n个线程，每个线程一
个libev的loop，这样，我们通过通过id或者任何你可以hash的key来确定该request应该
由module中的哪一个thread来处理。因为一个request只会被一个module的一个thread处
理，并且是通过loop来处理的，所以不会出现并发的现象，不需要mutex locker。  
deal function使用的也是callback的方式（PS：虽然callback的方式对于devper来说简
直就是灾难，但是在lib中你也不得不使用这种简单而高效的方式，就算我是callback编
程的反对者，但是也无济于事）。  
spx-module是一个base module，每个module都会拥有自己的功能，所以我们在spx中根据
ydb的需要，也根据通常的需要，我们定义了
notifier-module,network-module,task-module.它们分别用来处理网络连接的通知、网
络的读取和写入、任务的处理。在spx中定义的只是最基本的module操作，相对于ydb来说
，它还有自定义的notifier，network，task模块。因为ydb的特殊性，在ydb的task
module中，我们还使用thread的loop来处理对于dio的noblacking操作。  
####结构说明
![car](/img/module/dim.png)
<br />
![car](/img/module/cs.png)





