# from turfbooking.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Ground,Booking,Slot
from django.contrib.auth.models import User
from django.template import loader
import razorpay
import datetime
 

 

# ---------------display bookings
from django.shortcuts import render
from .models import Booking
from django.contrib.auth.decorators import login_required

 
#----------------------------------------------------------------
#--------------for ratings--------------------------------------
 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MyUsers
#----------------------------------------------------------------

# ---------> PDF Genaration
from django.http import FileResponse
import io
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# ---------> PDF Genaration
# ---------> PDF Genaration


# Create your views here.
def index(request):
    return render(request,'index2.html')



def bookit(request):
    exuser=request.user
    print(exuser)
    print(exuser.pk)
    try:
        exuser=request.user
        Ex_User = User.objects.get(pk=exuser.pk)
        print(Ex_User.pk)
        ground_list = Ground.objects.all()
        slots = Slot.objects.all()
        bookingsByUser=Booking.objects.filter(user=exuser)
        print(bookingsByUser)
        slotsToday=datetime.date.today()
        slotsTomorrow=datetime.date.today()+datetime.timedelta(1)
        slotsDayAfTomo=datetime.date.today()+datetime.timedelta(2)

        bookingsToday=Booking.objects.filter(book_date=slotsToday)
        bookingsTomorrow=Booking.objects.filter(book_date=slotsTomorrow)
        bookingsAfTomorrow=Booking.objects.filter(book_date=slotsDayAfTomo)
        
        print("Today's booking: ",bookingsToday)
        print("bookingsTomorrow: ",bookingsTomorrow)
        print("bookingsAfTomorrow: ",bookingsAfTomorrow)
        context={
            'allgrounds':ground_list,
            'allslots':slots,
            'userName':exuser,
            
        }
        template = loader.get_template('bookit.html')
        return HttpResponse(template.render(context,request))
    except Exception as e:
        print(e)
        return redirect('login')


    
def form(request,name):
    try:
        exuser=request.user
        Ex_User = User.objects.get(pk=exuser.pk)
        
        spec_ground = Ground.objects.get(name=name)
        slots = Slot.objects.all()
        slots1=Slot()
        slots2=Slot.objects.values('id')
        booking=Booking()
        abc1=Booking.objects.filter(venue__name=spec_ground).values('slot__id')
        
        slotBooked=Booking.objects.filter(venue__name=spec_ground).values('slot__start_time','slot__end_time')
        allSlots=Slot.objects.values('start_time')
        
        # ====SLOTS AS PER DAYS====
        # ===LOGIC TODAY SLOT===
        slotsToday=datetime.date.today()
        bookingsToday=Booking.objects.filter(book_date=slotsToday,venue__name=spec_ground)
        avlSlotsToday=[]
        for slot in allSlots.values():
            is_open = True
            for booked_slot in bookingsToday.values():
                if slot['id'] == booked_slot['slot_id']:
                    is_open = False
                    break
            if is_open:
                avlSlotToday = slot.copy()
                avlSlotsToday.append(avlSlotToday)
                print("open -->", slot)
        print("-----")

        # ===LOGIC TODAY SLOT===

        # ===LOGIC TOMORROW SLOT===
        slotsTomorrow=datetime.date.today()+datetime.timedelta(1)
        bookingsTomorrow=Booking.objects.filter(book_date=slotsTomorrow,venue__name=spec_ground)
        avlSlotsTomorrow=[]
        for slot in allSlots.values():
            is_open = True
            for booked_slot in bookingsTomorrow.values():
                if slot['id'] == booked_slot['slot_id']:
                    is_open = False
                    break
            if is_open:
                avlSlotTomorrow = slot.copy()
                avlSlotsTomorrow.append(avlSlotTomorrow)
                print("open -->", slot)
        print("-----")

        # ===LOGIC TOMORROW SLOT===

        # ===LOGIC DAYfTom SLOT===
        slotsDayAfTomo=datetime.date.today()+datetime.timedelta(2)
        bookingsAfTomorrow=Booking.objects.filter(book_date=slotsDayAfTomo,venue__name=spec_ground)
        avlSlotsDayfT=[]
        for slot in allSlots.values():
            is_open = True
            for booked_slot in bookingsAfTomorrow.values():
                if slot['id'] == booked_slot['slot_id']:
                    is_open = False
                    break
            if is_open:
                avlSlotDayfT = slot.copy()
                avlSlotsDayfT.append(avlSlotDayfT)
                print("open -->", slot)
        print("-----")
        # ===LOGIC DAYfTom SLOT===
        # ====SLOTS AS PER LOGIC====

        # ***** SLOT LOGIC ******
        avlSlots=[]
        for slot in allSlots.values():
            is_open = True
            for booked_slot in slotBooked.values():
                if slot['id'] == booked_slot['slot_id']:
                    is_open = False
                    break
            if is_open:
                avlSlot = slot.copy()
                avlSlots.append(avlSlot)
                print("open -->", slot)
        context={
        'avlSlot':avlSlots,
        'avlSlotsToday':avlSlotsToday,
        'avlSlotsTomorrow':avlSlotsTomorrow,
        'avlSlotsDayfT':avlSlotsDayfT,
        # 'slots2':abc1,
        # "slotsBook":abc,
        # 'amount':amount,
        # 'api_key':RAZORPAY_API_KEY,
        # 'order_id':payment_order_id,
        # 'amount':amount,
        # 'api_key':RAZORPAY_API_KEY,
        # 'order_id':payment_order_id,
        'selectedGround':spec_ground,
        'allslots':slots,
        'user':exuser,
        }

        template = loader.get_template('bookingform.html')
        return HttpResponse(template.render(context,request))
    
    except:
        return redirect('login')
    
    

