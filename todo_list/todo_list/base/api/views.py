from rest_framework.decorators import api_view,permission_classes
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from base.models import Task,User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login,logout
from .serializers import TaskSerializer
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .permissions import IsArab


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    username = request.data.get('username').strip()
    email = request.data.get('email').strip()
    password1 = request.data.get('password1').strip()
    password2 = request.data.get('password2').strip()

    if password1 != password2:
        return Response({'error':'passwords does not match'})
    
    if User.objects.filter(username=username).exists():
        return Response({'error':'username already exist'},status = status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error':'email already exist'},status= status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username = username,
        email = email,
        password = password1,
    )

    return Response({'message':'user created successfully'},status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getusertasks(request):
    user = request.user
    tasks = user.task_set.all()
    serializer = TaskSerializer(tasks,many=True)
    return Response({"tasks":serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gettask(request,pk):
    task = Task.objects.get(id=pk)
    if task.user == request.user:
        serializer = TaskSerializer(task)
        return Response({"task":serializer.data},status=status.HTTP_200_OK)
    else:
        return Response({"error":"this task isn't yours"},status=status.HTTP_403_FORBIDDEN)


@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def edittask(request,pk):
    task = Task.objects.get(id=pk)
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response({"task":serializer.data},status=status.HTTP_200_OK)
    else:
        title = request.data.get('title')
        description = request.data.get('description')
        task.title = title
        task.description = description
        task.save()
        return Response({"message":"the task was edited successfully"},status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtask(request):
    title = request.data.get('title')
    description = request.data.get('description')
    user = request.user

    try:
        task = Task.objects.create(
            title = title,
            description = description, 
            user = user,
            completed = False
        )
        return Response({"message":"task created"},status=status.HTTP_201_CREATED)

    except:
        return Response({"error":"Error occured try again"},status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletetask(request):
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    task.delete()
    return Response({"message":"Task deleted successfully"},status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def completetask(request):
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return Response({"message":"task is now completed"},status=status.HTTP_200_OK)
