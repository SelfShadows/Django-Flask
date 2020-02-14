import os
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyXadmin.settings')
    import django
    django.setup()

    from app01 import models
    from django.urls import reverse

    ret = models.Book._meta.get_field("publisher")
    from django.db.models.fields.related import ForeignKey
    from django.db.models.fields.related import ManyToManyField

    print('ret=', ret.remote_field.model.objects.all())

    print(isinstance(ret, ManyToManyField) or isinstance(ret, ForeignKey))