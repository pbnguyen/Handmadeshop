import os
from gluon.contrib.login_methods.rpx_account import RPXAccount
janrain_filename = '/home/www-data/web2py/janrain.txt'
if os.path.exists(janrain_filename):
    auth.settings.actions_disabled=['register','change_password','request_reset_password']
    domain,key=open(janrain_filename,'r').read().strip().split(':')
    auth.settings.login_form = RPXAccount(
        request,
        api_key=key,
        domain=domain,
        url = "http://%s/%s/default/user/login" % (request.env.http_host,request.application))
