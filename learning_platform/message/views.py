from django.urls import reverse_lazy
from .models import Message
from django.views.generic import View, ListView, DetailView, DeleteView
from django.shortcuts import render, redirect
from .forms import MessageForm


class MessageCreateView(View):
    form_class = MessageForm
    template_name = 'message/message_new.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user_from = self.request.user
            form.save()
            return redirect('index')

        return render(request, self.template_name, {'form': form})


class MessageListView(ListView):
    template_name = 'message/index.html'
    model = Message
    fields = ['user_from', 'created']

    def get_queryset(self):
        return Message.objects.filter(user_to=self.request.user).order_by('-created')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'
    fields = ['text', 'id']


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message/message_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('index')
