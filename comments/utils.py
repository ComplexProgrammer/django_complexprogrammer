from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import os
from datetime import datetime
from django.core.mail import get_connection, EmailMessage

def send_mail_with_timeout(subject, message, from_email, recipient_list, html_message=None):
    try:
        connection = get_connection(timeout=30)  # 30 sekundlik timeout
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            connection=connection,
        )
        if html_message:
            email.content_subtype = "html"
            email.body = html_message
        
        email.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f'Email yuborishda xatolik: {str(e)}')
        return False
# Logging ni sozlash
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log fayl sozlamalari
log_dir = os.path.join(settings.BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'mail.log')

# Handler yaratish
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Format yaratish
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Handler ni logger ga qo'shish
logger.addHandler(file_handler)
import logging
import os
from datetime import datetime

# Logging ni sozlash
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log fayl sozlamalari
log_dir = os.path.join(settings.BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'mail.log')

# Handler yaratish
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Format yaratish
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Handler ni logger ga qo'shish
logger.addHandler(file_handler)

def send_comment_notification(comment):
    """
    Yangi izoh haqida xabar yuborish
    """
    try:
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
        # send_mail funksiyasi o'rniga send_mail_with_timeout ni ishlatamiz
        success = send_mail_with_timeout(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            ['complexprogrammer@mail.ru'],
            html_message=html_message,
        )

        if not success:
            logger.error(f'Xabar yuborilmadi: {comment.username}')
        
        # Foydalanuvchiga tasdiqlash xabarini yuborish
        try:
            send_user_comment_confirmation(comment)
        except Exception as e:
            logger.error(f'Foydalanuvchi xabarini yuborishda xatolik: {str(e)}, Foydalanuvchi: {comment.username}')
            
    except Exception as e:
        logger.error(f'Admin xabarini yuborishda xatolik: {str(e)}, Foydalanuvchi: {comment.username}')

def send_reply_notification(reply, parent_comment):
    """
    Izohga yangi javob yozilganda xabar yuborish
    """
    try:
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
        logger.info(f'Javob xabari yuborildi: {parent_comment.username}ga, {reply.username}dan')

        # Administratorga xabar yuborish
        try:
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
            logger.info(f'Admin xabari yuborildi: {reply.username}dan yangi javob')
        except Exception as e:
            logger.error(f'Admin xabarini yuborishda xatolik: {str(e)}, Javob beruvchi: {reply.username}')

        # Javob yozgan foydalanuvchiga tasdiqlash xabari
        try:
            send_user_reply_confirmation(reply, parent_comment)
            logger.info(f'Javob beruvchi xabari yuborildi: {reply.username}')
        except Exception as e:
            logger.error(f'Javob beruvchi xabarini yuborishda xatolik: {str(e)}, Foydalanuvchi: {reply.username}')
            
    except Exception as e:
        logger.error(f'Asosiy xabarni yuborishda xatolik: {str(e)}, Javob: {reply.username} -> {parent_comment.username}')

def send_user_comment_confirmation(comment):
    """
    Foydalanuvchiga o'z izohi qabul qilingani haqida xabar yuborish
    """
    try:
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
        logger.info(f'Izoh tasdiqlash xabari yuborildi: {comment.username}')
    except Exception as e:
        logger.error(f'Izoh tasdiqlash xabarini yuborishda xatolik: {str(e)}, Foydalanuvchi: {comment.username}')

def send_user_reply_confirmation(reply, parent_comment):
    """
    Foydalanuvchiga o'z javobi qabul qilingani haqida xabar yuborish
    """
    try:
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
        logger.info(f'Javob tasdiqlash xabari yuborildi: {reply.username}')
    except Exception as e:
        logger.error(f'Javob tasdiqlash xabarini yuborishda xatolik: {str(e)}, Foydalanuvchi: {reply.username}')
