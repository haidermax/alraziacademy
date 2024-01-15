from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from accounts.models import UserProfile
from course.models import *
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET
def dept(request,dept):
    thedept=thedept = get_object_or_404(Speciality, sp_name__icontains=dept)
    grades=Grade.objects.filter(speciality=thedept)
    depts= Speciality.objects.all()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    else:
        user_profile=None
    user = request.user
    context={'user':user,'profile':user_profile, 'dept':depts,'grade':grades}

    return render(request,"grades.html",context)

def grade(request,grade,dept):
    subj = Subject.objects.filter(grade__grade=grade)
    depts= dept
    gr=grade

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    else:
        user_profile=None
    user = request.user
    context={'user':user,'profile':user_profile, 'dept':depts,'sub':subj,'grade':gr}
    return render(request,"subjects.html",context)

def subject(request, grade, subject):
    user = request.user
    depts= Speciality.objects.all()
    subject = Subject.objects.get(pk=subject)
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        
        if subject.paid :
            if subject.members.filter(pk=user.pk).exists() or request.user.is_staff:
                lectures = Lecture.objects.filter(Subject_id=subject)
                return render(request, 'lectures.html', {'subject': subject, 'lecture': lectures})
            else:

                return render(request, 'pay.html', {'subject': subject})                                       #edit to subscribe menu
                messages.error(request, 'This subject requires payment.')
            return render(request, 'lectures.html', {'subject': subject})
        else:
            if subject.members.filter(pk=user.pk).exists():
                lectures = Lecture.objects.filter(Subject_id=subject)
                return render(request, 'lectures.html', {'subject': subject, 'lecture': lectures})
            else:
                subject.members.add(user)

                lectures = Lecture.objects.filter(Subject_id=subject)
                messages.success(request, 'you enrolled in this subject')
                return render(request, 'lectures.html', {'subject': subject, 'lectures': lectures})
    else:

        messages.success(request, 'you must login to see the lectures')
        user_profile=None
        context={'user':user,'profile':user_profile, 'dept':depts,'grade':grade,'sub':subject}
        return render(request, 'lectures.html',context)
    
def lecture(request,lecture):
    if request.user.is_authenticated:
        lect=Lecture.objects.get(pk=lecture)
        if lect.Subject.members.filter(pk=request.user.pk).exists() or request.user.is_staff:
            return render(request,'video.html',{'lect':lect})
        else:
            return redirect('index')
    else:
        return redirect('index')
    

def mycourses(request):
    if request.user.is_authenticated:
        user = request.user
        courses = Subject.objects.filter(members=user)
        return render(request, 'mycourses.html', {'courses': courses})
    else:
        return redirect('index')
    

@staff_member_required(login_url='index')
def create_speciality(request):
    if request.method == 'POST':
        sp_name = request.POST.get('sp_name')
        N_of_grades = request.POST.get('N_of_grades')
        speciality = Speciality(sp_name=sp_name, N_of_grades=N_of_grades)
        speciality.save()
        return redirect('index')
    
    return render(request, 'create_speciality.html')

@staff_member_required(login_url='index')
def create_subject(request):
    if request.method == 'POST':
        grade_id = request.POST.get('grade')
        subject_name = request.POST.get('subject')
        paid = 'paid' in request.POST
        if paid==False:
            price=0
        else:
            price = request.POST.get('price')
        if not subject_name:  # Check if subject name is empty
            message = 'Subject name is required.'
            grades = Grade.objects.all()
            return render(request, 'create_subject.html', {'grades': grades, 'message': message})

        grade = Grade.objects.get(id=grade_id)
        subject = Subject(grade=grade, subject=subject_name, paid=paid, price=price)
        subject.save()
        grades = Grade.objects.all()
        message = 'Subject created sucessfuly.'
        return render(request, 'create_subject.html', {'grades': grades, 'message': message})

    else:
        grades = Grade.objects.all()
        return render(request, 'create_subject.html', {'grades': grades})
    
