from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Message
from .app import get_current_app

@csrf_exempt
@require_http_methods(["POST"])
def message_endpoint(request):
    try:
        data = json.loads(request.body)
        
        # Create Message object from incoming data
        message = Message(
            text=data.get('text', ''),
            chat_id=data.get('chat_id', ''),
            user_id=data.get('user_id', ''),
            attachments=[]
        )
        
        # Get current app and run handlers
        app = get_current_app()
        if app and app.message_handlers:
            response = app.message_handlers[0](message)
            
            return JsonResponse({
                "status": "success",
                "response": {
                    "text": response.text,
                    "attachments": [att.__dict__ for att in response.attachments]
                }
            })
        
        return JsonResponse({"status": "success", "message": "No handlers registered"})
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
