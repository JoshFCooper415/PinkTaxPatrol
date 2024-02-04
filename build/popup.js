chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId, function (tab) {
        // Check if the tab is loading or has finished loading
        if (tab.status === "complete") {
            // Execute your function on the active tab
            executeScriptOnTab(tab.id);
        }
    });
});

chrome.webNavigation.onCompleted.addListener(function (details) {
    // Check if the completed navigation is on an Amazon page
    if (details.url.includes("https://www.amazon.com/")) {
        // Execute your function on the active tab
        executeScriptOnTab(details.tabId);
    }
});

function executeScriptOnTab(tabId) {
    chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: findAndLogElements
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
        .then(response => response.json())
        .then(responseData => {
            console.log('Server response:', responseData);
        })
        .catch(error => {
            console.error('Error sending data to server:', error);
        });
    }
    
    var elementIds = {
        productName: 'productTitle',
        productCostWhole: { selector: '.a-price-whole', type: 'class' },
        productCostFraction: { selector: '.a-price-fraction', type: 'class' },
        listProducts: 'detailBullets_feature_div',
        productReviewCount: 'acrCustomerReviewLink',
        productReviewRating: { selector: '.a-icon-alt', type: 'class' }
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
            var elementContent = myElement.textContent.trim();
            elementContents[key] = elementContent;
        } else {
            elementContents[key] = "Element not found";
        }
    }

    sendToServer(elementContents);
}
