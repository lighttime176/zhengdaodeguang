import random
import time
import logging
from DrissionPage import ChromiumPage, ChromiumOptions

def logging_init():
    """ 初始化日志记录 """
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 文件处理器
    file_handler = logging.FileHandler('a.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

logger = logging_init()

def setup_browser():
    """ 配置浏览器并创建 ChromiumPage 实例 """
    co = ChromiumOptions()
    co.set_argument('--no-sandbox') 
    co.set_argument('--headless=new')  
    co.set_paths(browser_path="/opt/google/chrome/google-chrome")  
    co.set_argument('--disable-gpu')    
    co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

    return ChromiumPage(co)
browser = setup_browser()
tab = browser.latest_tab
def main():
    
    
    tab.get("https://aospmam.slczu.cn/uyiu/doc.html?")
    tab.set.window.max()

    # 进入账号输入界面
    tab.ele('css=#g_u > div.my').click()

    # 获取 numkey 里的所有按钮
    numkey = tab.ele('css=#key4')
    numele = numkey.eles('tag:li')  # 获取所有的 <li> 子元素
    #print(f'发现 {len(numele)} 个数字按键')

    # 生成随机账号
    qq = ''.join(random.choice('123456789') for _ in range(10))
    for num in qq:
        numele[int(num)-1].click()

    # 进入密码输入界面
    tab.ele('css=#g_p > div.my').click()

    # 获取键盘中的所有按键
    s = tab.ele('css=#key1').eles('tag:li')
    #print(f'发现 {len(s)} 个密码按键')
    time.sleep(2)

    # 生成随机密码
    password = ''
    time.sleep(0.8)
    #print(s)
    for _ in range(10):
        random_index = random.randint(0, 17)
        s[random_index].click()
        password += s[random_index].text  # 记录点击的文本


    #logger.info(f"最终输入的密码: {password}")


    # 提交表单
    tab.ele('css=#go').click()


    # 获取页面文本
    ele = tab.ele('css=#form > div.wrap')
    text = ele.text if ele else ""

    if "手机" in text:
        logger.info(f'账号：{qq}, 密码：{password}')
        tab.get_screenshot(path=r"./test_browser_page.png", full_page=True)
    else:
        logger.info("字符串不包含 '验证码'，程序退出")
        exit()
for i in range(10):
    main()
