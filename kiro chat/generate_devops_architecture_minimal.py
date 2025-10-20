#!/usr/bin/env python3
"""
Autonomous DevOps Incident Responder Architecture Diagram Generator (Minimal Version)

This script generates architecture diagrams using only basic, guaranteed-to-work imports.

Requirements:
    pip install diagrams

Usage:
    python generate_devops_architecture_minimal.py
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway
from diagrams.aws.management import Cloudwatch, SystemsManager
from diagrams.aws.integration import Eventbridge, SNS
from diagrams.generic.blank import Blank
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.generic.network import Firewall

def generate_detailed_architecture():
    """Generate the detailed DevOps Incident Responder architecture diagram."""
    
    with Diagram("Autonomous DevOps Incident Responder - Detailed Architecture", 
                 show=False, 
                 direction="TB",
                 filename="devops_incident_responder_detailed"):
        
        # Monitoring & Detection Layer
        with Cluster("Monitoring & Detection Layer"):
            cloudwatch_alarms = Cloudwatch("CloudWatch\nAlarms")
            xray_traces = Cloudwatch("X-Ray\nTraces")
            third_party = Rack("Third-party\nMonitoring")
        
        # Event Processing
        eventbridge = Eventbridge("EventBridge\n(Event Router)")
        
        # Smart Processing Layer
        with Cluster("Smart Processing Layer"):
            deduplicator = Lambda("Incident\nDeduplicator")
            incident_handler = Lambda("Enhanced Incident\nHandler")
        
        # Context & Intelligence Layer
        with Cluster("Context & Intelligence Layer"):
            logs_insights = Cloudwatch("CloudWatch\nLogs Insights")
            amazon_q = Rack("Amazon Q\n(AWS Runbooks)")
            knowledge_base = S3("S3 Knowledge Base\n(Vector Search)")
            historical_context = Dynamodb("Historical Context\n(DynamoDB)")
        
        # AI Decision Engine
        with Cluster("AI Decision Engine"):
            bedrock_agent = Rack("Enhanced Bedrock Agent\n(Claude 3.5 + AgentCore)")
            confidence_scoring = Lambda("Confidence &\nCost Scoring")
        
        # Remediation Layer
        with Cluster("Multi-Modal Remediation"):
            ssm_automation = SystemsManager("SSM Automation\nDocuments")
            lambda_remediation = Lambda("Lambda\nRemediation")
            sagemaker_ai = Rack("SageMaker AI\n(Anomaly Detection)")
        
        # Monitoring & Learning
        with Cluster("Monitoring & Learning"):
            remediation_monitor = Lambda("Remediation\nMonitor")
            ml_training = Rack("ML Model\nTraining (Optional)")
        
        # Human Interface
        with Cluster("Human Interface"):
            sns_notifications = SNS("SNS Smart\nNotifications")
            slack_integration = Blank("Slack/Teams\nIntegration")
        
        # Storage & Audit
        with Cluster("Storage & Compliance"):
            s3_storage = S3("S3 Encrypted\nStorage")
            cloudtrail = Firewall("CloudTrail\nAudit Logs")
            cost_monitor = Lambda("Cost Monitor\n& Dashboard")
        
        # Flow Connections
        [cloudwatch_alarms, xray_traces, third_party] >> eventbridge
        eventbridge >> deduplicator
        deduplicator >> Edge(label="New Incident") >> incident_handler
        deduplicator >> Edge(label="Duplicate") >> Blank("Log & Ignore")
        
        incident_handler >> [logs_insights, amazon_q, knowledge_base, historical_context]
        incident_handler >> bedrock_agent
        bedrock_agent >> confidence_scoring
        
        confidence_scoring >> Edge(label="High Conf + Low Cost") >> [ssm_automation, lambda_remediation, sagemaker_ai]
        confidence_scoring >> Edge(label="Medium Conf") >> sns_notifications
        confidence_scoring >> Edge(label="Low Conf + High Risk") >> sns_notifications
        
        [ssm_automation, lambda_remediation, sagemaker_ai] >> remediation_monitor
        remediation_monitor >> Edge(label="Success") >> ml_training
        remediation_monitor >> Edge(label="Failure") >> sns_notifications
        
        sns_notifications >> slack_integration
        
        # Storage connections
        [incident_handler, bedrock_agent, remediation_monitor] >> s3_storage
        historical_context >> ml_training
        ml_training >> bedrock_agent
        
        # Audit connections
        [s3_storage, historical_context] >> cloudtrail
        cost_monitor >> sns_notifications

def generate_simplified_architecture():
    """Generate a simplified version of the architecture diagram."""
    
    with Diagram("Autonomous DevOps Incident Responder - Simplified Architecture", 
                 show=False, 
                 direction="LR",
                 filename="devops_incident_responder_simplified"):
        
        # Input
        monitoring = Cloudwatch("Monitoring\n(CloudWatch + X-Ray)")
        
        # Processing
        event_router = Eventbridge("Event\nRouter")
        incident_processor = Lambda("Incident\nProcessor")
        
        # AI Engine
        ai_agent = Rack("Bedrock Agent\n(Claude 3.5)")
        
        # Knowledge
        with Cluster("Knowledge Sources"):
            amazon_q = Rack("Amazon Q")
            knowledge_db = S3("Knowledge\nBase")
            history = Dynamodb("Incident\nHistory")
        
        # Actions
        with Cluster("Remediation"):
            ssm = SystemsManager("SSM\nAutomation")
            lambda_fix = Lambda("Lambda\nFunctions")
            ml_detect = Rack("ML Anomaly\nDetection")
        
        # Human Interface
        alerts = SNS("Smart\nAlerts")
        chat = Blank("Slack/Teams")
        
        # Storage
        storage = S3("Audit &\nStorage")
        
        # Flow
        monitoring >> event_router >> incident_processor
        incident_processor >> ai_agent
        ai_agent >> [amazon_q, knowledge_db, history]
        ai_agent >> [ssm, lambda_fix, ml_detect]
        [ssm, lambda_fix, ml_detect] >> alerts
        alerts >> chat
        [incident_processor, ai_agent] >> storage

def generate_compliance_architecture():
    """Generate architecture diagram highlighting hackathon compliance."""
    
    with Diagram("DevOps Incident Responder - Hackathon Compliance View", 
                 show=False, 
                 direction="TB",
                 filename="devops_incident_responder_compliance"):
        
        # Required Components (Highlighted)
        with Cluster("✅ Required AWS Services"):
            bedrock_llm = Rack("Amazon Bedrock\n(Claude 3.5 LLM)")
            agent_core = Blank("AgentCore Primitives\n(toolUse, orchestration)")
            amazon_q_svc = Rack("Amazon Q\n(Runbooks)")
            sagemaker_svc = Rack("SageMaker AI\n(Optional)")
        
        # AI Agent Qualifications
        with Cluster("✅ AI Agent Qualifications"):
            reasoning = Lambda("Reasoning LLM\nDecision Making")
            autonomous = Lambda("Autonomous\nCapabilities")
            human_loop = SNS("Human-in-the-Loop\nFallback")
        
        # External Integrations
        with Cluster("✅ External Tool Integration"):
            apis = APIGateway("APIs")
            databases = Dynamodb("Databases")
            external_tools = SystemsManager("External Tools\n(SSM, CloudWatch)")
        
        # Helper Services
        with Cluster("✅ Helper Services (Optional)"):
            lambda_svc = Lambda("AWS Lambda")
            s3_svc = S3("Amazon S3")
            api_gateway = APIGateway("API Gateway")
        
        # Compliance Flow
        bedrock_llm >> agent_core
        agent_core >> reasoning
        reasoning >> autonomous
        autonomous >> human_loop
        
        reasoning >> apis
        reasoning >> databases
        reasoning >> external_tools
        lambda_svc >> reasoning
        s3_svc >> reasoning
        api_gateway >> reasoning
        
        # Cost Optimization Indicators
        with Cluster("💰 Cost Optimizations"):
            dedup = Lambda("Incident\nDeduplication")
            batch = Lambda("Intelligent\nBatching")
            cost_aware = Lambda("Cost-Aware\nRemediation")
        
        reasoning >> [dedup, batch, cost_aware]

def generate_cost_comparison():
    """Generate cost comparison diagram."""
    
    with Diagram("DevOps Incident Responder - Cost Comparison", 
                 show=False, 
                 direction="LR",
                 filename="devops_incident_responder_costs"):
        
        # Original Architecture Costs
        with Cluster("Original Architecture ($85-250/month)"):
            orig_bedrock = Rack("Bedrock\n$50-150")
            orig_q = Rack("Amazon Q\n$20-40")
            orig_lambda = Lambda("Lambda\n$10-30")
            orig_other = S3("Other Services\n$5-30")
        
        # Improved Architecture Costs
        with Cluster("Improved Architecture ($50-120/month)"):
            imp_bedrock = Rack("Bedrock\n$30-80")
            imp_q = Rack("Amazon Q\n$15-25")
            imp_s3 = S3("S3 Knowledge\n$2-5")
            imp_lambda = Lambda("Optimized Lambda\n$3-8")
            imp_other = Dynamodb("Other Services\n$10-15")
        
        # Savings Indicators
        savings = Blank("40-52% Cost Reduction\n$35-130 Monthly Savings")
        
        orig_bedrock >> Edge(label="Optimization") >> savings
        orig_q >> savings
        orig_lambda >> savings
        orig_other >> savings
        savings >> imp_bedrock
        savings >> imp_q
        savings >> imp_s3
        savings >> imp_lambda
        savings >> imp_other

if __name__ == "__main__":
    print("Generating Autonomous DevOps Incident Responder architecture diagrams...")
    print("Using minimal icons for maximum compatibility...")
    
    try:
        # Generate detailed architecture diagram
        generate_detailed_architecture()
        print("✅ Generated detailed architecture diagram: devops_incident_responder_detailed.png")
        
        # Generate simplified architecture diagram
        generate_simplified_architecture()
        print("✅ Generated simplified architecture diagram: devops_incident_responder_simplified.png")
        
        # Generate compliance-focused diagram
        generate_compliance_architecture()
        print("✅ Generated compliance architecture diagram: devops_incident_responder_compliance.png")
        
        # Generate cost comparison diagram
        generate_cost_comparison()
        print("✅ Generated cost comparison diagram: devops_incident_responder_costs.png")
        
        print("\n📊 Architecture diagrams have been generated successfully!")
        print("Files created:")
        print("  - devops_incident_responder_detailed.png (comprehensive view)")
        print("  - devops_incident_responder_simplified.png (high-level overview)")
        print("  - devops_incident_responder_compliance.png (hackathon requirements)")
        print("  - devops_incident_responder_costs.png (cost comparison)")
        
        print("\n🏆 Hackathon Submission Ready!")
        print("These diagrams demonstrate:")
        print("  ✅ Full compliance with all hackathon requirements")
        print("  ✅ Amazon Bedrock + AgentCore implementation")
        print("  ✅ Autonomous AI agent with human-in-the-loop")
        print("  ✅ External tool integration (CloudWatch, SSM, etc.)")
        print("  ✅ Cost-optimized architecture (40-52% savings)")
        
    except ImportError as e:
        print("❌ Error: Missing required package 'diagrams'")
        print("Please install it using: pip install diagrams")
        print("You may also need to install Graphviz:")
        print("  - macOS: brew install graphviz")
        print("  - Ubuntu: sudo apt-get install graphviz")
        print("  - Windows: Download from https://graphviz.org/download/")
    except Exception as e:
        print(f"❌ Error generating diagrams: {e}")
        print("Make sure you have Graphviz installed and accessible in your PATH")