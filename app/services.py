from datetime import datetime, timezone
from flask import current_app
from pymongo.errors import DuplicateKeyError
from .db import get_db

def format_timestamp(iso_str):
    """Formats ISO timestamp to human-readable UTC format."""
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.strftime('%d-%m-%Y %H:%M:%S UTC') # Example: 01-04-2021 15:30:00 UTC
    except (ValueError, TypeError):
        return str(iso_str)

def process_webhook(event_type, payload, delivery_id):
    """
    Processes the webhook payload and stores relevant data in MongoDB.
    """
    db = get_db()
    collection = db.events

    # Duplicate check using request_id (GitHub Delivery ID)
    if collection.find_one({"request_id": delivery_id}):
        return {"status": "skipped", "reason": "Duplicate event"}

    event_data = {
        "request_id": delivery_id,
        "created_at": datetime.now(timezone.utc)
    }

    # Extract common fields
    if event_type == 'push':
        # Ref looks like "refs/heads/main"
        ref = payload.get('ref', '')
        to_branch = ref.split('/')[-1] if ref else 'unknown'
        
        event_data.update({
            "type": "PUSH",
            "author": payload.get('pusher', {}).get('name', 'unknown'),
            "to_branch": to_branch,
            "timestamp": format_timestamp(payload.get('head_commit', {}).get('timestamp', ''))
        })

    elif event_type == 'pull_request':
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        
        # Check for MERGE event
        if action == 'closed' and pr.get('merged') is True:
            event_data.update({
                "type": "MERGE",
                "author": pr.get('user', {}).get('login', 'unknown'),
                "from_branch": pr.get('head', {}).get('ref', 'unknown'),
                "to_branch": pr.get('base', {}).get('ref', 'unknown'),
                "timestamp": format_timestamp(pr.get('merged_at', ''))
            })
        elif action in ['opened', 'reopened']: # Considering these as "submitted"
            event_data.update({
                "type": "PULL_REQUEST",
                "author": pr.get('user', {}).get('login', 'unknown'),
                "from_branch": pr.get('head', {}).get('ref', 'unknown'),
                "to_branch": pr.get('base', {}).get('ref', 'unknown'),
                "timestamp": format_timestamp(pr.get('created_at', ''))
            })
        else:
            return {"status": "ignored", "reason": f"Unhandled PR action: {action}"}

    else:
         return {"status": "ignored", "reason": f"Unhandled event type: {event_type}"}

    try:
        collection.insert_one(event_data)
        return {"status": "success"}
    except DuplicateKeyError:
        return {"status": "skipped", "reason": "Duplicate event logic caught by DB"}
    except Exception as e:
        current_app.logger.error(f"Error saving event: {e}")
        return {"status": "error", "message": str(e)}

def get_latest_events():
    """Fetches the latest events from MongoDB."""
    db = get_db()
    # Sort by created_at desc (newest first)
    # Limiting to last 10-20 to keep UI clean per "Minimal" requirement?
    # prompt says "Do NOT display old data already shown earlier" - this implies client side logic or simple polling.
    # The requirement "Do NOT display old data already shown earlier" is interesting.
    # It might mean the UI should only append new items.
    # Or strict polling simply returning what's there but the UI diffs it.
    # For a simple solution, returning the last N events is standard, 
    # but to satisfy "not display old data already shown", the UI (JS) usually handles filtering by ID/timestamp.
    # However, if I return everything sorted, the JS can filter. 
    # Let's return the last 20 events.
    events_cursor = db.events.find({}, {'_id': 0}).sort("created_at", -1).limit(20)
    return list(events_cursor)
