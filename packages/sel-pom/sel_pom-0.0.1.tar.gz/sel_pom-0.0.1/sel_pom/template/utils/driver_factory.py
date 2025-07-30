from selenium import webdriver

class DriverFactory:
    @staticmethod
    def get_driver(browser="chrome"):
        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            return webdriver.Chrome(options=options)
        elif browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            return webdriver.Firefox(options=options)
        elif browser.lower() == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("start-maximized")
            return webdriver.Edge(options=options)
        raise Exception("Provide a valid browser name")

    @staticmethod
    def quit_driver(driver):
        if driver:
            driver.quit() 