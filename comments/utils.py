from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_comment_notification(comment):
    """
    Yangi izoh haqida xabar yuborish
    """
    # Administratorga xabar yuborish
    subject = 'Yangi izoh qoldirildi'
    context = {
        'username': comment.username,
        'email': comment.email,
        'text': comment.text,
        'page_url': comment.page_url,
        'created_at': comment.created_at
    }
    
    html_message = render_to_string('comment_notification_email.html', context)
    plain_message = strip_tags(html_message)
    
    # Administratorga yuborish
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        ['complexprogrammer@mail.ru'],
        html_message=html_message,
        fail_silently=False,
    )
    
    # Foydalanuvchiga tasdiqlash xabarini yuborish
    send_user_comment_confirmation(comment)

def send_reply_notification(reply, parent_comment):
    """
    Izohga yangi javob yozilganda xabar yuborish
    """
    # Asosiy izoh egasiga xabar
    subject = 'Sizning izohingizga javob yozildi'
    context = {
        'username': reply.username,
        'email': reply.email,
        'reply_text': reply.text,
        'original_comment': parent_comment.text,
        'page_url': reply.page_url,
        'created_at': reply.created_at
    }
    
    html_message = render_to_string('reply_notification_email.html', context)
    plain_message = strip_tags(html_message)
      # Asosiy izoh egasiga yuborish
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [parent_comment.email],
        html_message=html_message,
        fail_silently=False,
    )

    
    # Administratorga xabar yuborish
    admin_subject = 'Yangi javob yozildi'
    admin_context = {
        'username': reply.username,
        'email': reply.email,
        'reply_text': reply.text,
        'original_comment': parent_comment.text,
        'original_author': parent_comment.username,
        'page_url': reply.page_url,
        'created_at': reply.created_at
    }
    
    admin_html_message = render_to_string('admin_reply_notification_email.html', admin_context)
    admin_plain_message = strip_tags(admin_html_message)
    
    send_mail(
        admin_subject,
        admin_plain_message,
        settings.DEFAULT_FROM_EMAIL,
        ['complexprogrammer@mail.ru'],
        html_message=admin_html_message,
        fail_silently=False,
    )
    
    # Javob yozgan foydalanuvchiga tasdiqlash xabarini yuborish
    send_user_reply_confirmation(reply, parent_comment)

def send_user_comment_confirmation(comment):
    """
    Foydalanuvchiga o'z izohi qabul qilingani haqida xabar yuborish
    """
    subject = 'Izohingiz muvaffaqiyatli qabul qilindi'
    context = {
        'username': comment.username,
        'text': comment.text,
        'page_url': comment.page_url,
        'created_at': comment.created_at
    }
    
    html_message = render_to_string('user_comment_confirmation_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [comment.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_user_reply_confirmation(reply, parent_comment):
    """
    Foydalanuvchiga o'z javobi qabul qilingani haqida xabar yuborish
    """
    subject = 'Javobingiz muvaffaqiyatli qabul qilindi'
    context = {
        'username': reply.username,
        'reply_text': reply.text,
        'original_comment': parent_comment.text,
        'original_author': parent_comment.username,
        'page_url': reply.page_url,
        'created_at': reply.created_at
    }
    
    html_message = render_to_string('user_reply_confirmation_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [reply.email],
        html_message=html_message,
        fail_silently=False,
    )
