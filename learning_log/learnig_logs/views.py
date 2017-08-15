from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic
from .forms import TopicForm,EntryForm



# Create your views here.
def index(request):
    '''学习笔记主页'''
    return render(request,'learnig_logs/index.html')

@login_required
def topics(request):
    '''显示所有主题'''
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'learnig_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    '''显示单个主题及其所有的条目'''
    topic = Topic.objects.get(id=topic_id)
    #确认请求主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries= topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'learnig_logs/topic.html',context)

@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method !='POST':
        #未提交数据 创建一个新表单
        form = TopicForm()
    else:
        #POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit =False)
            new_topic.owner = request.user
            new_topic.save( )
            return HttpResponseRedirect(reverse('learnig_logs:topics'))

    context = {'form':form}
    return render (request,'learnig_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    '''在特定主题中添加新条目'''
    topic = Topic.objects.get(id=topic_id)

    if request.method!='POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learnig_logs:topic',
                                                args=[topic_id]))
    context={'topic':topic,'form':form}
    return render (request, 'learnig_logs/new_entry.html',context)
