from web_honeypot.models import HoneypotSetting, MovementLog


def log_previous_page(request):
    if HoneypotSetting.objects.first().log_previous_page is True:
        previous_page = request.META.get('HTTP_REFERER')
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            ip_address = user_ip.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        if previous_page:
            instance = MovementLog.objects.create(
                session_key=request.session.session_key,
                ip_address=ip_address.split(':')[0],
                user_agent=request.META.get('HTTP_USER_AGENT'),
                path=request.get_full_path(),
                previous_page=previous_page
            )
        else:
            instance = MovementLog.objects.create(
                session_key=request.session.session_key,
                ip_address=ip_address.split(':')[0],
                user_agent=request.META.get('HTTP_USER_AGENT'),
                path=request.get_full_path(),
                previous_page="EXTERNAL"
            )
    else:
        return
