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

from app.models import ChatBot, MyContext


# from langchain_community.tools.amadeus.utils import authenticate


def index(request):
   
    # print(
    #     requests.get("https://huggingface.co").status_code
    # )
    return render(request, 'home.html')


@login_required()
def admin_dashboard(request):
    my_context = MyContext.objects.all()

    context = {
        'contexts': my_context
    }
    return render(request, 'admin_side/admin_dashboard.html',context=context)

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



API_URL = os.getenv("API_URL")

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json",
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

            # # First time user
            # if "step" not in request.session:
            #     request.session["step"] = "ask_name"

            # step = request.session["step"]

            # # Ask user's name
            # if step == "ask_name":
            #     request.session["step"] = "get_name"

            #     return JsonResponse({
            #         "reply": "Hello! What's your name?"
            #     })

            # # Save user's name
            # elif step == "get_name":

            #     request.session["name"] = user_message

            #     print("NAME:", request.session["name"])

            #     ChatBot.objects.create(
            #         name=request.session["name"]
            #     )

            #     request.session["step"] = "chat"

            #     return JsonResponse({
            #         "reply": f"Hello {user_message}, you are connected."
            #     })

            # Normal Chat
            # elif step == "chat":

            response = requests.post(
                    API_URL,
                    headers=HEADERS,
                    json={
                        "model": "meta-llama/Llama-3.1-8B-Instruct",
                        "messages": [
                            {
                                "role": "system",
                                "content": f"""
        You are an AI assistant representing Yuvraj Soni.

        The user's name is {request.session.get("name")}.

        Provide answers that are:
        - Short
        - Simple
        - Professional

        Formatting rules:
        - Do NOT use asterisks (*) or markdown
        - Keep replies natural
        - Use numbered points only when needed

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

def create_context(request):
    if request.method == "POST":
        title = request.POST.get("title")
        context = request.POST.get("context")

        print("This is Title",title)
        context_create = MyContext.objects.create(
            title = title,
            content = context

        )
        context_create.save()
        return redirect('admin_dashboard')

    else:
        print("error")
        return redirect('admin_dashboard')


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


def call_me(request):
    return render(request,'demo.html')