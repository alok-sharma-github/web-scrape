import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to login to LinkedIn
def login_to_linkedin(driver, email, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
   
    # Find the email and password fields and enter the credentials
    email_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
   
    email_input.send_keys(email)
    password_input.send_keys(password)
   
    # Click the login button
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    time.sleep(5)

# Function to search for a hashtag
def search_hashtag(driver, hashtag):
    search_url = f'https://www.linkedin.com/feed/hashtag/{hashtag}/'
    driver.get(search_url)
    time.sleep(5)

# Function to scrape post details
def scrape_posts(driver):
    scraped_data = []
   
    # Scroll to load more posts (adjust the range as needed)
    for _ in range(3):  # Number of scrolls to load more posts
        posts = driver.find_elements(By.CLASS_NAME, 'occludable-update')
        for post in posts:
            try:
                author_name = post.find_element(By.CLASS_NAME, 'feed-shared-actor__name').text.strip()
            except:
                author_name = ""
            
            try:
                job_title_and_company = post.find_element(By.CLASS_NAME, 'feed-shared-actor__description').text.strip()
            except:
                job_title_and_company = ""
            
            try:
                linkedin_profile_url = post.find_element(By.CLASS_NAME, 'app-aware-link').get_attribute('href')
            except:
                linkedin_profile_url = ""
            
            try:
                profile_image_url = post.find_element(By.CLASS_NAME, 'feed-shared-actor__image').get_attribute('src')
            except:
                profile_image_url = ""
            
            try:
                post_text = post.find_element(By.CLASS_NAME, 'feed-shared-update-v2__description').text
            except:
                post_text = ""

            scraped_data.append({
                'Author Name': author_name,
                'Job Title and Company': job_title_and_company,
                'LinkedIn Profile URL': linkedin_profile_url,
                'Profile Image URL': profile_image_url,
                'Post Content': post_text
            })
        
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    return scraped_data

# Function to save data to CSV
def save_to_csv(data, filename='scraped_data.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Author Name', 'Job Title and Company', 'LinkedIn Profile URL', 'Profile Image URL', 'Post Content'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main function
def main():
    email = 'kingofkingsalok@gmail.com'  # Replace with your LinkedIn email
    password = 'Alok@4641'  # Replace with your LinkedIn password
    hashtag = input("Enter the hashtag to search for: ").strip('#')
    
    # Set up the Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        login_to_linkedin(driver, email, password)
        search_hashtag(driver, hashtag)
        scraped_data = scrape_posts(driver)
        save_to_csv(scraped_data)
        print(f"Data scraped and saved to scraped_data.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
