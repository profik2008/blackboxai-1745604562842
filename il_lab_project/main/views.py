from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import Contact, Newsletter, BlogPost
import json
import requests

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def industries(request):
    return render(request, 'main/industries.html')

def case_studies(request):
    return render(request, 'main/case-studies.html')

def blog(request):
    posts = BlogPost.objects.filter(is_actual=True).order_by('-date')
    return render(request, 'main/blog.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_actual=True)
    return render(request, 'main/blog_detail.html', {'post': post})

def careers(request):
    return render(request, 'main/careers.html')

def certifications(request):
    return render(request, 'main/certifications.html')

def contact(request):
    return render(request, 'main/contact.html')

def news(request):
    # Fetch data from CISA KEV Catalog API
    cisa_url = "https://www.cisa.gov/api/known-exploited-vulnerabilities"
    cisa_response = requests.get(cisa_url)
    cisa_data = cisa_response.json() if cisa_response.status_code == 200 else {}
    cisa_vulns = cisa_data.get('vulnerabilities', [])[:10]

    # Fetch data from MITRE ATT&CK API
    mitre_url = "https://attack.mitre.org/api.php"
    mitre_response = requests.get(mitre_url)
    mitre_data = mitre_response.json() if mitre_response.status_code == 200 else {}
    mitre_tactics = mitre_data.get('tactics', [])[:10]

    context = {
        "cisa_data": {"vulnerabilities": cisa_vulns},
        "mitre_data": {"tactics": mitre_tactics},
    }
    return render(request, "main/news.html", context)

@csrf_exempt
def submit_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contact = Contact.objects.create(
                name=data.get('name'),
                company=data.get('company'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                message=data.get('message')
            )
            
            # Send notification email to admin
            send_mail(
                'New Contact Form Submission',
                f'New contact form submission from {contact.name} ({contact.company})',
                'noreply@il-lab.com',
                ['info@il-lab.com'],
                fail_silently=True,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your message. We will contact you shortly!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@csrf_exempt
def subscribe_newsletter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            # Check if email already exists
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'info',
                    'message': 'You are already subscribed to our newsletter!'
                })
            
            Newsletter.objects.create(email=email)
            
            # Send confirmation email
            send_mail(
                'Welcome to IL-LAB Newsletter',
                'Thank you for subscribing to our newsletter!',
                'noreply@il-lab.com',
                [email],
                fail_silently=True,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing to our newsletter!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
