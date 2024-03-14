function sendFile() {
  console.log('Uploading file...');
  const file = document.querySelector('#file').files[0];
  if (!file) {
    return;
  }
  const formData = new FormData();
  formData.append('file', file);
  fetch('http://127.0.0.1:5000/upload', {
    method: 'POST',
    application: 'multipart/form-data',
    body: formData
  }).then((response) => {
    console.log('File uploaded successfully');
    console.log(response);
  });
}
