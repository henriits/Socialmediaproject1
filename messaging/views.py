from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from messaging.forms import ThreadForm, MessageForm
from messaging.models import ThreadModel, MessageModel


class ListThreads(View):
    """
    This class-based view is responsible for listing threads for the current user.
    It retrieves all threads where the current user is either the sender or the receiver.
    """

    def get(self, request, *args, **kwargs):
        # Retrieve threads where the current user is either the sender or the receiver
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, "messages/inbox.html", context)


class CreateThread(View):
    """
    This class-based view is responsible for creating a new thread between users.
    It provides the functionality to display the form to create a thread and process the form submission.
    """

    def get(self, request, *args, **kwargs):
        # Display the form to create a thread
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'messages/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        # Process the form submission to create a new thread
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        try:
            # Get the receiver user object based on the provided username
            receiver = User.objects.get(username=username)

            # Check if a thread already exists between the current user and the receiver
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                # If a thread exists, redirect to the existing thread's view
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                # If the form is valid, create a new thread between the current user and the receiver
                sender_thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                sender_thread.save()
                thread_pk = sender_thread.pk
                return redirect('thread', pk=thread_pk)
        except:
            # If an error occurs (e.g., receiver user not found), redirect back to create thread view
            return redirect('create-thread')


class ThreadView(View):
    """
    This class-based view is responsible for displaying a thread and its messages.
    It retrieves the thread and its associated messages based on the provided thread ID (pk).
    """

    def get(self, request, pk, *args, **kwargs):
        # Retrieve the thread and its associated messages
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'messages/thread.html', context)


class CreateMessage(View):
    """
    This class-based view is responsible for creating a new message in a thread.
    It processes the form submission to create a new message associated with the provided thread ID (pk).
    """

    def post(self, request, pk, *args, **kwargs):
        # Retrieve the thread associated with the provided thread ID (pk)
        thread = ThreadModel.objects.get(pk=pk)

        # Determine the receiver of the message based on the thread's participants
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        # Create a new message associated with the thread, sender, receiver, and message body
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        return redirect('thread', pk=pk)
