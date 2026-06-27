from django.db import models
from django.conf import settings
import os

EXCEL_FILES_PATH = os.path.join(settings.BASE_DIR, "excel_files")

class ExcelFileInfo(models.Model):
    directory = models.CharField(max_length=8)
    name = models.CharField(max_length=11)   # name with extension
    is_contracts_saved = models.BooleanField(default=False)
    is_prices_saved = models.BooleanField(default=False)

    # overriding delete() method to delete actual excel file after deleting its object
    def delete(self, **kwargs):
        super().delete(**kwargs)

        # deleting the actual excel file
        file_path = os.path.join(EXCEL_FILES_PATH, self.directory, self.name)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                msg = ("An error occurred while deleting the file <%s> ==> because: %s" % (file_path, e))
                print(msg)
        # deleting the main directory of file if it is empty
        if(not os.listdir(os.path.dirname(file_path))):
            os.rmdir(os.path.dirname(file_path))


    def __str__(self):
        return os.path.join("excel_files", self.directory, self.name)
    
    class Meta:
        unique_together = ('directory', 'name')
        ordering = ["-directory", "-name"]