def saveBooking(request,name):
    exuser=request.user
    Ex_User = User.objects.get(pk=exuser.pk)
    spec_ground = Ground.objects.get(name=name)
    context={
        # 'amount':amount,
        # 'api_key':RAZORPAY_API_KEY,
        # 'order_id':payment_order_id,
        'selectedGround':spec_ground,
        # 'allslots':slots,
    }
    if request.method=="POST":
        user=exuser
        name1=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('contactNo')
        bookDate=request.POST.get('dateSelected')
        slotSelected=request.POST.get('slotSelected')
        start_time, end_time = slotSelected.split(' to ')
        slot=Slot.objects.get(start_time=start_time,end_time=end_time)
        desc=request.POST.get('description')
        global data
        data=name1,email,phone,bookDate,desc,slotSelected,spec_ground
        print(data)
        global insertDb
        insertDb=Booking(user=user,name=name1,book_date=bookDate,venue=spec_ground,description=desc,slot=slot)
        insertDb.save()
    
    template = loader.get_template('payment_success.html')
    return HttpResponse(template.render(context,request))


 
#display bookings
@login_required
def booking(request):
    current_user = request.user
    bookings = Booking.objects.filter(user=current_user)
    data = {
        'bookings': bookings
    }
    return render(request, "booking_details.html", data)


#---------------------------------------------------------------- 
@login_required
def account_information(request):
    user = request.user
    return render(request, 'account_information.html', {'user': user})

#----------------------------------------------------------------
 

def book_receipt(request):
    # Getting current date and time
    x = datetime.datetime.now()

    # Create PDF buffer
    buf = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buf, pagesize=letter)

    # Data for the receipt
    receipt_data = [
        ['Venue:', str(insertDb.venue)],
        ['Date:', x.strftime("%x")],
        ['Name:', insertDb.name],
        ['Date Booked for:', insertDb.book_date],
        ['Description:', insertDb.description],
        ['Slot:', str(insertDb.slot)]
    ]

    # Creating table
    table = Table(receipt_data)

    # Adding style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('SIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),  # Data background color
    ])

    table.setStyle(style)

    # Build PDF document
    doc.build([table])

    # Reset buffer position
    buf.seek(0)

    # Return PDF response
    return FileResponse(buf, as_attachment=True, filename='receipt.pdf')
     
