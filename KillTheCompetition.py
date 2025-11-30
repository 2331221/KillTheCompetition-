import requests
import os
import time
from datetime import datetime

# ==================== 炫酷配置 ====================
# 颜色常量（ANSI 转义序列，Windows 10+ 支持）
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
BLINK = "\033[5m"  # 闪烁效果（部分终端支持）

# 扫描目标列表（覆盖所有高频泄露类型）
LEAK_TYPES = {
    # bak 备份文件（常见文件名+后缀）
    "bak": [
        "index.php.bak", "config.php.bak", "database.php.bak",
        "web.zip.bak", "backup.rar.bak", "wwwroot.tar.gz.bak",
        "flag.txt.bak", "readme.md.bak", "app.py.bak",
        ".env.bak", "settings.py.bak", "db.sql.bak"
    ],
    # Vim 缓存文件（.swp 临时文件、.swo 交换文件、.swx 紧急文件）
    "vim": [
        "index.php.swp", "config.php.swp", "flag.txt.swp",
        "index.php.swo", "config.php.swo", "flag.txt.swo",
        "index.php.swx", "config.php.swx", "flag.txt.swx",
        ".index.php.swp", ".config.php.swp"  # 隐藏缓存文件
    ],
    # .DS_Store（Mac 隐藏文件，可能泄露目录结构）
    "ds_store": [".DS_Store", "backup/.DS_Store", "web/.DS_Store", "www/.DS_Store"]
}

# 请求配置
TIMEOUT = 3
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "close"
}

# ==================== 炫酷工具函数 ====================
def print_banner():
    """打印炫酷横幅"""
    banner = f"""
{BOLD}{PURPLE}
 
  _____________________________________________________________ 
 |                                                             |
 |{CYAN}泄露扫描{BOLD}{PURPLE}|{CYAN}BAK/VIM{BLUE}/DS_STORE{BOLD}{PURPLE}|{CYAN}全能探测{BOLD}{PURPLE}|{CYAN}极速响应{BOLD}{PURPLE}|{CYAN}杀死比赛{BOLD}{PURPLE}|{CYAN}安全可靠{BOLD}{PURPLE}|
 |_____________________________________________________________|
    {YELLOW}[+] 支持类型：bak备份文件 | Vim缓存文件 | .DS_Store泄露
    {YELLOW}[+] 扫描模式：全量探测 + 状态码验证 + 内容校验
    {YELLOW}[+] 高校扫描 + 进度动画 + 扫描统计
    {YELLOW}[+] 如虎踞官网：www.onechx.icu
    {YELLOW}[+] 本工具只用于学习交流，不得用于非法用途，一切后果与制作者无关！
{BOLD}{GREEN}  ==============================================
{RESET}
    """
    print(banner)

def print_loading(progress, total):
    """打印炫酷进度条"""
    bar_length = 50
    completed = int(bar_length * progress / total)
    remaining = bar_length - completed
    # 进度条动画
    bar = f"{GREEN}{'█' * completed}{YELLOW}{'░' * remaining}{RESET}"
    # 百分比和状态
    percent = f"{progress/total*100:.1f}%"
    # 动态覆盖输出
    print(f"\r{BOLD}{BLUE}[扫描进度] {bar} {percent} | 已探测：{progress}/{total} 个目标{BOLD}{RESET}", end="")

def print_result(found_leaks):
    """打印扫描结果（炫酷格式化）"""
    print(f"\n\n{BOLD}{CYAN}="*60)
    print(f"{BOLD}{GREEN}[{datetime.now().strftime('%H:%M:%S')}] 扫描完成！{RESET}")
    print(f"{BOLD}{CYAN}="*60)
    
    if found_leaks:
        print(f"\n{BOLD}{BLINK}{RED}[🎉 发现 {len(found_leaks)} 个泄露文件！] {RESET}")
        for idx, leak in enumerate(found_leaks, 1):
            print(f"\n{BOLD}{idx}. {GREEN}[{leak['type']}] {leak['url']}{RESET}")
            print(f"   {YELLOW}状态码：{leak['status_code']}{RESET}")
            print(f"   {CYAN}文件大小：{leak['size']} KB{RESET}")
    else:
        print(f"\n{BOLD}{YELLOW}[😢 未发现任何泄露文件] {RESET}")
        print(f"{BOLD}{BLUE}提示：尝试更换目标URL或扩展扫描字典{RESET}")

