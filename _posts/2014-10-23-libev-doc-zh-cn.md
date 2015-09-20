---
layout: post
categories: [c,libev]
title: "libev文档中文版--简介"
tags: [c,libev]
---

libev - a high performance full-featured event loop written in C  
libev-一个用c写成的全功能事件循环库（PS：event loop不知道怎么翻译好）。

SYNOPSIS  
简介  
```
	#include <ev.h>
```

<!-- more -->
EXAMPLE PROGRAM  
示例程序
<code>

    // a single header file is required
    // 需要包含ev.h头文件
    #include <ev.h>
    #include <stdio.h> // for puts
	// every watcher type has its own typedef'd struct
	// with the name ev_TYPE
	// 每一个观察者（watcher，以下还是用watcher吧，这种名称用中文很别扭）都有一个自己的结构体，
    // 结构体名称形如ev_TYPE

    ev_io stdin_watcher;
    ev_timer timeout_watcher;

	// all watcher callbacks have a similar signature
	// this callback is called when data is readable on stdin
	//所有的watcher回调函数也都有同样的函数签名
	//当stdin可读的时候，执行回调函数
	static void stdin_cb (EV_P_ ev_io *w, int revents) {
    	puts ("stdin ready");
    	//for one-shot events, one must manually stop the watcher
    	// with its corresponding stop function.
		// 对于一次性事件来说，我们必须使用watcher的相应停止函数来手动停止这个watcher
		//译者注：它的意思是对于一次性的事件，我们必须使用不同类型相应的函数来停止这个watcher在loop中继续被监视（比如，对于IO事件就是ev_io_stop,对于time事件  就是ev_time_stop）
     	ev_io_stop (EV_A_ w);

    	// this causes all nested ev_run's to stop iterating
		//停止对于EV_A（loop）的所有迭代（其实就是停止loop的运行，释放全部的watcher）
    	ev_break (EV_A_ EVBREAK_ALL);
    }

	// another callback, this time for a time-out
	//另外一个回调函数，是事件过期调用的
   	static void timeout_cb (EV_P_ ev_timer *w, int revents) {
  		puts ("timeout");
     	// this causes the innermost ev_run to stop iterating
		//停止当前loop循环
    	ev_break (EV_A_ EVBREAK_ONE);
	}
    
    int main (void) {
    	// use the default event loop unless you have special needs
		//使用默认的event loop除非你有特别的需求
         struct ev_loop *loop = EV_DEFAULT;

         // initialise an io watcher, then start it
         // this one will watch for stdin to become readable
        //初始化一个io watcher，将事件和loop关联
        //这个watcher监视stdin是否可读
         ev_io_init (&stdin_watcher, stdin_cb, /*STDIN_FILENO*/ 0, EV_READ);
         ev_io_start (loop, &stdin_watcher);

         // initialise a timer watcher, then start it
         // simple non-repeating 5.5 second timeout
        //初始化一个超时watcher，并将事件和loop关联
        //简单的非重复5.5s超时
         ev_timer_init (&timeout_watcher, timeout_cb, 5.5, 0.);
         ev_timer_start (loop, &timeout_watcher);

         // now wait for events to arrive
        //开始监听事件
         ev_run (loop, 0);

         // break was called, so exit
     	return 0;
  	 }

</code>
ABOUT THIS DOCUMENT  
关于这个文档  

This document documents the libev software package.  
这份文档记录了libev这个软件开发包。

The newest version of this document is also available as an html-formatted web page you might find easier to navigate when reading it for the first time: http://pod.tst.eu/http://cvs.schmorp.de/libev/ev.pod.  
这个文档最新的版本是一个html，你可以在这里找到它：http://pod.tst.eu/http://cvs.schmorp.de/libev/ev.pod.


While this document tries to be as complete as possible in documenting libev, its usage and the rationale behind its design, it is not a tutorial on event-based programming, nor will it introduce event-based programming with libev.  
尽管这篇文档试着尽可能详细的说明libev，他的使用方法和背后的设计理念，这不是一个基于事件编程的教程，也不会使用libev来引入事件编程（这句话怎么怪怪的？有更好的翻译嘛？）  

Familiarity with event based programming techniques in general is assumed throughout this document.  
这篇文档都假定你熟悉基于事件的编程技术  

WHAT TO READ WHEN IN A HURRY  

This manual tries to be very detailed, but unfortunately, this also makes it very long. If you just want to know the basics of libev, I suggest reading ANATOMY OF A WATCHER, then the EXAMPLE PROGRAM above and look up the missing functions in GLOBAL FUNCTIONS and the ev_io and ev_timer sections in WATCHER TYPES.  
这个手册试着说明的非常详细，但不幸的是，这也将让它变的很长。如果你只是想了解
libev的基础知识，我建议读ANATOMY OF A WATCHER章节。示例程序在它上面，缺少的函
数在GLOBAL FUNCTIONS章节中找，ev\_io和ev_timer部分在WATCHER TYPES章节  


