# 基于加密技术的农产品溯源仿真系统（后端说明）



后端使用python语言编写，利用flask框架开发的后台接口，可以实现一些基本的数据加密解密和数据持久化存储。
使用时需要对settings.py文件中的数据库进行相应配置，并在commodity.py文件中更改局域网ip，后端服务的
ip和端口我是直接在pycharm中配置的,如果需要模拟上传温湿度信息的话需要在uploadData.py中配置下base_url和user_id

下图为用户扫描二维码查询信息界面

![](/markdown_imgs/1.png)

![](/markdown_imgs/2.png)

![](/markdown_imgs/3.png)

![](/markdown_imgs/4.png)