---
layout: post
categories: [arch]
title: "redis vs rabbitmq队列功能介绍和测试"
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
<b>注意：本文只对redis和rabbitmq作为队列进行比较。</b>  
![redis-vs-rabbitmq](/img/redis-vs-rabbitmq/total.jpg)

<!-- more -->
####redis功能介绍
#####特性
1. 有现成的message功能；  
2. 性能强劲，eventloop，单进程，几乎能吃掉整个cpu（多核好像不在此列）；  
3. 有简单的分布式(可以使用M/S模式)，或者自己做集群；  
4. 支持IO，但是一般都是slave做；  

#####缺点
1. 对使用人员，不管是运维还是开发者要求都比较高;  
2. 对于功能完备的msg功能，比如ack，得另外想办法解决；  
3. 线程的msg会因为没有客户端监听丢失消息（不知道是不是我的环境问题造成的）；  
4. 自己完成M/S角色的转换，避免内存全部被清空；  

####rabbitmq功能介绍
#####特性
1. AMQP的工业标准，这个就不用多说了吧，代表了的东西太多，自己领会吧；  
2. 支持分布式，客户端比较多，还有官方的mgr插件；  
3. 通过erlang，可以支持分布式；  
4. 对于使用者的要求没有redis高，简单很多；  
5. 支持IO，和redis一样，一般也是slave做；  

#####缺点
1. 功能多，交的复杂税就多，所以庞大复杂；  
2. 性能不咋地，相比redis，差的不是一个数量级；  
3. 名词多，整个rabbitmq的过程有9个名词，理解起来还是挺费力；  

####message queue测试
#####情况和介绍
1. 使用单机，sender后入recver都是一台机器（没机器，我是一台mac，mac上的虚拟机
都是要钱的，穷，买不起，又不想用D版）；  
2. 不做多线程，只做单进程单线程，因为多线程的sender对于rabbitmq不公平；  
3. send和recv不是同时的，都是一起send，一起recv，这样能最大限度的避免cpu的
切换；  
4. 我的是mac，cpu是1.3g的i5，内存8g，没开io，所以磁盘无所谓；  

#####测试代码
我只贴出来一部分代码，一些简单的代码就不贴出来了。  
redis send with ack like topic
<pre><code>
        public static void SubscribePattern(String msg) {
		Jedis jedis = null;
		try {
			jedis = new Jedis("127.0.0.1", 6379);
			RedisMessageWithAck m1 = new RedisMessageWithAck("list2message_1",
					msg);
			jedis.lpush("list2message_1",JSONObject.fromObject(m1).toString());
			jedis.zadd("set_list2message_1",getTimeStamp(),JSONObject.fromObject(m1).toString());
			RedisMessageWithAck m2 = new RedisMessageWithAck("list2message_2",
					msg);
			jedis.lpush("list2message_2",JSONObject.fromObject(m2).toString());
			jedis.zadd("set_list2message_2",getTimeStamp(),JSONObject.fromObject(m2).toString());
			RedisMessageWithAck m3 = new RedisMessageWithAck("list2message_3",
					msg);
			jedis.lpush("list2message_3",JSONObject.fromObject(m3).toString());
			jedis.zadd("set_list2message_3",getTimeStamp(),JSONObject.fromObject(m3).toString());
			RedisMessageWithAck m4 = new RedisMessageWithAck("list2message_4",
					msg);
			jedis.lpush("list2message_4",JSONObject.fromObject(m4).toString());
			jedis.zadd("set_list2message_4",getTimeStamp(),JSONObject.fromObject(m4).toString());
		} catch (Exception e) {
			System.out.println(e);
		} finally {
			if (null != jedis) {
				jedis.close();
			}
		}
	}
