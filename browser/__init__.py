from selenium import webdriver

global browser

def visit(url):
    global browser
    browser=webdriver.Chrome(executable_path="/bin/chromedriver")
    browser.get(url)

def html():
    return browser.page_source

def close():
    browser.close()

def evaluate(script):
    browser.execute_script(script)
    return True

def cookie():
    return browser.get_cookies()