@staff_member_required(login_url='index')
def create_lecture(request):
    depts = Speciality.objects.all()
    grades = Grade.objects.all()
    subjects = Subject.objects.all()
    message = None  # Initialize message variable

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')
        drive = request.POST.get('drive')
        quiz = request.POST.get('quiz')
        subject = get_object_or_404(Subject, pk=subject_id)
        lecture = Lecture(Subject=subject, title=title, description=description, attachment=attachment, drive=drive, quiz=quiz)
        lecture.save()

        message = 'Lecture created successfully.'  # Set the message
        context = {'depts': depts, 'grades': grades, 'subjects': subjects, 'message': message}
        return render(request, 'create_lecture.html', context)

    context = {'depts': depts, 'grades': grades, 'subjects': subjects, 'message': message}
    return render(request, 'create_lecture.html', context)

@staff_member_required(login_url='index')
def subject_members(request):
    depts = Speciality.objects.all()
    grades = Grade.objects.all()
    subjects = Subject.objects.all()
    specialities = Speciality.objects.prefetch_related('grades__subjects').all()
    context = {
        'depts': depts,
        'grades': grades,
        'subjects': subjects,
        'specialities': specialities
    }
    return render(request, 'subscribe.html', context)

def get_members_table(request):
    subject_id = request.GET.get('subject_id')
    subject = Subject.objects.filter(pk=subject_id).prefetch_related('members').first()

    if subject:
        members = subject.members.all()
        members_table = '<table class="table table-success table-bordered"><thead><tr class="table-dark"><th>Name</th><th>Username</th><th>Actions</th></tr></thead><tbody>'

        for member in members:
            members_table += f'<tr><td>{member.first_name} {member.last_name}</td><td>{member.username}</td><td><button class="btn btn-danger btn-sm removeMemberButton" data-member-id="{member.id}" data-member-name="{member.username}">Remove</button></td></tr>'

        members_table += '</tbody></table>'
    else:
        members_table = ''

    return JsonResponse({'members_table': members_table})

@staff_member_required(login_url='index')
def add_member(request):
    message=''
    if request.method == 'POST':
        member_name = request.POST.get('member_name')
        subject_id = request.POST.get('subject_id')
        
        # Perform any additional validation or processing as needed
        
        subject = Subject.objects.filter(pk=subject_id).first()
        user = User.objects.filter(username=member_name).first()
        
        if not user:
            message = 'User does not exist.'
            success = False
        elif user in subject.members.all():
            message = 'User is already a member.'
            success = False
        else:
            subject.members.add(user)
            message = 'Member added successfully.'
            success = True
        
    
    return JsonResponse({'message': message})

