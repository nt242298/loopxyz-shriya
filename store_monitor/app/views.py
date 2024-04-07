# views.py

import uuid
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Store, StoreStatus
from .tasks import generate_report_task


def trigger_report(request):
    # Generate a random report_id
    report_id = str(uuid.uuid4())
    
    # Start the task to generate the report asynchronously
    generate_report_task.delay(report_id)
    
    # Return the report_id as the response
    return JsonResponse({'report_id': report_id})


def get_report(request):
    report_id = request.GET.get('report_id')
    
    try:
        # Check if the report with given report_id exists
        # If it exists, check if it's complete or running
        # If it's complete, return the CSV file
        # If it's running, return "Running" status
        # If it doesn't exist, return an error
        # This part will depend on how you store and retrieve report status in your database
        # Assuming here that the status is stored in a separate model ReportStatus
        # You should replace it with your actual implementation
        # For demonstration purpose, I'll just return a dummy response
        if report_id:
            return JsonResponse({'status': 'Running'})  # Dummy response
        else:
            return JsonResponse({'error': 'Report ID is required'}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
