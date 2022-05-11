<a name="ahaeU"></a>
# 基于 FastAPI 的房屋租赁系统
## 项目启动
1. 准备好MySQL 与 Redis数据库服务，修改相关数据库配置信息
1. 申请第三方服务：七牛云的OSS服务、容联云的短信服务、阿里的支付服务、百度地图服务
1. 依赖于 Python 3.7.9 编程环境
1. 安装 requirements.txt 项目依赖
```python
pip install -r requirements.txt
```

4. 启动项目 **python run.py**
<a name="oqTRa"></a>
## 项目背景
传统的线下租房不便、途径少、信息更新慢，导致房屋租赁效率低。为了有效的提升租赁效率和房源信息管理和提供更优质的租赁服务。本系统用户分为租客、房东、管家、管理员四种角色。<br />租客：浏览房源、收藏房源、预定房源、发布租房需求、查看电子合同。<br />房东：发布房源、订单管理、查看电子合同。<br />管家：查看房源信息、回复咨询、线下带看房源。<br />管理员：用户管理、房源管理、订单管理、租房需求、实名认证、系统公告管理。

<a name="MG2N8"></a>
## 系统整体功能图
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652283823459-a56f1dcf-720c-46c9-be8f-91b3e4c933db.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=470&id=u89954d6d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=587&originWidth=1092&originalType=binary&ratio=1&rotation=0&showTitle=false&size=116118&status=done&style=none&taskId=u2f6f6f22-31bb-4a82-9acf-39efe6e0210&title=&width=873.6)

