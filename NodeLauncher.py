import subprocess
import threading
import queue
import os
import urllib.request
import zipfile
import sys
import ctypes
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard  # 添加全局热键监听库
import win32gui
import win32con
import customtkinter as ctk
import time


# ========================= Overlay 窗口 =========================
class OverlayWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.config(bg="black")

        # 白色加粗字体
        self.label = tk.Label(
            self.root,
            text="等待数据...",
            font=("Arial", 10, "bold"),  # 14 → 10
            fg="white",
            bg="black",
            justify="left"
        )
        self.label.pack(anchor="w")

    def start(self):
        self.update_position()

    def update_position(self):
        hwnd = win32gui.FindWindow(None, "星痕共鸣")
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            # 右上角，往左10px，往下10px
            x = rect[2] - 10 - self.root.winfo_reqwidth()
            y = rect[1] + 10
            self.root.geometry(f"+{x}+{y}")
        self.root.after(1000, self.update_position)

    def update_text(self, text):
        self.label.config(text=text)


def check_and_install_dependencies(self):
    """ 检查并安装必需的模块，如 cap 和 winston """
    try:
        # 使用相对路径调用 npm 检查 cap 模块是否存在
        npm_path = os.path.join(os.getcwd(), self.NODE_NPM_PATH)  # 获取当前路径并拼接 npm 路径
        subprocess.check_call([npm_path, 'ls', 'cap'])
        self.log_queue.put("cap 模块已安装。\n")
    except subprocess.CalledProcessError:
        # cap 模块未安装，执行安装
        self.log_queue.put("检测到 cap 模块未安装，开始安装...\n")
        subprocess.check_call([npm_path, 'install', 'cap'])
        self.log_queue.put("cap 模块安装完成。\n")
    except FileNotFoundError:
        self.log_queue.put(f"未找到 npm，路径: {npm_path}\n")
        messagebox.showerror("错误", f"未找到 npm，请确保 Node.js 已正确安装。")

    try:
        # 使用相对路径调用 npm 检查 winston 模块是否存在
        subprocess.check_call([npm_path, 'ls', 'winston'])
        self.log_queue.put("winston 模块已安装。\n")
    except subprocess.CalledProcessError:
        # winston 模块未安装，执行安装
        self.log_queue.put("检测到 winston 模块未安装，开始安装...\n")
        subprocess.check_call([npm_path, 'install', 'winston'])
        self.log_queue.put("winston 模块安装完成。\n")
    except FileNotFoundError:
        self.log_queue.put(f"未找到 npm，路径: {npm_path}\n")
        messagebox.showerror("错误", f"未找到 npm，请确保 Node.js 已正确安装。")


