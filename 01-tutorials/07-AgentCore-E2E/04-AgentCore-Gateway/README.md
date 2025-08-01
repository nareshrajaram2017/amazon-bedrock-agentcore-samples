# Lab 4: Creating Agents with Amazon AgentCore Tool Gateway Functionality

## Overview

In this tutorial you will learn how to create a customer support agent using AWS Strands SDK and Amazon Bedrock AgentCore with a Bedrock AgentCore Gateway MCP Server. 

Bedrock AgentCore Gateway provides customers a way to turn their existing APIs and Lambda functions into fully-managed MCP servers without needing to manage infra or hosting. Customers can bring OpenAPI spec or Smithy models for their existing APIs, or add Lambda functions that front their tools. Gateway will provide a uniform Model Context Protocol (MCP) interface across all these tools. Gateway employs a dual authentication model to ensure secure access control for both incoming requests and outbound connections to target resources. 

The customer support agent in this lab will have:
1. AgentCore Identity using Amazon Cognito
2. AgentCore Memory
3. Tools
   - Custom Tools:
     - Order status checking
     - Product information
     - Shipping details
     - Return policy information
   - Strands Built-in Tools:
     - Current Time
     - Retrieve
   - AgentCore Gateway MCP Tools:
     - Check Warranty
     - Get Customer Profile

![Architecture Diagram](images/architecture.png)


**Based on**: [Official Customer Support Assistant](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases/customer-support-assistant)

## Prerequisites

* Python 3.10+
* AWS credentials configured
* Strands Agents and supporting libraries


## Defining concepts
**Amazon Bedrock AgentCore Gateway:** HTTP endpoint that customers can call with an MCP client for executing the standard MCP operations (i.e. listTools and invokeTool). Customers can also invoke this AmazonCore Gateway using an AWS SDK such as boto3.

**Bedrock AgentCore Gateway Target:** a resource that customer uses to attach targets to their AmazonCore Gateway. Currently the following types are supported as targets for AgentCore Gateway:
- Lambda ARNs
- API specifications → OpenAPI, Smithy

**MCP Transport:** mechanism that defines how messages move between clients (applications using LLMs) and the MCP servers. Currently AgentCore Gateway supports only Streamable HTTP connections as transport.

### Inbound and outbound authorization
Bedrock AgentCore Gateway provides secure connections via inbound and outbound authentication. For the inbound authentication, the AgentCore Gateway analyzes the OAuth token passed during invocation to decide allow or deny the access to a tool in the gateway. If a tool needs access to external resources, the AgentCore Gateway can use outbound authentication via API Key, IAM or OAuth Token to allow or deny the access to the external resource.

During the inbound authorization flow, an agent or the MCP client calls an MCP tool in the AgentCore Gateway adding an OAuth access token (generated from the user’s IdP). AgentCore Gateway then validates the OAuth access token and performs inbound authorization.

If the tool running in AgentCore Gateway needs to access external resources, OAuth will retrieve credentials of downstream resources using the resource credential provider for the Gateway target. AgentCore Gateway pass the authorization credentials to the caller to get access to the downstream API.

### Integration
Bedrock AgentCore Gateway integrates with:
- Bedrock AgentCore Identity
- Bedrock AgentCore Runtime

### Use cases
- Real-time interactive agents calling MCP tools
- Inbound & outbound authorization using different IdPs
- MCP-fying the AWS Lambda functions, Open APIs and Smithy models
- MCP tools discovery

### Benefits
Gateway provides several key benefits that simplify AI agent development and deployment: 
- **No infrastructure management:** Fully managed service with no hosting concerns. Amazon Bedrock AgentCore handles all infrastructure for you automatically.
- **Unified interface:** Single MCP protocol for all tools eliminates the complexity of managing multiple API formats and authentication mechanisms in your agent code.
- **Built-in authentication:** OAuth and credential management handles token lifecycle, refresh, and secure storage without additional development effort.
- **Automatic scaling:** Scales automatically based on demand to handle varying workloads without manual intervention or capacity planning.
- **Enterprise security:** Enterprise-grade security features including encryption, access controls, and audit logging ensure secure tool access.