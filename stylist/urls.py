from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

from stylist.views import AddItem, MyForecast, MyItems, \
        RemoveItem, SignUpView


urlpatterns = [
    url(r'^$', login, {'template_name': 'stylist/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'stylist:login'}, name='logout'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^my_items/$', login_required(MyItems.as_view()), name='my_items'),
    url(r'^add_item/$', login_required(AddItem.as_view()), name='add_item'),
    url(r'^remove_item/(?P<pk>[0-9]+)/$', login_required(RemoveItem.as_view()),
        name='remove_item'),
    url(r'^forecast/$', login_required(MyForecast.as_view()), name='forecast'),
]
