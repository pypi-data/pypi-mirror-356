from utils.driver_factory import DriverFactory
from pages.base_page import BasePage

def main():
    url = input("Please enter the URL to open: ")
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
        
    browser = input("Please enter the browser (chrome, firefox, or edge): ").lower()

    driver = None
    try:
        driver = DriverFactory.get_driver(browser)
        driver.get(url)

        base_page = BasePage(driver)
        print(f"Page title is: '{base_page.get_title()}'")

        # You can add more interactions here using the base_page object
        # For example, to find an element by its ID and get its text:
        # from selenium.webdriver.common.by import By
        # element_text = base_page.get_text(By.ID, "your_element_id")
        # print(f"Element text is: {element_text}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to close the browser...")
        DriverFactory.quit_driver(driver)

if __name__ == "__main__":
    main() 