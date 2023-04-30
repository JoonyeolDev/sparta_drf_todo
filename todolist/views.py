from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from todolist.models import Todolist
from todolist.serializers import TodolistSerializer,TodolistCreateSerializer


class TodolistView(APIView):
    def get(self,request):
        todolist = Todolist.objects.all()
        serializer = TodolistSerializer(todolist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TodolistCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TodolistDetailView(APIView):
    def get(self,request,todolist_id):
        todolist = get_object_or_404(Todolist, id=todolist_id)
        serializer = TodolistSerializer(todolist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request, todolist_id):
        todolist = get_object_or_404(Todolist, id = todolist_id)
        print(request.user,todolist.user)
        if request.user == todolist.user:
            todolist.is_complete = not todolist.is_complete
            todolist.save()
            return Response(f"todo 완료 여부를 {todolist.is_complete}로 변경했습니다", status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

    def put(self,request,todolist_id):
        todolist = get_object_or_404(Todolist, id=todolist_id)
        if request.user == todolist.user:
            serializer = TodolistSerializer(todolist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

    def delete(self,request,todolist_id):
        todolist = get_object_or_404(Todolist, id=todolist_id)
        if request.user == todolist.user:
            todolist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
