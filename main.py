import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Step 1: Function to get initial questions using requests and BeautifulSoup
def get_initial_questions(keyword):
    try:
        url = f"https://www.google.com/search?q={keyword}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        
        questions = []
        for div in soup.find_all('div', class_='related-question-pair'):
            questions.append(div.text)
        
        return questions
    except requests.RequestException as e:
        logger.error(f"Error fetching initial questions: {e}")
        return []

# Step 2: Function to get additional questions using Selenium
def get_additional_questions(driver, initial_questions, max_time=60):
    start_time = time.time()
    all_questions = initial_questions.copy()
    clicked_questions = set()

    try:
        while time.time() - start_time < max_time:
            try:
                # Wait for the "People also ask" section to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "related-question-pair"))
                )
                
                # Get all visible questions
                visible_questions = driver.find_elements(By.CLASS_NAME, "related-question-pair")
                
                # Click on each unclicked question to reveal more
                for q in visible_questions:
                    if q.text not in clicked_questions:
                        q.click()
                        clicked_questions.add(q.text)
                        time.sleep(2)  # Wait for new questions to load
                        
                        # Get new questions that appeared
                        new_questions = driver.find_elements(By.CLASS_NAME, "related-question-pair")
                        for nq in new_questions:
                            if nq.text not in all_questions:
                                all_questions.append(nq.text)
                
                # If no new questions were found, break the loop
                if len(all_questions) == len(clicked_questions):
                    break

            except Exception as e:
                logger.warning(f"An error occurred while fetching additional questions: {e}")
                break

    except Exception as e:
        logger.error(f"Critical error in get_additional_questions: {e}")

    return all_questions

# Step 3: Save questions to file
def save_questions_to_file(questions, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for q in questions:
                f.write(q + '\n')
        logger.info(f"Successfully saved {len(questions)} questions to {filename}")
    except IOError as e:
        logger.error(f"Error saving questions to file: {e}")

# Step 4: Filter questions that end with a question mark
def filter_questions(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    if line.strip().endswith('?') and not line.strip().startswith(("খুঁজুন", "Search for")):
                        outfile.write(line)
        logger.info(f"Filtered lines have been written to {output_file}")
    except IOError as e:
        logger.error(f"Error filtering questions: {e}")

# Main execution
if __name__ == "__main__":
    try:
        keyword = input("Enter your search keyword: ")
        
        # Step 1: Get initial questions using requests and BeautifulSoup
        initial_questions = get_initial_questions(keyword)

        # Step 2: Use Selenium to get additional questions
        driver = None
        try:
            driver = webdriver.Firefox()  # Make sure you have ChromeDriver installed
            driver.get(f"https://www.google.com/search?q={keyword}")
            time.sleep(30)
            
            all_questions = get_additional_questions(driver, initial_questions)
        except Exception as e:
            logger.error(f"Error during Selenium operations: {e}")
            all_questions = initial_questions
        finally:
            if driver:
                driver.quit()

        # Step 3: Save all questions to a file
        questions_file = "google_questions.txt"
        save_questions_to_file(all_questions, questions_file)

        # Step 4: Filter questions and save to a new file
        filtered_output_file = "filtered_questions.txt"
        filter_questions(questions_file, filtered_output_file)

    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
