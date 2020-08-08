from django.shortcuts import render, HttpResponseRedirect, Http404
from learning_logs.models import Topic, Entry
from learning_logs.forms import TopicForm, EntryForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'index.html')


@login_required
def topics(request):
    topic_list = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topic_list}
    return render(request, 'topics.html', context)


@login_required
def topic(request, topic_id):
    tp = Topic.objects.get(id=topic_id)
    if tp.owner != request.user:
        raise Http404
    entries = tp.entry_set.order_by('-date_added')
    context = {'topic': tp, 'entries': entries}
    return render(request, 'topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_tp = form.save(commit=False)
            new_tp.owner = request.user
            new_tp.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    tp = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            ne = form.save(commit=False)
            ne.topic = tp
            ne.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': tp, 'form': form}
    return render(request, 'new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    tp = entry.topic
    if tp.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 用entry实例填充表单
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[tp.id]))
    context = {'entry': entry, 'topic': tp, 'form': form}
    return render(request, 'edit_entry.html', context)