<a name="bbBTz"></a>
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
└─README.md ------------------ 项目说明文档
└─requirements.txt ----------- 项目依赖库文件
└─run.py --------------------- 项目启动入口
```

<a name="Q6MSP"></a>
## 系统整体ER图
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652284012928-c7460ede-9b14-4d13-a65f-91696f3e772a.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=701&id=ud9b72803&margin=%5Bobject%20Object%5D&name=image.png&originHeight=876&originWidth=945&originalType=binary&ratio=1&rotation=0&showTitle=false&size=199987&status=done&style=none&taskId=ua79af982-c72a-4f66-9c28-f897526a458&title=&width=756)

房屋属性太多故在整体ER图省略<br />
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652286424574-29e9e6f1-afae-4a26-9cf7-baf3bb189e1e.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=656&id=u169c145e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=820&originWidth=883&originalType=binary&ratio=1&rotation=0&showTitle=false&size=278364&status=done&style=none&taskId=ueb760ed6-ebba-4b55-a93c-7f526de2ec7&title=&width=706.4)
<br/>实际表属性更多进行了垂直分表。
<a name="FhR7I"></a>
## 项目界面展示
<a name="m8kne"></a>
### 首页
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652287020379-4b28f18b-a766-40f8-a9a4-9397d763b407.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=628&id=uafea45f7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=785&originWidth=1574&originalType=binary&ratio=1&rotation=0&showTitle=false&size=1133835&status=done&style=none&taskId=u32e658f7-d175-4570-95fe-1e577ee6756&title=&width=1259.2)
<br />
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652284711600-edfd7b3a-f011-4d87-bcdb-636dd33e305c.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=531&id=u0a00e654&margin=%5Bobject%20Object%5D&name=image.png&originHeight=664&originWidth=945&originalType=binary&ratio=1&rotation=0&showTitle=false&size=750259&status=done&style=none&taskId=uc497f725-9f3c-4096-8ed2-bf2b7b695f6&title=&width=756)

### 登录注册
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652287055880-59faa2ef-b884-4794-9f8f-e888e0394cca.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=660&id=u33284912&margin=%5Bobject%20Object%5D&name=image.png&originHeight=825&originWidth=1781&originalType=binary&ratio=1&rotation=0&showTitle=false&size=769121&status=done&style=none&taskId=u6acdad72-4c93-4b43-a571-5fae8576e6c&title=&width=1424.8)

<a name="OXdtf"></a>
### 房源列表
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652286197786-3ac0f45a-a540-45c2-857e-444f2f0af1f7.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=648&id=u1f307d01&margin=%5Bobject%20Object%5D&name=image.png&originHeight=810&originWidth=1900&originalType=binary&ratio=1&rotation=0&showTitle=false&size=707208&status=done&style=none&taskId=ub46a1f8a-7265-4516-886a-9afd8f30162&title=&width=1520)
<a name="oxHFF"></a>
### 房源收藏
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652284752004-aac709e0-7df4-4f15-8f3c-3f8b0aa03e75.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=426&id=u4fdda84c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=532&originWidth=945&originalType=binary&ratio=1&rotation=0&showTitle=false&size=187037&status=done&style=none&taskId=ubece7db6-4504-4fd3-8040-624d71e0eaa&title=&width=756)

<a name="kjhyi"></a>
### 房源详情
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652284785793-ac549739-61c5-457b-a638-cccf30a983ef.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=504&id=u6ba21067&margin=%5Bobject%20Object%5D&name=image.png&originHeight=630&originWidth=945&originalType=binary&ratio=1&rotation=0&showTitle=false&size=503472&status=done&style=none&taskId=u93ca8daa-7666-4b91-a13e-767181ecf76&title=&width=756)
<br />
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652284796985-2af896c8-3df8-4327-9052-51e54dacd4cc.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=493&id=u41df1baf&margin=%5Bobject%20Object%5D&name=image.png&originHeight=616&originWidth=945&originalType=binary&ratio=1&rotation=0&showTitle=false&size=82963&status=done&style=none&taskId=ud21bad4a-a7ea-43bf-b682-d2e4f8b2706&title=&width=756)
<br />
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652284829463-0ff8b806-8311-4aff-8ab4-6ee1eebd841f.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=581&id=ub5376f5d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=726&originWidth=945&originalType=binary&ratio=1&rotation=0&showTitle=false&size=556655&status=done&style=none&taskId=u0d9eec17-5aea-430a-8f99-6d2d97c97a2&title=&width=756)

<a name="eUFdU"></a>
### 房源地图服务
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285151652-1c163014-50d6-49f7-b79c-80e2d3004027.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=702&id=u051ce937&margin=%5Bobject%20Object%5D&name=image.png&originHeight=877&originWidth=1877&originalType=binary&ratio=1&rotation=0&showTitle=false&size=494456&status=done&style=none&taskId=ua47856d6-c57d-4acd-bda7-76058beeb37&title=&width=1501.6)
<a name="oTyT9"></a>
### 房源订单
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285270539-7080a1a4-3a5f-4172-8155-3f1969269c1b.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=691&id=ud87b1061&margin=%5Bobject%20Object%5D&name=image.png&originHeight=864&originWidth=1842&originalType=binary&ratio=1&rotation=0&showTitle=false&size=226346&status=done&style=none&taskId=u91810d48-f81e-4b3b-b046-829d133a553&title=&width=1473.6)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285319190-bf8fb1af-3d0b-45ab-b2a0-c951a2ff27cd.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=534&id=uab7002de&margin=%5Bobject%20Object%5D&name=image.png&originHeight=667&originWidth=1374&originalType=binary&ratio=1&rotation=0&showTitle=false&size=374950&status=done&style=none&taskId=ud3b255a6-7925-46aa-9775-34125d11dbf&title=&width=1099.2)
<a name="X7TMa"></a>
### 电子合同
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285398540-7e917fc2-3f47-41ee-83fa-7c5b7a5f3b7f.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=637&id=u76a7386c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=796&originWidth=1392&originalType=binary&ratio=1&rotation=0&showTitle=false&size=91572&status=done&style=none&taskId=u682bc98c-140f-426b-ad29-5236219a131&title=&width=1113.6)
<a name="h4bWb"></a>
### 求租管理
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285862005-3049f659-f6b5-4f28-abbd-355dbcf7f4de.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=457&id=u8dc15de9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=571&originWidth=1336&originalType=binary&ratio=1&rotation=0&showTitle=false&size=39968&status=done&style=none&taskId=uacd76fdc-cd84-4a6d-acbc-fd620bb9128&title=&width=1068.8)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285648963-123986b8-9e08-4210-8634-efff62093369.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=1106&id=ua35fe521&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1383&originWidth=1345&originalType=binary&ratio=1&rotation=0&showTitle=false&size=71833&status=done&style=none&taskId=u6c5aaebb-e8cc-4c30-8683-729f0aa0aa9&title=&width=1076)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652285971643-2722c419-420f-4548-8a0d-3769db475297.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=720&id=ua0d04d60&margin=%5Bobject%20Object%5D&name=image.png&originHeight=900&originWidth=1339&originalType=binary&ratio=1&rotation=0&showTitle=false&size=79585&status=done&style=none&taskId=u43e91f64-3474-4bba-a3a4-c3f938e594c&title=&width=1071.2)
<a name="wM6E8"></a>
### 系统公告
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652286109177-572601a1-e63c-45e0-b55c-07241d48e274.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=628&id=ua6d35722&margin=%5Bobject%20Object%5D&name=image.png&originHeight=785&originWidth=1539&originalType=binary&ratio=1&rotation=0&showTitle=false&size=82122&status=done&style=none&taskId=u12dad6a2-9391-4d8f-8e67-22bf199f0e8&title=&width=1231.2)
<a name="rZdmt"></a>
### 房东房源管理
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652288576618-fef3a5b5-c3c5-4f4d-9a8c-50bb9f71ac38.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=641&id=u53bba65a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=801&originWidth=1391&originalType=binary&ratio=1&rotation=0&showTitle=false&size=551336&status=done&style=none&taskId=u7d782852-5a3b-4b1c-8029-6046e6b8ebb&title=&width=1112.8)

<a name="YJ48p"></a>
### 房东发布房源
![image.png](https://cdn.nlark.com/yuque/0/2022/png/20361978/1652288191175-c97a3da4-d1e8-47ee-a64e-6a59c7623386.png#clientId=u60657c17-c91f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=2285&id=u43134050&margin=%5Bobject%20Object%5D&name=image.png&originHeight=2856&originWidth=1872&originalType=binary&ratio=1&rotation=0&showTitle=false&size=148588&status=done&style=none&taskId=u68118467-8889-4f25-ae17-08d8bdfc6ea&title=&width=1497.6)
