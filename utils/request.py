def extract_request_ip(request):
    # copied from django_ratchet.middleware.py
    # some common things passed by load balancers... will need more of these.
    forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        forwarded_ips = forwarded_for.split(',')
        # take the last one in the list
        return forwarded_for.split(',')[-1].strip()
    real_ip = request.environ.get('HTTP_X_REAL_IP')
    if real_ip:
        return real_ip
    return request.environ['REMOTE_ADDR']
