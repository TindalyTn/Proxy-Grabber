import requests
from concurrent.futures import ThreadPoolExecutor
import time

def display_banner():
    print("""
_______ _           _       _      _______     
 |__   __(_)Sel3a    | |9wiya| |    |__   __|    
    | |   _ _ __   __| | __ _| |_The   | |_ __   
    | |  | | '_ \ / _` |/ _` | | | | | | | '_ \  
    | |  | | | | | (_| | (_| | | |_| |_| | | | |
    |_|  |_|_| |_|\__,_|\__,_|_|\__, (_)_|_| |_|
     Just For Fun!               __/ |          
                                |___/                                                                                              
                 =================================
                 [*] Fast Proxy Harvesting Tool [*]
                 [*] Multi-Source Scraper       [*]
                 [*] Real-Time Verification     [*]
                 =================================
    """)

def fetch_proxies(source_url):
    """Fetch proxies from a single source"""
    try:
        response = requests.get(source_url, timeout=10)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if ':' in line]
    except:
        pass
    return []

def verify_proxy(proxy):
    """Check if a proxy is working"""
    try:
        test_url = "http://www.google.com"
        response = requests.get(
            test_url,
            proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
            timeout=5
        )
        if response.status_code == 200:
            return proxy
    except:
        pass
    return None

def get_fresh_proxies():
    """Get and verify proxies from multiple sources"""
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
        "https://www.proxy-list.download/api/v1/get?type=http"
    ]

    print("🔍 Fetching proxies from multiple sources...")
    raw_proxies = []
    
    # Fetch from all sources in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_proxies, sources)
        for result in results:
            raw_proxies.extend(result)
    
    # Remove duplicates
    unique_proxies = list(set(raw_proxies))
    print(f"🔄 Found {len(unique_proxies)} raw proxies, now verifying...")
    
    # Verify proxies in parallel
    working_proxies = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(verify_proxy, unique_proxies)
        for result in results:
            if result:
                working_proxies.append(result)
                print(f"✅ Working proxy: {result}")
    
    return working_proxies

def save_proxies(proxies, filename="proxies.txt"):
    """Save proxies to a text file"""
    with open(filename, 'w') as f:
        f.write('\n'.join(proxies))
    print(f"\n💾 Saved {len(proxies)} working proxies to {filename}")

if __name__ == "__main__":
    display_banner()
    start_time = time.time()
    
    proxies = get_fresh_proxies()
    
    if proxies:
        save_proxies(proxies)
        print(f"\n⚡ Total working proxies: {len(proxies)}")
        print(f"⏱️  Execution time: {time.time() - start_time:.2f} seconds")
    else:
        print("❌ No working proxies found. Try again later.")