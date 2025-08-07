# Lab 3: Creating Agents with Amazon AgentCore Identity 

## Overview

In this tutorial you will learn how to enhance your existing customer support agent by integrating Amazon Bedrock AgentCore Identity functionality. This enables your agent to securely authenticate with external services like Google Calendar using OAuth2 flows, while maintaining proper credential management through AgentCore's identity providers.

Amazon Bedrock AgentCore Identity provides a streamlined approach to managing OAuth2 authentication flows, eliminating the complexity of manual token management, refresh handling, and credential storage. This service acts as a secure intermediary between your agent and external service providers, enabling seamless integration with third-party APIs while maintaining enterprise-grade security.

The enhanced customer support agent in this lab will have:
- **AgentCore Identity**: Secure OAuth2 credential management
- **AgentCore Memory**: Conversation context and history (from Lab 2)
- **Core Customer Support Tools**: Order status, product info, shipping, returns (from Lab 1)
- **Google Calendar Integration**: Create events and view calendar information
- **Multi-Provider Support**: Both Google OAuth2 and Cognito identity providers

![Agent Architecture](images/architecture.png)

**Based on**: [Official Customer Support Assistant](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases/customer-support-assistant)

## Prerequisites

- Python 3.10+
- AWS credentials configured
- Strands Agents and supporting libraries
- **Google Developer Console access** - For creating OAuth2 credentials. You will need a Google account for this
- **AgentCore Identity permissions** - IAM role with AgentCore Identity access

## Defining Concepts

**Amazon Bedrock AgentCore Identity**: A managed service that handles OAuth2 authentication flows, credential storage, and token lifecycle management for AI agents accessing external services.

**OAuth2 Credential Provider**: A configured authentication endpoint in AgentCore Identity that manages credentials for specific external services (e.g., Google, Microsoft, custom providers).

**User Federation Flow**: An OAuth2 authentication pattern where users authenticate directly with the external service provider, and AgentCore Identity manages the resulting tokens on behalf of the agent.

**Access Token Management**: Automatic handling of OAuth2 token refresh, expiration, and secure storage without requiring manual token management in agent code.

## Integration

Bedrock AgentCore Identity integrates with:
- **Bedrock AgentCore Runtime**: For production agent deployment
- **Bedrock AgentCore Gateway**: For secure tool access and routing
- **External OAuth2 Providers**: Google, Microsoft, Okta and custom identity providers
- **AWS Systems Manager**: For secure parameter storage

## Use Cases

- **Calendar Integration**: Agents scheduling appointments and managing calendars
- **Email Access**: Agents reading and sending emails on behalf of users
- **Document Management**: Agents accessing cloud storage and document services
- **CRM Integration**: Agents updating customer records in external systems
- **Multi-tenant Applications**: Different users accessing their own external accounts

## Benefits

AgentCore Identity provides several key benefits for AI agent development:

**Simplified Authentication**: Eliminates complex OAuth2 implementation details from agent code with declarative authentication decorators.

**Automatic Token Management**: Handles token refresh, expiration, and secure storage without additional development effort.

**Enterprise Security**: Built-in security features including encrypted credential storage, audit logging, and access controls.

**Multi-Provider Support**: Single interface for multiple identity providers reduces integration complexity.

**Scalable Architecture**: Managed service that scales automatically based on authentication demand.

**Developer Productivity**: Focus on agent logic rather than authentication infrastructure, accelerating development cycles.

## Lab Architecture

This lab extends your customer support agent with secure external service access:

1. **Identity Provider Setup**: Configure Google OAuth2 credentials and create AgentCore Identity providers
2. **Authentication Flow**: Implement user federation with automatic token management
3. **Calendar Tools**: Build identity-aware tools for Google Calendar integration
4. **Agent Enhancement**: Combine existing customer support capabilities with new calendar features
5. **Testing & Validation**: Comprehensive testing of authentication flows and tool functionality

The result is a customer support agent that can handle traditional support queries while also managing calendar-related tasks securely on behalf of authenticated users.
