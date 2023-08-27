// Typing style
const textElement = document.getElementById('text');
const words = [
  "Hi 🙋‍♂️ ",
  "Welcome to Rate Inn !",
  "I can tell your favourite 😀",
  "Restaurant rating 🌟 !"
];
let wordIndex = 0;
let charIndex = 0;

function type() {
  if (charIndex < words[wordIndex].length) {
    textElement.textContent += words[wordIndex].charAt(charIndex);
    charIndex++;
    setTimeout(type, 150); 
  } else {
    charIndex = 0;
    wordIndex++;
    if (wordIndex === words.length) {
      wordIndex = 0;
    }
    textElement.textContent = "";
    setTimeout(type, 500); 
  }
}

type(); 
