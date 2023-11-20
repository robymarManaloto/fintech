from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .generator import generate_results, generate_html, analyze

# Load Speech Recognition Page
def speech_recognition(request):
    request.session.clear()
    return render(request, 'speech_recognition_app/index.html')

# Request AI Summary from Transcript
def result_view(request):
    if request.method == "POST":
        transcript = request.POST['transcript']        
        text = generate_results(transcript)
        return render(request, 'speech_recognition_app/result.html', {'text': text})
    return render(request, 'speech_recognition_app/index.html')

# Analyze AI Campaign Input Field 
@csrf_exempt
def input_analyze(request):
    if request.method == 'POST':
        transcription = request.POST.get('transcription')
        field = request.POST.get('field')
        
        if transcription == '':
            return JsonResponse({'error': 'Transcription data is empty'}, status=400)
                
        response_data = analyze({'field': field, 'transcript': transcription})
        response_data.update({'success': True})      
        
    else:
        response_data = {'success': False}
    
    return JsonResponse(response_data)
# Request to Generate Campaign Page
@csrf_exempt
def generate_campaign(request):
    if request.method == "POST":
        if 'data_dict' in request.session and request.session['data_dict']:
            data_dict = request.session['data_dict']
            campaign_page_result = generate_html(data_dict)
            if campaign_page_result != -1:
                request.session['campaign_page'] = campaign_page_result
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            reward_titles = request.POST.getlist('reward_title')
            reward_descriptions = request.POST.getlist('reward_description')
            reward_amounts = request.POST.getlist('reward_amount')
            data_dict = {
                "title": request.POST.get("title"),
                "description": request.POST.get("description"),
                "category": request.POST.get("category"),
                "fundgoal": request.POST.get("funding_goal"),
                "duration": request.POST.get("duration"),
                "rewards": [
                    {"title": title, "description": description, "amount": amount}
                    for title, description, amount in zip(reward_titles, reward_descriptions, reward_amounts)
                ]
            }
            
            campaign_page_result = generate_html(data_dict)
            if campaign_page_result != -1:
                request.session['campaign_page'] = campaign_page_result
                request.session['data_dict'] = data_dict
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
    return JsonResponse({'success': False})

# Preview Campaign Page
def preview_campaign_view(request):
    campaign_page_data = request.session.get('campaign_page')
    data_dict = request.session.get('data_dict')
    if campaign_page_data:
        return render(request, 'edit_campaign_page_app/preview_campaign.html', {'page': campaign_page_data, 'data': data_dict})
    else:
        return HttpResponse("Campaign page data not found in session")

# Save Campaign Page
def save_campaign(request):
    html_data = request.POST.get('html_data')
    return render(request, 'edit_campaign_page_app/save_campaign.html', {'data': html_data})
