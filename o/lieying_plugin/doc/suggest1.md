:: suggest1.md, for parse_video for lieying_plugin, sceext 2015.06
:: last_update 2015-06-26 01:08 GMT+0800 CST

# 猎影 插件接口, 新增功能说明


## 逐个解析功能

新增函数 ParseSomeUrl()

**函数定义**

	def ParseSomeUrl(url, format, i_min, i_max)

**函数参数说明**

+ url: 视频播放页面的 URL

+ format: 为 ParseFormat() 返回的 format 字符串

+ i_min: 希望获取的 分段文件信息的 最小 序号, 按数组下标, 0 表示第 1 段

+ i_max: 希望获取的 分段文件信息的 最大 序号, 按数组下标, 0 表示第 1 段

**函数返回值说明**

返回 json 格式的字符串

内容是一个数组, 定义类似于 ParseUrl() 函数的返回结果

**区别**:

对每一个分段文件, 插件进行如下 检查处理:

1. 若 分段序号 < i_min 则在此位置返回 null, 处理结束

2. 若 分段序号 > i_max 则在此位置返回 null, 处理结束

3. 在此位置返回一个 object, 格式与 ParseUrl() 返回的相同
  
  即
  
  {
  	Protocal: "http", 
  	Args: , 
  	Value: 
  }

对于返回 null 的分段文件, 插件 应该 尽可能 
避免 对此分段文件 进行 解析操作, 以便 加快解析速度, 节省资源. 


# 举例说明

假设分段文件总共有 4 个

完整的分段文件信息简化如下: {} 表示 一个 object

	[
		{}, 
		{}, 
		{}, 
		{}
	]

上面的信息, 和 ParseUrl(url, format) 返回的相同

+ 若使用 ParseSomeUrl(url, format, 0, 1) 则应返回如下内容
  	
  	[
  		{}, 
  		{}, 
  		null, 
  		null
  	]

+ 若使用 ParseSomeUrl(url, format, 2, 2) 则应返回如下内容
  
  	[
  		null, 
  		null, 
  		{}, 
  		null
  	]

**注意**

+ i_min 和 i_max 的取值是 任意的, 
  不要求 i_min <= i_max, 
  也不要求 i_min >= 0, 
  也不要求 i_max 不能 超过最后一个分段序号

也就是说, i_min 和 i_max 取 任何整数, 都 不会 导致 错误发生


**举例如下**

+ 若使用 ParseSomeUrl(url, format, -1, 5) 则应返回如下内容
  
  	[
  		{}, 
  		{}, 
  		{}, 
  		{}
  	]

+ 若使用 ParseSomeUrl(url, format, 6, 7) 则应返回如下内容
  
  	[
  		null, 
  		null, 
  		null, 
  		null
  	]

+ 若使用 ParseSomeUrl(url, format, 2, 1) 则应返回如下内容
  
  	[
  		null, 
  		null, 
  		null, 
  		null
  	]


## 更多说明

+ 无论任何情况下, 插件都返回完整长度的列表 (数组)
  
  获取 返回列表的长度, 即可得知 全部分段文件的 个数. 
  
  所以, 仅仅想要获取 分段文件个数, 而 不想执行 具体的解析操作, 可以这样做
  
  	ParseSomeUrl(url, format, 1, 0)
  
  此操作 将返回一个 全是 null 的列表, 而不执行具体的解析操作

+ ParseSomeUrl() 通过仅仅定义一个简单的函数, 就实现 丰富 灵活 的操作. ;-)
  
  剩下的事情, 就留给 猎影 自由发挥 了. ^_^


:: end suggest1.md


