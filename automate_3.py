import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Function to login to LinkedIn
def login_to_linkedin(driver, email, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
   
    email_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
   
    email_input.send_keys(email)
    password_input.send_keys(password)
   
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    time.sleep(10)

# Function to perform a simple search and scroll
def search_simple(driver, query, max_scroll=5):
    search_url = f'https://www.linkedin.com/search/results/all/?keywords={query}'
    driver.get(search_url)
    time.sleep(5)

    for _ in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

# Function to extract post content using BeautifulSoup
def extract_post_content(soup):
    post_contents = []
    try:
        containers = soup.find_all('div', {'class': 'update-components-text relative update-components-update-v2__commentary'})
        
        for container in containers:
            spans = container.find_all('span', {'dir': 'ltr'})
            post_content = ' '.join(span.get_text(separator=' ', strip=True) for span in spans)
            post_contents.append(post_content)
    except Exception as e:
        print(f"Error extracting post content: {e}")

    return post_contents

# Function to extract URLs and post content from search results
def extract_urls_and_content(driver):
    urls_and_content = []
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        containers = soup.find_all('div', {'id': 'fie-impression-container'})
        
        for container in containers:
            link_tag = container.find('a', {'class': 'app-aware-link update-components-actor__meta-link'})
            if link_tag and 'href' in link_tag.attrs:
                url = link_tag['href']
                post_content = extract_post_content(soup)
                urls_and_content.append((url, post_content))
    except Exception as e:
        print(f"Error extracting URLs and content: {e}")

    return urls_and_content

# Function to save data to CSV
def save_to_csv(data, filename='scraped_data_3.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Post Content'])
        for url, post_content in data:
            writer.writerow([url, post_content])

# Function to go to the next page of search results and scroll
def go_to_next_page(driver, max_scroll=5):
    try:
        next_button = driver.find_element(By.XPATH, '//button[contains(@class, "artdeco-pagination__button--next")]')
        next_button.click()
        time.sleep(5)  # wait for the next page to load
        for _ in range(max_scroll):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        return True
    except Exception as e:
        print(f"Error going to the next page: {e}")
        return False

# Main function
def main():
    email = 'kingofkingsalok@gmail.com'
    password = 'Alok@4641'
    query = input("Enter the search query: ")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        login_to_linkedin(driver, email, password)
        search_simple(driver, query)
        
        all_urls_and_content = []
        while True:
            urls_and_content = extract_urls_and_content(driver)
            all_urls_and_content.extend(urls_and_content)
            if not go_to_next_page(driver):
                break
        
        save_to_csv(all_urls_and_content)
        print(f"Data scraped and saved to scraped_data.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
