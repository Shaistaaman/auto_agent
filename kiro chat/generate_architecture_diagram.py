#!/usr/bin/env python3
"""
Alhambra Banking Architecture Diagram Generator

This script generates an architecture diagram for the Alhambra Banking application.
Run this script to create a visual representation of the system architecture.

Requirements:
    pip install diagrams

Usage:
    python generate_architecture_diagram.py
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.engagement import SES
from diagrams.aws.management import ParameterStore, Cloudwatch
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server

def generate_architecture_diagram():
    """Generate the Alhambra Banking architecture diagram."""
    
    with Diagram("Alhambra Banking - Microservices Architecture", 
                 show=False, 
                 direction="TB",
                 filename="alhambra_banking_architecture"):
        
        # Frontend Layer
        with Cluster("Frontend Layer"):
            users = Users("Bank Users")
            frontend = Server("React Frontend\n(TypeScript + Vite)")
        
        # API Gateway Layer
        api_gateway = APIGateway("API Gateway\n(Regional)")
        
        # Authentication Layer
        cognito_pool = Cognito("Cognito User Pool\n(Custom Auth Flow)")
        
        # Lambda Microservices
        with Cluster("Lambda Microservices"):
            with Cluster("Auth Service"):
                auth_create = Lambda("Create Auth\nChallenge")
                auth_define = Lambda("Define Auth\nChallenge")
                auth_verify = Lambda("Verify Auth\nChallenge")
                auth_message = Lambda("Custom\nMessage")
                auth_confirm = Lambda("Post\nConfirmation")
            
            with Cluster("Business Services"):
                user_get = Lambda("Get User\nProfile")
                user_update = Lambda("Update User\nProfile")
                notification = Lambda("Send\nNotification")
                integration = Lambda("Third Party\nProxy")
        
        # Data Layer
        with Cluster("Data Storage"):
            users_table = Dynamodb("Users Table\n(GSI: email, accountType)")
            sessions_table = Dynamodb("User Sessions\n(TTL enabled)")
        
        # External Services
        with Cluster("External Services"):
            ses_service = SES("SES Email\nService")
            param_store = ParameterStore("Parameter Store\n(Integration Configs)")
        
        # Monitoring
        monitoring = Cloudwatch("CloudWatch\n(Logs & Metrics)")
        
        # User Flow
        users >> frontend >> api_gateway
        
        # API Gateway to Business Services
        api_gateway >> Edge(label="REST API") >> [user_get, user_update, notification, integration]
        
        # Cognito Authentication Triggers
        cognito_pool >> Edge(label="Lambda Triggers") >> [auth_create, auth_define, auth_verify, auth_message, auth_confirm]
        
        # Database Connections
        [user_get, user_update, auth_confirm] >> Edge(label="Read/Write") >> users_table
        auth_confirm >> Edge(label="Session Management") >> sessions_table
        
        # External Service Connections
        [notification, auth_message] >> Edge(label="Email") >> ses_service
        integration >> Edge(label="Config") >> param_store
        
        # Monitoring Connections
        [api_gateway, auth_create, auth_define, auth_verify, auth_message, 
         auth_confirm, user_get, user_update, notification, integration] >> Edge(label="Logs") >> monitoring

def generate_simplified_diagram():
    """Generate a simplified version of the architecture diagram."""
    
    with Diagram("Alhambra Banking - Simplified Architecture", 
                 show=False, 
                 direction="LR",
                 filename="alhambra_banking_simplified"):
        
        # Main Components
        users = Users("Users")
        frontend = Server("React App")
        api = APIGateway("API Gateway")
        cognito = Cognito("Cognito")
        
        # Services
        with Cluster("Lambda Services"):
            auth_svc = Lambda("Auth Service")
            user_svc = Lambda("User Service")
            notify_svc = Lambda("Notification")
            integration_svc = Lambda("Integration")
        
        # Storage
        with Cluster("Data Layer"):
            users_db = Dynamodb("Users Table")
            sessions_db = Dynamodb("Sessions")
        
        # External
        email = SES("SES")
        config = ParameterStore("Parameter Store")
        logs = Cloudwatch("CloudWatch")
        
        # Flow
        users >> frontend >> api
        api >> [auth_svc, user_svc, notify_svc, integration_svc]
        cognito >> auth_svc
        [auth_svc, user_svc] >> users_db
        auth_svc >> sessions_db
        [notify_svc, auth_svc] >> email
        integration_svc >> config
        [api, auth_svc, user_svc, notify_svc, integration_svc] >> logs

if __name__ == "__main__":
    print("Generating Alhambra Banking architecture diagrams...")
    
    try:
        # Generate detailed architecture diagram
        generate_architecture_diagram()
        print("✅ Generated detailed architecture diagram: alhambra_banking_architecture.png")
        
        # Generate simplified architecture diagram
        generate_simplified_diagram()
        print("✅ Generated simplified architecture diagram: alhambra_banking_simplified.png")
        
        print("\n📊 Architecture diagrams have been generated successfully!")
        print("Files created:")
        print("  - alhambra_banking_architecture.png (detailed)")
        print("  - alhambra_banking_simplified.png (simplified)")
        
    except ImportError as e:
        print("❌ Error: Missing required package 'diagrams'")
        print("Please install it using: pip install diagrams")
        print("You may also need to install Graphviz: brew install graphviz")
    except Exception as e:
        print(f"❌ Error generating diagrams: {e}")
        print("Make sure you have Graphviz installed: brew install graphviz")
