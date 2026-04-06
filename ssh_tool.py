import re
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


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
    except OSError as e:
        messagebox.showerror("写入失败", f"无法写入配置文件：\n{e}")


root = tk.Tk()
root.title("SSH Config 生成工具")

frame = tk.Frame(root, padx=12, pady=12)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="输入 ssh 命令：").grid(row=0, column=0, sticky="w")
entry = tk.Entry(frame, width=55)
entry.grid(row=1, column=0, sticky="we")
entry.insert(0, "ssh -p 23497 root@connect.westc.gpuhub.com")

btn = tk.Button(frame, text="生成配置", command=parse_ssh)
btn.grid(row=1, column=1, padx=(8, 0))

write_btn = tk.Button(frame, text="写入确认", command=write_config)
write_btn.grid(row=1, column=2, padx=(8, 0))

tk.Label(frame, text="输出（可复制）：").grid(row=2, column=0, sticky="w", pady=(10, 0))

output_text = tk.Text(frame, width=55, height=5, fg="blue")
output_text.grid(row=3, column=0, columnspan=3, sticky="we")
output_text.insert("1.0", "输出会显示在这里")

frame.columnconfigure(0, weight=1)

root.mainloop()
