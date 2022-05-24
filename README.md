# 基于FastAPI的房屋租赁系统
## 项目背景
传统的线下租房不便、途径少、信息更新慢，导致房屋租赁效率低。为了有效的提升租赁效率和房源信息管理和提供更优质的租赁服务。f房东好租、用户满意。本系统用户分为租客、房东、管家、管理员四种角色。

- 租客：浏览房源、收藏房源、预定房源、发布租房需求、查看电子合同。
- 房东：发布房源、订单管理、查看电子合同。
- 管家：查看房源信息、回复咨询、线下带看房源。
- 管理员：用户管理、房源管理、订单管理、租房需求、实名认证、系统公告管理。
## TODO

- 房源全文检索
- 租房需求支持评论
- 日租、合租模式
- 房源推荐系统（Go开发）
## 项目体验
项目体验地址 [http://43.138.220.206/static/index.html](http://43.138.220.206/static/index.html)
由于注册需要发送短信验证码，而手机验证码服务现在只能给我的测试手机号发送验证码，因此不能使用注册服务。大家可以使用已有账号去登录体验。

| 账号类别 | 用户名 | 密码 | 备注 |
| --- | --- | --- | --- |
| 用户账号 | hui | 123456 | 租客账号 |
| 用户账号 | wang | 123456 | 房东账号 |

项目还没有太完善，服务器也只是学习级别的，可能会出现很多异常，望大家多担待。如有好的建议或者不懂的可以加入我们的群聊一起探讨与学习 **684822472**
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/272d7bf010d2474fb4edb1c32cab5302~tplv-k3u1fbpfcp-zoom-1.image)
## 项目启动

1. 准备好MySQL 与 Redis数据库服务，修改相关数据库配置信息
1. 申请第三方服务：七牛云的OSS服务、容联云的短信服务、阿里的支付服务、百度地图服务
1. 依赖于 Python 3.7.9 编程环境
1. 安装 requirements.txt 项目依赖 `pip install -r requirements.txt`
5. 启动项目 **python run.py**
5. 如果成功在本地启动项目，访问 [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs) 地址查看接口文档

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5d7ff9b4e3534217ae645912bfa60f43~tplv-k3u1fbpfcp-zoom-1.image)
## 项目部署

1. 确保Mysql、Redis服务正常
1. 在存在Dockerfile文件的项目目录下构建镜像 docker build -t  house_rental_image  **. （最后.不要忘记）**
1. 运行镜像产生容器 docker run -d --name house_rental_container -p 80:80 house_rental_image
1. docker ps 查看容器是否启动
## 系统整体功能图
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/cdcf09e3c7d84c73af44da846eded33a~tplv-k3u1fbpfcp-zoom-1.image)

## 项目结构
项目开发整体采用的是Python的FastAPI框架来搭建系统的接口服务，接口设计遵循 `Restful API`接口规范。接口前后端交互都采用json格式进行数据交互，项目整体的结构如下：
```python
─house_rental
    ├─commons ------------------------- 项目公共模块
    │  ├─exceptions ------------------- 项目全局异常模块
    │  ├─libs ------------------------- 第三方服务模块
    │  ├─responses -------------------- 项目全局响应模块
    │  ├─settings --------------------- 项目配置
    │  └─utils ------------------------ 项目工具类
    ├─constants ----------------------- 项目常量模块
    ├─logic --------------------------- 项目逻辑模块
    ├─managers ------------------------ 项目数据库模型管理器模块
    ├─middlewares --------------------- 项目中间件模块
    ├─models -------------------------- 项目数据库模型模块
    ├─routers ------------------------- 项目路由模块
    │  ├─admin ------------------------ 后台管理路由
    │  │  ├─apis ---------------------- 后台管理路由接口
    │  │  ├─request_models ------------ 后台路由请求模型
    │  │  └─response_models ----------- 后台路由响应模型
    │  ├─common ----------- 公共路由模块
    │  │  ├─apis
    │  │  ├─request_models
    │  │  └─response_models
    │  ├─house ------------ 房源路由模块
    │  │  ├─apis
    │  │  ├─request_models
    │  │  └─response_models
    │  ├─order ------------ 订单路由模块
    │  │  ├─apis
    │  │  ├─request_models
    │  │  └─response_models
    │  ├─payment ---------- 支付路由模块
    │  │  ├─apis
    │  │  ├─request_models
    │  │  └─response_models
    │  ├─user ------------- 用户路由模块
    │  │  ├─apis
    │  │  ├─request_models
    │  │  ├─response_models
    └─__init__.py --------- 项目初始化文件
└─Dockerfile ----------------- 项目docker部署文件
└─requirements.txt ----------- 项目依赖库文件
└─README.md ------------------ 项目说明文档
└─run.py --------------------- 项目启动入口
```
## 项目Redis缓存设计
### Redis key 规范：
```python
project : module : business : unique key
 项目名 :  模块名 :  业务    : 唯一区别key 

例如：用户手机短信验证码缓存
house_rental:user:sms_code:13022331752
```
### 用户模块缓存
| Key | 类型 | 过期时间 | 说明 |
| --- | --- | --- | --- |
| **house_rental:user:sms_code:{mobile}** | string | 5分钟 | 存储用户手机短信验证码 |
| 
 |  |  | 
 |