@staff_member_required(login_url='index')
def remove_member(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        subject_id = request.POST.get('subject_id')

        subject = get_object_or_404(Subject, pk=subject_id)
        user = get_object_or_404(User, pk=member_id)

        if user in subject.members.all():
            subject.members.remove(user)
            message = 'Member removed successfully.'
        else:
            message = 'Member is not a member of this subject.'

        return JsonResponse({'message': message})

    return JsonResponse({'message': 'Invalid request.'})


@staff_member_required(login_url='index')
def user_management(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users.html', context)

@staff_member_required(login_url='index')
def search_users(request):
    search_query = request.GET.get('search_query')
    users = User.objects.filter(username__icontains=search_query)
    context = {'users': users}
    return render(request, 'user_table.html', context)




@staff_member_required(login_url='index')
def subject_management(request):
    grade_id = request.GET.get('grade_id')
    search_query = request.GET.get('search_query', '')

    subjects = Subject.objects.filter(grade_id=grade_id, subject__icontains=search_query)
    grades = Grade.objects.all()

    context = {
        'subjects': subjects,
        'grades': grades,
        'grade_id': grade_id,
        'search_query': search_query,
    }

    return render(request, 'subject_management.html', context)

@staff_member_required(login_url='index')
def get_subject_details(request):
    subject_id = request.GET.get('subject_id')
    subject = get_object_or_404(Subject, id=subject_id)

    # Prepare subject details
    subject_details = {
        'subject': subject.subject,
        'paid': subject.paid,
        'price': subject.price,
    }

    return JsonResponse({'subject_details': subject_details})

@staff_member_required(login_url='index')
def remove_subject(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)

        # Delete the subject
        subject.delete()

        return JsonResponse({'message': 'Subject has been removed.'})

@staff_member_required(login_url='index')
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    grades = Grade.objects.all()  # Retrieve all grades for the dropdown

    if request.method == 'POST':
        grade_id = int(request.POST['grade'])
        subject.subject = request.POST['subject']
        subject.paid = bool(request.POST.get('paid', False))
        subject.price = int(request.POST.get('price', 0))

        if grade_id != subject.grade_id:
            grade = get_object_or_404(Grade, id=grade_id)
            subject.grade = grade
        
        subject.save()
        return redirect('subject_management')  # Redirect to subject management page after saving
    
    context = {
        'grades': grades,
        'subject': subject,
    }
    return render(request, 'edit_subject.html', context)

@staff_member_required(login_url='index')
def lecture_management(request):
    depts = Speciality.objects.all()
    grades = Grade.objects.all()
    subjects = Subject.objects.all()

    selected_subject_id = request.GET.get('subject_id')
    lectures = None

    if selected_subject_id:
        lectures = Lecture.objects.filter(Subject_id=selected_subject_id)

    context = {
        'depts': depts,
        'grades': grades,
        'subjects': subjects,
        'selected_subject_id': selected_subject_id,
        'lectures': lectures
    }

    return render(request, 'lecture_management.html', context)

@require_GET
@staff_member_required(login_url='index')
def lecture_search(request):
    search_query = request.GET.get('search_query')
    selected_subject_id = request.GET.get('subject_id')

    if selected_subject_id:
        lectures = Lecture.objects.filter(Subject_id=selected_subject_id)
    else:
        lectures = Lecture.objects.all()

    if search_query:
        lectures = lectures.filter(title__icontains=search_query)

    context = {
        'lectures': lectures
    }

    # Render the lecture table template and return it as JSON response
    lecture_table_html = render_to_string('lecture_table.html', context)
    return JsonResponse({'lecture_table_html': lecture_table_html})

@require_GET
@staff_member_required(login_url='index')
def lecture_subject(request):
    subject_id = request.GET.get('subject_id')

    if subject_id:
        lectures = Lecture.objects.filter(Subject_id=subject_id)
    else:
        lectures = Lecture.objects.all()

    context = {
        'lectures': lectures
    }

    # Render the lecture table template and return it as JSON response
    lecture_table_html = render_to_string('lecture_table.html', context)
    return JsonResponse({'lecture_table_html': lecture_table_html})

@staff_member_required(login_url='index')
def edit_lecture(request, lecture_id):
    subjects = Subject.objects.all()
    depts = Speciality.objects.all()
    grades = Grade.objects.all()

    lecture = get_object_or_404(Lecture, pk=lecture_id)

    if request.method == 'POST':
        subject_id = request.POST['subject']
        title = request.POST['title']
        description = request.POST['description']
        attachment = request.FILES.get('attachment')
        drive = request.POST['drive']
        quiz = request.POST['quiz']

        subject = get_object_or_404(Subject, pk=subject_id)

        lecture.Subject = subject
        lecture.title = title
        lecture.description = description
        lecture.drive = drive
        lecture.quiz = quiz

        if attachment:
            lecture.attachment = attachment

        lecture.save()
        return redirect('lecture_management')

    context = {
        'subjects': subjects,
        'depts': depts,
        'grades': grades,
        'lecture': lecture
    }

    return render(request, 'edit_lecture.html', context)

@staff_member_required(login_url='index')
def remove_lecture(request):
    if request.method == 'POST':
        lecture_id = request.POST['lecture_id']
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        lecture.delete()
        message = 'Lecture Deleted Successfuly'
    return JsonResponse({'message': message})