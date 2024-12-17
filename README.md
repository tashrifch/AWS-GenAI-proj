This code automatically scans an Amazon S3 bucket every 60 seconds for new PDF files. It extracts text from each PDF, generates a 100-word summary using OpenAI's API, and saves the summary back into the S3 bucket as a .txt file. Once a PDF has been processed, it is renamed to indicate completion (appending _processed), ensuring the code only processes new PDFs added to the bucket.

How to Run
Set Environment Variables:
Before running the script, ensure the following environment variables are configured:

OPENAI_API_KEY: Your OpenAI API key
AWS_ACCESS_KEY_ID: Your AWS access key ID
AWS_SECRET_ACCESS_KEY: Your AWS secret key
Update the S3 Bucket Name:
Replace the placeholder bucket name in the code with the name of your Amazon S3 bucket.

Run the Script:

Load the code into your preferred IDE (e.g., PyCharm, VSCode).
Run the script.
Once set up, the script will:

Automatically scan the specified S3 bucket every 60 seconds.
Summarize any new PDFs and save the summaries as .txt files in the same bucket.
Rename processed PDFs to avoid reprocessing them.
