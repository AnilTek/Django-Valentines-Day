from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/',views.home, name='home'),
    path('pref/',views.pref, name='pref'),
    path('get_gold/', views.get_gold, name='get_gold'),



    # Gamble
    path('gamble/',views.gamble,name='gamble'),
    path('baccarat/', views.baccarat, name='baccarat'),
    path('rps/',views.rps,name='rps'),
    path('slot/',views.slot,name='slot'),



    path('decide_for_me/',views.decide_for_me,name='decide_for_me'),
    path('product/', views.product, name='product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('new_product/', views.new_product, name='new_product'), 




    # Help
    path('help/', views.help, name='help'),
    path('money_req/', views.money_req, name='money_req'),


    # Secret
    path('secret_entrance/', views.secret_entrance, name='secret_entrance'),
    path('galeri/', views.gallery_view, name='galeri'),
    path('upload/', views.upload, name='upload'),

    # Store
    path('store/', views.store, name='store'),
    path('purchase_completed/', views.purchase_completed, name='purchase_completed'),

    # Quiz
    path('quiz_menu/', views.quiz_menu, name='quiz_menu'),
    path('quiz/<int:id>/', views.quiz, name='quiz'),
    path('result/<int:prize>/<int:how_many_correct>/', views.result, name='result'), 








]
