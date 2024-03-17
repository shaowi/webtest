# Pre-requisites

Ensure you have the following installed on your local machine:

1. Python 3.6 or higher
1. PostgreSQL
1. An API key from [VirusTotal](https://www.virustotal.com/gui/join-us)

## Instructions of usage

1. Clone the repository
1. Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the server directory and add the following environment variables:

```env
API_KEY=<YOUR_VIRUSTOTAL_API_KEY>
DB_NAME=<YOUR_DB_NAME>
DB_USER=<YOUR_DB_USER>
DB_PASSWORD=<YOUR_DB_PASSWORD>
DB_HOST=<YOUR_DB_HOST>
```

4. Run the following command to start the server:

```bash
python3 app.py
```

5. Open the browser and go to the following link: `http://127.0.0.1:5000`
5. Upload a file and click on the submit button to get the results from the virustotal scan.
5. The results will be displayed on the webpage and stored in a PostgreSQL database.
