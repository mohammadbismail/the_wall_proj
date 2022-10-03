from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt


def index(request):
    context = {"users": User.objects.all()}
    return render(request, "index.html", context)


def register_user(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    password = request.POST["password"]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=pw_hash,
    )
    return redirect("/")


def check_login(request):
    user = User.objects.filter(email=request.POST["email"])
    if user:  # if True (email is found with registration database)
        logged_user = user[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_user.password.encode()
        ):
            request.session["userid"] = logged_user.id
            request.session["usrname"] = logged_user.first_name
            return redirect("/wall/")
        return redirect("/")


def logout_user(request):
    del request.session["userid"]
    del request.session["usrname"]
    return redirect("/")


def user_wall_page(request):
    if "userid" not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session["userid"]),
        "users": User.objects.all(),
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
    }
    # print(f"user id is {user_id}")
    return render(request, "user_wall.html", context)


def add_message(request):  # FIXME: take user_id from user_wall page
    user_id = request.session["userid"]
    print(f"user id is {user_id}")
    Message.objects.create(
        content=request.POST["msg"], user=User.objects.get(id=user_id)
    )
    return redirect("/wall/")


def add_comment(request):  # FIXME:
    message_id = request.POST["msgid"]
    user_id = request.session["userid"]
    # print(f"message id is {message_id}")
    # print(f"user id is {user_id}")
    Comment.objects.create(
        content=request.POST["comment"],
        message=Message.objects.get(id=message_id),
        user=User.objects.get(id=user_id),
    )
    return redirect("/wall/")
