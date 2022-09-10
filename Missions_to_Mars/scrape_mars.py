# Automates browser actions
from splinter import Browser
import time
# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Setup splinter
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for listings that we can save to Mongo
    mars = {}

    # The url we want to scrape
    # url = "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"
    url = 'https://redplanetscience.com/'


    # # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    # # Let it sleep for 1 second
    time.sleep(1)

    # # Return all the HTML on our page
    # html = browser.html
    
    # # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    # soup = BeautifulSoup(html, "html.parser")

    # Build our dictionary for the headline, price, and neighborhood from our scraped data
    mars["news_title"] = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text
    mars["news_p"] = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text
    
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    time.sleep(1)

    browser.find_by_xpath('/html/body/div[1]/div/a/button').click()

    mars["featured_image"]= browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')["src"]

    df = pd.read_html('https://galaxyfacts-mars.com')[0]

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    mars["mars_facts"]= df.to_html(classes='table table-stripped')
    
    time.sleep(1)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    for image in range(1,5):
        xpath = f'//*[@id="product-section"]/div[2]/div[{image}]/div/a/h3'
        browser.find_by_xpath(xpath).click()
        img = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')['href']
        title = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
        urls = {}
        urls["title"]= title
        urls["img_url"]= img
        hemisphere_image_urls.append(urls)
        browser.back()
    mars["hemispheres"]= hemisphere_image_urls


    # Quit the browser
    browser.quit()

    # Return our dictionary
    return mars
