from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup FastAPI
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load secrets from environment
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")       # e.g., https://your-resource.openai.azure.com/
openai.api_version = "2024-12-01-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")         # Keep this in .env file only
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME")      # e.g., gpt-4-note

# Pydantic model
class EmailData(BaseModel):
    email_body: str

@app.post("/generate-qualification-note")
async def generate_qualification_note(data: EmailData):
    prompt = f"""
You are a sales assistant. Analyze the following email body and generate a structured qualification note.

Email Body:
{data.email_body}

Return the result in JSON format with:
- Opportunity Summary
- Pain Points
- Budget & Timeline
- Decision Makers
- Next Steps
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
            max_tokens=800
        )

        result = response['choices'][0]['message']['content']
        logger.info("Response generated successfully.")
        return {"qualification_note": result}

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail="Internal Server Error")
