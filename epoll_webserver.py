#------------------------------v3.0 epoll--------------------------------------
#coding=utf-8
import select
from socket import *
import re
#创建一个服务器套接字
serverSocket = socket(AF_INET,SOCK_STREAM)
#绑定地址以及地址重利用
localaddres=('',8888)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR ,1)
serverSocket.bind(localaddres)
#设置套接字处于监听状态
serverSocket.listen(10)
# 创建一个epoll对象
epoll=select.epoll()
# 将创建的套接字添加到epoll的事件监听中
epoll.register(serverSocket.fileno(),select.EPOLLIN)
connections = {}
addresses = {}


#定义一个用户请求类
class UserRequest:
	def __init__(self,userSocket):
		self.userSocket=userSocket
		#设置html文件夹的路径
		self.path='/home/python/ftp/share'
		#初始化请求文件的路径
		self.fileDir=''
	def recv(self):
		recv=self.userSocket.recv(1024)
		tempDir=re.search(' /.* ',recv)

		if tempDir:	
			reqDir=tempDir.group()[1:-1]
			#如果访问的是HTML文件夹默认访问index.html
			if re.match('/.+/$',reqDir):
				self.fileDir=self.path+ reqDir+'index.html'
			else:
				if re.match('.+\..+',reqDir):
					self.fileDir=self.path+reqDir
				else:
					self.fileDir=self.path+ reqDir+'/index.html'
		else:
			pass
#定义一个系统处理类	
class SysDel:
	def __init__(self):
		#初始化处理后的文件内容以及请求发送出去标识内容
		self.responsesDir={'200':'HTTP/1.1 200 OK\r\n','404':'HTTP/1.1 404 Not Found\r\n','505':'HTTP/1.1 500 Internal Server Error\r\n'}
		self.message=''
	def startDel(self,userRequest):	
		#获得用户请求这个对象
		self.userRequest=userRequest
		try:
			f=open(self.userRequest.fileDir,'r')
		#如果文件打开异常，发送文件不存在
		except IOError,e:
			self.message=self.responsesDir['404']
		else:
		#如果打开正确就组织发送内容
			content=f.read()
		#组织正确后的发送内容
			#文件标识
			mark=self.responsesDir['200']
			#组织文件的后缀
			tempSuffix=re.search('\..+$',self.userRequest.fileDir).group()
			suffix=tempSuffix[1:]
			#发送出的文件类型
			contentType='Content-Type: text/'+suffix
			#留白
			blank='\r\n\r\n'
			self.message=mark+contentType+blank+content
		

#定义一个回应类
class Responses:
	def __init__(self,sysDel):
		#获得系统处理这个对象
		self.sysDel=sysDel
	def startSend(self):
		self.sysDel.userRequest.userSocket.send(self.sysDel.message)
		#短链接发送完数据就断开连接，等待新请求
		tempfd=connections[self.sysDel.userRequest.userSocket]
		print tempfd
		epoll.unregister(tempfd)
		print '-----------'
		self.sysDel.userRequest.userSocket.close()
		print '-------------'
def main():
	global fd
	
	global epoll_list
	
	# 循环等待客户端的到来或者对方发送数据
	while True:
	    # epoll 进行 fd 扫描的地方 -- 未指定超时时间则为阻塞等待
	    epoll_list=epoll.poll()
	    print epoll_list

	     # 对事件进行判断 
	    for fd,events in epoll_list:
	        print fd
	        print events

	        # 如果是socket创建的套接字被激活即serverSocket被触发
	        if fd == serverSocket.fileno():
	            newSocket,addr=serverSocket.accept()
	            print('有新的客户端到来%s'%str(addr))
	            # 将 newsocket 和 addr 信息分别保存起来
	            connections[newSocket.fileno()] = newSocket
	            connections[newSocket]=newSocket.fileno()
	            addresses[newSocket.fileno()] = addr
	            # 向 epoll 中注册 连接 socket 的 可读 事件
	            epoll.register(newSocket.fileno(), select.EPOLLIN )
	         #如果是newSocket触发
	        elif events == select.EPOLLIN:
	        	

	        	# tempsock=connections[fd]

	        	newRequeses=UserRequest(connections[fd])
	        	newRequeses.recv()
	        	sysDel=SysDel()
	        	sysDel.startDel(newRequeses)
	        	responses=Responses(sysDel)
	        	responses.startSend()
if __name__ == '__main__':
	main()
	        	# sysDel.startDel(newRequeses)
				#调用接收方法

				# newRequeses.recv()

				#实例化系统处理类
				#sysDel=SysDel()
				#调用开始处理方法,将用户请求实例传进去
				# sysDel.startDel(newRequeses)
				#实例化回应类,并将处理实例传进去
				# responses=Responses(sysDel)
				# # responses.getSysDel(sysDel)
				# #开始发送内容
				# responses.startSend()	

	        	


	            # # 从激活 fd 上接收
	            # recvData = connections[fd].recv(1024)

	            # if len(recvData)>0:
	            #     print('recv:%s'%recvData)
	            # else:
	            #     # 从 epoll 中移除该 连接 fd
	            #     epoll.unregister(fd)

	            #     # server 侧主动关闭该 连接 fd
	            #     connections[fd].close()

	            #     break

