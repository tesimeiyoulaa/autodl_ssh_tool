import re
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


def parse_ssh():
    text = entry.get().strip()
    m = re.match(r"ssh\s+-p\s+(\d+)\s+(\S+)", text, re.IGNORECASE)
    if not m:
        messagebox.showwarning("格式错误", "请输入形如：ssh -p 23497 root@host")
        return

    port = m.group(1)
    user_host = m.group(2)
    if "@" not in user_host:
        messagebox.showwarning("格式错误", "缺少用户，如：root@connect.westc.gpuhub.com")
        return

    user, host_name = user_host.split("@", 1)

    # 生成配置，Host 用端口号命名
    lines = [
        f"Host {port}",
        f"  HostName {host_name}",
        f"  Port {port}",
        f"  User {user}",
    ]
    result = "\n".join(lines)

    # 输出到文本框
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result)
    output_text.config(state="normal")  # 保持可选中/复制
    status_var.set("已生成配置，可点击“写入确认”保存到 config")


def write_config():
    config_text = output_text.get("1.0", tk.END).strip()
    if not config_text or config_text == "输出会显示在这里":
        messagebox.showwarning("无可写入内容", "请先点击“生成配置”再写入。")
        return

    confirm = messagebox.askyesno(
        "确认写入",
        "即将把当前配置追加写入：\nC:\\Users\\zrh\\.ssh\\config\n\n是否继续？",
    )
    if not confirm:
        return

    config_path = Path.home() / ".ssh" / "config"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with config_path.open("a", encoding="utf-8") as f:
            if config_path.stat().st_size > 0:
                f.write("\n\n")
            f.write(config_text)
            f.write("\n")
        messagebox.showinfo("写入成功", f"配置已写入：\n{config_path}")
        status_var.set(f"写入成功：{config_path}")
    except OSError as e:
        messagebox.showerror("写入失败", f"无法写入配置文件：\n{e}")
        status_var.set("写入失败，请检查权限或路径")


root = tk.Tk()
root.title("SSH Config Builder")
root.geometry("820x460")
root.minsize(760, 420)
root.configure(bg="#eef2f7")

style = ttk.Style()
style.theme_use("clam")
# 使用更适合中文显示的字体，提升清晰度
ui_font = ("Microsoft YaHei UI", 10)
title_font = ("Microsoft YaHei UI", 16, "bold")
mono_font = ("Microsoft YaHei UI", 11)
root.option_add("*Font", ui_font)

style.configure("Card.TFrame", background="#ffffff")
style.configure("Title.TLabel", background="#ffffff", foreground="#0f172a", font=title_font)
style.configure("Hint.TLabel", background="#ffffff", foreground="#64748b", font=ui_font)
style.configure("Field.TLabel", background="#ffffff", foreground="#334155", font=ui_font)
style.configure("Primary.TButton", font=("Microsoft YaHei UI", 10, "bold"))
style.configure("Secondary.TButton", font=ui_font)
style.configure("Status.TLabel", background="#eef2f7", foreground="#475569", font=ui_font)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

main_card = ttk.Frame(root, style="Card.TFrame", padding=20)
main_card.grid(row=0, column=0, sticky="nsew", padx=18, pady=(18, 10))
main_card.grid_columnconfigure(0, weight=1)
main_card.grid_rowconfigure(4, weight=1)

ttk.Label(main_card, text="SSH Config 生成工具", style="Title.TLabel").grid(row=0, column=0, sticky="w")
ttk.Label(main_card, text="输入 SSH 命令，一键生成并安全写入本地 SSH 配置。", style="Hint.TLabel").grid(
    row=1, column=0, sticky="w", pady=(4, 14)
)

input_wrap = ttk.Frame(main_card, style="Card.TFrame")
input_wrap.grid(row=2, column=0, sticky="ew")
input_wrap.grid_columnconfigure(0, weight=1)

ttk.Label(input_wrap, text="输入 ssh 命令", style="Field.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
entry = ttk.Entry(input_wrap)
entry.grid(row=1, column=0, sticky="ew")
entry.insert(0, "ssh -p 23497 root@connect.westc.gpuhub.com")

btns = ttk.Frame(input_wrap, style="Card.TFrame")
btns.grid(row=1, column=1, sticky="e", padx=(10, 0))

btn = ttk.Button(btns, text="生成配置", command=parse_ssh, style="Primary.TButton")
btn.grid(row=0, column=0, padx=(0, 8))

write_btn = ttk.Button(btns, text="写入确认", command=write_config, style="Secondary.TButton")
write_btn.grid(row=0, column=1)

ttk.Label(main_card, text="输出（可复制）", style="Field.TLabel").grid(row=3, column=0, sticky="sw", pady=(12, 6))

output_text = tk.Text(
    main_card,
    height=10,
    wrap="word",
    relief="flat",
    borderwidth=0,
    padx=12,
    pady=10,
    bg="#f8fafc",
    fg="#0f172a",
    insertbackground="#1e293b",
    font=mono_font,
)
output_text.grid(row=4, column=0, sticky="nsew")
output_text.insert("1.0", "输出会显示在这里")

status_var = tk.StringVar(value="就绪：请先输入 SSH 命令并点击“生成配置”")
status = ttk.Label(root, textvariable=status_var, style="Status.TLabel")
status.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 14))

root.mainloop()
