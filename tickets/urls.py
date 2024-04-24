from django.urls import path,include
from  . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests',views.viewsets_guests)
router.register('movies',views.viewsets_movie)
router.register('res',views.viewsets_res)


app_name = 'tickets'

urlpatterns = [
    path('rest/fbvlist',views.FBV_List),
    
    
    path('rest/fbvlist/<int:pk>',views.FBV_pk),
    
    
    ##Class Based View
    path('rest/cbv',views.CBV_List.as_view()),
    path('rest/cbv/<int:pk>',views.CBV_pk.as_view()),
    
    
    # Mixnis
    path('rest/mixins',views.Mixins_list.as_view()),
    path('rest/mixins/<int:pk>',views.Mixins_pk.as_view()),
    
    
    
    ##Generics
    path('rest/generics',views.Generics_list.as_view()),
    path('rest/generics/<int:pk>',views.Generics_pk.as_view()),
    
    ##viewsets
    path('rest/viewsets/',include(router.urls)),
    
    
    ## Find Movie
    path('rest/findmovie/',views.find_movie),
    
    ## New Reservation
    path('rest/newreservation/',views.new_res),
    
    ## Post pk Generics 
    path('generics/post',views.Post_list.as_view()),
    path('generics/post/<int:pk>',views.Post_pk.as_view()),
    
    
    
    
]
