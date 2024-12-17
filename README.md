# PDF Summarizer for Amazon S3

This script automatically scans an Amazon S3 bucket every 60 seconds for new PDF files. It extracts text from each PDF, generates a 100-word summary using OpenAI's API, and saves the summary back into the S3 bucket as a `.txt` file. Once a PDF is processed, the script renames it to indicate completion (appending `_processed`), ensuring only new PDFs are handled.

---

## Features
- Scans the specified S3 bucket for new PDF files every 60 seconds.
- Extracts text from PDFs and generates 100-word summaries using OpenAI's API.
- Saves summaries as `.txt` files in the same S3 bucket.
- Renames processed PDFs by appending `_processed` to avoid duplicate processing.

---

## Prerequisites

Ensure the following tools and credentials are set up:

### Environment Variables
Before running the script, configure the following environment variables:

| Variable              | Description                     |
|-----------------------|---------------------------------|
| `OPENAI_API_KEY`      | Your OpenAI API key             |
| `AWS_ACCESS_KEY_ID`   | Your AWS access key ID          |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key            |

---

## Setup Instructions

1. **Update the S3 Bucket Name**  
   Replace the placeholder bucket name in the script with the name of your Amazon S3 bucket.

2. **Run the Script**  
   - Load the code into your preferred IDE (e.g., PyCharm, VSCode).
   - Run the script.

---

## How It Works

Once running, the script will:
1. **Automatically scan the specified S3 bucket** every 60 seconds.
2. **Summarize any new PDFs** and save the summaries as `.txt` files in the same bucket.
3. **Rename processed PDFs** to append `_processed` to their filenames, ensuring they are not reprocessed.

---

## Dependencies
Ensure the following libraries are installed:
- `boto3` for interacting with Amazon S3.
- `openai` for accessing the OpenAI API.
- `PyPDF2` (or another library for PDF text extraction).

Install dependencies using pip:
```bash
pip install boto3 openai PyPDF2
