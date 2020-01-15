import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

#tired of calling it for things.
def CallBrowser():
    executable_path = {'executable_path': 'C:/Users/User/Documents/Homework/Assingment_WebScrapping/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False) 
    return browser 

#using this to make sure i was actually looking at the correct thing in here.
def OutputSoup(soup):
    with open('myout.html','w',encoding='utf-8') as file:
        file.write(str(soup))

def scrape():
    # # Scrape everything
    # this dictionary will hold everything we pull from all the sites
    scraped_data = {}

    # site 1 -https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest
    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    tempbrowser=CallBrowser()
    tempbrowser.visit(news_url)

    #had to use a timer otherwise the javascript wouldnt be seen. that one took a minute to realize.
    time.sleep(5)
    # Parse HTML with Beautiful Soup
    html = tempbrowser.html
    soup = bs(html,'html.parser')
    tempbrowser.quit()

    # use bs to find() the example_title_div and filter on the class_='content_tile'
    level1=soup.find_all('div', class_='content_title')
    news_title = level1[0].text.strip()
    scraped_data['news_title'] = news_title

    # use bs to find() the example_title_div and filter on the class_='article_teaser_body'
    level1=soup.find_all('div',class_='article_teaser_body')
    news_p=level1[0].text.strip()
    scraped_data['news_p'] = news_p


    # site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    Image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
    tempbrowser=CallBrowser()
    tempbrowser.visit(Image_url)
    #super navigation fun time.
    time.sleep(5)
    tempbrowser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    tempbrowser.click_link_by_partial_text('more info')
    time.sleep(5)

    html = tempbrowser.html
    soup = bs(html,'html.parser')
    tempbrowser.quit()

    dump = soup.find('figure', class_='lede').find('a')['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + dump
    scraped_data['featured_image_url'] = featured_image_url

    # site 3 - https://twitter.com/marswxreport?lang=en
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    tempbrowser=CallBrowser()
    tempbrowser.visit(weather_url)
    html = tempbrowser.html
    soup = bs(html,'html.parser')
    tempbrowser.quit()
    #OutputSoup(soup)
    # grab the latest tweet and be careful its a weather tweet
    
    tw=soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather=tw[0].text.strip()    
    scraped_data['mars_weather'] = mars_weather

    # site 4 - https://space-facts.com/mars/
    facts_url = 'https://space-facts.com/mars/'
    tempbrowser=CallBrowser()
    tempbrowser.visit(facts_url)
    time.sleep(5)
    html = tempbrowser.html
    soup = bs(html,'html.parser')
    tempbrowser.quit()
    #OutputSoup(soup)
    # use pandas to parse the table
    tables = pd.read_html(facts_url)[0]
    tables = tables.rename(columns={'Mars - Earth Comparison':'Descriptions','Mars':'Values'})
    facts_df=tables[['Descriptions','Values']]
    facts_df.set_index('Descriptions', inplace=True)
    # convert facts_df to a html string and add to dictionary.
    facts_html=facts_df.to_html()
    scraped_data['facts_html'] = facts_html

    # site 5 - https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    #hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' the site wouldnt connect. so i found another.
    hemi_url_backup='http://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html'
    tempbrowser=CallBrowser()
    tempbrowser.visit(hemi_url_backup)
    html = tempbrowser.html
    soup = bs(html,'html.parser')
    tempbrowser.quit()
   
    # use bs4 to scrape the title and url and add to dictionary
    itr = range(1,5)
    hemisphere_image_urls = []

    for n in itr:
        thisdict={}
        lp=soup.find_all('div', class_='img-caption-box')[n]
        thisdict['title']=lp.find('h5').text.strip()
        thisdict['img_url']=lp.find('img')['src']
        hemisphere_image_urls.append(thisdict)

    scraped_data['hemisphere_image_urls'] = hemisphere_image_urls
    return scraped_data
   

