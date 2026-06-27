from django.shortcuts import render, redirect
from django.conf import settings
# from django.http import JsonResponse
from .models import ExcelFileInfo
import os, shutil


def get_excel_files_list(request):
    files = ExcelFileInfo.objects.all()
    all_files = files.count()
    saved_files = all_files - files.filter(is_contracts_saved=False, is_prices_saved=False).count()
    not_saved_files = all_files - saved_files
    context={
        'files': files,
        'all_files': all_files,
        'saved_files':saved_files,
        'not_saved_files':not_saved_files
    }
    return render(request, "file_tracker/list.html", context=context)


def delete_excel_file(request, directory, name):
    file_path = os.path.join(settings.BASE_DIR,
            "excel_files",
            directory,
            name
    )

    file = ExcelFileInfo.objects.get(directory=directory, name=name).delete()
    return redirect("file_tracker:file_list")


def delete_all_excel_files(request):
    # delete all excel file objects in database
    ExcelFileInfo.objects.all().delete()

    # delete all actual excel files
    excel_files_path = os.path.join(settings.BASE_DIR, "excel_files")
    for filename in os.listdir(excel_files_path):
        file_path = os.path.join(excel_files_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return redirect("file_tracker:file_list")


def delete_saved_excel_files(request):
    # do it
    return redirect("file_tracker:file_list")


def delete_not_saved_excel_files(request):
    # do it
    return redirect("file_tracker:file_list")