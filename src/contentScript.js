chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getDOMElement") {
    const elementId = prompt("Enter the ID of the element to display:");
    const element = document.getElementById(elementId);
    const content = element ? element.outerHTML : `Element with ID '${elementId}' not found.`;
    sendResponse({ content: content });
  }
});
