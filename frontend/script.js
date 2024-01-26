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
const p = document.getElementById("content");
var summary = ""
var en_translate = ""
var es_translate = ""
var fr_translate = ""
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

      // const p = document.getElementById("content");
      const kw = document.getElementById("kws");

      var text = JSON.parse(textStr);

      var keywords = text.keywords || "";
       summary = text.summary || "";
       en_translate = text.en_translate || "";
       es_translate = text.es_translate || "";
       fr_translate = text.fr_translate || "";
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


// let synth = window.speechSynthesis;
// let utterance = new SpeechSynthesisUtterance();
// let isPlaying = false;
// const btn2 = document.getElementById("audioButton");
// btn2.addEventListener("click", toggleAudio);
// function toggleAudio() {
//   if (isPlaying) {
//     synth.cancel();
//     isPlaying = false;
//     // document.getElementById('audioButton').innerHTML = '<i class="fas fa-play"></i>';
//     document.getElementById('audioButton').innerHTML = '▶️';
//   } else {
//     const content = document.getElementById('content').innerText;
//     const selectedLanguage = document.getElementById('languageSelector').value;

//     utterance.text = content;
//     utterance.lang = selectedLanguage;
//     synth.speak(utterance);

//     isPlaying = true;
//     // document.getElementById('audioButton').innerHTML = '<i class="fas fa-pause"></i>';
//     document.getElementById('audioButton').innerHTML = '⏸️';
//   }
// }

// let synth = window.speechSynthesis;
// let utterance = new SpeechSynthesisUtterance();
// let isPlaying = false;

// const btn2 = document.getElementById("audioButton");
// btn2.addEventListener("click", toggleAudio);

// function toggleAudio() {
//   if (isPlaying) {
//     synth.cancel();
//     isPlaying = false;
//     document.getElementById('audioButton').innerHTML = '▶️';
//   } else {
//     const content = document.getElementById('content').value;
//     const selectedLanguage = document.getElementById('languageSelector').value;

//     // Translate the content to the selected language
//     translateText(content, selectedLanguage)
//       .then(translatedText => {
//         // Create a gtts object with the translated text and language
//         const gttsObj = new gTTS(translatedText, selectedLanguage);

//         // Save the audio file
//         gttsObj.save('output.mp3', function (err, result) {
//           if (err) {
//             console.error(`Audio save failed: ${err}`);
//           } else {
//             // Play the audio
//             playAudio('output.mp3');

//             isPlaying = true;
//             document.getElementById('audioButton').innerHTML = '⏸️';
//           }
//         });
//       })
//       .catch(error => {
//         console.error('Translation error:', error);
//       });
//   }
// }

// function translateText(text, targetLanguage) {
//   // Your translation logic here
//   return Promise.resolve(text);
// }

// function playAudio(audioFile) {
//   // Your code to play the audio using an HTML audio element or other suitable method
//   // Example: Create an audio element and play the audio
//   const audio = new Audio(audioFile);
//   audio.play();
// }

// let synth = window.speechSynthesis;
// let utterance = new SpeechSynthesisUtterance();
// let isPlaying = false;

// const btn2 = document.getElementById("audioButton");
// btn2.addEventListener("click", toggleAudio);

// function toggleAudio() {
//   if (isPlaying) {
//     synth.cancel();
//     isPlaying = false;
//     document.getElementById('audioButton').innerHTML = '▶️';
//   } else {
//     const content = document.getElementById('content').innerText;
//     const selectedLanguage = document.getElementById('languageSelector').value;

//     // Set the text and language for the utterance
//     utterance.text = content;
//     utterance.lang = selectedLanguage;

//     // Speak the utterance
//     synth.speak(utterance);

//     isPlaying = true;
//     document.getElementById('audioButton').innerHTML = '⏸️';
//   }
// }


let isPlaying = false;

const btn2 = document.getElementById("audioButton");
btn2.addEventListener("click", toggleAudio);

function toggleAudio() {
  if (isPlaying) {
    document.getElementById('audio').pause();
    p.innerHTML = summary
    isPlaying = false;
    document.getElementById('audioButton').innerHTML = '▶️';
  } else {
    const selectedLanguage = document.getElementById('languageSelector').value;

    // Set the audio source URL based on the selected language
    const audioFile = `audio/translated_summary_${selectedLanguage}.mp3`
   
    // const audioFile = `D:\be-project\frontend\audio\translated_summary_${selectedLanguage}.mp3`;
    document.getElementById('audio').src = audioFile;

    // Play the audio
    document.getElementById('audio').play();
   if(selectedLanguage == "en"){
    p.innerHTML = en_translate
   }
   else if(selectedLanguage == "es"){
    p.innerHTML = es_translate
   }
   else if(selectedLanguage == "fr"){
    p.innerHTML = fr_translate
   }
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