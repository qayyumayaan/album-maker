const fs = require('fs');
const path = require('path');
const { electron } = window;

window.addEventListener('DOMContentLoaded', () => {
  // create a button dynamically
  const btn = document.createElement("button");
  btn.innerText = 'Upload txt file';
  document.body.appendChild(btn);

  btn.addEventListener('click', () => {
    // open dialog to select file
    dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [
        { name: 'Text Files', extensions: ['txt'] }
      ]
    }).then((filePaths) => {
      if (!filePaths.canceled && filePaths.filePaths.length > 0) {
        // read file
        fs.readFile(filePaths.filePaths[0], 'utf-8', (err, data) => {
          if (err) {
            console.error("An error occurred reading the file :" + err.message);
            return;
          }
          
          // split data by line
          const lines = data.split('\n');
          lines.forEach((line) => {
            const ext = path.extname(line).toLowerCase();
            if (ext === '.jpg' || ext === '.jpeg' || ext === '.png') {
              // create image element
              const img = document.createElement('img');
              img.src = line;
              img.height = 200;  // Set the image height
              img.width = 200;   // Set the image width

              // append to body
              document.body.appendChild(img);
            }
          });
        });
      }
    });
  });
});