</code></pre>
</br>
redis recv with ack like topic
<pre><code>
    public static void SubscribePattern() {
		long time = getTimeStamp();
		Jedis jedis = null;
		try {
			jedis = new Jedis("127.0.0.1", 6379, 30);
			while (true) {
				Set<String> old_channel = jedis.keys("set_list2message_*");
				if (null != old_channel && 0 != old_channel.size()) {
					Iterator<String> i = old_channel.iterator();
					while (i.hasNext()) {
						String s = i.next();
						Set<String> old = jedis.zrangeByScore(s, 0, time);
						if (null != old && 0 != old.size()) {
							Iterator<String> it = old.iterator();
							while (it.hasNext()) {
								String sv = it.next();
								JSONObject jsonObject = JSONObject
										.fromObject(sv);
								System.out.println(jsonObject);
								RedisMessageWithAck bean = (RedisMessageWithAck) JSONObject
										.toBean(jsonObject);
								System.out.println(bean.getChannel() + ":"
										+ bean.getMsg());
								jedis.zrem("set_" + bean.getChannel(), sv);// ack
							}
						}
					}
				}
				Set<String> keys = jedis.keys("list2message_*");
				if (null == keys || 0 == keys.size()) {
					continue;
				}
				String[] ks = new String[keys.size()];
				keys.toArray(ks);
				List<String> mess = null;
				do {
					mess = jedis.brpop(0, ks);
				} while (null == mess);
				for (int i = 0; i < mess.size(); i++) {
					JSONObject jsonObject = JSONObject.fromObject(mess.get(i));
					System.out.println(jsonObject);
					RedisMessageWithAck bean = (RedisMessageWithAck) JSONObject
							.toBean(jsonObject);
					System.out.println(bean.getChannel() + ":" + bean.getMsg());
					jedis.zrem("set_" + bean.getChannel(), mess.get(i));// ack
					System.out.println(mess.get(i));
				}
			}
		} catch (Exception e) {
			System.out.println(e);
		} finally {
			if (null != jedis) {
				jedis.close();
			}
		}
</code></pre>
</br>
rabbitmq send with topic
<pre><code>
public static void publish(String msg) throws IOException {
		ConnectionFactory connFac = new ConnectionFactory();
		connFac.setHost(RmqMsgInfo.Ip);
		Connection conn = null;
		Channel channel = null;
		try {
			conn = connFac.newConnection();
			channel = conn.createChannel();
			String exchangeName = RmqMsgInfo.MsgExchangeForTopic;
			String messageType = RmqMsgInfo.MsgExchangeNameForTopic;
			channel.exchangeDeclare(exchangeName, "topic");
			channel.basicPublish(exchangeName, messageType, null,
					msg.getBytes());
			System.out.println("send message[" + msg + "] to " + exchangeName
					+ " success!");
		} catch (Exception e) {
			System.err.println(e);
		} finally {
			if (null != channel)
				channel.close();
			if (null != conn)
				conn.close();
		}
	}
</code></pre>
    </br>
rabbitmq recv with topic
<pre><code>
public static void subscribe() throws IOException {
		ConnectionFactory connFac = new ConnectionFactory();
		connFac.setHost(RmqMsgInfo.Ip);
		Connection conn = null;
		Channel channel = null;
		try {
			conn = connFac.newConnection();
			channel = conn.createChannel();
			String exchangeName = RmqMsgInfo.MsgExchangeForTopic;
			channel.exchangeDeclare(exchangeName, "topic");
			String queueName = channel.queueDeclare().getQueue();
			channel.queueBind(queueName, exchangeName,
					RmqMsgInfo.MsgExchangePatternForTopic);
			QueueingConsumer consumer = new QueueingConsumer(channel);
			boolean autoack = true;
			channel.basicConsume(queueName, autoack, consumer); // 为了高性能，必须这样用，不要用basic.get
			int i = 0;
			while (true) {
				Delivery delivery = consumer.nextDelivery();
				String msg = new String(delivery.getBody());
				System.out.println("idx:" + i + "received message[" + msg + "] from "
						+ exchangeName);
				if(i == 9999) break;
				i++;
			}
		} catch (Exception e) {
			System.err.println(e);
		} finally {
			if (null != channel)
				channel.close();
			if (null != conn)
				conn.close();
		}
	}
</code></pre>

#####测试结果
10000次循环，看需要多少时间  
![result](/img/redis-vs-rabbitmq/rc.png)
</br>
分析其原因主要还是可以这些问题导致的：  
1. redis是单进程单线程，rabbitmq是本身就支持分布式的，但是erlang复制消息肯定还
是需要时间，比redis的指针指向慢很多；  
2. redis功能简单，流水线短，rabbitmq功能复杂，流水线长，缴税多了；  
3. c相比erlang是不是还是有运行上的优势？  
4. 不测多客户并发了，测试并发rabbitmq估计吃亏还要多；  
####建议和意见
1. 如果人手够，redis可以维护和运维，那么首选redis；  
2. 如果rabbitmq能满足压力，但是rabbitmq会比较省心；  
3. 如果数据量大，并发大，还是redis；  
4. 在互联网行业，没有理由不是首选redis；  

