import express from 'express';
import fileUpload from 'express-fileupload';

const app = express();
const PORT = 3000;

app.use(fileUpload());

app.post('/upload', async (req, res) => {
  if (!req.files || Object.keys(req.files).length === 0) {
    console.log('No files were uploaded.');
    return res.status(400).send('No files were uploaded.');
  }

  const uploadedFile = req.files.file;
  const fileName = uploadedFile.name;
  const filePath = __dirname + '/uploads/' + fileName;

  try {
    console.log('Uploaded file:', uploadedFile);
    // await saveUploadedFile(uploadedFile, filePath);

    // // Scan the uploaded file
    // const scanResult = await scanFile(filePath);
    // console.log('Scan Result:', scanResult);

    // // Store file data in the database
    // await storeFileData(fileName, uploadedFile.data);

    res.send('File uploaded successfully.');
  } catch (error) {
    console.error('Error handling file upload:', error);
    res.status(500).send('Error handling file upload.');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
