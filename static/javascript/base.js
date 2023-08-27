// onClick Sidebar control

document.getElementById('showDivLink').addEventListener('click', function() {
    fetch('/show_div')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('myDiv').style.display = 'block';
                document.getElementById('myDiv-2').style.display = 'none';
            }
        })
        .catch(error => console.error(error));
});
document.getElementById('showDivLink-2').addEventListener('click', function() {
    fetch('/show_div')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('myDiv-2').style.display = 'block';
                document.getElementById('myDiv').style.display = 'none';
            }
        })
        .catch(error => console.error(error));
});

// screenshot capture
const divToCapture = document.getElementById('divToCapture');
  const captureButton = document.getElementById('captureButton');

  captureButton.addEventListener('click', () => {
    html2canvas(divToCapture).then(canvas => {
      // Create a temporary link to trigger the download
      const link = document.createElement('a');
      link.download = 'screenshot.png';
      link.href = canvas.toDataURL();
      link.click();
    });
  });

  const divToCapture2 = document.getElementById('divToCapture2');
  const captureButton2 = document.getElementById('captureButton2');

  captureButton2.addEventListener('click', () => {
    html2canvas(divToCapture2).then(canvas => {
      // Create a temporary link to trigger the download
      const link = document.createElement('a');
      link.download = 'screenshot.png';
      link.href = canvas.toDataURL();
      link.click();
    });
  });  

  const divToCapture3 = document.getElementById('divToCapture3');
  const captureButton3 = document.getElementById('captureButton3');

  captureButton3.addEventListener('click', () => {
    html2canvas(divToCapture3).then(canvas => {
      // Create a temporary link to trigger the download
      const link = document.createElement('a');
      link.download = 'screenshot.png';
      link.href = canvas.toDataURL();
      link.click();
    });
  });  

  const divToCapture4 = document.getElementById('divToCapture4');
  const captureButton4 = document.getElementById('captureButton4');

  captureButton4.addEventListener('click', () => {
    html2canvas(divToCapture4).then(canvas => {
      // Create a temporary link to trigger the download
      const link = document.createElement('a');
      link.download = 'screenshot.png';
      link.href = canvas.toDataURL();
      link.click();
    });
  });  

  const divToCapture5 = document.getElementById('divToCapture5');
  const captureButton5 = document.getElementById('captureButton5');

  captureButton5.addEventListener('click', () => {
    html2canvas(divToCapture5).then(canvas => {
      // Create a temporary link to trigger the download
      const link = document.createElement('a');
      link.download = 'screenshot.png';
      link.href = canvas.toDataURL();
      link.click();
    });
  });  
