# user_operation/adminx.py


import xadmin
from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavAdmin(object):
    list_display = ['user', 'goods', "add_time"]
    model_icon = 'fa-heart-o'


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', "message", "add_time"]
    model_icon = 'fa-heart-o'


class UserAddressAdmin(object):
    list_display = ["signer_name", "signer_mobile", "district", "address"]
    model_icon = 'fa-heart-o'


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
