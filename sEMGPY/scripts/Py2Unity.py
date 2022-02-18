import socket

# 构建Socket实例,设置端口号和监听队列大小
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1', 10086))
listener.listen(5)

# 进入死循环,等待新的客户端连入,一旦有客户端连入,就分配一个线程去做专门处理,然后自己继续等待
while True:
    client_executor, addr = listener.accept()
    print('Accept new connection from %s:%s...' % addr)

    while True:
        client_executor.send(bytes(repr("100000100").encode('utf-8')))

        msg = client_executor.recv(1024).decode('utf-8')
        if msg == '2':
            break

    client_executor.close()
    print('Connection from %s:%s closed.' % addr)