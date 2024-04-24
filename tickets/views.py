from django.shortcuts import render
from . models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics , viewsets
from rest_framework import filters
from rest_framework.generics import mixins
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import *
# Create your views here.


## List ==> GET   ---
## Create ==> POST
## pk Query ==> GET
## Update ==> PUT
## Delete,Destroy ==> DELETE


## Functions Based View
## GET , POST
@api_view(['GET','POST'])
def FBV_List(request):
    if request.method=='GET':
        guests = Guest.objects.all()
        serializer  =  GuestSerializer(guests,many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)        

# GET , PUT , DELETE
@api_view(['GET' , 'PUT' , 'DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method=='GET':
        serializer  =  GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        


## Class Based View 
class CBV_List(APIView):
    
    
    def get(self,request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many = True)
        return Response(serializer.data)
    
    def post(self,request ):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
class CBV_pk(APIView):    
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self,request , pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self,request,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    
    
## Mixins 
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
class Mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
        
    def get(self,request,pk):
        return self.retrieve(request)
    def post(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)
   



## Generics
class Generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer     
    authentication_classes =[TokenAuthentication]  
    permission_classes = [IsAuthorOrReadOnly]
    
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer  
    authentication_classes =[TokenAuthentication]  
    # permission_classes = [IsAuthenticated]
    
    
    
## Viewsets
class viewsets_guests(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer  
    
    
    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']
    
    
    
class viewsets_res(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    
## Find Movie
@api_view(["GET"])
def find_movie(request):
    movie = Movie.objects.filter(
        name = request.data['name_movie'],

    )
    serializer = MovieSerializer(movie,many = True)
    return Response(serializer.data)



# Create new Reservations
  
@api_view(["POST"])
def new_res(request):
    try:
        movie = Movie.objects.get(name_movie__iexact=request.data.get('name_movie'))
        guest = Guest.objects.create(name=request.data['name'], mobile=request.data['mobile'])
        guest.save()
        res = Reservation.objects.create(guest=guest, movie=movie)
        res.save()
        serializer_data = {
            'guest': guest.name,
            'movie': movie.name_movie,
            'Hall':movie.hall,
        }
        print(res)
        serializer = ReservationSerializer(data= request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    
    
    
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer  
    # authentication_classes = [TokenAuthentication]    
    
    
    
class Post_list(generics.ListCreateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    # authentication_classes = [TokenAuthentication]    
    serializer_class = PostSerializer  