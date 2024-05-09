from django.shortcuts import render
from django.http import HttpResponseRedirect;
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import ExamName,Start_exam_user
from users.models import UsersConfig
from datetime import datetime
from pytz import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse;
def exam_list(request):
    request.session['userid'];
    if request.session['useremail'] != "":
        exams = ExamName.objects.all()
        return render(request, 'exam_list.html', {'exams': exams})
    else:
        return HttpResponseRedirect('/login')

def exam_details(request,id):
    exam = ExamName.objects.filter(id=id).values()
    if(exam[0]!=""):
        exam_1 = ExamName.objects.get(id=id)
        question_ids = exam_1.questions.values_list('id', flat=True)
        questions_queryset = exam_1.questions.all()
        return render(request, 'exam_detail.html',{"user_email":request.session['useremail'],'questions_queryset':questions_queryset,'exam':exam[0],'id':id})
    else:
        return HttpResponseRedirect('/login')


def views_exam_details(request,id):
    if request.session['useremail'] != "":
        exam_qs = ExamName.objects.filter(id=id)
        if exam_qs.exists():
            exam = exam_qs.values()
            duration=0
            remaining_time=0
            if len(exam)!=0:
                exam1 = exam[0]
                remaining_time=exam1['duration']
                exam_1 = ExamName.objects.get(id=id)
                question_ids = exam_1.questions.values_list('id', flat=True)
                questions_queryset = exam_1.questions.all()
                question_data = questions_queryset[0]
                num_questions = questions_queryset.count()
                exam_instances = Start_exam_user.objects.filter(exam=id)
                examidouser = ""
                ist_time = None
                for instance in exam_instances:
                    examidouser = instance.id
                    ist_time = instance.timestamp.astimezone(timezone('Asia/Kolkata'))
                if(examidouser==""):
                    user =UsersConfig.objects.get(id=request.session['userid']);
                    start_examUser = Start_exam_user(
                        user=user,
                        exam=exam_1,
                        timestamp=datetime.now(timezone('Asia/Kolkata'))
                    )
                    start_examUser.save()
                    messages.success(request, "Exam Started...")
                else:
                    dt = ist_time.replace(second=0, microsecond=0)
                    end_time = dt + timedelta(minutes=remaining_time)
                    current_time = datetime.now(timezone('Asia/Kolkata'))
                    remaining_time = end_time - current_time
                    remaining_time = int(remaining_time.total_seconds() //60)
        else:
            messages.success(request, "Handle non-existent exam query gracefully with custom error message.")
    else:
        messages.success(request, "Handle non-existent exam query gracefully with custom error message.")
        return HttpResponseRedirect('/login')

    return render(request, 'start_exam.html',{"user_email":request.session['useremail'],'question_data':question_data,'exam':exam[0],"num_questions":num_questions,"remaining_time":remaining_time})

def startexam(request):
    return render(request, 'start_exam.html')

def get_next_question(request):
    if request.session['useremail'] != "":
        id = request.POST.get('id')
        exam_qs = ExamName.objects.filter(id=id)
        if exam_qs.exists():
            exam = exam_qs.first()  # Use first() instead of values()
            remaining_time = exam.duration
            
            # Get questions for the exam
            question_ids = exam.questions.values_list('id', flat=True)
            questions_queryset = exam.questions.all()
            
            # Paginate the questions
            page_number = request.POST.get('page', 1)  # Default page is 1
            paginator = Paginator(questions_queryset, 1)  # Change 1 to the desired number of questions per page
            
            try:
                page = paginator.page(page_number)
            except EmptyPage:
                # Handle the case when the page number is out of range
                return HttpResponse("Page not found")
            
            # Now you can access questions for the current page
            current_questions = page.object_list
            
            # Do something with current_questions
            
            # Example: Prepare data to send as JSON
            data = {
                'remaining_time': remaining_time,
                'current_questions': current_questions,
                'total_questions': paginator.count,
            }
            return HttpResponse(data, content_type='application/json')
    
    # Handle the case when the session useremail is not set
    return HttpResponse('Unauthorized', status=401)

