from django.shortcuts import render
import os
import json
from django.core.paginator import Paginator
from django.http import HttpResponse

def load_students():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'student.json')
    with open(file_path, 'r') as file:
        return json.load(file)

def load_student_page(page_number, page_size):
    students_data = load_students()
    paginator = Paginator(students_data, page_size)
    students_page = paginator.page(page_number)
    return students_page

def get_students(request):
    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('size', 5))

    students_page = load_student_page(page_number, page_size)

    context = {
        'students': students_page,
        'paginator': students_page.paginator,
        'current_page': page_number,
    }

    return render(request, 'students.html', context)

def filter_students(request):
    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('size', 5))
    name_filter = request.GET.get('name')
    min_marks_filter = request.GET.get('min_marks')
    max_marks_filter = request.GET.get('max_marks')

    students_page = load_student_page(page_number, page_size)

    filtered_students = students_page.object_list
    if name_filter:
        filtered_students = [s for s in filtered_students if name_filter.lower() in s['name'].lower()]
    if min_marks_filter:
        filtered_students = [s for s in filtered_students if s['total_marks'] >= int(min_marks_filter)]
    if max_marks_filter:
        filtered_students = [s for s in filtered_students if s['total_marks'] <= int(max_marks_filter)]

    paginator = Paginator(filtered_students, page_size)
    students_page = paginator.page(page_number)

    context = {
        'students': students_page,
        'paginator': students_page.paginator,
        'current_page': page_number,
    }

    return render(request, 'filtered_students.html', context)


    
