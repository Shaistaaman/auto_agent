"""
Main Incident Handler Lambda Function

This function processes new incidents, analyzes logs, invokes the Bedrock Agent,
and executes appropriate remediation actions.
"""

import json
import os
import boto3
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock_agent = boto3.client('bedrock-agent-runtime')
logs_client = boto3.client('logs')
sns_client = boto3.client('sns')
ssm_client = boto3.client('ssm')
lambda_client = boto3.client('lambda')

# Environment variables
INCIDENT_BUCKET = os.environ['INCIDENT_BUCKET']
INCIDENT_HISTORY_TABLE = os.environ['INCIDENT_HISTORY_TABLE']
ALERT_TOPIC_ARN = os.environ['ALERT_TOPIC_ARN']
BEDROCK_AGENT_ID = os.environ.get('BEDROCK_AGENT_ID', 'PLACEHOLDER')
BEDROCK_AGENT_ALIAS_ID = os.environ.get('BEDROCK_AGENT_ALIAS_ID', 'TSTALIASID')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Initialize DynamoDB table
incident_table = dynamodb.Table(INCIDENT_HISTORY_TABLE)

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Main Lambda handler for incident processing.
    
    Args:
        event: New incident event from deduplicator
        context: Lambda context
        
    Returns:
        Dict with processing status
    """
    print(f"Received incident event: {json.dumps(event)}")
    
    try:
        # Extract incident information
        detail = json.loads(event['detail'])
        incident_id = detail['incidentId']
        original_event = detail['originalEvent']
        
        print(f"Processing incident: {incident_id}")
        
        # Update incident status
        update_incident_status(incident_id, 'processing')
        
        # Gather context information
        context_data = gather_incident_context(original_event)
        
        # Store context in S3 for audit
        store_incident_context(incident_id, context_data)
        
        # Check if Bedrock Agent is configured
        if BEDROCK_AGENT_ID == 'PLACEHOLDER':
            print("Bedrock Agent not configured, using fallback logic")
            result = fallback_incident_processing(incident_id, context_data)
        else:
            # Invoke Bedrock Agent for decision making
            result = invoke_bedrock_agent(incident_id, context_data)
        
        # Update incident with result
        update_incident_status(incident_id, 'completed', result)
        
        print(f"Incident processing completed: {incident_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Incident processed successfully',
                'incidentId': incident_id,
                'result': result
            })
        }
        
    except Exception as e:
        print(f"Error processing incident: {str(e)}")
        
        # Update incident status to failed
        if 'incident_id' in locals():
            update_incident_status(incident_id, 'failed', {'error': str(e)})
        
        # Send alert to humans
        send_alert(f"Incident processing failed: {str(e)}", 'critical')
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing incident',
                'error': str(e)
            })
        }

def gather_incident_context(original_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gather context information about the incident.
    
    Args:
        original_event: Original CloudWatch alarm event
        
    Returns:
        Dict containing incident context
    """
    alarm_name = original_event['detail']['alarmName']
    region = original_event['region']
    
    context = {
        'alarm': {
            'name': alarm_name,
            'state': original_event['detail']['state']['value'],
            'reason': original_event['detail']['state'].get('reason', ''),
            'timestamp': original_event['detail']['state'].get('timestamp', ''),
        },
        'region': region,
        'account': original_event['account'],
        'logs': get_recent_logs(alarm_name),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return context

def get_recent_logs(alarm_name: str, minutes: int = 15) -> List[str]:
    """
    Get recent error logs related to the alarm.
    
    Args:
        alarm_name: CloudWatch alarm name
        minutes: Number of minutes to look back
        
    Returns:
        List of recent log messages
    """
    try:
        # This is a simplified implementation
        # In production, you would use CloudWatch Logs Insights
        # to query specific log groups based on the alarm
        
        query = f"""
        fields @timestamp, @message
        | filter @message like /ERROR|Exception|Failed/
        | filter @timestamp > ago({minutes}m)
        | sort @timestamp desc
        | limit 10
        """
        
        # For now, return mock logs
        # TODO: Implement actual CloudWatch Logs Insights query
        return [
            f"Sample error log related to {alarm_name}",
            "Application experiencing high CPU usage",
            "Database connection timeout detected"
        ]
        
    except Exception as e:
        print(f"Error fetching logs: {str(e)}")
        return []

def store_incident_context(incident_id: str, context_data: Dict[str, Any]) -> None:
    """Store incident context in S3 for audit purposes."""
    try:
        key = f"incidents/{incident_id}/context.json"
        s3_client.put_object(
            Bucket=INCIDENT_BUCKET,
            Key=key,
            Body=json.dumps(context_data, indent=2),
            ContentType='application/json'
        )
        print(f"Context stored in S3: s3://{INCIDENT_BUCKET}/{key}")
        
    except Exception as e:
        print(f"Error storing context: {str(e)}")

def invoke_bedrock_agent(incident_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke Bedrock Agent to analyze incident and decide on actions.
    
    Args:
        incident_id: Unique incident identifier
        context_data: Incident context information
        
    Returns:
        Dict containing agent decision and actions taken
    """
    try:
        # Prepare input for Bedrock Agent
        input_text = f"""
        Incident Analysis Request:
        
        Incident ID: {incident_id}
        Alarm: {context_data['alarm']['name']}
        State: {context_data['alarm']['state']}
        Reason: {context_data['alarm']['reason']}
        Region: {context_data['region']}
        
        Recent Logs:
        {chr(10).join(context_data['logs'])}
        
        Please analyze this incident and recommend appropriate remediation actions.
        """
        
        print(f"Invoking Bedrock Agent with input: {input_text[:200]}...")
        
        # Invoke Bedrock Agent
        response = bedrock_agent.invoke_agent(
            agentId=BEDROCK_AGENT_ID,
            agentAliasId=BEDROCK_AGENT_ALIAS_ID,
            sessionId=incident_id,
            inputText=input_text
        )
        
        # Process agent response
        completion = ""
        for event in response['completion']:
            if 'chunk' in event:
                completion += event['chunk']['bytes'].decode('utf-8')
        
        print(f"Bedrock Agent response: {completion}")
        
        # Parse agent response and execute actions
        # This is a simplified implementation
        # In production, you would parse structured tool responses
        
        return {
            'agent_response': completion,
            'actions_taken': ['analysis_completed'],
            'confidence': 0.8,
            'recommendation': 'Monitor situation'
        }
        
    except Exception as e:
        print(f"Error invoking Bedrock Agent: {str(e)}")
        return fallback_incident_processing(incident_id, context_data)

def fallback_incident_processing(incident_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fallback processing when Bedrock Agent is not available.
    
    Args:
        incident_id: Unique incident identifier
        context_data: Incident context information
        
    Returns:
        Dict containing fallback processing result
    """
    alarm_name = context_data['alarm']['name']
    
    # Simple rule-based fallback logic
    if 'CPU' in alarm_name.upper():
        action = 'cpu_high_detected'
        recommendation = 'Consider scaling out or investigating high CPU usage'
    elif 'MEMORY' in alarm_name.upper():
        action = 'memory_high_detected'
        recommendation = 'Check for memory leaks or scale up instance'
    else:
        action = 'generic_alarm'
        recommendation = 'Manual investigation required'
    
    # Send notification for human review
    send_alert(
        f"Incident {incident_id} requires attention: {alarm_name}",
        'medium'
    )
    
    return {
        'fallback_processing': True,
        'action': action,
        'recommendation': recommendation,
        'human_notified': True
    }

def update_incident_status(incident_id: str, status: str, result: Optional[Dict[str, Any]] = None) -> None:
    """Update incident status in DynamoDB."""
    try:
        update_expression = "SET #status = :status, updatedAt = :updated_at"
        expression_values = {
            ':status': status,
            ':updated_at': datetime.utcnow().isoformat()
        }
        expression_names = {'#status': 'status'}
        
        if result:
            update_expression += ", result = :result"
            expression_values[':result'] = json.dumps(result)
        
        incident_table.update_item(
            Key={'incidentId': incident_id, 'timestamp': 0},  # Use 0 for main record
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values
        )
        
        print(f"Incident status updated: {incident_id} -> {status}")
        
    except Exception as e:
        print(f"Error updating incident status: {str(e)}")

def send_alert(message: str, severity: str = 'medium') -> None:
    """Send alert notification via SNS."""
    try:
        subject = f"🚨 DevOps Agent Alert ({severity.upper()})"
        
        sns_client.publish(
            TopicArn=ALERT_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        
        print(f"Alert sent: {message}")
        
    except Exception as e:
        print(f"Error sending alert: {str(e)}")