import requests
import json
import random
import string
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============ KONFIGURASI ============
total_accounts = 50000000000        # total akun yang ingin dibuat
max_workers = 50            # jumlah thread paralel (setting sesuai kemampuan jaringan/API)
min_delay = 1.0             # jeda minimum antar request (detik)
max_delay = 15.0             # jeda maksimum antar request (detik)
output_file = "accounts-4.txt"
# =====================================

file_lock = threading.Lock()
success_count = 0
fail_count = 0

def random_account():
    prefix = "859"
    suffix = ''.join(random.choices(string.digits, k=8))
    return prefix + suffix

def random_finger_prefix():
    return ''.join(random.choices(string.hexdigits.lower(), k=8))

def register_one(index):
    global success_count, fail_count
    account = random_account()
    finger = random_finger_prefix() + "bb820ff793a04ff1ea67e0a0"
    
    payload = {
        "account": account,
        "password": "123456",
        "currency_id": 2,
        "name": "",
        "contact": {"m_prefix": "62", "mobile": "", "email": ""},
        "birthday": 0,
        "payment": [],
        "finger": finger,
        "ua": "Mozilla/5.0 (Linux; Android 14; SM-A042F Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/151.0.7922.47 Mobile Safari/537.36 app/H5",
        "platformChannel": {"pix": ""},
        "smsVerifyCode": "",
        "profile": "{\"fbDynamicPixel\":null,\"ttPixel\":null,\"gtmId\":null}",
        "invite_code": "",
        "captchaKey": "",
        "captchaValue": ""
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 14; SM-A042F Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/151.0.7922.47 Mobile Safari/537.36 app/H5",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Not=A?Brand\";v=\"99\", \"Android WebView\";v=\"151\", \"Chromium\";v=\"151\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://wgappi02.com",
        'x-requested-with': "com.ukk.wg87",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://wgappi02.com/IDR-id/register",
        'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i"
    }
    
    try:
        # jeda acak sebelum request (agar tidak bersamaan persis)
        time.sleep(random.uniform(min_delay, max_delay))
        
        response = requests.post(
            "https://wgappi02.com/api/Register",
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("code") == 0:
                with file_lock:
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(f"{account}|123456\n")
                success_count += 1
                print(f"[Thread-{index}] ✅ Berhasil: {account} (sukses={success_count}, gagal={fail_count})")
                return True
            else:
                fail_count += 1
                print(f"[Thread-{index}] ❌ Gagal code {resp_json.get('code')}: {resp_json.get('msg', '')} (sukses={success_count}, gagal={fail_count})")
                return False
        else:
            fail_count += 1
            print(f"[Thread-{index}] ❌ HTTP {response.status_code} (sukses={success_count}, gagal={fail_count})")
            return False
    except Exception as e:
        fail_count += 1
        print(f"[Thread-{index}] ⚠️ Exception: {e} (sukses={success_count}, gagal={fail_count})")
        return False

def main():
    print(f"🚀 Memulai registrasi paralel: {total_accounts} akun, {max_workers} thread")
    print(f"⏳ Jeda antar request: {min_delay}–{max_delay} detik\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(register_one, i): i for i in range(1, total_accounts + 1)}
        for future in as_completed(futures):
            # biarkan print dari dalam thread, kita tunggu selesai semua
            pass
    
    print(f"\n✅ Selesai! Total sukses: {success_count}, gagal: {fail_count}")
    print(f"📁 Akun tersimpan di {output_file}")

if __name__ == "__main__":
    main()
