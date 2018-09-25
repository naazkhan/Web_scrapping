from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    news_title,news_p=marsNews(browser)
    image=marsImage(browser)
    weather_tweet=marsWeather(browser)
    url_list=marsHem(browser)
    table=marsFacts()
    mars_data = {
        'news_title':news_title,
        'news_p':news_p,
        'image':image,
        'weather_tweet':weather_tweet,
        'url_list':url_list,
        'table':table
    }
    return mars_data
   
    #NASA Mars News
def marsNews(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_ ="article_teaser_body").text
    return news_title,news_p

    #JPL Mars Space Images - Featured Image
def marsImage(browser):
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html=browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    return image
    
    #Mars Weather
def marsWeather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html, "html.parser")
    soup.find_all('p', class_='TweetTextSize')
    for tweets in soup.find_all('p', class_='TweetTextSize'):
        if 'Sol' in tweets.text:
            weather_tweet = tweets.text
    return weather_tweet
        

    #Mars Facts
def marsFacts():
    url = 'https://space-facts.com/mars/'
    df= pd.read_html(url)[0]
    table = df.to_dict()
    return table

    #Mars Hemispheres
def marsHem(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    image_link = BeautifulSoup(html, 'html.parser')
    url_list = []
    for link in image_link.find_all('a', class_='itemLink'):
        if link["href"] not in url_list:
            url_list.append(link["href"])         
        image_list = []
        for url in url_list:
            browser.visit('https://astrogeology.usgs.gov'+ url)
            time.sleep(3)
            image = browser.find_link_by_text('Sample')['href']
            image_list.append(image)
            return url_list