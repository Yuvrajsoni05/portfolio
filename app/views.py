from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from dotenv import load_dotenv
import json
import requests
import os
from django.contrib.auth import authenticate, login, logout

from app.models import ChatBot


# from langchain_community.tools.amadeus.utils import authenticate


def index(request):
    print("THis ",os.getenv("HF_TOKEN"))
    print(
        requests.get("https://huggingface.co").status_code
    )
    return render(request, 'home.html')


@login_required()
def admin_dashboard(request):
    return render(request, 'admin_side/admin_dashboard.html')

def admin_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username)
            print(password)

            try:
                user =  authenticate(request,username=username,password=password)
                if user is not None:
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    return redirect('admin_login')
            except Exception as e:
                print("except",e)
    except Exception as e:
        print("Error")
    return render(request, 'admin_side/admin_login.html')
API_URL =  os.getenv("API_URL")

HEADERS = {
    "Authorization": os.getenv("HF_TOKEN"),
    "Content-Type": "application/json"
}



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


def load_resume():

    resume_path = os.path.join(
        BASE_DIR,
        "resume_context.txt"
    )

    try:

        with open(
            resume_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except FileNotFoundError:

        return "Resume context file not found."


resume_context = load_resume()


# =========================
# CHATBOT
# =========================

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            # Get frontend data
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({
                    "reply": "Please enter a message."
                })

            if "step" not in request.session:
                request.session["step"] = "ask_name"

            step = request.session["step"]

            if step == "ask_name":

                request.session["step"] = "get_name"

                return JsonResponse({
                    "reply": "What is your name?"
                })

            elif step == "get_name":

                request.session["name"] = user_message

                print("NAME:", request.session["name"])
                chat = ChatBot.objects.create(name=request.session["name"])
                chat.save()

                request.session["step"] = "chat"

                return JsonResponse({
                    "reply": f"Hello {user_message}, you are connected."
                })
            # AI Request
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={
                    "model": "meta-llama/Llama-3.1-8B-Instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"""
                            You are Yuvraj Soni's AI assistant.
                            Use the resume context below to answer questions professionally.
                            Resume Context:
                            {resume_context}
                            """
                        },
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                    "max_tokens": 200,
                    "temperature": 0.7
                }
            )
            if response.status_code != 200:
                return JsonResponse({
                    "reply": response.text
                })

            result = response.json()
            bot_reply = result["choices"][0]["message"]["content"]
            return JsonResponse({
                "reply": bot_reply
            })
        except Exception as e:
            return JsonResponse({
                "reply": str(e)
            })
    return JsonResponse({
        "error": "Invalid request"
    })




# def Datasent(request):
#
#     if request.method == 'POST':
#
#         name = request.POST.get('name')
#
#         email = request.POST.get('email')
#
#         subject = request.POST.get('subject')
#
#         message = request.POST.get('message')
#
#
#         email_message = EmailMessage(
#
#             'USER DATA SUBMISSION',
#
#             f'''
#             Name: {name}
#
#             Subject: {subject}
#
#             Email: {email}
#
#             Message: {message}
#             ''',
#
#             settings.DEFAULT_FROM_EMAIL,
#
#             ['yuvrajsoni9192@gmail.com'],
#
#             headers={
#                 'Reply-To': email
#             }
#
#         )
#
#
#         email_message.send(
#             fail_silently=False
#         )
#
#
#         return render(
#             request,
#             'thankyou.html',
#             {
#                 'name': name
#             }
#         )
#
#
#     return HttpResponseRedirect('/')
#
#
# # =========================
# # CERTIFICATIONS PAGE
# # =========================
#
# def certification(request):
#
#     return render(
#         request,
#         'certifications.html'
#     )