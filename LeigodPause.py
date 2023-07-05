from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import configparser
import time
import psutil
import time
# 设置Chrome选项
def pauseLeiGod():
    options = Options()
    #设置缓存路径，使用用户cookie自动登录
    #options.add_argument("user-data-dir=C:\\Users\\63484\\AppData\\Local\\Google\\Chrome\\User Data")
    #模拟正常浏览器
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"')
    options.add_argument("--headless")  # 无头模式
    #隐藏"Chrome正在受到自动软件的控制"
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #创建浏览器示例
    webdriver_service = Service('C:\\app\\pythonDriver\\chromedriver.exe')
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    driver.set_window_size(1920, 1080)
    driver.get('https://vip.leigod.com/user.html')

    try:
        # 定位手机号输入框并输入手机号
        phone_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="手机号"]')))
        phone_input.clear()
        phone_input.send_keys("PhoneNumber")  # 请替换为你的手机号
        # 定位密码输入框并输入密码
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="密码"]')))
        password_input.clear()
        password_input.send_keys("Password")  # 请替换为你的密码
        # 定位登录按钮并点击
        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="web_login_btn pos_banner_txt1"]')))
        login_button.click()
    except TimeoutException as e:
        print(e)
    try:
        pause_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="暂停中"]'))
            )
        print("加速器已经暂停")
    except TimeoutException as e:
        stop_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[3]/a[1]/i')))
        stop_button.click()
        pause_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="暂停中"]'))
            )
        print("加速器已经暂停")
    driver.quit()
        
def monitor_games():
    # 读取配置文件
    import os
    #这里修改为工作目录
    os.chdir('C:\\Users\\63484\\.cursor-tutor\\projects\\python\\雷神自动暂停')
    if not os.path.exists('config.ini'):
        print('config.ini文件不存在')
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 获取游戏进程的路径
    game_names = config.get('Games', 'game_names').split(',')
    # 上一次检查时的游戏进程状态
    last_game_status = {path: False for path in game_names}

    while True:
        # 检查每个游戏进程
        running_processes = [proc.info['name'] for proc in psutil.process_iter(['name'])]
        for game_name in game_names:
            # 获取当前的游戏进程状态
            current_game_status = game_name in running_processes

            # 如果游戏进程已经开始运行，那么打印一条消息
            if not last_game_status[game_name] and current_game_status:
                print(f"游戏运行中: {game_name}")

            # 如果游戏进程已经结束，那么调用pauseLeiGod函数
            if last_game_status[game_name] and not current_game_status:
                pauseLeiGod()

            # 更新游戏进程状态
            last_game_status[game_name] = current_game_status

        # 每隔一段时间检查一次
        time.sleep(5)
if __name__ == "__main__":
    monitor_games()