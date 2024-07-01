const videoId = new URLSearchParams(window.location.search).get('v');
chrome.runtime.sendMessage({
  contentScriptQuery: "fetchSummary",
  videoId: videoId
}, response => {
  alert(`Summary: ${response.summary}`);
});