# ==================== 核心扫描逻辑 ====================
def scan_leaks(target_url):
    """扫描目标URL的泄露文件"""
    # 格式化目标URL（确保以/结尾）
    target_url = target_url.rstrip("/") + "/"
    found_leaks = []
    total_targets = sum(len(files) for files in LEAK_TYPES.values())
    scanned = 0

    print(f"\n{BOLD}{PURPLE}[🚀 开始扫描目标：{target_url}]{RESET}")
    print(f"{BOLD}{BLUE}[ℹ️  扫描类型：bak文件({len(LEAK_TYPES['bak'])}个) | Vim文件({len(LEAK_TYPES['vim'])}个) | DS_Store({len(LEAK_TYPES['ds_store'])}个){RESET}")
    time.sleep(1)

    # 遍历所有泄露类型和目标文件
    for leak_type, files in LEAK_TYPES.items():
        for file in files:
            scanned += 1
            # 拼接完整URL
            leak_url = f"{target_url}{file}"
            try:
                # 发送请求（禁止重定向，避免误判）
                response = requests.get(
                    leak_url,
                    headers=HEADERS,
                    timeout=TIMEOUT,
                    allow_redirects=False,
                    verify=False  # 忽略SSL证书错误
                )

                # 验证有效泄露（状态码200 + 内容非空）
                if response.status_code == 200 and len(response.content) > 0:
                    leak_info = {
                        "type": leak_type.upper(),
                        "url": leak_url,
                        "status_code": response.status_code,
                        "size": round(len(response.content)/1024, 2)
                    }
                    found_leaks.append(leak_info)
                    # 实时提示发现泄露
                    print(f"\n{BOLD}{RED}[⚠️  发现{leak_type.upper()}泄露！] {GREEN}{leak_url}{RESET}")

                # 更新进度条
                print_loading(scanned, total_targets)

            except requests.exceptions.Timeout:
                print_loading(scanned, total_targets)
            except requests.exceptions.ConnectionError:
                print(f"\n{BOLD}{RED}[❌ 连接失败：{target_url} 无法访问]{RESET}")
                return found_leaks
            except Exception as e:
                print_loading(scanned, total_targets)

    return found_leaks

# ==================== 主函数 ====================
def main():
    # 打印炫酷横幅
    print_banner()

    # 让用户输入目标URL
    target_url = input(f"{BOLD}{YELLOW}[📌 请输入目标URL（例：http://xxx.com）：]{RESET}").strip()

    # 验证URL格式
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print(f"{BOLD}{RED}[❌ 错误：URL必须以http://或https://开头！]{RESET}")
        return

    # 开始扫描
    found_leaks = scan_leaks(target_url)

    # 打印结果
    print_result(found_leaks)

    # 保存结果到文件（可选）
    save = input(f"\n{BOLD}{CYAN}[💾 是否保存扫描结果到文件？(y/n)：]{RESET}").strip().lower()
    if save == "y":
        filename = f"leak_scan_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"目标URL：{target_url}\n")
            f.write(f"扫描总数：{sum(len(files) for files in LEAK_TYPES.values())}\n")
            f.write(f"泄露数量：{len(found_leaks)}\n")
            f.write("="*50 + "\n")
            for leak in found_leaks:
                f.write(f"类型：{leak['type']}\n")
                f.write(f"URL：{leak['url']}\n")
                f.write(f"状态码：{leak['status_code']}\n")
                f.write(f"大小：{leak['size']} KB\n")
                f.write("-"*30 + "\n")
        print(f"{BOLD}{GREEN}[✅ 结果已保存到：{os.path.abspath(filename)}]{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{BOLD}{RED}[⚠️  用户中断扫描！]{RESET}")
    except Exception as e:
        print(f"\n{BOLD}{RED}[❌ 程序异常：{str(e)}]{RESET}")
