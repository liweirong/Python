MapReduce是一个用于处理海量数据的分布式计算框架，解决数据量大，可以切分进行计算
这个框架解决了
    * 数据分布式存储
	* 作业调度
	* 容错
	* 机器间通信等复杂问题

MapReduce分而治之思想 --  分解->求解->合并
    map：把复杂问题分解成若干的简单“任务”
    reduce：合并分解结果