from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.edge.service import Service
#NOTE: SUPPORTS ONLY MICROSOFT EDGE
# Enter Username & Password
username = "Username Here"
password = "Password Here"
# Ask the User if they want to use a proxy
use_proxy = input("Do you want to use a proxy? (y/n): ").lower()
if use_proxy == "y":
    # Ask for proxy Details
    proxy_host = input("Enter the Proxy IP: ")
    proxy_port = input("Enter the Proxy Port: ")
    # Create a proxy string
    proxy_string = f"{proxy_host}:{proxy_port}"
    # Set up a proxy with Edge WebDriver
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_string
    proxy.ssl_proxy = proxy_string
    capabilities = webdriver.DesiredCapabilities.EDGE
    proxy.add_to_capabilities(capabilities)
    # Initialize the Edge WebDriver Service
    service = Service(executable_path=r"msedgedriver.exe")
    service.start()
    driver = webdriver.Remote(service.service_url, desired_capabilities=capabilities)
else:
    # Initialize the Edge WebDriver Service without proxy
    service = Service(executable_path=r"msedgedriver.exe")
    service.start()
    driver = webdriver.Remote(service.service_url)
# Open Page
driver.get("https://codeforces.com/enter?back=%2F")
# Find the username and password Fields
username_field = driver.find_element_by_name("handleOrEmail")
password_field = driver.find_element_by_name("password")
# Fill in the username and password
username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)     # Submit
# Wait
import time
time.sleep(5)
# print Outputs
page_content = driver.page_source
if "Invalid handle/email or password" in page_content:
    print("Either Username, Email, or Password is wrong")
elif "Please, confirm email before entering the website." in page_content:
    print("Account Not Activated Yet")
elif "logout" in page_content:
    print("Successfully Logged In")
else:
    print("Unexpected Error")
# Close the browser and the service
driver.quit()
service.stop()
