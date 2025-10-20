#!/bin/bash

# Setup script for Autonomous DevOps Incident Responder
# This script sets up the development environment and deploys the initial infrastructure

set -e  # Exit on any error

echo "🚀 Setting up Autonomous DevOps Incident Responder..."

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ required. Current version: $(node --version)"
    exit 1
fi

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install AWS CLI first."
    exit 1
fi

# Check CDK
if ! command -v cdk &> /dev/null; then
    echo "📦 Installing AWS CDK..."
    npm install -g aws-cdk
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install dependencies
echo "📦 Installing project dependencies..."
npm install

# Check if CDK is bootstrapped
echo "🔧 Checking CDK bootstrap status..."
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region || echo "us-east-1")

if ! aws cloudformation describe-stacks --stack-name CDKToolkit --region $REGION &> /dev/null; then
    echo "🚀 Bootstrapping CDK..."
    cdk bootstrap aws://$ACCOUNT/$REGION
else
    echo "✅ CDK already bootstrapped"
fi

# Build the project
echo "🔨 Building project..."
npm run build

# Deploy to development environment
echo "🚀 Deploying to development environment..."
npm run deploy:dev

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure Bedrock model access in AWS Console"
echo "2. Create Bedrock Agent (see docs/architecture/)"
echo "3. Update BEDROCK_AGENT_ID in Lambda environment variables"
echo "4. Test the system with a CloudWatch alarm"
echo ""
echo "📊 Useful commands:"
echo "  npm run deploy:dev    # Deploy to development"
echo "  npm run test          # Run tests"
echo "  npm run destroy       # Clean up resources"
echo ""
echo "🎉 Happy hacking!"