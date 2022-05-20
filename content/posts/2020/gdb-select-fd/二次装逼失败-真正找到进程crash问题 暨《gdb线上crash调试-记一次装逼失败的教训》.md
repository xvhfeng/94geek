Title: 二次装逼失败-真正找到进程crash问题 暨《gdb线上crash调试-记一次装逼失败的教训》
Date: 2020-06-08
Category: 调试
Tags: 调试
Slug: gdb-select-fd
Author: spk xu
Status: published
Summary:很早之前，写过一遍文章[gdb线上crash调试-记一次装逼失败的教训]({filename}../../2017/gdb-stacksize/2017-06-27-gdb-stacksize.md)，这篇文章主要讲了我使用gdb来调试一次进程crash事件。当时因为没有注意core文件中参数的问题，导致了其实找到的问题引起点是错误的。问题再次出现，进程又crash了。

可惜这是一次完完全全的装逼不成反被X的典型例子。

但是，这是二次装逼失败，嗯！是真正的装逼失败!

对不起大家，学艺不精，有待更加努力！ 

## 背景
很早之前，我写过一遍文章[gdb线上crash调试-记一次装逼失败的教训]({filename}../../2017/gdb-stacksize/2017-06-27-gdb-stacksize.md)，这篇文章主要讲了我使用gdb来调试一次进程crash事件。当时因为没有注意core文件中参数的问题，导致了其实找到的问题引起点是错误的。

为什么我们后来知道当时找到问题的点错误了呢？嗯....因为问题再次出现，进程又crash了。

## 再次排查
其实上一次gdb的操作方法都对，但我们分析的路走错了，找了一个错误的方向。

首先，我们发现stack的sym信息没了，然后我们靠寄存器恢复stack的信息。恢复stack的信息后我们再定位到调用的函数，进行分析。这个套路没有错，但是我们却大意了stack信息中的参数问题。

具体的前面的操作我就不累述了，需要了解的请看前文《[gdb线上crash调试-记一次装逼失败的教训]({filename}../../2017/gdb-stacksize/2017-06-27-gdb-stacksize.md)。

我们开始这次的分析。为了对比，我就拿上一次的截图来分析：

![图片](4.png)

上一次我们分析到这儿的时候，我们被stack的乱序给迷惑了。以至于出现了最基本的debug错误：未观察参数就乱下定论。现在冷静下来，好好研究一下：

从图上可以看到，在spx_socket_connect_nb函数的下面，是一排hex的数字。这些数字是什么？其实这些就是stack上的变量，紧靠函数的就是这个函数的参数（这段不熟悉或者不清楚的可以看一下微机原理或者计算机原理的相关书籍）。spx_socket_connect_nb有4个参数，分别是fd，ip，port和timeout，所以这里紧邻着的就是这4个参数信息。友情提醒一下：因为stack的特性，在运行时，参数的顺序和代码中参数的顺序正好的颠倒的。也即代码中第一个参数，在运行时是最后一个；而代码中最后一个是运行时的第一个。这也就是stack的特性。

下来我们分析一下这4个参数，根据stack的特性，我们能得到这样一个list：
	 
1. x1d -> timeout 算到十进制为30
2. 0x10360...000le -> port 算到十进制是4150。我们展开讲一下，从timeout我们能看出，这台机器的内存为高寻址机器。为啥？因为0x1d在最前面，如果低寻址，那么应该是0x0..01d.所以，同理我们知道0x1036其实就是port的值，那么又为什么后面还有00le，而我们没有计算在内呢？那是因为port是一个int型参数，所以主要前面的32位即可。但机器是64位，所以每个显示是64位的int而已，而存在le，是因为c的stack内存要在需要使用的时候才会清零，在这里这段其实就是内存垃圾。
3. 0x1292928 -> ip 不用计算，因为ip本来就是一个指针，这即指针而已。
4. 0x4c30...0 ->fd,换算到十进制是1219.换算原理同上面的port。
    
