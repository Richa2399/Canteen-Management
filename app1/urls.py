from django.urls import path
from . import views

from django.contrib.auth import views as v
urlpatterns=[

    path('dashboard',views.indexPage,name='index_canteen'),
    path('food_category/',views.categoryPage,name='food_category'),
    path('food_menu/',views.menuPage,name='food_menu'),
    path('cateory/',views.manage_category,name='manage_category'),
    path('manage_menu/',views.manage_menu,name='manage_menu'),
    path('delCat/<int:pk>',views.cat_del,name='del_cat'),
    path('delmenu/<int:pk>',views.menu_del,name='del_menu'),
    path('editcat/<int:pk>',views.cat_edit,name='edit_cat'),
    path('editmenu/<int:pk>',views.menu_edit,name='edit_menu'),
    path('',views.canteenregisterpage,name='canteenregister'),
    path('canteenlogin/',views.can_login,name='can_login'),
    path('logout/',views.logout_user,name='logout'),
    path('pending_order/',views.pending_order,name='pending_order'),
    path('new_order/',views.new_order,name='new_order'),
    path('completed_order/',views.completed_order,name='completed_order'),
    path('processing_order/',views.processing_order,name='processing_order'),
    path('accept_order/<int:pk>',views.accept_order,name='accept_order'),
    path('cancel_order/<int:pk>',views.cancel_order,name='cancel_order'),
    path('complete_order/<int:pk>',views.complete_order,name='complete_order'),
    path('completed_order/<int:pk>',views.completed_order,name='completed_order'),
    path('quality/',views.quality,name='quality'),
    path('add_ingredient/<int:id>',views.add_ingredient,name='add_ingredient'),
    path('sale_report/',views.sale_report,name='sale_report'),
    path('can_account/',views.can_account,name='can_account'),

    path('change_pass_can/',v.PasswordChangeView.as_view(template_name='app1/change_pass_can.html'),name='change_pass_can'),
 
    path('can_pass_done/', v.PasswordChangeDoneView.as_view(template_name='app1/can_pass_done.html'),name='can_pass_done'),

    #path('add_ingredient/<int:id>',views.add_ingredient,name='add_ingredient')


    

    
    
    
    
    ]