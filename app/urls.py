from django.urls import path
from . import views
from django.contrib.auth import views as v

urlpatterns=[

    path('',views.indexPage,name='index'),
    path('register/',views.registerPage,name='register'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('menu/',views.menu,name='menu'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('add/<int:pk>',views.add_cart,name='add_cart'),
    path('del/<int:pk>',views.delete_cart,name='del'),
    path('plus/<int:pk>',views.plus_item,name='plus'),
    path('minus/<int:pk>',views.minus_item,name='minus'),
    path('my_account',views.my_account,name='my_account'),
    path('fil_category/<int:cat>/<int:canteen>',views.fil_category,name='fil_category'),
    path('my_order/',views.my_order,name='my_order'),

#for password change and reset purpose
    path('password-chang/',v.PasswordChangeView.as_view(template_name='app/password_change.html'),name='change_password'),
 
    path('password-change-done/', v.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'),name='password_change_done'),

    path('password-reset/', v.PasswordResetView.as_view(template_name='app/password_reset.html', email_template_name='app/password_reset_email.html',subject_template_name='app/password_reset_email_subject.txt'),name='password_reset'),
    path('password-reset-done/', v.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', v.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', v.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('details/<int:pk>',views.ingredients,name='ingredients'),
    path('add_rating',views.add_rating,name='add_rating'),
    path('home_search',views.home_search,name='home_search'),
    path('about_us',views.about_us,name='about_us'),
    path('back',views.back,name='back'),
    path('edit_profile/',views.edit_profile,name='user_edit'),

    #payment
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    
    ]