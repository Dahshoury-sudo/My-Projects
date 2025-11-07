from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    specialty_choices=[
        ("heart","Heart"),
        ("skin","Skin"),
        ("children","Children"),
        ("bones_and_joints","Bones and Joints"),
        ("eyes","Eyes")
    ]
    gender_choices = [
        ("male","Male"),
        ("female","Female"),
        ("other","Other")
    ]
    img = CloudinaryField("img",null=True,default="https://res.cloudinary.com/dtssxxfra/image/upload/v1761411333/default-profile-picture-avatar-user-icon-vector-46389216_y0zwei.avif")
    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','username'] # email is already required by USERNAME_FIELD

    # --- Fields from "Personal Information" section ---
    phone_number = models.CharField(max_length=20,)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=8,
        choices=gender_choices,
        default="male",
    )
    address = models.CharField(max_length=255, blank=True,null=True)
    occupation = models.CharField(max_length=100, blank=True,null=True)
    
    # --- Emergency Contact ---
    emergency_contact_name = models.CharField(max_length=100, blank=True,null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True,null=True)

    # --- Role (Useful for your clinic) ---
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    specialty = models.CharField(max_length=200,blank=True,null=True,choices= specialty_choices)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    def save(self,*args,**kwargs):
        if self.is_doctor == False:
            self.specialty = None
        super().save(*args,**kwargs)


class PatientProfile(models.Model):
    """
    Handles the "Medical Information" for a user.
    Linked one-to-one with the CustomUser model.
    """
    # This links the profile to our CustomUser model.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile', # Access with user.profile
        limit_choices_to={'is_patient': True}
    )
    

    primary_care_physician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Don't delete profile if doctor is deleted
        null=True,
        blank=True,
        related_name='patients', # Access with doctor.patients
        limit_choices_to={'is_doctor': True}
    )
    
    insurance_provider = models.CharField(max_length=100, blank=True,null=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True,null=True)
    
    # TextField is best for long, multi-line text
    allergies = models.TextField(blank=True,null=True)
    current_medications = models.TextField(blank=True,null=True)
    family_medical_history = models.TextField(blank=True,null=True)
    past_medical_history = models.TextField(blank=True,null=True)

    def __str__(self):
        # Use user.first_name and user.last_name from the linked CustomUser
        return f"{self.user.first_name} {self.user.last_name}'s Medical Profile"
    


class Appointment(models.Model):
    appointment_status = [
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled'),
        ('completed','Completed'),
        ('scheduled','Scheduled')
    ]
    doctor = models.ForeignKey(User,limit_choices_to={"is_doctor":True},on_delete=models.CASCADE,related_name="doctor_appointments")
    patient = models.ForeignKey(User,limit_choices_to={"is_patient":True},on_delete=models.CASCADE,related_name="patient_appointments")
    reason_for_appointment = models.CharField(max_length=255)
    reason_for_cancellation = models.CharField(max_length=255,null=True,blank=True)
    
    additional_notes = models.TextField(
        blank=True, 
        null=True,
        help_text="ex. Prefer afternoon appointments, if possible"
    )
    
    status = models.CharField(choices=appointment_status,max_length=20,default="pending")

    expected_appointment_date = models.DateField(
        help_text="The date requested by the patient."
    )
    
    # --- Additional important fields ---
    
    # It can be null at first (when 'Pending') and set by the doctor/admin
    confirmed_appointment_datetime = models.DateTimeField(
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor.last_name} on {self.confirmed_appointment_datetime}"