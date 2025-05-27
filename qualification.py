from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import logging
from dotenv import load_dotenv
from openai.types import OpenAIError 
# Load environment variables from .env file
load_dotenv()

# Setup FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running! Welcome to qualification-note!"}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Azure OpenAI configuration from environment
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")          # e.g., https://your-resource.openai.azure.com/
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")    # e.g., 2024-12-01-preview
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")            # stored in .env
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME")    # e.g., gpt-4-note

# Pydantic model for request body
class EmailData(BaseModel):
    email_body: str

@app.post("/generate-qualification-note")
async def generate_qualification_note(data: EmailData):
    prompt = f"""
You are the assistant specific towards the generating qualification. Analyze the following email body and generate a structured qualification note.

Email Body:
{data.email_body}

Return the result in JSON format with the following fields:
{{
  "salutation": "string (e.g., Dear [Client Name],)",
  "customer_overview": "string (brief overview of the customer)",
  "customer_details": {{
    "name": "string (e.g., Company Name)",
    "Annual Revenue": "string (e.g., $10M)",
    "No. of Employees": "string (e.g., 200)"
  }},
  "opportunity_overview": "string (summary of the opportunity)",
  "key_highlights": "string (main points or quotes from the email)",
  "target_timeline": "string (expected timeline mentioned)",
  "tcv_estimate": "string (Total Contract Value estimate if any)"
}}

Only return valid JSON, nothing else.
"""

    try:
        logger.info("Sending prompt to Azure OpenAI...")

        response = openai.ChatCompletion.create(
            engine=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in business documentation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )

        result = response["choices"][0]["message"]["content"]
        logger.info("Response generated successfully.")
        return {"qualification_note": result}

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)