**各个可执行文件的介绍**  
&emsp;&emsp;整体上就是一个流式转发，目的是这样接口流式消息，我就可以用自己的端口了，当然用 nginx 或许可以轻松实现，但那样你还得改别人的nginx，不想这样做  
&emsp;&emsp;至于实际在使用的时候，需要改下.py中的url或者变量OPENAI_API_BASE，这都比较简单  

* proxy_server_syn.py  
&emsp;&emsp;启动的一个 http 服务，把其它ip的流式通过这个服务转发出去，利用的是 requests 包，但启动http服务这里用的是 fastapi，没有用 flask   
&emsp;&emsp;这里加一个后缀 syn是表示同步的意思，是相对于 proxy_server.py文件来说的，因为它里面用的是异步的消息   
* proxy_server.py   
&emsp;&emsp;功能和 proxy_server_syn.py 是一样的，只不过里面用的是 httpx包的异步client，说实话具体的异步细节我也不清楚，外部也是用 fastapi启动的http服务    
* main.py  
&emsp;&emsp;它是模拟的一个 openai 的服务端，我用 cherry studio 也测试过，可以正常收发消息  
* client.py  
&emsp;&emsp;它是用python requests 包写的一个 openai的客户端，并不是用的 openai 的包，细节我就更清楚了   


```python

```