# ========================= 主 GUI =========================
class NodeLauncher(ctk.CTk):
    NODE_VERSION = "v22.18.0"
    NODE_BASE_URL = f"https://nodejs.org/dist/{NODE_VERSION}/node-{NODE_VERSION}-win-x64.zip"
    NODE_DIR = "nodejs"
    NODE_EXE_RELATIVE = f"node-{NODE_VERSION}-win-x64/node.exe"
    NODE_NPM_PATH = os.path.join("nodejs", f"node-{NODE_VERSION}-win-x64", "npm")

    def __init__(self):
        super().__init__()
        self.title("Star Resonance Damage Counter 启动器")
        self.geometry("450x500")
        self.config(bg="#2f3136")

        self.proc = None
        self.log_queue = queue.Queue()

        # 标题
        ttk.Label(self, text="设备编号:", font=("Arial", 10), foreground="white", background="#2f3136").grid(row=0,
                                                                                                             column=0,
                                                                                                             sticky="w",
                                                                                                             padx=20,
                                                                                                             pady=10)
        self.device_var = tk.StringVar(value="0")
        ttk.Entry(self, textvariable=self.device_var, width=20, font=("Arial", 10)).grid(row=0, column=1, sticky="w",
                                                                                         padx=20)

        ttk.Label(self, text="日志等级:", font=("Arial", 10), foreground="white", background="#2f3136").grid(row=1,
                                                                                                             column=0,
                                                                                                             sticky="w",
                                                                                                             padx=20,
                                                                                                             pady=10)
        self.log_level_var = tk.StringVar(value="info")
        ttk.Combobox(self, values=["info", "debug"], textvariable=self.log_level_var, state="readonly", width=18,
                     font=("Arial", 10)).grid(row=1, column=1, sticky="w", padx=20)

        ttk.Label(self, text="自动清空时间(秒):", font=("Arial", 10), foreground="white", background="#2f3136").grid(
            row=2, column=0, sticky="w", padx=20, pady=10)
        self.clear_interval_var = tk.IntVar(value=60)  # 默认 1 分钟
        ttk.Entry(self, textvariable=self.clear_interval_var, width=20, font=("Arial", 10)).grid(row=2, column=1,
                                                                                                 sticky="w", padx=20)

        # 启动按钮
        self.start_btn = ttk.Button(self, text="启动", command=self.start_server, style="TButton")
        self.start_btn.grid(row=3, column=0, padx=20, pady=15, sticky="ew")
        self.stop_btn = ttk.Button(self, text="停止", command=self.stop_server, state="disabled", style="TButton")
        self.stop_btn.grid(row=3, column=1, padx=20, pady=15, sticky="ew")

        # 日志显示区域
        self.log_text = tk.Text(self, width=50, height=15, state="disabled", font=("Courier New", 10), bg="#1e2124",
                                fg="white", bd=0, wrap="word")
        self.log_text.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

        # 进度条
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="indeterminate")
        self.progress.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

        self.after(100, self.poll_log)

        # 启动 Overlay
        self.overlay = OverlayWindow()
        self.overlay.start()

        # 启动全局热键监听（F6 清空数据）
        threading.Thread(target=self.listen_global_hotkeys, daemon=True).start()

        # 启动自动清空计时器
        self.auto_clear_timer()

    def check_and_install_cap(self):
        """ 检查并安装 cap 模块 """
        try:
            # 使用相对路径调用 npm 检查 cap 模块是否存在
            npm_path = os.path.join(os.getcwd(), self.NODE_NPM_PATH)  # 获取当前路径并拼接 npm 路径
            subprocess.check_call([npm_path, 'ls', 'cap'])
            self.log_queue.put("cap 模块已安装。\n")
        except subprocess.CalledProcessError:
            # cap 模块未安装，执行安装
            self.log_queue.put("检测到 cap 模块未安装，开始安装...\n")
            subprocess.check_call([npm_path, 'install', 'cap'])
            self.log_queue.put("cap 模块安装完成。\n")
        except FileNotFoundError:
            self.log_queue.put(f"未找到 npm，路径: {npm_path}\n")
            messagebox.showerror("错误", f"未找到 npm，请确保 Node.js 已正确安装。")

    def start_server(self):
        #启动服务器
        if self.proc:
            messagebox.showwarning("警告", "服务已经启动了！")
            return

        device = self.device_var.get()
        log_level = self.log_level_var.get()

        if not device.isdigit():
            messagebox.showerror("错误", "设备编号必须是数字")
            return

        if log_level not in ("info", "debug"):
            messagebox.showerror("错误", "日志等级必须是 info 或 debug")
            return

        # 下载并安装 Node.js 和 npm
        node_path = self.check_and_download_node()
        if not node_path:
            messagebox.showerror("错误", "无法找到或安装 Node.js，无法启动服务。")
            return

        folder_path = os.getcwd()  # 当前工作目录作为项目目录
        cmd = [node_path, "server.js", device, log_level]

        try:
            self.proc = subprocess.Popen(
                cmd,
                cwd=folder_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except Exception as e:
            messagebox.showerror("错误", f"启动服务失败: {e}")
            return

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        threading.Thread(target=self._read_output, daemon=True).start()
        threading.Thread(target=self.update_overlay_data, daemon=True).start()

    def _read_output(self):
        #读取输出
        try:
            for line in self.proc.stdout:
                self.log_queue.put(line)
        except Exception as e:
            self.log_queue.put(f"读取输出失败: {e}\n")

    def check_and_download_node(self):
        #检查并下载 Node.js
        node_exe_path = os.path.join(self.NODE_DIR, self.NODE_EXE_RELATIVE)
        if os.path.exists(node_exe_path):
            return node_exe_path

        self.log_queue.put("检测到未安装 Node.js，开始下载...\n")
        os.makedirs(self.NODE_DIR, exist_ok=True)
        zip_path = os.path.join(self.NODE_DIR, "node.zip")

        def download_thread():
            try:
                self.progress.start()  # 开始显示进度条
                urllib.request.urlretrieve(self.NODE_BASE_URL, zip_path, reporthook=self.download_progress)
                self.log_queue.put("下载完成，开始解压...\n")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.NODE_DIR)
                os.remove(zip_path)
                self.log_queue.put("Node.js 解压完成。\n")
            except Exception as e:
                self.log_queue.put(f"下载或解压失败: {e}\n")

            self.progress.stop()  # 下载完成后停止进度条

        download_thread = threading.Thread(target=download_thread, daemon=True)
        download_thread.start()

        return node_exe_path

    def download_progress(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percentage = (downloaded / total_size) * 100
            self.overlay.update_text(f"下载进度: {percentage:.2f}%")

    def poll_log(self):
        while not self.log_queue.empty():
            line = self.log_queue.get_nowait()
            if "Damage/Healing" in line:
                continue
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
            self.log_text.config(state="disabled")

        if self.proc and self.proc.poll() is not None:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.proc = None
            self.log_queue.put("\n[服务已停止]\n")

        self.after(100, self.poll_log)

    def stop_server(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.log_queue.put("\n[发送停止命令]\n")

    def update_overlay_data(self):
        while True:
            if not self.proc:
                self.overlay.update_text("服务未启动")
            else:
                try:
                    resp = requests.get("http://localhost:8989/api/data", timeout=1)
                    if resp.status_code == 200:
                        json_data = resp.json()
                        user_data = json_data.get("user", {})
                        parts = []
                        for uid, stats in user_data.items():
                            total_damage = int(stats['total_damage']['total'])
                            total_dps = stats.get('total_dps', 0)
                            # 显示总伤害和总DPS/HPS，格式化成整数或保留1位小数
                            parts.append(
                                f"UID:{uid}\n总伤害: {total_damage}\n总DPS/HPS: {total_dps:.1f}"
                            )
                        self.overlay.update_text("\n\n".join(parts))
                    else:
                        self.overlay.update_text(f"获取数据失败：{resp.status_code}")
                except Exception:
                    self.overlay.update_text("等待数据中...")
            time.sleep(2)

    def listen_global_hotkeys(self):
        # 监听 F6 键，全局清空数据
        keyboard.add_hotkey('F6', self.clear_data)
        keyboard.wait()  # 等待热键按下

    def auto_clear_timer(self):
        # 自动清空定时器
        interval = self.clear_interval_var.get()
        threading.Timer(interval, self.auto_clear_data).start()

    def auto_clear_data(self):
        self.clear_data()
        self.auto_clear_timer()

    def clear_data(self):
        # 清空日志显示区域
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        self.log_queue.queue.clear()
        self.overlay.update_text("数据已清空")


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

    app = NodeLauncher()
    app.mainloop()
