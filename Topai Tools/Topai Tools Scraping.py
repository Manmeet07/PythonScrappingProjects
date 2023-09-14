import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def scroll_down_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Adjust the sleep time if needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_topai_tools():
    url = "https://topai.tools/browse"
    
    # Use Selenium to simulate Edge browser in headless mode
    edge_options = Options()
    edge_options.add_argument("--headless")  # Run browser in headless mode
    edge_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    service = Service("F:\BTech\Projects\Scrape Python\msedgedriver.exe")
    service.start()
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get(url)
    scroll_down_page(driver)
    html_content = driver.page_source
    driver.quit()
    service.stop()

    soup = BeautifulSoup(html_content, "html.parser")
    tools = []

    for tool_box in soup.find_all("div", class_="tool_box"):
        tool_name = tool_box.find("i", class_="bi-heart").get("data-title", "").strip()
        tool_url = tool_box.find("i", class_="bi-heart")["data-website"]
        pricing = tool_box.find("span", class_="pricing-badge").text.strip()
        tags = tool_box.find("i", class_="bi-heart").get("data-tags", "").strip()
        tool_use = ""
        tool_use_element = tool_box.find("p", class_="my-1 font-weight-lighter px-1")
        if tool_use_element:
            tool_use = tool_use_element.text.strip()
            
        tools.append([tool_name, tool_url, pricing, tags, tool_use])

    return tools

def save_to_excel(tools_list, filename):
    df = pd.DataFrame(tools_list, columns=["Tool Name", "Tool URL", "Pricing", "Tags", "Tool Use"])
    df.to_excel(filename, index=False)
    print(f"Data has been saved to '{filename}'")

if __name__ == "__main__":
    tools_data = scrape_topai_tools()

    if tools_data:
        save_to_excel(tools_data, "topai_tools.xlsx")
