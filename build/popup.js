chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId, function (tab) {
        // Check if the tab is loading or has finished loading
        if (tab.status === "complete" && tab.url.includes("https://www.amazon.com/")) {
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
        target: {tabId: tabId},
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
            chrome.runtime.sendMessage({ action: 'updateAppState', data: responseData })
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

// Add this listener to handle the state update from the content script
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === 'updateAppState') {
        updateAppState(request.data);
    }
});

function updateAppState(data) {
    // Assuming that data contains the necessary arrays
    console.log("heuawifn")
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: function (data) {
                // Assuming that the React app has a global function updateAppStateFromBackground
                if (typeof updateAppStateFromBackground === 'function') {
                    updateAppStateFromBackground(data);
                }
            },
        });
    });
}



