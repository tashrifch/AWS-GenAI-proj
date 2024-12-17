import boto3
from PyPDF2 import PdfReader
from io import BytesIO
from openai import OpenAI
import time  # To add a delay
import os


# Initialize OpenAI API Key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") #Set your enviorment variable
)


# Function to summarize text with OpenAI
def summarize_text(text):
    try:
        # Use the OpenAI API to summarize the content
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model
            messages=[
                {"role": "user", "content": f"Summarize the following text in 100 words:\n\n{text}"}
            ],
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None


# Function to process the PDFs in the S3 bucket
def process_pdfs(bucket_name):
    # Initialize S3 resource
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-2",
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),  # Set your enviorment variable
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY') # Set your enviorment variable
    )
    bucket = s3.Bucket(bucket_name)

    # Process PDFs in the specified bucket
    print(f"Processing bucket: {bucket_name}")
    for obj in bucket.objects.all():
        if obj.key.endswith(".pdf") and not obj.key.endswith("_processed.pdf"):
            print(f"PDF Found: {obj.key}")
            s3_object = obj.get()
            content = s3_object["Body"].read()

            # Use BytesIO to handle the content as a file-like object
            with BytesIO(content) as pdf_file:

                # Get the text with pdf reader
                reader = PdfReader(pdf_file)
                pdf_text = ""
                for page in reader.pages:
                    pdf_text += page.extract_text()

                # Summarize if there's text
                if pdf_text.strip():
                    print(f"Summarizing content of {obj.key}...\n")
                    summary = summarize_text(pdf_text)
                    if summary:
                        print(f"Summary of {obj.key}:\n{summary}")

                        # Save the summary back to S3 as a .txt file
                        txt_key = obj.key.replace(".pdf", ".txt")
                        s3.Object(bucket_name, txt_key).put(
                            Body=summary.encode("utf-8"),
                            ContentType="text/plain"
                        )
                        print(f"Summary saved to {txt_key}")

                        # Rename the PDF by copying it to a new key with "processed" appended
                        new_pdf_key = obj.key.replace(".pdf", "_processed.pdf")
                        s3.Object(bucket_name, new_pdf_key).copy_from(CopySource={"Bucket": bucket_name, "Key": obj.key})
                        print(f"PDF renamed to {new_pdf_key}")

                        # Delete the original PDF
                        s3.Object(bucket_name, obj.key).delete()
                        print(f"Original PDF {obj.key} deleted.")
                        print("=" * 50)
                else:
                    print(f"No readable text found in {obj.key}.\n")
        elif obj.key.endswith("_processed.pdf"):
            print(f"Skipping already processed PDF: {obj.key}")

# Main Loop to Run Every 60 Seconds
if __name__ == "__main__":
    bucket_name = 'tashbucket1'  # Replace with the name of your target bucket

    while True:  # Infinite loop
        print("Starting PDF processing cycle...")
        process_pdfs(bucket_name)
        print("Cycle completed. Waiting for 60 seconds...")


        time.sleep(60)  # Pause for 60 seconds
