#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋租赁系统主入口模块 }
# @Date: 2022/02/27 20:57
import uvicorn
from house_rental import app

# irhkhm7606@sandbox.com
if __name__ == '__main__':
    # uvicorn.run(app, host='0.0.0.0', port=8080)
    uvicorn.run('house_rental:app', host='0.0.0.0', port=8080, reload=False, debug=True)
