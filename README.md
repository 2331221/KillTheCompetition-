# KillTheCompetition [杀死比赛]

![GitHub stars](https://img.shields.io/github/stars/2331221/KillTheCompetition?style=flat-square)
![GitHub license](https://img.shields.io/github/license/2331221/KillTheCompetition?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue?style=flat-square)

一款轻量、高效的 Web 信息泄露检测工具，专注于快速探测目标网站的敏感文件泄露（如备份文件、缓存文件、系统隐藏文件等），适用于安全测试工程师、网站维护人员进行合法授权的安全审计。

## 🔍 核心功能
- ✅ 多类型泄露检测：支持 bak 备份文件、Vim 缓存文件（.swp）、.DS_Store、配置文件等常见敏感文件探测
- ✅ 实时进度可视化：扫描过程中显示进度条，直观查看扫描进度（已扫描数/总数+百分比）
- ✅ 双重验证机制：通过 HTTP 状态码 + 文件大小双重判断，减少误报
- ✅ 结果本地保存：支持将扫描结果导出为 TXT 文件（带时间戳，方便归档）
- ✅ 易扩展：可直接在脚本中添加自定义泄露文件路径，扩展扫描范围
- ✅ 轻量无冗余：仅依赖 `requests` 库，运行速度快，无多余依赖

## 📋 环境要求
- 编程语言：Python 3.6 及以上
- 依赖库：`requests`（版本 ≥ 2.25.0）

## 🚀 快速开始

### 1. 下载仓库
#### 方法 1：Git 克隆（推荐）
```bash
git clone https://github.com/2331221/KillTheCompetition.git
cd KillTheCompetition
```

#### 方法 2：下载 ZIP 包
直接点击 GitHub 仓库页面的「Code」→「Download ZIP」，解压后进入文件夹。

### 2. 安装依赖
打开终端 / 命令行，执行以下命令安装所需依赖：
```bash
pip install -r requirements.txt
```
### 3. 运行工具
```bash
python KillTheCompetition.py
```

### 4. 操作步骤

    工具启动后，输入目标 URL（必须带 http:// 或 https://，例：https://example.com）
    等待扫描完成，实时查看泄露文件详情（类型、URL、状态码、文件大小）
    扫描结束后，输入 y 可保存结果到本地（文件名为 leak_scan_result_时间戳.txt）

### 📌 工具演示（示例）
```plaintext
[🎯 KillTheCompetition - Web信息泄露检测工具]
[⚠️  警告：仅用于合法授权测试，禁止未授权使用！]

[📌 请输入目标URL（例：http://xxx.com）：] https://test.com

[🔍 扫描中... 10/50 (20%)]
[✅ 发现泄露文件]
类型：bak备份文件
URL：https://test.com/config.php.bak
状态码：200
文件大小：1.2KB

[🔍 扫描中... 50/50 (100%)]
[📊 扫描完成！共发现 3 个泄露文件]

[💾 是否保存结果到本地？(y/n)：] y
[✅ 结果已保存至：leak_scan_result_202512011530.txt]
```
### ⚙️ 自定义扩展
#### 1. 新增泄露文件类型
编辑 KillTheCompetition.py 中的 LEAK_TYPES 字典，添加自定义文件路径，例：
```python
LEAK_TYPES = {
    "bak备份文件": ["./config.php.bak", "./index.html.bak"],
    "Vim缓存文件": ["./app.py.swp", "./db.conf.swp"],
    "自定义文件": ["./secret.txt", "./api_key.json"]  # 新增自定义类型
}
```
### 2. 修改超时时间
脚本中 TIMEOUT = 3 表示请求超时时间为 3 秒，可根据网络环境修改（例：TIMEOUT = 5）。

### ⚠️ 重要声明

    本工具仅用于 合法授权 的网络安全测试、网站维护等场景，禁止用于任何未授权的攻击行为。
    使用本工具前，必须获得目标网站所有者的书面授权，否则使用者需承担全部法律责任。
    开发者（dawn）不对工具的非法使用行为负责，也不承担因使用本工具造成的任何直接或间接损失。

### 📞 开发者信息

    作者：dawn
    官网：www.onechx.icu
    GitHub 仓库：https://github.com/2331221/KillTheCompetition
    功能反馈：欢迎提交 Issues 或 Pull Request 优化工具

    


