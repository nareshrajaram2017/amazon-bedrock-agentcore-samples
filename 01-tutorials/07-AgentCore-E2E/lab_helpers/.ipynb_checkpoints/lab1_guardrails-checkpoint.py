import logging
import os
import sys
import uuid

import boto3
from boto3.session import Session
from scripts.utils import get_ssm_parameter, put_ssm_parameter

boto_session = Session()
REGION = boto_session.region_name
logger = logging.getLogger(__name__)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

bedrock_client = boto3.client("bedrock", region_name=REGION)


def create_or_get_guardrail_resource():
    try:
        guardrail_id = get_ssm_parameter("/app/customersupport/bedrock/guardrail_id")
        guardrail_version = get_ssm_parameter(
            "/app/customersupport/bedrock/guardrail_version"
        )
        return guardrail_id, guardrail_version
    except Exception:
        try:
            response = bedrock_client.create_guardrail(
                name="customer-support-assistant-guardrail-{}".format(
                    str(uuid.uuid4())[:4]
                ),
                description="Only respond to the customer support related questions, is protected against the most common prompt mis-use threads, provides content moderation.",
                topicPolicyConfig={
                    "topicsConfig": [
                        {
                            "name": "Finance",
                            "definition": "Statements or questions about finances, transactions or monetary advise.",
                            "examples": [
                                "What are the cheapest rates?",
                                "Where can I invest?",
                            ],
                            "type": "DENY",
                        }
                    ]
                },
                contentPolicyConfig={
                    "filtersConfig": [
                        {
                            "type": "SEXUAL",
                            "inputStrength": "HIGH",
                            "outputStrength": "HIGH",
                        },
                        {
                            "type": "VIOLENCE",
                            "inputStrength": "HIGH",
                            "outputStrength": "HIGH",
                        },
                        {
                            "type": "HATE",
                            "inputStrength": "HIGH",
                            "outputStrength": "HIGH",
                        },
                        {
                            "type": "INSULTS",
                            "inputStrength": "HIGH",
                            "outputStrength": "HIGH",
                        },
                        {
                            "type": "MISCONDUCT",
                            "inputStrength": "HIGH",
                            "outputStrength": "HIGH",
                        },
                        {
                            "type": "PROMPT_ATTACK",
                            "inputStrength": "HIGH",
                            "outputStrength": "NONE",
                        },
                    ]
                },
                sensitiveInformationPolicyConfig={
                    "piiEntitiesConfig": [
                        {"type": "AGE", "action": "ANONYMIZE"},
                    ]
                },
                blockedInputMessaging="Sorry, I can not respond to this. I'm supposed to assist in customer support related questions only.'",
                blockedOutputsMessaging="Sorry, I can not respond to this. I'm supposed to assist in customer support related questions only.'",
            )
            response_version = bedrock_client.create_guardrail_version(
                guardrailIdentifier=response["guardrailId"], description="First version"
            )
            guardrail_id, guardrail_version = (
                response_version["guardrailId"],
                response_version["version"],
            )
            try:
                put_ssm_parameter(
                    "/app/customersupport/bedrock/guardrail_id", guardrail_id
                )
                put_ssm_parameter(
                    "/app/customersupport/bedrock/guardrail_version",
                    guardrail_version,
                )
            except:
                pass
            return guardrail_id, guardrail_version
        except:
            return None, None
