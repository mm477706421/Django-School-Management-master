import csv, io
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from academics.views import user_is_staff
from academics.models import Semester
from students.models import Student,StudentBase
from result.models import Result, StudentInfo


@user_passes_test(user_is_staff)
def show_result_by_semester(request, student_id, semester):
    student = Student.objects.get(pk=student_id)
    semester = Semester.objects.get(number=semester)
    results = Result.objects.filter(student_id=student_id,
                                    semester=semester)
    context = {'results': results, 'student': student}
    return render(request, 'students/result_in_detail.html', context)



@user_passes_test(user_is_staff)
def upload_subjects_csv(request):
    if request.user.has_perm('create_stuff'):
        template = 'result/add_subject_csv.html'
        prompt = {
            'order': '学生姓名, 学生学号，学生专业'
        }
        if request.method == 'GET':
            return render(request, template, prompt)
        
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, '请上传CSV格式的文件')
        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            # TODO: upload data for foreignkey also, and
            # create object for foreignkey if no data found.
            for column in csv.reader(io_string, delimiter=',', quotechar='|'):
                _, created = Student.objects.update_or_create(
                    name=column[0],
                    registration_number=column[1],
                    department=column[2],
                )
        except:
            pass
        context = {}
        return render(request, template, context)
    else:
        return render(request, 'admin_tools/permission_required.html')
