# 星痕共鸣实时战斗数据统计工具- 客户端 一键安装&游戏屏幕显示 (StarResonanceDamageCounter-Client)

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![pnpm](https://img.shields.io/badge/pnpm-10.13.1-orange.svg)](https://pnpm.io/)

一个用于《星痕共鸣》游戏的实时战斗数据统计工具，通过网络抓包技术实时分析战斗数据，提供伤害统计、DPS 计算等功能。

该工具的数据准确性已经经过多次实际战斗验证，在网络环境稳定的情况下暂未发现数据丢失的问题。

该工具无需修改游戏客户端，不违反游戏服务条款。该工具旨在帮助玩家更好地理解战斗数据，减少无效提升，提升游戏体验。使用该工具前，请确保不会将数据结果用于战力歧视等破坏游戏社区环境的行为。

[介绍视频]([https://www.bilibili.com/video/BV1T4hGzGEeX/](https://www.bilibili.com/video/BV1vohjzTEiX/?spm_id_from=333.1387.homepage.video_card.click&vd_source=f31af4ca9b27f30a85203528c8602c0d))

## ✨ 功能特性

- 🎯 **实时伤害统计** - 实时捕获并统计战斗中的伤害数据
- 📊 **DPS 计算** - 提供瞬时 DPS 和总体 DPS 计算
- 🎲 **详细分类** - 区分普通伤害、暴击伤害、幸运伤害等类型
- 🌐 **Web 界面** - 提供美观的实时数据展示界面
- 🌙 **主题切换** - 支持日间/夜间模式切换
- 🔄 **自动刷新** - 数据实时更新，无需手动刷新
- 📈 **统计分析** - 暴击率、幸运率等详细统计信息

- ☀ 这个版本增加了什么？
- 一键安装 无需配置环境
- 一键启动 配置更新
- web保留的同时增加了在游戏窗口内显示
- 我哦哦哦我是男神

## 🚀 快速开始


### 安装步骤

1. **下载仓库ZIP**
   ```

   <img width="995" height="482" alt="0cea3a98-de76-4916-bb62-0cf43cdf3517" src="https://github.com/user-attachments/assets/7f618881-8033-42eb-9dd1-b895297bc73f" />

   ```

2. **根据里面的教程一键安装即可**
   ```
   随后打开exe文件即可！
   ```

### 使用方法

1. **选择网络设备**
   - 启动程序后，会显示可用的网络设备列表
   - 输入对应设备的编号（通常选择主网卡）
   - 可以前往控制面板或者系统设置查找使用的网卡

2. **设置日志级别**
   - 选择日志级别：`info` 或 `debug`
   - 推荐使用 `info` 级别以减少日志输出

3. **启动游戏**
   - 程序会自动检测游戏服务器连接
   - 当检测到游戏服务器时，会输出服务器信息，并开始统计数据

4. **查看数据**
   - 打开浏览器访问：`http://localhost:8989`
   - 实时查看战斗数据统计

## 📱 Web 界面功能

### 数据展示
- **角色 ID** - 玩家角色标识
- **总伤害/治疗** - 累计造成的总伤害/治疗量
- **伤害分类** - 纯暴击、纯幸运、暴击幸运等详细分类
- **暴击率/幸运率** - 战斗中的暴击和幸运触发概率
- **瞬时 DPS/HPS** - 当前秒的伤害/治疗输出
- **最大瞬时** - 历史最高瞬时输出记录
- **总 DPS/HPS** - 整体平均输出效率

### 操作功能
- **清空数据** - 重置所有统计数据
- **主题切换** - 在日间/夜间模式间切换
- **自动刷新** - 每 100ms 自动更新数据

## 🛠️ 技术架构

### 核心依赖
- **[cap](https://github.com/mscdex/cap)** - 网络数据包捕获
- **[express](https://expressjs.com/)** - Web 服务器框架
- **[protobufjs](https://github.com/protobufjs/protobuf.js)** - Protocol Buffers 解析
- **[winston](https://github.com/winstonjs/winston)** - 日志管理

## 📡 API 接口

### GET /api/data
获取实时战斗数据统计

**响应示例：**
```json
{
  "code": 0,
  "user": {
    "114514": {
      "realtime_dps": 1250,
      "realtime_dps_max": 2100,
      "total_dps": 850.25,
      "total_damage": {
        "normal": 75000,
        "critical": 25000,
        "lucky": 25000,
        "crit_lucky": 10000,
        "hpLessen": 75000,
        "total": 135000
      },
      "total_count": {
        "normal": 45,
        "critical": 30,
        "lucky": 15,
        "total": 90
      }
    }
  }
}
```

### GET /api/clear
清空所有统计数据

**响应示例：**
```json
{
  "code": 0,
  "msg": "Statistics have been cleared!"
}
```

## 🔧 故障排除

### 常见问题

1. **无法检测到游戏服务器**
   - 检查网络设备选择是否正确
   - 确认游戏正在运行且已连接服务器
   - 尝试前往同一张地图的非人群密集处

2. **Web 界面无法访问**
   - 检查端口 8989 是否被占用
   - 确认防火墙设置允许本地连接

3. **数据统计异常**
   - 检查日志输出是否有错误信息
   - 尝试重启程序重新捕获

4. **cap 模块编译错误**
   - 确保已安装 Visual Studio Build Tools 和 Python
   - 确认 Node.js 版本符合要求

## 📄 许可证

本项目采用 [Mozilla Public License 2.0](LICENSE) 许可证。

使用本项目即表示您同意遵守该许可证的条款。

## 👥 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！

## ⭐ 支持

如果这个项目对您有帮助，请给它一个 Star ⭐

---

**免责声明**：本工具仅用于游戏数据分析学习目的，不得用于任何违反游戏服务条款的行为。使用者需自行承担相关风险。项目开发者不对任何他人使用本工具的恶意战力歧视行为负责。请在使用前确保遵守游戏社区的相关规定和道德标准。
