# Web Scraping Script Documentation

## Overview

This Python script is designed to scrape Google search results for "People also ask" questions related to a given keyword. It combines multiple web scraping techniques to gather a comprehensive list of questions, filter them, and save the results to files.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Main Components](#main-components)
5. [Error Handling and Logging](#error-handling-and-logging)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.7 or higher
- Firefox web browser (for Selenium WebDriver)

## Installation

1. Clone the repository or download the script file.

2. Install the required Python packages:

   ```
   pip install requests beautifulsoup4 selenium
   ```

3. Download and install GeckoDriver for Firefox:
   - Visit the [GeckoDriver releases page](https://github.com/mozilla/geckodriver/releases)
   - Download the appropriate version for your operating system
   - Extract the executable and add its location to your system's PATH

## Usage

1. Open a terminal or command prompt.

2. Navigate to the directory containing the script.

3. Run the script:

   ```
   python script_name.py
   ```

4. When prompted, enter your search keyword.

5. The script will run for approximately 60 seconds, gathering questions from Google.

6. Two output files will be generated in the same directory as the script.

## Main Components

### 1. get_initial_questions(keyword)

This function performs an initial search using the requests library and BeautifulSoup to parse the HTML. It extracts the first set of "People also ask" questions from the Google search results page.

### 2. get_additional_questions(driver, initial_questions, max_time=60)

Using Selenium WebDriver, this function interacts with the Google search results page to expand the "People also ask" section and gather additional questions. It runs for a maximum of 60 seconds (by default) or until no new questions are found.

### 3. save_questions_to_file(questions, filename)

This function saves the collected questions to a text file, with each question on a new line.

### 4. filter_questions(input_file, output_file)

This function reads the saved questions, filters out any lines that don't end with a question mark or start with specific excluded phrases, and saves the filtered questions to a new file.

## Error Handling and Logging

The script includes comprehensive error handling and logging:

- Logging is configured to display timestamps, log levels, and messages.
- Each main function includes try-except blocks to catch and log specific errors.
- The main execution block is wrapped in a try-except clause to catch any unexpected errors.

## Output Files

1. `google_questions.txt`: Contains all scraped questions, including potential non-questions.
2. `filtered_questions.txt`: Contains only the filtered questions that end with a question mark and don't start with excluded phrases.

## Troubleshooting

1. **Selenium WebDriver issues:**
   - Ensure GeckoDriver is correctly installed and its location is in your system's PATH.
   - Check that you have the latest version of Firefox installed.

2. **No questions scraped:**
   - Verify your internet connection.
   - Check if Google is blocking automated requests from your IP address. You may need to use a VPN or wait before trying again.

3. **Script crashes or hangs:**
   - Check the log output for error messages.
   - Ensure all required packages are installed and up to date.
   - Try increasing the `time.sleep()` duration if pages are loading slowly.

4. **Empty output files:**
   - Verify that the search keyword generates "People also ask" questions on Google.
   - Check the log for any file writing errors.

If problems persist, review the log files for specific error messages and consult the error handling section of the script for more information on where the issue might be occurring.
