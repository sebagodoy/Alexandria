import datetime
import os, time, pathlib
from django.utils import timezone
import pytz

from AlexandriaLog.settings import DATABASES
db_dir = str(DATABASES['default']['NAME'])
db_name = str(DATABASES['default']['NAME']).split('/')[-1]

bkp_dir = "\'" + db_dir + '.bkp' + '\''
sbkp_dir = "~/AlexandriaLog." + db_name + '.bkp'



from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from . models import RunModel
from .forms import RunForm

def index(request):
    print("## Refreshing index")
    RunLogsData = RunModel.objects.all()
    RunLogsData = RunLogsData.order_by('-created')[:25]
    form = RunForm

    # log times
    db_ctime = time.ctime(os.path.getctime(db_dir))
    bkp_ctime = time.ctime(os.path.getctime(bkp_dir[:-1][1:]))
    sbkp_ctime = time.ctime(os.path.getctime(str(pathlib.Path.home())+"/"+sbkp_dir.split('/')[-1]))

    if request.method == "POST":
        print(" ## Solicited: adding new task")
        form = RunForm(request.POST)
        if form.is_valid():
            newsave = form.save(commit=False)
            newsave.lastedited = timezone.now()
            newsave.save()
            print(" >> Added task")
        else:
            print(" >> Error adding")
        return redirect('/')

    # Checking stats
    StatTotalTasks = len([i for i in RunLogsData])
    StatActiveTasks = len([i for i in RunLogsData if i.active])

    context = {'RunLogs':RunLogsData,
               'RunForm':form,
               'Updating':False,
               'StatsTotal':StatTotalTasks,
               'StatsActive':StatActiveTasks,
               'db_updated':db_ctime,
               'bkp_updated':bkp_ctime,
               'sbkp_updated':sbkp_ctime}

    return render(request, 'MyLog.html', context)

def ShowMore(request, pk):
    print("## Index: longer list")
    print("   Modify url for more results")
    RunLogsData = RunModel.objects.all()
    RunLogsData = RunLogsData.order_by('-created')[:int(pk)]
    form = RunForm

    # log times
    db_ctime = time.ctime(os.path.getctime(db_dir))
    bkp_ctime = time.ctime(os.path.getctime(bkp_dir[:-1][1:]))
    sbkp_ctime = time.ctime(os.path.getctime(str(pathlib.Path.home())+"/"+sbkp_dir.split('/')[-1]))

    if request.method == "POST":
        print(" Solicited: adding new task")
        form = RunForm(request.POST)
        if form.is_valid():
            newsave = form.save(commit=False)
            newsave.lastedited = timezone.now()
            newsave.save()
            print(" >> Added task")
        else:
            print(" >> Error saving")
        return redirect('/')

    # Checking stats
    StatTotalTasks = len([i for i in RunLogsData])
    StatActiveTasks = len([i for i in RunLogsData if i.active])

    context = {'RunLogs':RunLogsData,
               'RunForm':form,
               'Updating':False,
               'StatsTotal':StatTotalTasks,
               'StatsActive':StatActiveTasks,
               'db_updated':db_ctime,
               'bkp_updated':bkp_ctime,
               'sbkp_updated':sbkp_ctime}

    return render(request, 'MyLog.html', context)


def Updating(request, pk):
    print("## Solicited updating")
    UpdatingTask = RunModel.objects.get(id=pk)
    form = RunForm(instance=UpdatingTask)

    print("Taken task instance : (" + str(UpdatingTask.runID) + ") " + str(UpdatingTask.title))

    RunLogsData = RunModel.objects.all()
    RunLogsData = RunLogsData.order_by('-created')

    # log times
    db_ctime = time.ctime(os.path.getctime(db_dir))
    bkp_ctime = time.ctime(os.path.getctime(bkp_dir[:-1][1:]))
    sbkp_ctime = time.ctime(os.path.getctime(str(pathlib.Path.home())+"/"+sbkp_dir.split('/')[-1]))

    if request.method == "POST":
        form = RunForm(request.POST, instance=UpdatingTask)
        print(" >> Taking form to update entry")
        if form.is_valid():
            newsave = form.save(commit=False)
            newsave.lastedited = timezone.now()
            newsave.save()
            print(" >> Updated task instance")
        else:
            print(" >> Error updating")
        return redirect('/')

    # Checking stats
    StatTotalTasks = len([i for i in RunLogsData])
    StatActiveTasks = len([i for i in RunLogsData if i.active])


    context = {'RunLogs':RunLogsData,
               'RunForm':form,
               'Updating':UpdatingTask,
               'StatsTotal':StatTotalTasks,
               'StatsActive':StatActiveTasks,
               'db_updated':db_ctime,
               'bkp_updated':bkp_ctime,
               'sbkp_updated':sbkp_ctime}

    return render(request, 'MyLog.html', context)

def DeleteTask(request, pk):
    print("## Solicited deleting")
    DeletingTask = RunModel.objects.get(id=pk)
    print("Taken task instance : (" + str(UpdatingTask.runID) + ") " + str(UpdatingTask.title))
    form = RunForm(instance=DeletingTask)

    RunLogsData = RunModel.objects.all()
    RunLogsData = RunLogsData.order_by('-created')

    # log times
    db_ctime = time.ctime(os.path.getctime(db_dir))
    bkp_ctime = time.ctime(os.path.getctime(bkp_dir[:-1][1:]))
    sbkp_ctime = time.ctime(os.path.getctime(str(pathlib.Path.home())+"/"+sbkp_dir.split('/')[-1]))

    if request.method == "POST":
        DeletingTask.delete()
        print(" >> Deleted task instance")
        return redirect('/')

    # Checking stats
    StatTotalTasks = len([i for i in RunLogsData])
    StatActiveTasks = len([i for i in RunLogsData if i.active])


    context = {'RunLogs':RunLogsData,
               'RunForm':form,
               'Updating':False,
               'Deleting':DeletingTask,
               'StatsTotal':StatTotalTasks,
               'StatsActive':StatActiveTasks,
               'db_updated':db_ctime,
               'bkp_updated':bkp_ctime,
               'sbkp_updated':sbkp_ctime}

    return render(request, 'MyLog.html', context)

def LocalBackUp(request):
    print("## Backing up (local)")
    os.system('cp ' + "\'" + db_dir + "\' \'" + db_dir + '.bkp' + '\'')
    print(">> copy backup at " + str(db_dir))
    print('cp ' + "\'" + db_dir + "\' " + bkp_dir)

    return redirect('')

def SecureBackUp(request):
    print("## Backing up (home folder)")
    print("copy backup at " + str(db_dir))
    print('cp ' + "\'" + db_dir + "\' " + sbkp_dir)
    os.system('cp ' + "\'" + db_dir + "\' " + sbkp_dir)

    return redirect('')