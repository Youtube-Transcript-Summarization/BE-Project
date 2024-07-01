chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      files: ['content.js']
    });
  });
  
  // Listening for a message from content.js
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.contentScriptQuery == "fetchSummary") {
      const videoId = request.videoId;
      // Assuming you have an API that returns a summary for a given YouTube video ID
      fetch(`http://127.0.0.1:5000/summary?videoId=${videoId}`)
        .then(response => response.text())
        .then(summary => {
          sendResponse({summary: summary});
        })
        .catch(error => console.error('Error fetching summary:', error));
      return true; // indicates you wish to send a response asynchronously
    }
  });
  