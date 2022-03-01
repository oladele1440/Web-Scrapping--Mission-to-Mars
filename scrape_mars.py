import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests as req
from splinter import Browser
import time

def scrape():
# A webscraping function for the latest news on mars
    # Python dictionary of the results
    scrape_rsult = {}

    # ### NASA Mars News

    # In[2]:

    # *** Scrape the [NASA Mars News Site] ***
    url_NASA = "https://mars.nasa.gov/news"
    r = req.get(url_NASA) # sends a request to the url
    time.sleep(1)
    data = r.text # turns response into texts
    soup = BeautifulSoup(data, "html.parser") # changes the response from text to html


    # In[3]:


    # collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
    soup_div = soup.find(class_="slide") # within div in body, within <ul>, <li class=slide>.
    soup_news = soup_div.find_all('a') # search by anchor

    # In[4]:

    #getting the title
    NASA_latest_t = soup_news[1].get_text().strip()     
    # ^^^Latest News Title
    scrape_rsult["Nasa_latest_title"] = NASA_latest_t

    # In[5]:


    #getting the paragraph
        # getting the paragraph url
    soup_p = soup_div.find_all('a', href=True)
    soup_p_url = soup_p[0]['href']
    # only the url of latest news article's paragraph 

    # In[6]:


    #    Scrape the href of the first news article
    url = "https://mars.nasa.gov/"
    news_url = url + soup_p_url
    # request url
    r = requests.get(news_url)
    time.sleep(1)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    soup_para = soup.find(class_='wysiwyg_content')
    soup_para = soup_para.find_all('p')


    # In[7]:


    #    save the text of the paragraphs to a list
    NASA_latest_p = []
    for entry in soup_para:
        paragraph = entry.get_text().strip()    
        NASA_latest_p.append(paragraph)
        # ^^^ NASA_latest_p is list of paragraphs from the latest news article

    scrape_rsult["Nasa_latest_paragraph"] = NASA_latest_p

    # ### JPL Mars Space Images - Featured Image

    # In[8]:


    # Visit the url for JPL's Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    # In[9]:


    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    #     the mars featured images are under a list element of the slide class. '>' signifies a child element.  
    browser.find_by_css('li.slide>a.fancybox').first.click()
    time.sleep(1)

    # clicks the 'more info' button (caution!: the 'share' button is under a similar but different class)
    browser.find_by_css('div.buttons>a.button').first.click()
    time.sleep(1)
    # In[10]:


    # assign the url string to a variable called `featured_image_url`.
    #     Here, I decide to get both the full-size .jpg and an 800x600 size image for the webpage
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # full-size jpg (to be linked if image is clicked)
    feat_full_img_soup = soup.find(class_="main_image")
    feat_full_img = feat_full_img_soup.get('src')

    # smaller size jpg (to be displayed on the webpage)
    #     uses splinter instead of beautiful soup
    browser.click_link_by_partial_href('800x600.jpg')
    #     switch over to the next browser (window no. 2)
    #     save it's url, then close 2nd window
    browser.windows.current = browser.windows[1]  
    featured_image_url = browser.url
    browser.windows[1].close()

    # save the two urls 
    ori_url = 'https://www.jpl.nasa.gov'
    feat_full_img = ori_url + feat_full_img
    # ^^^ feat_full_img is https://www.jpl.nasa.gov + url of the full-sized featured image
    #     featured_image_url is the smaller 800x600 image that will be featured on the webpage

    scrape_rsult["featured_image_url"] = featured_image_url
    scrape_rsult['feat_full_img'] = feat_full_img

    # ### Mars Weather

    # In[11]:


    ''' 
    *** Visit the Mars Weather twitter account (https://twitter.com/marswxreport?lang=en) and scrape the latest 
    Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`. ***
    '''
    url = 'https://twitter.com/marswxreport?lang=en'
    r = requests.get(url)
    time.sleep(1)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    mars_tweets = soup.find(class_='stream-items js-navigable-stream')
    mars_tweets = mars_tweets.find(class_="js-tweet-text-container")

    mars_weather = mars_tweets.p.text
    # ^^^ mars_weather is the paragraph <p> text of the latest tweet from the Mars weather handle 

    scrape_rsult["mars_weather_tweet"] = mars_weather

    # ### Mars Facts

    # In[12]:


    ''' 
    *** Visit the Mars Facts webpage (http://space-facts.com/mars/) and use Pandas to scrape the table containing 
    facts about the planet including Diameter, Mass, etc. ***
    '''
    facts_url = 'http://space-facts.com/mars/'
    all_facts_df = pd.read_html(facts_url)     # searches for html tables & returns list of dataframes
    all_facts_df = all_facts_df[0]

    # In[14]:


    # Use Pandas to convert the data to a HTML table string.
    facts_html = all_facts_df.to_html(header=False, index=False, justify='left')

    # ^^^ facts_html is the html table of the mars facts table
    scrape_rsult["mars_facts_table"] = facts_html

    # ### Mars Hemispheres

    # In[114]:


    ''' 
    *** Visit the USGS Astrogeology site 
    (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    to obtain high resolution images for each of Mar's hemispheres.
    '''
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)

    # In[115]:


    # click each of the links to the hemispheres to find the image url to the full resolution image.
    # old code, may be useful later
    '''
    #    get list of <a href links> 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemi_soup = soup.find_all(class_='itemLink product-item')
    hemi_href_ls = []
    for item in hemi_soup:
        url_index = 'https://astrogeology.usgs.gov'
        href = item['href']
        link = url_index + href
        hemi_href_ls.append(link)
    '''
    # Get unique hrefs
    '''     I could just go to these urls separately using browser.visit(url). But I interpret the instructions 
            as saying that I need to use splinter to click on the link in the browser.     '''
    # hemi_href_ls = np.unique(hemi_href_ls)
    # hemi_href_ls


    # In[116]:


    ''' Caution!: It seems splinter can only click link based on the exact wording of the text
    browser.click_link_by_partial_text('Cerberus Hemisphere')    #e.g. function will fail to find lower case 'cerberus'
    '''


    # In[117]:


    # Beautiful soup to search browser html for headers (these contain the hemisphere names)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    headers_soup = soup.find_all('h3')
    #test = headers_soup[2].text.replace(" Enhanced", "")
    #test


    # In[128]:


    # For each header in the beautiful soup, click link associated with it and get img_url 
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    for header in headers_soup:
        #start at origin url for the Mars hemisphere section 
        window = browser.windows[0]     # current window, the first window
        browser.visit(url)
        time.sleep(2)     # wait 2 secs for browser to load 
        #getting title
        title = header.text
        title = title.replace(" Enhanced", "")     #get rid of " " + "Enhanced" for when dict is appended
        browser.click_link_by_partial_text(title)
        time.sleep(2)     # again, wait 2 secs for browser to load    
        browser.click_link_by_text('Sample')
        browser.windows.current = browser.windows[1]     # switch current window to the window that just opened
        img_url = browser.url
        browser.windows.current = window     # switch the current window back 
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})
        window.close_others()    # close all the other windows to keep browser nice and tidy!

    # ^^^ hemisphere_image_urls is list of dicts of img_url and title of hemisphere
    scrape_rsult["hemispheres"] = hemisphere_image_urls

    return scrape_rsult

# Testing: printed to verify all variables stored in dict
'''results = scrape()
if type(results) is dict:
    print(results)
'''