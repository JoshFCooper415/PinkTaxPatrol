# PinkTaxPatrol
Chrome extension to prevent overspending on pink tax

## How to add the extention
* Download the zip file from this repo
* Unzip the file
* Open up your nearest Chrome Tab
* Click on the puzzle piece icon in the taskbar on the right
* Click "Manage extensions" on the bottom of the popup
* Turn on "Developer Mode" in the top right corner of the screen
* Click the "Load unpacked" button on the left of the screen
* Select the file folder that contains the unzipped files
* Click "Select folder" 
* You're done! You can pin the chrome extension to your taskbar for easy access

## Inspiration
We were inspired to do this project by the injustice of the **Pink Tax**. Pink Tax is a price markup that is applied to products that are specifically marketed towards women. 

## What it does
When you search for an Amazon product, the Pink Tax Patrol chrome extension takes note of the product information and sends it to a hacker-made gradient boosted decision tree algorithm that decides if a product is likely to be pink taxed. If so, the algorithm recommends other Amazon products that are not pink taxed. Those items are then displayed on the extension to be chosen from by the user.

## How we built it
**Chrome extension**
Using React.js, we created a chrome extension that displays the recommended non-pink taxed items.
We also scrape the Amazon site for the critical product information.

**Docker Container**

**Web Scraping**

**Machine Learning**

## Challenges we ran into
* Pathing with both files in react and docker.
* Due to the lack of free Amazon API's to generate a database to inference off of, we instead turned to other options. Using the 100 free searches from 3 different Amazon API's, we were able to create a dataset with 10,000 elements.

## Accomplishments that we're proud of
* One hacker went from **never having used react** to building an entire chrome extension with it. 
* One hacker **created a Docker container** to communicate between the ML algorithm and chrome extension front end.
* One hacker **scraped the web** for Amazon images that were cleverly hidden in the website.
* One hacker wrote a **gradient-boosted random forests with dropout algorithm** from scratch to perform NLP on the Amazon products.

## What we learned


## What's next for Pink Tax Patrol
Moving forward, we would love to implement the Pink Tax Patrol with **other websites** outside of Amazon. Being able to dynamically suggest equivalent products across websites would offer our customers a wider variety of products and give them an easier way to save money.
