// const btn = document.getElementsByClassName("btn");
// btn.addEventListener("click", function(){
//     btn.disabled = true;
//     btn.innerHTML = "Summarising...";
//     chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
//         var url = tabs[0].url;
//         var xhr = new XMLHttpRequest();
//         xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
//         xhr.onload = function(){
//             var text = xhr.responseText;
//             const p = document.getElementsByClassName("summary");
//             p.innerHTML = text;
//             btn.disabled = false;
//             btn.innerHTML = "Summarise";
//             p.style.display = "block";
//         }
//         xhr.send();
//     });
// });
const btn = document.getElementById("btn");
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

      const p = document.getElementById("content");
      const kw = document.getElementById("kws");

      var text = JSON.parse(textStr);

      var keywords = text.keywords || "";
      var summary = text.summary || "";
      p.innerHTML = summary;
      kw.innerHTML = keywords;
      btn.disabled = false;
      btn.innerHTML = "Get Summary";
      console.log(text)

      var tabs = document.getElementsByClassName("tab");
      for (var i = 0; i < tabs.length; i += 1) {
        tabs[i].style.display = "block";
      }
    }
    xhr.send();
  });
};


let synth = window.speechSynthesis;
let utterance = new SpeechSynthesisUtterance();
let isPlaying = false;
const btn2 = document.getElementById("audioButton");
btn2.addEventListener("click", toggleAudio);
function toggleAudio() {
  if (isPlaying) {
    synth.cancel();
    isPlaying = false;
    // document.getElementById('audioButton').innerHTML = '<i class="fas fa-play"></i>';
    document.getElementById('audioButton').innerHTML = '▶️';
  } else {
    const content = document.getElementById('content').innerText;
    const selectedLanguage = document.getElementById('languageSelector').value;

    utterance.text = content;
    utterance.lang = selectedLanguage;
    synth.speak(utterance);

    isPlaying = true;
    // document.getElementById('audioButton').innerHTML = '<i class="fas fa-pause"></i>';
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