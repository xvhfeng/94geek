---
layout: post
categories: [c,libev,arch,network]
title: "关于使用libev设计YDB的网络主体结构"
tags: [c,libev,arch,network]
---
####摘要
![car](/img/sol/1.png)
</br>
在前两年中，我在5173写了一个分布式文件系统（以下简称DFS），后来在写完以后因为
某些原因，最后并没有在线上实施（目前5173 online环境上的DFS还是09年的时候部署的
DIY版本的FASTDFS）。后来离开5173后，来到了腾讯文学，再一次需要DFS，所以重新动
工开始写DFS，到目前为止，我一个人写了3个月了，基本的功能差不多了，数据备份和恢
复功能已经完成了1/4，还有一半的完整性同步和整个的单盘恢复还没完成。从5173到腾
讯文学，第二次写DFS，重新设计了DFS的内核框架，纠正了以前犯的一些错误。  
相对于DFS来说，主要的问题有2个，一个是对于磁盘的IO，另外一个是对于网络的IO。这
里我们只要讨论对于网络的IO。  

<!-- more -->
####5173的DFS内核结构
PS:因为我离开5173的时候没有携带任何的源代码，所以以下的代码基本上都是伪代码。  
以前的DFS的网络通讯是基于libevent的，现在的基于libev的，libev是libevent的高性
能版本，原本想自己写一个，但是看过了libev的源码后（虽然看的时候有点吐），还是
决定不折腾，使用libev就行了。所以因为libevent和libev的相关性，其基本的框架应该
都是一样的，但是恰恰就是在这个问题上我犯了错。  
原来的DFS中，nio的结构我是这样定义的  
<pre><code>
    struct spx\_job{
        event\_loop *loop;
        int fd;
        watcher *watcher;
    };
</code></pre>
然后按照每个线程一个loop的原则，初始化了spx_job_pool，供每个network的线程使用
。但是这个结构其实是有问题的，问题就是出在把loop和watcher放在了一起。对于job来
说，它应该只关心watcher，而不用关心loop，而对于线程来说，它需要关心loop，而
watcher只是在loop中排队的一个项而已。但是就像上面这种写法，程序一样也能运行，
但是运行起来的效率就会大打折扣。原因就是在于对于线程多管理了watcher。如果你的
程序需要支撑10k的请求，那么按照上面的结构定义，就需要定义10k个线程，每个线程管
理一个loop和它对应的那个watcher。效率那是相当的低，并且10k的线程也不现实。这个
就是为什么原理的DFS并发上不去的原因。loop和watcher之间的引用变得紧密了，并没有
拆解开。  
####解决方案
那么在现在的DFS中，我解决掉了这个问题，首先把这一整个结构体拆开，变成2个，一个
是job相关性的watcher，一个是线程相关性的loop。  
<pre><code>
    struct spx\_job{
        watcher *w;
        int fd;
    };
</br>
    struct spx\_network\_module{
        event\_loop *loop;
    };
</code></pre>
首先，我们让job主要去关心watcher，相对于watcher，它监听的是一个fd，所以那个fd
也必须时刻跟随着watcher，所以我们把它们两个放在一起；另外一个是nio-module，其
实它仅仅是一个线程池，主要就是负责网络的IO。那么它需要一个loop来管理所有注册到
该module下的watcher。这样，把线程和job分开，我们就可以保证module和watcher之间
的1：n关系了。也就是说，我们可以开n（n等于cpu的核数）个线程，组成一个network
module的线程池，然后我们可以再初始化10k个job，在程序运行的过程中，根据一定的负
载算法，把10k个的job分别注册到不同线程的loop上去。这样，就可以更大的发挥loop和
loop的功效。  


