const btn = document.getElementById("btn");
const p = document.getElementById("content");
const kw = document.getElementById("kws");
const highlights = document.getElementById("highlights");
var summary = ""
var en_translate = ""
var es_translate = ""
var fr_translate = ""
var en_keywords = ""
var es_keywords = ""
var fr_keywords = ""
var highlights_ts = ""
btn.addEventListener("click", get_summary);
function get_summary() {
  btn.disabled = true;
  btn.innerHTML = "Summarising...";
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    var url = tabs[0].url;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
    xhr.onload = function () {
      var textStr = xhr.responseText;

      var text = JSON.parse(textStr);

      var keywords = text.keywords || "";
      summary = text.summary || "";
      en_translate = text.en_translate || "";
      es_translate = text.es_translate || "";
      fr_translate = text.fr_translate || "";
      en_keywords = text.en_keywords || "";
      es_keywords = text.es_keywords || "";
      fr_keywords = text.fr_keywords || "";
      highlights_ts = text.highlights_ts || "";
      p.innerHTML = summary;
      kw.innerHTML = keywords;
      highlights_ts.forEach(item => {
        // Create a new <li> element
        const listItem = document.createElement('li');
        // Set the text content of the <li> element
        listItem.textContent = item;
        // Append the <li> element to the <ul> element
        highlights.appendChild(listItem);
    });
      btn.disabled = false;
      btn.innerHTML = "Get Summary";
      console.log(text)

      var tabs = document.getElementsByClassName("tab");
      for (var i = 0; i < tabs.length; i += 1) {
        tabs[i].style.display = "block";
      }
      btn.style.display = "none";
    }
    xhr.send();
  });
};

const select_btn = document.getElementById('languageSelector');
select_btn.addEventListener("click", languageSelection);

function languageSelection(){
  const selectedLanguage = select_btn.value;
  console.log(selectedLanguage)
  if(selectedLanguage != ""){
    if(selectedLanguage == "en"){
      p.innerHTML = en_translate
      kw.innerHTML = en_keywords
     }
     else if(selectedLanguage == "es"){
      p.innerHTML = es_translate
      kw.innerHTML = es_keywords
     }
     else if(selectedLanguage == "fr"){
      p.innerHTML = fr_translate
      kw.innerHTML = fr_keywords
     }
  }
}


let isPlaying = false;

const btn2 = document.getElementById("audioButton");
btn2.addEventListener("click", toggleAudio);

function toggleAudio() {
  if (isPlaying) {
    document.getElementById('audio').pause();
    isPlaying = false;
    document.getElementById('audioButton').innerHTML = '▶️';
  } else {
    const selectedLanguage = document.getElementById('languageSelector').value;

    // Set the audio source URL based on the selected language
    const audioFile = `audio/translated_summary_${selectedLanguage}.mp3`

    document.getElementById('audio').src = audioFile;

    // Play the audio
    document.getElementById('audio').play();
    isPlaying = true;
    document.getElementById('audioButton').innerHTML = '⏸️';
  }
}
document.addEventListener('DOMContentLoaded', function () {
  // Get all the buttons with class "tablinks"
  var tabButtons = document.querySelectorAll('.tablinks');

  // Attach a click event listener to each button
  tabButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
      var cityName = event.target.dataset.city;
      openCity(event, cityName);
    });
  });
});

function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
document.addEventListener('DOMContentLoaded', function () {
  // Get the download button
  const downloadButton = document.getElementById('downloadButton');

  // Attach a click event listener to the download button
  downloadButton.addEventListener('click', function () {
    // Get the selected option from the dropdown
    const selectedOption = document.querySelector('select[name="downloadOption"]').value;

    if (selectedOption === 'Summary') {
      downloadSummary();
    } else if (selectedOption === 'Audio') {
      downloadAudio();
    }

  });
  // Add event listener for the new tab button
  const feedbackTabButton = document.querySelector('.tablinks[data-city="Feedback"]');
  feedbackTabButton.addEventListener('click', function () {
    openCity(event, 'Feedback');
  });
});

function downloadSummary() {
  const summaryText = document.getElementById('content').innerText;
  download('summary.txt', summaryText);
}

function downloadAudio() {
  // Assuming the audio source URL is set in the audio element
  const audioSource = document.getElementById('audio').src;
  // Replace 'audio' with the actual audio file URL
  download('audio.mp3', audioSource);
}

// Function to trigger the download
function download(filename, text) {
  const element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