### 房源模块缓存
| Key | 类型 | 过期时间 | 说明 |
| --- | --- | --- | --- |
| **house_rental:house:{user_id}** | set | 不过期 | 存储用户收藏的房源id |
| **house_rental:house:home_houses:{city}** | string | 15天 | 首页房源信息缓存，存储json |
| **house_rental:house:facilities** | string | 3个月 | 房源设施缓存，存储json |
| **house_rental:house:detail:{house_id}** | string | 15天 | 房源详情缓存，存储json |

### 其他缓存
| Key | 类型 | 过期时间 | 说明 |
| --- | --- | --- | --- |
| **house_rental:common:areas** | string | 3个月 | 存储省市区json字符串数据 |
|  |  |  |  |

## 系统整体ER图
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1baf1f94dcbf4dda8e258e1299fd2122~tplv-k3u1fbpfcp-zoom-1.image)

房屋属性太多故在整体ER图省略
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4bf9595860d541fd8f29aa9c5ab55adb~tplv-k3u1fbpfcp-zoom-1.image)
实际表属性更多进行了垂直分表。
## 项目界面展示
### 首页
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/71257888e35a4f90a9718dc9e97d5f0a~tplv-k3u1fbpfcp-zoom-1.image)
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6c8b00da51ba457281d22948ee6a8fbd~tplv-k3u1fbpfcp-zoom-1.image)
### 登录注册
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1073239a66e44d6ea27dcc78b7db5dc8~tplv-k3u1fbpfcp-zoom-1.image)

### 房源列表
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/16b5ec3000a3461c936a44b8944f80aa~tplv-k3u1fbpfcp-zoom-1.image)
### 房源收藏
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e1e4d249357f46b6bd147d0362fc4f9b~tplv-k3u1fbpfcp-zoom-1.image)

### 房源详情
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e17d14a9e0fe4e8a9fde764368fc65b4~tplv-k3u1fbpfcp-zoom-1.image)
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8247f828f2e24c6b8b40b899c366d3fa~tplv-k3u1fbpfcp-zoom-1.image)
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/77968652aeed4493a8daf010d1ba93b9~tplv-k3u1fbpfcp-zoom-1.image)

### 房源地图服务
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/86d69ad736704aed8abeb277895036a6~tplv-k3u1fbpfcp-zoom-1.image)
### 房源订单
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7949f2f448d140409ce14b60dc897f60~tplv-k3u1fbpfcp-zoom-1.image)

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/25c41143aa1046bcbee2f88f17edfe74~tplv-k3u1fbpfcp-zoom-1.image)
### 电子合同
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fae1edecbab64867a3dbe2adb3f00b54~tplv-k3u1fbpfcp-zoom-1.image)
### 求租管理
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9c0501168e9941dd8959de74a5f2eded~tplv-k3u1fbpfcp-zoom-1.image)

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6339a4d391dd4699be55e434f8798cac~tplv-k3u1fbpfcp-zoom-1.image)

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6149b851b6374406b7571f94e3c1e1c3~tplv-k3u1fbpfcp-zoom-1.image)
### 系统公告
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c34b5dfd3e8b4849a6b741ad61e4653f~tplv-k3u1fbpfcp-zoom-1.image)
### 房东房源管理
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a879e62879984ba7823bd7b2460e9a05~tplv-k3u1fbpfcp-zoom-1.image)

### 房东发布房源
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d56e8edadd174ab5af1cd2a47f40008f~tplv-k3u1fbpfcp-zoom-1.image)
