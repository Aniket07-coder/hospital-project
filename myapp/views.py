from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Doctor, Appointment, Contact, Profile
from django.contrib.auth.hashers import make_password


# 🏠 Home
def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')

    return render(request, 'home.html')


# 👨‍⚕️ Doctors (🔐 login required)
@login_required
def doctors(request):
    query = request.GET.get('q')
    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(name__icontains=query)

    return render(request, 'doctors.html', {'doctors': doctors})


# 📅 Appointment (🔐 login required)
@login_required
def appointment(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        doctor = Doctor.objects.get(id=doctor_id)

        # 🔥 Auto take logged-in user data
        Appointment.objects.create(
            user=request.user,
            patient_name=request.user.username,
            email=request.user.email,
            doctor=doctor,
            date=date,
            time=time
        )

        return redirect('success')

    return render(request, 'appointment.html', {'doctors': doctors})


# ✅ Success Page
def success(request):
    return render(request, 'success.html')


# 🔐 Register
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        image = request.FILES.get('image')   # 🔥 get image

        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            # 🔥 Save image in profile
            profile = Profile.objects.get(user=user)
            if image:
                profile.image = image
                profile.save()

            return redirect('login')

    return render(request, 'register.html')


# 👑 Admin Dashboard Only
@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    appointments = Appointment.objects.all()
    doctors = Doctor.objects.all()
    users = User.objects.all()

    # 📊 Status count
    pending = appointments.filter(status='Pending').count()
    accepted = appointments.filter(status='Accepted').count()
    rejected = appointments.filter(status='Rejected').count()

    return render(request, 'dashboard.html', {
        'appointments': appointments,
        'doctors': doctors,
        'users': users,
        'pending': pending,
        'accepted': accepted,
        'rejected': rejected
    })


# ➕ Add Doctor
@login_required
def add_doctor(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        image = request.FILES.get('image')

        Doctor.objects.create(
            name=name,
            specialization=specialization,
            image=image
        )
        return redirect('dashboard')

    return render(request, 'add_doctor.html')


# ✏ Edit Doctor
@login_required
def edit_doctor(request, id):
    if not request.user.is_superuser:
        return redirect('home')

    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.specialization = request.POST.get('specialization')

        if request.FILES.get('image'):
            doctor.image = request.FILES.get('image')

        doctor.save()
        return redirect('dashboard')

    return render(request, 'edit_doctor.html', {'doctor': doctor})


# ❌ Delete Doctor
@login_required
def delete_doctor(request, id):
    if not request.user.is_superuser:
        return redirect('home')

    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect('dashboard')


@login_required
def accept_appointment(request, id):
    if not request.user.is_superuser:
        return redirect('home')

    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = 'Accepted'
    appointment.save()

    return redirect('admin_appointments')


@login_required
def reject_appointment(request, id):
    if not request.user.is_superuser:
        return redirect('home')

    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = 'Rejected'
    appointment.save()

    return redirect('admin_appointments')


@login_required
def user_dashboard(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')

    return render(request, 'user_dashboard.html', {
        'appointments': appointments
    })


@login_required
def admin_appointments(request):
    if not request.user.is_superuser:
        return redirect('home')

    appointments = Appointment.objects.all()
    return render(request, 'admin_appointments.html', {'appointments': appointments})


@login_required
def admin_doctors(request):
    if not request.user.is_superuser:
        return redirect('home')

    doctors = Doctor.objects.all()
    return render(request, 'admin_doctors.html', {'doctors': doctors})


@login_required
def admin_users(request):
    if not request.user.is_superuser:
        return redirect('home')

    users = User.objects.all()
    return render(request, 'admin_users.html', {'users': users})


@login_required
def admin_messages(request):
    if not request.user.is_superuser:
        return redirect('home')

    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'admin_messages.html', {'messages': messages})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect('contact')

    return render(request, 'contact.html')



def forgot_password(request):
    message = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()
            message = "Password updated successfully"
        except User.DoesNotExist:
            message = "User not found"

    return render(request, 'forgot_password.html', {'message': message})