'''
from socket import *
from select import select
import re


#定义一个用户请求类
class UserRequest:
	def __init__(self,userSocket):
		self.userSocket=userSocket
		#设置html文件夹的路径
		self.path='/home/python/ftp/share'
		#初始化请求文件的路径
		self.fileDir=''
		self.flag=0
	def recv(self):
		recv=self.userSocket.recv(1024)
		print recv
		tempDir=re.search(' /.* ',recv)
      #如果找到了为返回对像可以执行，没找到为none
		if tempDir:	
			reqDir=tempDir.group()[1:-1]
			#如果访问的是HTML文件夹默认访问index.html
			if re.match('/.+/$',reqDir):
				self.fileDir=self.path+ reqDir+'index.html'
			else:
				if re.match('.+\..+',reqDir):
					self.fileDir=self.path+reqDir
				else:
					self.fileDir=self.path+ reqDir+'/index.html'
					self.flag=1
					# print 'test'
					# tempsock.send('Content-Length:313\n Content-Type: text/html \n Location:192.168.160.130:8888/html/')
					# readablelist.remove(tempsock)
					# tempsock.close()			
		else:
			pass
#定义一个系统处理类	
class SysDel:
	def __init__(self):
		#初始化处理后的文件内容以及请求发送出去标识内容
		self.responsesDir={'200':'HTTP/1.1 200 OK\r\n','404':'HTTP/1.1 404 Not Found\r\n','505':'HTTP/1.1 500 Internal Server Error\r\n'}
		self.message=''
	def startDel(self,userRequest):	
		#获得用户请求这个对象
		self.userRequest=userRequest
		try:
			f=open(self.userRequest.fileDir,'r')
		#如果文件打开异常，发送文件不存在
		except IOError,e:
			self.message=self.responsesDir['404']
		else:
		#如果打开正确就组织发送内容
			content=f.read()
		#组织正确后的发送内容
			#文件标识
			mark=self.responsesDir['200']
			#组织文件的后缀
			tempSuffix=re.search('\..+$',self.userRequest.fileDir).group()
			suffix=tempSuffix[1:]
			#发送出的文件类型
			contentType='Content-Type: text/'+suffix
			#留白
			blank='\r\n\r\n'
			self.message=mark+contentType+blank+content
		

#定义一个回应类
class Responses:
	def __init__(self,sysDel):
		#获得系统处理这个对象
		self.sysDel=sysDel
	def startSend(self):

		if self.sysDel.userRequest.flag==1:
			#测试实现重定向,未完成待续
			# Response_Headers='Location:192.168.160.130:8888/html/\r\n\r\n'
			self.sysDel.userRequest.userSocket.send(self.sysDel.message+'Location:192.168.160.130:8888/html')
			# tempsock.send(Response_Headers)
			print 'test======'
		else:
			self.sysDel.userRequest.userSocket.send(self.sysDel.message)
			#短链接发送完数据就断开连接，等待新请求Content-Length:313\nHTTP/1.1 307 Temporary RedirectrLocation:192.168.160.130:8888/html/
		# print a
		readablelist.remove(self.sysDel.userRequest.userSocket)
		self.sysDel.userRequest.userSocket.close()

def main():
	#创建一个服务器套接字
	serverSocket=socket(AF_INET,SOCK_STREAM)
	#绑定地址，以及地址重利用
	localaddres=('',8888)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR ,1)
	serverSocket.bind(localaddres)
	#设置套接字为监听状态
	serverSocket.listen(5)
	#初始化可读（可以响应请求的）列表
	readablelist=[serverSocket]
	# global tempsock , readablelist
	#循环监控readlist中的套接字状态
	global readablelist
	while True:
		print '1'
		#当可有信息来时放在readlist中处理
		readlist,writelist,exptionlist=select(readablelist,[],[])
		for tempsock in readlist:
			if tempsock==serverSocket:
				newsocket,destaddres=serverSocket.accept()
				print '%s上线'%(str(destaddres))
				readablelist.append(newsocket)
			else:
				print '有用户发来请求'
				#实例化新用户请求类
				newRequeses=UserRequest(tempsock)
				#调用接收方法
				newRequeses.recv()
				#实例化系统处理类
				sysDel=SysDel()
				#调用开始处理方法,将用户请求实例传进去
				sysDel.startDel(newRequeses)
				#实例化回应类,并将处理实例传进去
				responses=Responses(sysDel)
				# responses.getSysDel(sysDel)
				#开始发送内容
				responses.startSend()		

if __name__ == '__main__':
	main()
'''