import os
import sys
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
load_dotenv()

endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
model_name = os.environ.get("FOUNDRY_MINI_MODEL", "gpt-5.6-sol")

if not endpoint or "your-project" in endpoint:
    print("❌ ERROR: FOUNDRY_PROJECT_ENDPOINT is missing or unconfigured in .env file.")
    sys.exit(1)

print(f"Connecting to Microsoft Foundry Project: {endpoint}...")

try:
    credential = DefaultAzureCredential()
    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
        openai_client = project_client.get_openai_client()
        
        print("Sending test request to model over Responses API...")
        response = openai_client.responses.create(
            model=model_name,
            input="Respond with 'ManuscriptShield AI connection verified!' if you can read this.",
        )
        
        print("\n✅ Service Verification Output:")
        print(f"Status: {response.status}")
        print(f"Response: {response.output_text}")
        print("\n🎉 Connection to Microsoft Foundry successfully verified!")

except Exception as e:
    print(f"\n❌ Verification failed: {e}")
    sys.exit(1)
