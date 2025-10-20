"""
Incident Deduplicator Lambda Function

This function receives CloudWatch alarm events and checks for duplicate incidents
to prevent unnecessary processing and costs.
"""

import json
import os
import boto3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
events_client = boto3.client('events')

# Environment variables
INCIDENT_HISTORY_TABLE = os.environ['INCIDENT_HISTORY_TABLE']
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Initialize DynamoDB table
incident_table = dynamodb.Table(INCIDENT_HISTORY_TABLE)

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Main Lambda handler for incident deduplication.
    
    Args:
        event: CloudWatch alarm event
        context: Lambda context
        
    Returns:
        Dict with processing status
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract alarm information
        alarm_name = event['detail']['alarmName']
        alarm_state = event['detail']['state']['value']
        region = event['region']
        account = event['account']
        timestamp = datetime.utcnow()
        
        # Create incident ID based on alarm characteristics
        incident_id = generate_incident_id(alarm_name, region, account)
        
        print(f"Processing incident: {incident_id}")
        
        # Check for recent duplicate incidents
        if is_duplicate_incident(incident_id, timestamp):
            print(f"Duplicate incident detected: {incident_id}")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Duplicate incident ignored',
                    'incidentId': incident_id,
                    'action': 'ignored'
                })
            }
        
        # Record new incident
        record_incident(incident_id, event, timestamp)
        
        # Forward to main incident handler
        forward_to_handler(incident_id, event)
        
        print(f"New incident forwarded: {incident_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'New incident processed',
                'incidentId': incident_id,
                'action': 'forwarded'
            })
        }
        
    except Exception as e:
        print(f"Error processing incident: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing incident',
                'error': str(e)
            })
        }

def generate_incident_id(alarm_name: str, region: str, account: str) -> str:
    """Generate a unique incident ID based on alarm characteristics."""
    content = f"{alarm_name}:{region}:{account}"
    return hashlib.md5(content.encode()).hexdigest()[:16]

def is_duplicate_incident(incident_id: str, current_time: datetime, window_minutes: int = 15) -> bool:
    """
    Check if this incident occurred recently (within the time window).
    
    Args:
        incident_id: Unique incident identifier
        current_time: Current timestamp
        window_minutes: Deduplication window in minutes
        
    Returns:
        True if duplicate found, False otherwise
    """
    try:
        # Calculate time window
        window_start = current_time - timedelta(minutes=window_minutes)
        window_start_timestamp = int(window_start.timestamp() * 1000)
        
        # Query recent incidents
        response = incident_table.query(
            KeyConditionExpression='incidentId = :incident_id AND #ts >= :window_start',
            ExpressionAttributeNames={
                '#ts': 'timestamp'
            },
            ExpressionAttributeValues={
                ':incident_id': incident_id,
                ':window_start': window_start_timestamp
            },
            Limit=1
        )
        
        return len(response['Items']) > 0
        
    except Exception as e:
        print(f"Error checking for duplicates: {str(e)}")
        return False

def record_incident(incident_id: str, event: Dict[str, Any], timestamp: datetime) -> None:
    """Record the incident in DynamoDB."""
    try:
        incident_table.put_item(
            Item={
                'incidentId': incident_id,
                'timestamp': int(timestamp.timestamp() * 1000),
                'status': 'new',
                'alarmName': event['detail']['alarmName'],
                'alarmState': event['detail']['state']['value'],
                'region': event['region'],
                'account': event['account'],
                'originalEvent': json.dumps(event),
                'createdAt': timestamp.isoformat(),
                'ttl': int((timestamp + timedelta(days=90)).timestamp())  # Auto-cleanup after 90 days
            }
        )
        print(f"Incident recorded: {incident_id}")
        
    except Exception as e:
        print(f"Error recording incident: {str(e)}")
        raise

def forward_to_handler(incident_id: str, original_event: Dict[str, Any]) -> None:
    """Forward new incident to the main handler via EventBridge."""
    try:
        # Create custom event for the main handler
        custom_event = {
            'Source': 'devops.agent',
            'DetailType': 'New Incident Detected',
            'Detail': json.dumps({
                'incidentId': incident_id,
                'originalEvent': original_event,
                'processedAt': datetime.utcnow().isoformat()
            })
        }
        
        # Send to EventBridge
        events_client.put_events(Entries=[custom_event])
        print(f"Event forwarded to handler: {incident_id}")
        
    except Exception as e:
        print(f"Error forwarding event: {str(e)}")
        raise