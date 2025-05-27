from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import logging
from dotenv import load_dotenv

<<<<<<< Updated upstream
# Load environment variables from .env file (local development)
=======
# Load environment variables from .env file
>>>>>>> Stashed changes
load_dotenv()

# Setup FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running! Welcome to qualification-note!"}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Azure OpenAI configuration from environment variables
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")          # e.g., https://your-resource.openai.azure.com/
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")    # e.g., 2024-12-01-preview
<<<<<<< Updated upstream
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")            # your Azure OpenAI key
=======
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")            # stored in .env
>>>>>>> Stashed changes
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME")         # e.g., gpt-4-note

logger.info(f"Loaded deployment: {AZURE_DEPLOYMENT}")

# Pydantic model for incoming request body
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
<<<<<<< Updated upstream
=======
  
>>>>>>> Stashed changes
  "customer_overview": "string (brief overview of the customer)",
  "customer_details": {{
    "name": "string (e.g., Company Name)",
    "location": "string (e.g., San Francisco, CA)",
    "Annual Revenue": "string (e.g., $10M)",
    "No. of Employees": "string (e.g., 200)"
  }},
  "opportunity_overview": "string (summary of the opportunity)",
  "key_highlights": "string (main points or quotes from the email)",
  "target_timeline": "string (expected timeline mentioned)",
  "engagement_phases": "string (phases of engagement such as discovery, planning, execution, etc.)",
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
            max_tokens=500
        )

        result = response["choices"][0]["message"]["content"]
        logger.info("Response generated successfully.")
        return {"qualification_note": result}

    except Exception as e:
        logger.exception("Unexpected error occurred")
<<<<<<< Updated upstream
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Entry point for running locally with reload during development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
=======
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
>>>>>>> Stashed changes
