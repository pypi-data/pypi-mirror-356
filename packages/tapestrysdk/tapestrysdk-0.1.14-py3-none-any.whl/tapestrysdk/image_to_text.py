import os
import pymysql
import openai
from dotenv import load_dotenv
from .db import get_db_connection
from .helper.decrypt_ai_key import decrypt_ai_key

# Load environment variables
load_dotenv()

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant. Given the user's prompt and the AI-generated content, your task is to "
    "combine them into a clear, natural description or summary that sounds like a direct answer. Do not "
    "explain the AI's response or the user's prompt separately — instead, produce a single, coherent statement "
    "that captures the essence of both. Be concise and descriptive."
)

def image_to_text(token, user_prompt, image_url, system_prompt=""):
    if not image_url or not user_prompt or not token:
        return {"error": "Missing required fields"}

    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Authenticate API token
            cursor.execute("SELECT * FROM tool WHERE tool_secret_key = %s", (token,))
            tool_key = cursor.fetchone()
            if not tool_key:
                return {"error": "Invalid token"}

            # 1. Find document
            cursor.execute("SELECT * FROM documents WHERE file_id = %s", (image_url,))
            doc = cursor.fetchone()
            if not doc:
                return {"error": "Document not found for the given URL"}

            print(doc,"docc")

            tapestry_id = doc.get("tapestry_id")
            if not tapestry_id:
                return {"error": "Missing tapestry_id in the document"}

            # 2. Find organization by tapestry_id
            cursor.execute("SELECT * FROM tapestry_detail WHERE id = %s", (tapestry_id,))
            org = cursor.fetchone()
            if not org:
                return {"error": f"Organization not found for tapestry_id {tapestry_id}"}
            
            print(org,"org")

        # Proceed with OpenAI call
        org_name = org.get("name", "UnknownOrg").replace(" ", "_")
        openai_key = org.get("open_ai_key")
        if not openai_key:
            return {"error": "Missing OpenAI API key for organization"}

        decrypted_key = decrypt_ai_key(openai_key)
        print(decrypted_key,"decrypted_key")
        model_name = org.get("model", "gpt-4-vision-preview")

        # Step 1: OpenAI image analysis
        openai_client = openai.OpenAI(api_key=decrypted_key)
        user_prompt_text = "You are a helpful assistant. Your task is to accurately extract details from the provided image."

        vision_response = openai_client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt_text},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ]
                }
            ],
            max_tokens=1000
        )

        ai_generated_result = vision_response.choices[0].message.content

        # Step 2: Refine response with system prompt
        final_system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        chat_response = openai_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": final_system_prompt},
                {
                    "role": "user",
                    "content": f"ai_generated_result-{ai_generated_result} user_prompt-{user_prompt}"
                },
            ],
            stream=False
        )

        final_result = chat_response.choices[0].message.content
        return {"result": final_result}

    except Exception as e:
        print("Error:", e)
        return {"error": "Internal server error", "details": str(e)}
