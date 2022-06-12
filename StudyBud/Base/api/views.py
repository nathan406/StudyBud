from rest_framework.decorators import api_view
from rest_framework.response import Response
from Base.models import Room
from .serializers import Roomserializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        "GET/api",
        'GET/api/rooms',
        'GET/api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serialize = Roomserializer(rooms,many=True)
    return Response(serialize.data)

@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serialize = Roomserializer(room,many=False)
    return Response(serialize.data)