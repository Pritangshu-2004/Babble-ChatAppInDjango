from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q
from django.utils.dateformat import DateFormat
from django.http import JsonResponse

# Create your views here.
@login_required
def chatRoom(request, username):
    receiver = User.objects.filter(username=username).first()

    # Exclude messages that have been deleted by the logged-in user
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=request.user))
    ).exclude(deleted_by=request.user).order_by("timestamp")

    if request.method == 'POST':
        msg = request.POST.get('msg')
        if msg:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=msg
            )

    return render(request, "chat/chat.html", {"r": receiver, "messages": messages})

@login_required
def get_messages(request, username):
    r = User.objects.filter(username=username).first()
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=r)) |
        (Q(sender=r) & Q(receiver=request.user))
    ).exclude(deleted_by=request.user).order_by("timestamp")
    
    messages_data = [
        {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": DateFormat(message.timestamp).format('H:i'),
            "can_delete": (request.user == message.sender or request.user == message.receiver)
        }
        for message in messages               
    ]
    return JsonResponse({"messages": messages_data})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Check if the user is the sender or receiver
    if request.user == message.sender:
        # If the sender deletes, delete for everyone
        message.delete()
        return JsonResponse({'success': True, 'message': 'Message deleted for everyone.'})
    elif request.user == message.receiver:
        # If the receiver deletes, delete only for themselves
        message.deleted_by.add(request.user)
        return JsonResponse({'success': True, 'message': 'Message deleted for you.'})
    else:
        return JsonResponse({'success': False, 'error': 'You are not authorized to delete this message.'}, status=403)

@login_required
def delete_chat(request, username):
    receiver = get_object_or_404(User, username=username)

    # Mark all messages as deleted for the sender's side
    if request.user:
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
        )
        for message in messages:
            message.deleted_by.add(request.user)  # Mark the message as deleted by the sender
        return JsonResponse({'success': True, 'message': 'Chat deleted successfully for your side.'})
    else:
        return JsonResponse({'success': False, 'error': 'You are not authorized to delete this chat.'}, status=403)