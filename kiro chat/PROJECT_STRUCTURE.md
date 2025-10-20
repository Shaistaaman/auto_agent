# Autonomous DevOps Incident Responder - Project Structure

## 📁 Recommended Directory Structure

```
autonomous-devops-incident-responder/
├── README.md                           # Main project documentation
├── PROJECT_PLAN.md                     # This planning document
├── TASKS.md                            # Detailed task breakdown
├── LICENSE                             # MIT or Apache 2.0
├── .gitignore                          # Git ignore rules
├── package.json                        # CDK dependencies
├── tsconfig.json                       # TypeScript configuration
├── cdk.json                            # CDK configuration
├── jest.config.js                      # Testing configuration
│
├── bin/                                # CDK app entry point
│   └── devops-agent.ts                 # Main CDK app
│
├── lib/                                # CDK stack definitions
│   ├── devops-agent-stack.ts           # Main infrastructure stack
│   ├── constructs/                     # Custom CDK constructs
│   │   ├── bedrock-agent-construct.ts  # Bedrock Agent setup
│   │   ├── monitoring-construct.ts     # CloudWatch/EventBridge
│   │   └── storage-construct.ts        # S3/DynamoDB setup
│   └── config/                         # Configuration files
│       ├── agent-instructions.txt      # Bedrock Agent prompts
│       └── tool-schemas.json           # AgentCore tool definitions
│
├── lambda/                             # Lambda function code
│   ├── incident-handler/               # Main incident processor
│   │   ├── index.py                    # Lambda entry point
│   │   ├── requirements.txt            # Python dependencies
│   │   ├── incident_processor.py       # Core logic
│   │   ├── bedrock_client.py           # Bedrock integration
│   │   ├── logs_analyzer.py            # CloudWatch Logs analysis
│   │   └── utils.py                    # Utility functions
│   │
│   ├── deduplicator/                   # Incident deduplication
│   │   ├── index.py                    # Lambda entry point
│   │   ├── requirements.txt            # Python dependencies
│   │   └── deduplication_logic.py      # Dedup algorithms
│   │
│   ├── remediation-tools/              # Tool implementations
│   │   ├── amazon-q-client/            # Amazon Q integration
│   │   │   ├── index.py
│   │   │   └── q_client.py
│   │   ├── ssm-executor/               # SSM automation
│   │   │   ├── index.py
│   │   │   └── ssm_client.py
│   │   └── notification-sender/        # SNS notifications
│   │       ├── index.py
│   │       └── notification_client.py
│   │
│   └── shared/                         # Shared utilities
│       ├── __init__.py
│       ├── aws_clients.py              # AWS service clients
│       ├── logging_config.py           # Logging setup
│       └── constants.py                # Application constants
│
├── ssm-documents/                      # SSM Automation Documents
│   ├── restart-ec2-instance.yaml       # EC2 restart automation
│   ├── scale-auto-scaling-group.yaml   # ASG scaling automation
│   ├── rollback-codedeploy.yaml        # CodeDeploy rollback
│   └── custom-remediation.yaml         # Custom remediation template
│
├── test/                               # Test files
│   ├── unit/                           # Unit tests
│   │   ├── lambda/                     # Lambda function tests
│   │   └── constructs/                 # CDK construct tests
│   ├── integration/                    # Integration tests
│   │   ├── test-events/                # Sample CloudWatch events
│   │   └── end-to-end/                 # E2E test scenarios
│   └── fixtures/                       # Test data and mocks
│       ├── sample-logs.json            # Sample log entries
│       └── mock-responses.json         # Mock API responses
│
├── docs/                               # Documentation
│   ├── architecture/                   # Architecture documentation
│   │   ├── detailed-design.md          # Detailed system design
│   │   ├── api-documentation.md        # API specs
│   │   └── deployment-guide.md         # Deployment instructions
│   ├── diagrams/                       # Architecture diagrams
│   │   ├── *.png                       # Generated diagram files
│   │   └── generate_diagrams.py        # Diagram generation script
│   └── demo/                           # Demo materials
│       ├── demo-script.md              # Demo presentation script
│       ├── demo-scenarios.md           # Test scenarios for demo
│       └── video-outline.md            # Video structure outline
│
├── scripts/                            # Utility scripts
│   ├── setup.sh                       # Environment setup
│   ├── deploy.sh                       # Deployment script
│   ├── test.sh                         # Test runner
│   └── cleanup.sh                      # Resource cleanup
│
├── config/                             # Configuration files
│   ├── dev.json                        # Development environment config
│   ├── prod.json                       # Production environment config
│   └── test.json                       # Test environment config
│
└── examples/                           # Example configurations
    ├── cloudwatch-alarms/              # Sample alarm configurations
    ├── test-events/                    # Sample incident events
    └── runbooks/                       # Sample runbook procedures
```

## 📋 File Descriptions

### **Core CDK Files**

- **`bin/devops-agent.ts`**: CDK app entry point, defines stacks
- **`lib/devops-agent-stack.ts`**: Main infrastructure stack
- **`lib/constructs/`**: Reusable CDK constructs for modularity

### **Lambda Functions**

- **`incident-handler/`**: Main processor that orchestrates incident response
- **`deduplicator/`**: Prevents duplicate incident processing
- **`remediation-tools/`**: Individual tool implementations for AgentCore
- **`shared/`**: Common utilities and AWS clients

### **Configuration & Documentation**

- **`lib/config/`**: Agent instructions and tool schemas
- **`ssm-documents/`**: Pre-built automation documents
- **`docs/`**: Comprehensive documentation and diagrams
- **`examples/`**: Sample configurations and test data

### **Testing & Scripts**

- **`test/`**: Unit, integration, and end-to-end tests
- **`scripts/`**: Automation scripts for common tasks
- **`config/`**: Environment-specific configurations

## 🚀 Getting Started Commands

### **Initial Setup**

```bash
# Create project directory
mkdir autonomous-devops-incident-responder
cd autonomous-devops-incident-responder

# Initialize CDK project
cdk init app --language typescript

# Install additional dependencies
npm install @aws-cdk/aws-bedrock @aws-cdk/aws-events-targets

# Create directory structure
mkdir -p lambda/{incident-handler,deduplicator,remediation-tools,shared}
mkdir -p lib/{constructs,config}
mkdir -p ssm-documents docs/{architecture,diagrams,demo}
mkdir -p test/{unit,integration,fixtures}
mkdir -p scripts config examples
```

### **Development Workflow**

```bash
# Install dependencies
npm install

# Run tests
npm test

# Deploy to development
npm run deploy:dev

# Deploy to production
npm run deploy:prod

# Clean up resources
npm run cleanup
```

## 🎯 Key Design Principles

### **Modularity**

- Separate CDK constructs for different components
- Individual Lambda functions for specific responsibilities
- Reusable SSM documents and configurations

### **Testability**

- Unit tests for all Lambda functions
- Integration tests for AWS service interactions
- End-to-end tests for complete workflows

### **Maintainability**

- Clear separation of concerns
- Comprehensive documentation
- Consistent naming conventions
- Environment-specific configurations

### **Security**

- Least privilege IAM permissions
- Encrypted storage and communication
- Secure credential management
- Audit logging throughout

This structure provides a solid foundation for building a professional, maintainable, and hackathon-winning AWS AI Agent! 🏆
