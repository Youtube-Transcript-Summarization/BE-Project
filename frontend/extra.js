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