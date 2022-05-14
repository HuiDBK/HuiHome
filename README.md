# 基于FastAPI的房屋租赁系统
## 项目启动
1. 准备好MySQL 与 Redis数据库服务，修改相关数据库配置信息
1. 申请第三方服务：七牛云的OSS服务、容联云的短信服务、阿里的支付服务、百度地图服务
1. 依赖于 Python 3.7.9 编程环境
1. 安装 requirements.txt 项目依赖
```python
pip install -r requirements.txt
```

4. 启动项目 **python run.py**
## 项目背景
传统的线下租房不便、途径少、信息更新慢，导致房屋租赁效率低。为了有效的提升租赁效率和房源信息管理和提供更优质的租赁服务。本系统用户分为租客、房东、管家、管理员四种角色。
租客：浏览房源、收藏房源、预定房源、发布租房需求、查看电子合同。
房东：发布房源、订单管理、查看电子合同。
管家：查看房源信息、回复咨询、线下带看房源。
管理员：用户管理、房源管理、订单管理、租房需求、实名认证、系统公告管理。

## 系统整体功能图
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2c2d8c90385942deb26edcf27ee4b7e6~tplv-k3u1fbpfcp-zoom-1.image)

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
└─__init__.py ---------------- 项目初始化文件
└─requirements.txt ----------- 项目依赖库文件
└─README.md ------------------ 项目说明文档
└─run.py --------------------- 项目启动入口
```

## 系统整体ER图
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d4494e706f394d69be0da51b8a137ae3~tplv-k3u1fbpfcp-zoom-1.image)

房屋属性太多故在整体ER图省略
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f9243e7254414c3db0e4bcfbcb6a50ae~tplv-k3u1fbpfcp-zoom-1.image)
实际表属性更多进行了垂直分表。
## 项目界面展示
### 首页
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9dfa889ed3c64022850398d33c8527a0~tplv-k3u1fbpfcp-zoom-1.image)
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5795e30510a249fd82f12a687f7b2e5e~tplv-k3u1fbpfcp-zoom-1.image)
### 登录注册
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/668aafa48fc0489da5a789f610091b54~tplv-k3u1fbpfcp-zoom-1.image)

### 房源列表
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4e97c5ad3d0243f0b8b725ce2eb30652~tplv-k3u1fbpfcp-zoom-1.image)
### 房源收藏
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3181a9fdb0c6408a9492dac0f0ff5b4c~tplv-k3u1fbpfcp-zoom-1.image)

### 房源详情
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5bfe1cd977ac46cab532a8dd6efa2c47~tplv-k3u1fbpfcp-zoom-1.image)
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b57ea2bfa14a4d2d99035af0dc5fd5cd~tplv-k3u1fbpfcp-zoom-1.image)
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/02fcf51168d14efc9bf503225a48627d~tplv-k3u1fbpfcp-zoom-1.image)

### 房源地图服务
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5232ae442ad94c928e5e2493ff98a563~tplv-k3u1fbpfcp-zoom-1.image)
### 房源订单
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bafb7d3b4a46497eafe21a049a3a5b12~tplv-k3u1fbpfcp-zoom-1.image)

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7ed6691d9c9a4b239dae50b739724b1d~tplv-k3u1fbpfcp-zoom-1.image)
### 电子合同
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5dada82ebd1a4e79b1e042f5eed3d9cd~tplv-k3u1fbpfcp-zoom-1.image)
### 求租管理
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ad7cdb68e46c4f989375a3e5256e75ce~tplv-k3u1fbpfcp-zoom-1.image)

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d261499b242f4aba97909e6b7d3e72b8~tplv-k3u1fbpfcp-zoom-1.image)

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/08dacb1ac2424b368802a4c3d1106d90~tplv-k3u1fbpfcp-zoom-1.image)
### 系统公告
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4017e4160e494cf4b30334d2234fe894~tplv-k3u1fbpfcp-zoom-1.image)
### 房东房源管理
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b0f1c8456c3742369e906e873b2e8da0~tplv-k3u1fbpfcp-zoom-1.image)

### 房东发布房源
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8e042eb2674f48baadc45ddddf4b7a9c~tplv-k3u1fbpfcp-zoom-1.image)
