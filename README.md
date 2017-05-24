# P2P
A simple P2P file transmission script for LAN
一个简单的局域网P2P文件传输程序(Python 2.7)

## 需求
处于同一个LAN内的用户有时需要互传文件，而几十MB甚至几十KB的文件，若用U盘传输，未免太慢了一些，如我们寝室，每个人习惯使用的操作系统各不相同，有Windows、macOS、Linux，为了实现LAN内的用户方便互传文件，设计了这样一个简单的P2P文件传输程序。

## 开发环境
Python 2.7 

## 设计思路
遵循UNIX的设计原则之一“Keep It Simple，Stupid”，整个程序只含有一个Python文件，只要启动的时候加上对应的参数，就可以以“Receiver”或者”Sender“的身份启动。 


## 运行流程
当不加参数启动时，会显示以下这些帮助文字：
```
This is a P2P file transmission script, allowing file transmission between hosts in LAN, requring python 2.7"
        -s:  run as server mode, for recerving files "
        -c:  run as client mode, for sending files"
```

当以“Receiver”的参数启动时，会显示本机的IP，随后只需等待socket连接和文件传送即可，文件传输中会显示 **进度条**、**文件大小**，**sender的IP地址与端口号**。文件默认存放为P2P.py的 **同级目录** 下。

当以“Sender”的参数启动时，只需按照文字提示一步步操作即可，输入receiver的局域网IP地址 (让receiver告诉你就好:))，这需要receiver端先启动该脚本，随后输入文件路径，便可以开启传输。

## 源代码
在该文档的同级目录下 (./P2P.py)

## 实现原理
在 server 和 client 之间建立 socket 连接，进行文件的传输。client 在传送文件内容之前先发送一个文件头，包含了该文件的主要信息，包括 **文件名** 和 **文件大小**。之后再将文件拆分成固定size的多个block进行传输。
