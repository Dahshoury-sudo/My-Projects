from base import models
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from .permissions import UnAuthenticated
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from . import serializers

# User
@api_view(['POST'])
@permission_classes([UnAuthenticated])
@transaction.atomic
def register(request):

    try:

        profile_data = request.data.pop('profile')
            
            # 2. Extract password so we can hash it
        password = request.data.pop('password')
            
            # 3. All remaining data in request.data should be for the CustomUser
            # This includes email, first_name, last_name, etc.
        user_data = request.data

            # We MUST use .create_user() to ensure the password is HASHED
        user = models.User.objects.create_user(
                password=password,
                **user_data
            )
            
            # 5. Create the PatientProfile and link it to the user
        models.PatientProfile.objects.create(
                user=user,
                **profile_data
            )

            # 6. Generate tokens for the new user
        refresh = RefreshToken.for_user(user)

            # 7. Prepare the successful response
        response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
                'message': 'User registered successfully.'
            }
            
        return Response(response_data, status=status.HTTP_201_CREATED)

    except IntegrityError:
        # This catches the `unique=True` error on the email field
        return Response(
            {"error": "An account with this email already exists."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except KeyError as e:
        # This catches missing fields (e.g., if "profile" or "password" is missing)
        return Response(
            {"error": f"Missing required field: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # A general catch-all for any other errors
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    id = request.user.id
    return Response({"user_id":id,'is_admin':request.user.is_staff},status=status.HTTP_200_OK)


# Appointment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    
    # The patient is the currently logged-in user
    patient = request.user

    # Security check: Ensure the user is a patient
    if not patient.is_patient:
        return Response(
            {"error": "Only patients can book appointments."}, 
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        # 1. Get data from the request body
        data = request.data
        doctor_id = data['doctor_id']
        reason = data['reason_for_appointment']
        expected_date = data['expected_appointment_date']
        
        # .get() is used for optional fields
        notes = data.get('additional_notes', '') 

        # 2. Validate the Doctor
        try:
            # Check that the ID exists AND the user is a doctor
            doctor = models.User.objects.get(id=doctor_id, is_doctor=True)
        except models.User.DoesNotExist:
            return Response(
                {"error": "The specified doctor does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Create the Appointment
        # The 'status' field will use its default 'Pending' value
        appointment = models.Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            reason_for_appointment=reason,
            expected_appointment_date=expected_date,
            additional_notes=notes
        )

        # 4. Send a success response
        response_data = {
            "message": "Appointment request submitted successfully.",
            "appointment_id": appointment.id,
            "user_id":patient.id,
            "patient": patient.email,
            "doctor": doctor.email,
            "status": appointment.status,
            "expected_date": appointment.expected_appointment_date
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    except KeyError as e:
        # This catches missing required fields in the JSON payload
        return Response(
            {"error": f"Missing required field: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except ValidationError as e:
        # This will catch errors like an invalid date format
         return Response(
            {"error": f"Invalid data: {e}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # A general catch-all for any other errors
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAdminUser]) 
def cancel_appointment(request,pk):
    reason = request.data.get('reason')

    # 2. VALIDATE input
    if not pk:
        return Response(
            {"error": "appointment_id is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3. HANDLE Not Found (404)
    try:
        # We also check for ownership in the 'get' query itself
        appointment = models.Appointment.objects.get(
            id=pk,
                
        )
        
    except models.Appointment.DoesNotExist:
        return Response(
            {"error": "Appointment not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 5. CHECK state
    if appointment.status == 'cancelled':
        return Response(
            {"error": "This appointment is already cancelled."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if appointment.status == 'completed':
         return Response(
            {"error": "Cannot cancel a completed appointment."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # --- Original Logic (now much safer) ---
    try:
        appointment.status = 'cancelled'
        appointment.reason_for_cancellation = reason
        # Only update the fields that changed
        appointment.save(update_fields=['status', 'reason_for_cancellation'])
        
        return Response(
            {'message': "Appointment Cancelled"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        # This will now only catch actual server errors (e.g., database connection)
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['GET'])
@permission_classes([IsAdminUser]) 
def get_all_appointments(request):
    appointments = models.Appointment.objects.all()
    serializer = serializers.Get_Appointments_Serializer(appointments,many=True)
    return Response({"appointments":serializer.data},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_appointments_stat(request):
    pending_appointments_count = models.Appointment.objects.filter(status = "pending").count()
    cancelled_appointments_count = models.Appointment.objects.filter(status = "cancelled").count()
    total = models.Appointment.objects.count()
    data = {"pending_appointments_count":pending_appointments_count,
                    "cancelled_appointments_count":cancelled_appointments_count,
                    "total":total}
    
    return Response(data,status=status.HTTP_200_OK)


@api_view(['GET','PATCH'])
@permission_classes([IsAdminUser]) 
def schedule_appointment(request,pk):
    try:
        appointment = models.Appointment.objects.get(id=pk)
    except models.Appointment.DoesNotExist:
        return Response({"error":"there is no appointment exist with this id"},status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == 'GET':
        doctor = appointment.doctor
        serialzer = serializers.SimpleDoctorSerializer(doctor)
        data = {"reason":appointment.reason_for_appointment,
                "doctor":serialzer.data,
                "expected_appointment_date":appointment.expected_appointment_date,
                "confirmed_appointment_datetime":appointment.confirmed_appointment_datetime}
        
        return Response(data,status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        confirmed_date = request.data.get("confirmed_date")
        if not confirmed_date:
            return Response(
            {"error": "confirmed_date is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
        appointment.confirmed_appointment_datetime = confirmed_date
        appointment.status = "scheduled"
        appointment.save()
        return Response({"message":"date updated"},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_info(request,pk):
    appointment = models.Appointment.objects.get(id=pk)
    serializer = serializers.Get_Appointments_Serializer(appointment)
    return Response({"info":serializer.data},status=status.HTTP_200_OK)

# Doctors
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_doctors(request):
    doctors = models.User.objects.filter(is_doctor = True)
    serializer = serializers.Get_All_Doctors_Serializer(doctors,many=True)
    return Response({"doctors":serializer.data},status=status.HTTP_200_OK)
