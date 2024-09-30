from bs4 import BeautifulSoup
import urllib.request as request 
import urllib.parse as parse

URL_FILE = "urls.csv"

def class_empty(soup):
    return soup.find(attrs={'class':'empty'}) is not None

def class_warning(soup):
    return soup.find(attrs={'class':'warning'}) is not None

def result_not_found(soup):
    return class_empty(soup) or class_warning(soup)

def scrape_images():
    with open(URL_FILE, "w") as fl_urls:
        with open("issues.csv", "r") as fl_issues:
            for issue in fl_issues:
                try:
                    issue_id, title, series_no = issue.strip().split(",")
                    
                    title_to_search = parse.quote(title)

                    socket = request.urlopen(f"https://www.coverbrowser.com/search?q={title_to_search}\n") 
                    htmlSource = socket.read()                            
                    socket.close() 
                    soup = BeautifulSoup(htmlSource, 'html.parser')

                    p_tags = soup.find_all("p")
                    
                    # There was an alternative path to search for on the same API 
                    if result_not_found(soup):
                        socket = request.urlopen(f"https://www.coverbrowser.com/covers/{title_to_search}\n") 
                        htmlSource = socket.read()                            
                        socket.close() 
                        soup = BeautifulSoup(htmlSource, 'html.parser')
                        p_tags = soup.find_all("p")
                    

                        if result_not_found(soup):
                            print(f"Could not find image for {title}")
                            raise Exception

                    for i in soup.find_all("img"):
                        if title.replace("+", " ") in i["alt"]:
                            print(i['src'] + " ALT: " + i['alt'])

                            # Some of the image urls are hosted on the site, others are referred to by external URLS
                            if (i['src']).startswith("http"):
                                fl_urls.write(f"{issue_id},{i['src']},/images/{title}.jpg")
                                # request.urlretrieve(i['src'], f"images/{title}.jpg")
                            else:
                                fl_urls.write(f"{issue_id},https://www.coverbrowser.com{i['src']},/images/{title}.jpg")
                                # request.urlretrieve(f"https://www.coverbrowser.com{i['src']}", f"images/{title}.jpg")
                            break
                except:
                    print("cant find anything for " + issue.strip())

if __name__ == "main":
    scrape_images()