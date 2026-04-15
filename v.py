import concurrent.futures
import requests
import os
import sys

# Tắt cảnh báo SSL
requests.packages.urllib3.disable_warnings()

def check_one_proxy(proxy):
    # Thử lần lượt các giao thức
    protocols = ['http://', 'socks5://', 'socks4://']
    for proto in protocols:
        try:
            proxy_dict = {"http": f"{proto}{proxy}", "https": f"{proto}{proxy}"}
            # Thử kết nối đến Google hoặc Httpbin
            response = requests.get(
                "http://google.com", 
                proxies=proxy_dict, 
                timeout=5, # Giảm xuống 5s cho nhanh
                verify=False
            )
            if response.status_code == 200:
                return proxy, proto.upper().replace('://','')
        except:
            continue
    return None

def main():
    input_file = "proxy.txt"
    if not os.path.exists(input_file):
        print(f"Lỗi: Không tìm thấy file {input_file}")
        return

    with open(input_file, "r") as f:
        proxies = list(set([line.strip() for line in f if ":" in line]))

    print(f"Đang check {len(proxies)} proxy. Sử dụng 150 luồng...")
    
    with open("live_proxy.txt", "w") as f: pass # Reset file

    live_count = 0
    checked_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        futures = {executor.submit(check_one_proxy, p): p for p in proxies}
        
        for future in concurrent.futures.as_completed(futures):
            checked_count += 1
            result = future.result()
            
            if result:
                live_count += 1
                proxy_live, proto_name = result
                print(f"\n[LIVE] {proxy_live} ({proto_name})")
                with open("live_proxy.txt", "a") as f:
                    f.write(proxy_live + "\n")
            
            # Hiển thị tiến trình trên cùng 1 dòng để biết máy vẫn đang làm việc
            sys.stdout.write(f"\rTiến độ: {checked_count}/{len(proxies)} | Đã tìm thấy: {live_count}")
            sys.stdout.flush()

    print(f"\n\nHoàn tất! Đã lưu {live_count} proxy vào live_proxy.txt")

if __name__ == "__main__":
    main()
