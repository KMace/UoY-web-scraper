import requests
from bs4 import BeautifulSoup

def scrapeYorkUni(url):
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
    html_content = response.content
    print('successful')
    print()
  else:
    print("Failed to retrieve the webpage.")
    exit()

  soup = BeautifulSoup(html_content, 'html.parser')

  # get all links to professors pages, skipping irrelavent links
  links = soup.find_all('a')
  
  return searchProfessorPages(url, links)
  
def searchProfessorPages(url, links):
  """
    Takes all the scrapped links (containing links to UoY professor pages), and
    iteratively writes their content to a file.
  """
  
  start_search = 31 # everything before 31st link can be safely skipped
  irrelavent_tags = [
    'Legal statement', 
    'Privacy', 
    'E-mail', 
    'Cookies', 
    'Accessibility', 
    'Modify', 
    'Direct Edit', 
    'Back to Top', 
    'Legal statements',
    ]

  for link in links[start_search:]:
    try:
      name = link.text
      if name not in irrelavent_tags:
        print(name)
        
        personal_page = link.get('href')
        weblink = url + personal_page
        interests = getInterests(weblink)
        
        with open('lecturer-interests.txt', 'a') as f:
          f.write(f"{name}:\n")
          
          for thing in interests:
            f.write(f"{thing}\n")
          
          f.write('\n')
    except:
      print('End of professors reached')
      break

def getInterests(link):
  html_content = getHTML(link)
  soup = BeautifulSoup(html_content, 'html.parser')  
  interests, text = [], []
  
  try:
    div = soup.find('div', id='tab-1-content')
    
    all_text = div.find_all('p')
    text = [i.text for i in all_text]
      
    all_interests = div.find_all('li')
    interests = [i.text for i in all_interests]
  except:
    print("Didn't work")
  
  return interests + text
  
def getHTML(link):
  response = requests.get(link)

  # Check if the request was successful
  if response.status_code == 200:
    html_content = response.content
    return html_content
  
  print(f"Failed to retrieve {link}")
      
def main():
  url = 'https://www.cs.york.ac.uk/people/'
  scrapeYorkUni(url)

main()