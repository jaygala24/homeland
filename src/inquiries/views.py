from django.shortcuts import render
from .models import Contact

# Create your views here.
def contact_us(request):
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']
    
    contact=Contact.objects.Create(name=name,email=email,subject=subject,message=message)
   

    return render(request, 'pages/contact.html')