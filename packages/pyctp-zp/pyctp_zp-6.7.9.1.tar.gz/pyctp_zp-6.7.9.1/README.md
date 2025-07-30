# pyctp-zp: CTP Python API 接口

[![PyPI version](https://img.shields.io/pypi/v/pyctp-zp.svg)](https://pypi.org/project/pyctp-zp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/pypi/pyversions/pyctp-zp.svg)](https://pypi.org/project/pyctp-zp/)
[![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)](https://pypi.org/project/pyctp-zp/)

一个为中国期货市场量身打造的 CTP (Comprehensive Transaction Platform) Python 接口库。

本项目基于官方 C++ API，使用 SWIG 工具进行封装，旨在为 Python 开发者提供一个稳定、高效且与官方版本完全兼容的交易和行情接口。

为了方便开发和测试，`pyctp-zp` 在同一个包内同时提供了两个独立的接口模块：

* **`PyCTP`**: 用于连接**真实期货账户**的生产环境接口。
* **`CPPyCTP`**: 用于连接 **SimNow 模拟环境**的测评接口。

## 核心特性

* **双版本支持**: 一次安装，即可同时拥有连接实盘和模拟盘的能力，方便开发、测试与实盘无缝切换。
* **纯正官方封装**: 100% 基于 CTP 官方的 C++ API 进行转换，保证了接口的完整性、稳定性和低延迟特性。
* **Windows 平台**: 目前专注于提供 Windows 操作系统下的最佳体验。
* **Pythonic 体验**: 支持 Director 模式，允许用户通过继承 `Spi` 类来轻松处理回调事件，符合 Python 的面向对象编程习惯。

## 安装指南

**环境要求**:

* 操作系统: Windows
* Python 版本: 3.12 或更高

使用 pip 可以轻松安装：

```bash
pip install pyctp-zp
```

## 快速上手

下面是一个获取行情数据的简单示例。

### 1. 准备 `Spi` (回调处理)

你需要创建一个类来继承 `MdApi` 的 `Spi` 类，并重写你需要的回调函数，比如 `OnRtnDepthMarketData` (行情通知)。

```python
# a_simple_test.py

import time
import sys
import os

# 根据需要选择导入测评版或正式版
# 测评版 (SimNow)
from CPPyCTP import tdapi, mdapi
# 正式版 (实盘)
# from PyCTP import tdapi, mdapi

# --- 配置信息 ---
# SimNow 测评环境
SIMNOW_MD_FRONT = "tcp://180.168.146.187:10131"
SIMNOW_TD_FRONT = "tcp://180.168.146.187:10130"
BROKER_ID = "9999" # SimNow 经纪商代码
INVESTOR_ID = "YOUR_INVESTOR_ID" # 你的 SimNow 账号
PASSWORD = "YOUR_PASSWORD" # 你的 SimNow 密码
INSTRUMENT_ID = "ag2412" # 你想订阅的合约代码, 例如白银2412

# --- 回调处理类 ---
class MyMdSpi(mdapi.CThostFtdcMdSpi):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.is_login = False

    def OnFrontConnected(self) -> "void":
        print("行情服务器连接成功！")
        # 连接成功后，立即登录
        req = mdapi.CThostFtdcReqUserLoginField()
        req.BrokerID = BROKER_ID
        req.UserID = INVESTOR_ID
        req.Password = PASSWORD
        self.api.ReqUserLogin(req, 0)

    def OnFrontDisconnected(self, nReason: int) -> "void":
        print(f"行情服务器连接断开，原因: {nReason}")

    def OnRspUserLogin(self, pRspUserLogin: 'CThostFtdcRspUserLoginField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        if pRspInfo is not None and pRspInfo.ErrorID == 0:
            print("行情服务器登录成功！")
            self.is_login = True
        else:
            print(f"行情服务器登录失败: {pRspInfo.ErrorMsg}")

    def OnRtnDepthMarketData(self, pDepthMarketData: 'CThostFtdcDepthMarketDataField') -> "void":
        # 收到行情数据
        print(f"--- 行情更新 ---")
        print(f"合约代码: {pDepthMarketData.InstrumentID}")
        print(f"最新价: {pDepthMarketData.LastPrice}")
        print(f"成交量: {pDepthMarketData.Volume}")
        print(f"买一价: {pDepthMarketData.BidPrice1}")
        print(f"卖一价: {pDepthMarketData.AskPrice1}")
        print(f"时间: {pDepthMarketData.UpdateTime}.{pDepthMarketData.UpdateMillisec}")
        print("-----------------\n")

    def OnRspSubMarketData(self, pSpecificInstrument: 'CThostFtdcSpecificInstrumentField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        if pRspInfo is not None and pRspInfo.ErrorID == 0:
            print(f"合约 {pSpecificInstrument.InstrumentID} 订阅成功！")
        else:
            print(f"合约 {pSpecificInstrument.InstrumentID} 订阅失败: {pRspInfo.ErrorMsg if pRspInfo else '未知错误'}")

# --- 主程序 ---
def main():
    # 解决中文乱码
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
  
    # 创建 API 实例
    mdapi.CThostFtdcMdApi_CreateFtdcMdApi("flow/")
    api = mdapi.CThostFtdcMdApi_CreateFtdcMdApi("flow/")
    spi = MyMdSpi(api)
    api.RegisterSpi(spi)

    # 注册服务器地址
    api.RegisterFront(SIMNOW_MD_FRONT)
    # 初始化 API
    api.Init()
    print("行情API初始化...")

    # 等待登录成功
    while not spi.is_login:
        time.sleep(1)

    # 订阅行情
    api.SubscribeMarketData([INSTRUMENT_ID.encode()], 1)

    print("按 Ctrl+C 退出")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序退出")
  
    # 释放 API
    api.Release()

if __name__ == "__main__":
    main()
```

### 2. 运行示例

1. 将上面的代码保存为 `a_simple_test.py`。
2. **重要**: 将 `INVESTOR_ID` 和 `PASSWORD` 替换为你自己的 SimNow 账号和密码。
3. 运行 `python a_simple_test.py`，你就能看到实时的行情数据了。

## 项目结构说明

安装后，你的 Python 环境中会包含两个独立的包：

* `CPPyCTP`: 测评版接口
  * `CPPyCTP.tdapi`: 交易接口模块
  * `CPPyCTP.mdapi`: 行情接口模块
* `PyCTP`: 正式版接口
  * `PyCTP.tdapi`: 交易接口模块
  * `PyCTP.mdapi`: 行情接口模块

## 贡献

欢迎任何形式的贡献，无论是提交 issue、请求新功能还是提交代码。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

## 免责声明

本项目是用于学习和研究目的的工具，不构成任何投资建议。在进行真实交易前，请务必在模拟环境中进行充分的测试。任何由于使用本项目导致的损失，作者概不负责。
