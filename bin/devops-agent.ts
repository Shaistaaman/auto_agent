#!/usr/bin/env node
import 'source-map-support/register'
import * as cdk from 'aws-cdk-lib'
import { DevopsAgentStack } from '../lib/devops-agent-stack'

const app = new cdk.App()

// Get environment from context or default to 'dev'
const environment = app.node.tryGetContext('environment') || 'dev'

// Environment-specific configuration
const envConfig = {
  dev: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1'
  },
  prod: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1'
  }
}

const config = envConfig[environment as keyof typeof envConfig]

new DevopsAgentStack(app, `DevopsAgentStack-${environment}`, {
  env: config,
  environment,
  description:
    'Autonomous DevOps Incident Responder using AWS Bedrock AgentCore',
  tags: {
    Project: 'AutonomousDevOpsIncidentResponder',
    Environment: environment,
    Purpose: 'AWS-AI-Agent-Hackathon',
    Owner: 'DevOps-Team'
  }
})

app.synth()
