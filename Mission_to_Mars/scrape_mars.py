from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    mars_dict2 = {}

    #NASA Mars News Site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text

    #JPL Mars Space Images
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url2)
    for x in range(1):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('ul', class_='articles')

        for article in articles:
            li = article.find('li')
            link = li.find('a')
            href = link['data-fancybox-href']

            featured_image = ('https://www.jpl.nasa.gov') + href
            
    print(featured_image)
    browser.quit

    #Mars Facts
    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    df = tables[0]
    df = df.rename(columns={0: 'Statistic', 1: 'Mars Data'})
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, 'html.parser')
    hemisphere = mars_soup.find_all('a')
    hemi = []

    for x in hemisphere:
        if x.h3:
            title = x.h3.text
            link = x['href']
            main_url="https://astrogeology.usgs.gov/"
            next_url=main_url+link
            browser.visit(next_url)
            html=browser.html
            soup=BeautifulSoup(html, 'html.parser')
            hemisphere=soup.find('div', class_='downloads')
            image=hemisphere.ul.a['href']
            mars_dict={}
            mars_dict['Title']=title
            mars_dict['Image']=image
            hemi.append(mars_dict)
            browser.back()
    browser.quit
    
    mars_dict2 = {
    'news_title_cleaned': news_title,
    'news_paragraph': news_p,
    'featured_image_url' : featured_image,
    'mars_table': df,
    'hemispheres_images': hemi
    }

    return mars_dict2