import boto3
import json
import os
import sys
import webbrowser
from botocore.exceptions import ClientError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bedrock_agentcore.identity.auth import requires_access_token
from datetime import datetime, timedelta
from strands import tool

# Constants
SCOPES = ["https://www.googleapis.com/auth/calendar"]
credentials_file = "../credentials.json"
google_provider_name = "customersupport-google-calendar"
region = boto3.session.Session().region_name

def store_provider_name_in_ssm(provider_name):
    ssm = boto3.client('ssm')
    try:
        ssm.put_parameter(
            Name='/customersupport/google_provider_name',
            Value=provider_name,
            Type='String',
            Overwrite=True
        )
    except Exception as e:
        print(f"Error storing provider name in SSM: {str(e)}")

def setup_credentials():
    if not os.path.isfile(credentials_file):
        raise FileNotFoundError(f"'{credentials_file}' file not found")

    with open(credentials_file, "r") as f:
        data = json.load(f)

    web_config = data.get("web")
    if not web_config:
        raise ValueError("'web' section missing in credentials.json")

    client_id = web_config.get("client_id")
    client_secret = web_config.get("client_secret")

    if not client_id or not client_secret:
        raise ValueError("client_id or client_secret not found in credentials.json")

    # Create the OAuth2 credential provider
    try:
        print("🔧 Setting up Google OAuth2 credential provider...")
        identity_client = boto3.client(
            "bedrock-agentcore-control",
            region_name=region,
        )

        # Try to get existing provider
        try:
            existing_provider = identity_client.get_oauth2_credential_provider(
                name=google_provider_name
            )
            print("✅ Found existing Google OAuth2 credential provider")
            google_provider_arn = existing_provider["credentialProviderArn"]
            print(f"   Provider ARN: {google_provider_arn}")
            print(f"   Provider Name: {existing_provider['name']}")
            
        except identity_client.exceptions.ResourceNotFoundException:
            # Create new provider if it doesn't exist
            print("Creating new Google OAuth2 credential provider...")
            google_provider = identity_client.create_oauth2_credential_provider(
                name=google_provider_name,
                credentialProviderVendor="GoogleOauth2",
                oauth2ProviderConfigInput={
                    "googleOauth2ProviderConfig": {
                        "clientId": client_id,
                        "clientSecret": client_secret,
                    }
                },
            )
            print("✅ Google OAuth2 credential provider created successfully")
            google_provider_arn = google_provider["credentialProviderArn"]
            print(f"   Provider ARN: {google_provider_arn}")
            print(f"   Provider Name: {google_provider['name']}")

        # Store provider name in SSM
        store_provider_name_in_ssm(google_provider_name)

    except Exception as e:
        print(f"❌ Error with Google credential provider: {str(e)}")
        raise

    return client_id, client_secret

async def on_auth_url(url: str):
    webbrowser.open(url)

@requires_access_token(
    provider_name=google_provider_name,
    scopes=SCOPES,
    auth_flow="USER_FEDERATION",
    on_auth_url=on_auth_url,
    force_authentication=True,
    into="access_token",
)
def get_google_access_token(access_token: str):
    return access_token

@tool(
    name="Create_calendar_event",
    description="Creates a new event on your Google Calendar",
)
def create_calendar_event() -> str:
    google_access_token = ''
    try:
        google_access_token = get_google_access_token(access_token=google_access_token)
        if not google_access_token:
            raise Exception("requires_access_token did not provide tokens")
    except Exception as e:
        return "Error Authentication with Google: " + str(e)

    creds = Credentials(token=google_access_token, scopes=SCOPES)
    
    try:
        service = build("calendar", "v3", credentials=creds)
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)

        event = {
            "summary": "Test Event from API",
            "location": "Virtual",
            "description": "This event was created using the Google Calendar API.",
            "start": {
                "dateTime": start_time.isoformat() + "Z",
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat() + "Z",
                "timeZone": "UTC",
            },
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        return json.dumps({
            "event_created": True,
            "event_id": created_event.get("id"),
            "htmlLink": created_event.get("htmlLink"),
        })

    except HttpError as error:
        return json.dumps({"error": str(error), "event_created": False})
    except Exception as e:
        return json.dumps({"error": str(e), "event_created": False})

@tool(
    name="Get_calendar_events_today",
    description="Retrieves the calendar events for the day from your Google Calendar",
)
def get_calendar_events_today() -> str:
    google_access_token = ''
    try:
        google_access_token = get_google_access_token(access_token=google_access_token)
        if not google_access_token:
            raise Exception("requires_access_token did not provide tokens")
    except Exception as e:
        return "Error Authentication with Google: " + str(e)

    creds = Credentials(token=google_access_token, scopes=SCOPES)
    try:
        service = build("calendar", "v3", credentials=creds)
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59)

        timeMin = today_start.strftime("%Y-%m-%dT00:00:00-05:00")
        timeMax = today_end.strftime("%Y-%m-%dT23:59:59-05:00")

        events_result = service.events().list(
            calendarId="primary",
            timeMin=timeMin,
            timeMax=timeMax,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        
        events = events_result.get("items", [])
        return json.dumps({"events": events})
        
    except HttpError as error:
        return json.dumps({"error": str(error), "events": []})
    except Exception as e:
        return json.dumps({"error": str(e), "events": []})

# Setup is done automatically when this module is imported
setup_credentials()
