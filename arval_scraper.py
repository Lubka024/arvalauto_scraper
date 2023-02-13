import requests
import csv
from bs4 import BeautifulSoup

# Define the base URL (testing git)
base_url = 'https://www.arvalauto.cz/nabidka-vozu/operativni-leasing/cena-bez-dph/'

# Open the CSV file for writing
with open('cars.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['Car Name', 'Car Details', 'Car Price', 'Car Detail Link'])

    page_number = 1
    while page_number <= 100:
        # Make the request to the URL for the current page
        url = f"{base_url}?pg={page_number}"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the page content
            page_content = response.content
            # Use BeautifulSoup to parse the HTML structure
            soup = BeautifulSoup(page_content, 'html.parser')
            # Find all the listings in the page
            listings = soup.find_all('div', class_='content')

            # Check if there are any listings on the page
            if not listings:
                break

            # Loop through each listing
            for listing in listings:
                try:
                    # Get the car name
                    car_name = listing.find('h2').text
                    # Get the car details
                    car_details = listing.find('div', class_='info').text
                    # Get the car price
                    car_price = listing.find('p', class_='price').text.replace('\n', '').replace(' Kč', '').strip().replace(' ', '')
                    # Get the link to the car detail
                    car_detail_link = "https://www.arvalauto.cz" + listing.find('a', class_='button-more button-more3')['href']
                    # Write the extracted information to the CSV file
                    writer.writerow([car_name, car_details, car_price, car_detail_link])
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print(f"Request failed with status code {response.status_code}")

        page_number += 1
