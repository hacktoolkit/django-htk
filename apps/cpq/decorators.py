from django.contrib.admin.views.decorators import staff_member_required

def cpq_admin_required(*args, **kwargs):
    return staff_member_required(*args, **kwargs)
