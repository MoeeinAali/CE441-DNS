import subprocess

def get_target_info():
    # دستوراتی که می‌خواهیم در GDB اجرا شوند
    # ۱. گذاشتن breakpoint روی تابع foo
    # ۲. اجرا با فایل اکسپلویت
    # ۳. چاپ آدرس بافر buf
    # ۴. چاپ آدرس rbp برای محاسبه فاصله
    gdb_commands = """
    break foo
    run /tmp/xploit1_output
    echo \n--- TARGET INFO ---\n
    print/p "Address of buf: "
    print &buf
    print/p "Saved RBP: "
    print $rbp
    echo \n--- STACK FRAME ---\n
    info frame
    quit
    """
    
    # ذخیره دستورات در یک فایل موقت
    with open("gdb_script.txt", "w") as f:
        f.write(gdb_commands)

    # اجرای gdb به صورت مستقیم
    try:
        result = subprocess.run(
            ['gdb', '-q', '-batch', '-x', 'gdb_script.txt', '/tmp/target1'],
            capture_output=True, text=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_target_info()