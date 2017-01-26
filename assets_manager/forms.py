# -*- coding: utf-8 -*-
from django import forms


class FileFieldForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput())

    def clean_file(self):
        file = self.cleaned_data['file']
        # http://stackoverflow.com/questions/4853581/django-get-uploaded-file-type-mimetype#4855340
        # try:
        #     if file:
        #         file_type = file.content_type.split('/')[0]
        #         print file_type

        #         if len(file.name.split('.')) == 1:
        #             raise forms.ValidationError(_('File type is not supported'))

        #         if file_type in settings.TASK_UPLOAD_FILE_TYPES:
        #             if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
        #                 raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
        #         else:
        #             raise forms.ValidationError(_('File type is not supported'))
        # except:
        #     pass

        return file
