from selenium import webdriver

def prepare_webdriver():
    headless_mode = 0
    proxy_mode = 0
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
        
    if headless_mode == 1:
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
        options.add_argument("--lang=en-us")

    if proxy_mode == 1:
        # https://www.hide-my-ip.com/proxylist.shtml
        # Type:HTTPS, Anon:High, 그리고 속도 빠른 걸로 선택.
        PROXY = "5.135.164.72:3128"
        options.add_argument('--proxy-server=%s' % PROXY)
        
    browser = webdriver.Chrome(chrome_options=options)

    return browser
