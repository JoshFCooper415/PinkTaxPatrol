// Background script
chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId, function (tab) {
      if (tab.status === 'complete' && tab.url.includes('https://www.amazon.com/')) {
        executeScriptOnTab(tab.id);
      }
    });
  });
  
  chrome.webNavigation.onCompleted.addListener(function (details) {
    if (details.url.includes('https://www.amazon.com/')) {
      executeScriptOnTab(details.tabId);
    }
  });
  
  function executeScriptOnTab(tabId) {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      function: findAndLogElements,
    });
  }
  
  function findAndLogElements() {
    function sendToServer(data) {
      fetch('http://localhost:5000/product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((responseData) => {
          // Send a message to the background script with the data
          chrome.runtime.sendMessage({ action: 'downloadData', data: responseData });
        })
        .catch((error) => {
          console.error('Error sending data to server:', error);
        });
    }
  
    var elementIds = {
      productName: 'productTitle',
      productCostWhole: { selector: '.a-price-whole', type: 'class' },
      productCostFraction: { selector: '.a-price-fraction', type: 'class' },
      listProducts: 'detailBullets_feature_div',
      productReviewCount: 'acrCustomerReviewLink',
      productReviewRating: { selector: '.a-icon-alt', type: 'class' },
    };
  
    var elementContents = {};
  
    for (const [key, elementInfo] of Object.entries(elementIds)) {
      var myElement;
  
      if (elementInfo.type === 'class') {
        myElement = document.querySelector(elementInfo.selector);
      } else {
        myElement = document.getElementById(elementInfo);
      }
  
      if (myElement) {
        var elementContent;

            // Check if the current element is the 'listProducts' container
            if (key === 'listProducts') {
                // For listProducts, get each element under the container
                var listElements = myElement.querySelectorAll('.a-list-item');
                elementContent = [];

                console.log(elementContent)

                listElements.forEach((listElement) => {
                    // Clean up each item in the listProducts array and concatenate with "+++"
                    var cleanedItem = listElement.textContent.trim().replace(/\n\s*/g, ' ');
                    elementContent.push(cleanedItem);
                });

                // Concatenate the cleaned items with "+++" between elements
                elementContent = elementContent.join('+++');
            } else {
                // For other elements, get the text content
                elementContent = myElement.textContent.trim();
            }

            elementContents[key] = elementContent;
      } else {
        elementContents[key] = 'Element not found';
      }
    }
  
    sendToServer(elementContents);
  }
  
  // Background script
  chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'downloadData') {
      const data = message.data;
  
      // Convert the server response to a JSON string
      const jsonString = JSON.stringify(data);
  
      // Create a data URI from the JSON string
      const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(jsonString);
  
      // Create a unique name for the downloaded file
      const fileName = 'server_response'+ '.json';
  
      // Use the chrome.downloads API to initiate the download
      chrome.downloads.download({
        url: dataUri,
        filename: fileName,
        saveAs: true,
      }, function(downloadId) {
        // Handle download completion or errors if needed
        if (chrome.runtime.lastError) {
          console.error('Download failed: ' + chrome.runtime.lastError);
        } else {
          console.log('Download initiated with ID: ' + downloadId);
        }
      });
    }
  });
  