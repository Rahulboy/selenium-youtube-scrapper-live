from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
import json
import os

YOUTUBE_TRENDING_URL ='https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url= title_tag.get_attribute('href')
  thumbnail_tag = video.find_element(By.TAG_NAME,'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')
  channel_div= video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text
  description = video.find_element(By.ID, 'description-text').text

  return {
    'title': title,
    'url': url,
    'thumbnail_url': thumbnail_url,
    'channel': channel_name,
    'description':description
  }
  
def send_email(body):
 
  
  try:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
  
    SENDER_EMAIL = 'rchauhan9893@gmail.com'
    RECIEVER_EMAIL='rchauhan9893@gmail.com'
    SENDER_PASSWORD=os.environ['GMAIL_PASSWORD']
    
    subject = 'YouTube Trending Videos'
 
  
    email_text = f"""\
    From: {SENDER_EMAIL}
    To: {RECIEVER_EMAIL}
    Subject:{subject}
   
  
    {body}
    """ 
    
    server.login(SENDER_EMAIL,SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL,RECIEVER_EMAIL,email_text)
    server.close()
    print('email sent')
  except smtplib.SMTPException as e: # Catch specific SMTP exception
    print('Something went wrong:', e)
      

if __name__ == "__main__":
  print('Creating Driver')
  driver=get_driver()
  print('Fetching the page')
  
  print('Fetching treding videos')
  videos = get_videos(driver)
  
  print(f'Found {len(videos)} videos')
  
  print('Parsing top 10 videos')
  videos_data = [parse_video(video) for video in videos[:10]]
  
  print('Save the data to a csv')
  videos_df = pd.DataFrame(videos_data)
  
  videos_df.to_csv('trending.csv',index=None)

  print("Send an email with the results")
  body = json.dumps(videos_data, indent=2)
  send_email(body)

print('Finished')
  
  
  