至此，我们的参数分析结束。从参数分析看，好像没问题。然后我们看一下我们的代码。

		
		  err_t spx_socket_connect_nb(int fd,string_t ip,int port,u32_t timeout){  
		      struct sockaddr_in addr;  
		      bzero(&addr,sizeof(addr));  
		      addr.sin_family = AF_INET;  
		      addr.sin_port=htons(port);  
		      addr.sin_addr.s_addr = inet_addr(ip);  
		      err_t err = 0;  
		      err_t rc = 0;  
		      if(0 > connect(fd,(struct sockaddr *) &addr,sizeof(addr))){  
		          //filter this errno,  
		          //socket is not connect to server and return at once  
		          if (EINPROGRESS == errno) {  
		              struct timeval tv;  
		              SpxZero(tv);  
		              tv.tv_sec = timeout;  
		              tv.tv_usec = 0;  
		              fd_set frd;  
		              FD_ZERO(&frd);  
		              FD_SET(fd,&frd);  
		              socklen_t len = sizeof(err);  
		              if (0 < (rc = select (fd+1 , NULL,&frd,NULL,&tv))) {  
		                  if(0 > getsockopt(fd,SOL_SOCKET,SO_ERROR,(void*)(&err),&len)) {  
		                      err = errno;  
		                      return err;  
		                  }  
		                  if (0 != err) {  
		                      return err;  
		                  }  
		              } else if(0 == rc) {  
		                  err = ETIMEDOUT;  
		                  return err;  
		              } else {  
		                  err = EXDEV;  
		                  return err;  
		              }  
		              SpxErrReset;  
		              return 0;  
		          } else {  
		              return errno;  
		          }  
		      }  
		      return 0;  
		  }

从代码中我们得到这样的信息：在解决socket的nonblocking的时候，使用的api是select。man一下select，手册中说明该api可以监控的fd最大不能超过1024.而我们的fd是1219.显然超过了最大的fd限度，导致了fd的溢出。

到这里，找到了真正的问题。

下面我们解释一下这个问题出现的现象原因。

这个问题很少出现，从我们上线到现在一共5年一共出现了2次。第一次就是上次定位错误，再来就是这一次。为什么要那么久才出现或者说不是必现呢？原因如下:

1. 当传递给select的fd小于1024的时候，此程序一切正常，并不会溢出。而只有当fd大于1024的时候才会crash;
2. spx_socket_connect_nb这个函数是心跳函数，每30s一次。虽然很频繁，每次都会open一个新的fd，但是鉴于fd的reuse技术，fd大于1024的可能性比较小，只有当连接非常多的时候才会出此问题

这就造成了一个不经常出现，一出现就crash的现象。这也就是为什么我们第一次排查后，找错了地方，但是启动后却是正常运行了。其实调整stacksize的值并没有什么用。有用的是，再次启动进程时，fd被清零。相当于fd又从最小的开始，所以不管你是不是调整了stacksize的值，只要重启一般都不会再出问题，除非瞬间的链接压力特别大，导致fd短期内再次超过1024并且还要正好被这个心跳线程open fd的时候获取才会再次出现。这种概率其实是非常非常小的。

那么怎么改正呢？只要把select的api改成poll即可，代码如下：

		
		 err_t spx_socket_connect_nb(int fd, string_t ip, int port, u32_t timeout) {  
		    struct sockaddr_in addr;  
		    bzero(&addr, sizeof(addr));  
		    addr.sin_family = AF_INET;  
		    addr.sin_port = htons(port);  
		    addr.sin_addr.s_addr = inet_addr(ip);  
		    err_t err = 0;  
		    err_t rc = 0;  
		    if (0 > connect(fd, (struct sockaddr *) &addr, sizeof(addr))) {  
		        //filter this errno,socket is not connect to server and return at once  
		        if (EINPROGRESS == errno) {  
		            socklen_t len = sizeof(err);  
		            struct pollfd p;  
		            p.fd = fd;  
		            p.events = POLLOUT;  
		            if (0 < (rc = poll(&p, 1, timeout * 1000))) {  
		                if (0 > getsockopt(fd, SOL_SOCKET, SO_ERROR, (void *) (&err), &len)) {  
		                    err = errno;  
		                    return err;  
		                }  
		                if (0 != err) {  
		                    return err;  
		                }  
		            } else if (0 == rc) {  
		                err = ETIMEDOUT;  
		                return err;  
		            } else {  
		                err = errno == 0 ? EXDEV : errno;  
		                return err;  
		            }  
		            SpxErrReset;  
		            return 0;  
		        } else {  
		            return errno;  
		        }  
		    }  
		    return 0;  
		 }

莫装逼，装逼遭雷劈;  

莫装帅，装帅遭人踹;  

莫装吊，装吊遭狗咬…
