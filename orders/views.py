from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Accommodation, HKUMember, Reservation
from .models import HKUMember, PropertyOwner, CEDARSSpecialist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# 1. Browse + Filter + Sort accommodations
def browse_accommodations(request):

    accommodations = Accommodation.objects.all()

    acc_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_distance = request.GET.get('min_distance')
    max_distance = request.GET.get('max_distance')
    sort_by = request.GET.get('sort_by')

    # 只有在参数不为空时才进行过滤
    if min_price and min_price.strip() != "":
        accommodations = accommodations.filter(price__gte=min_price)
    if max_price and max_price.strip() != "":
        accommodations = accommodations.filter(price__lte=max_price)

    if min_distance and min_distance.strip() != "":
        accommodations = accommodations.filter(distance__gte=min_distance)
    if max_distance and max_distance.strip() != "":
        accommodations = accommodations.filter(distance__lte=max_distance)

    # 排序逻辑
    if sort_by == 'price':
        accommodations = accommodations.order_by('price')
    elif sort_by == 'distance':
        accommodations = accommodations.order_by('distance')

    #  accommodation 是否已预订
    for acc in accommodations:
        acc.is_reserved = acc.reservations.filter(status='confirmed').exists()

    return render(request, 'browse.html', {
        'accommodations': accommodations,
            'filters': {
                'type': acc_type or '',
                'min_price': min_price or '',
                'max_price': max_price or '',
                'min_distance': min_distance or '',
                'max_distance': max_distance or '',
                'sort_by': sort_by or '',
            }
    })





# 2. choose/View accommodation details
def accommodation_detail(request, address):
    accommodation = get_object_or_404(Accommodation, pk=address)
    is_reserved = accommodation.reservations.filter(status='confirmed').exists()
    return render(request, 'detail.html', {
        'accommodation': accommodation,
        'is_reserved': is_reserved,
    })

# 3. Reserve accommodation
def reserve_accommodation(request, address):
    accommodation = get_object_or_404(Accommodation, pk=address)

    if request.method == 'POST':
        # 获取当前登录的 member
        member_id = request.session.get('member_id')
        if not member_id:
            return redirect('login')

        member = get_object_or_404(HKUMember, pk=member_id)

        # 检查该 accommodation 是否已被预定
        if accommodation.reservations.filter(status='confirmed').exists():
            # 如果已被预订，显示错误信息
            return render(request, 'reserve_confirm.html', {
                'accommodation': accommodation,
                'error': 'This accommodation has already been reserved. Please choose another one.'
            })

        # 如果未被预订，则创建 reservation
        reservation = Reservation.objects.create(
            member=member,
            accommodation=accommodation,
            reservation_date=timezone.now(),
            status='confirmed',
            rating=None
        )
        return render(request, 'reserve_success.html', {'reservation': reservation})

    return render(request, 'reserve_confirm.html', {'accommodation': accommodation})



def login_member(request):
    # if request.method == 'POST':
    #     member_id = request.POST.get('member_id')
    #     name = request.POST.get('name')
    if request.method == 'POST':
        role = request.POST.get('role')
        member_id = request.POST.get('member_id')
        name = request.POST.get('name')

        if role == 'member':
            if not member_id or not name:
                messages.error(request, "Please enter both ID and name.")
                return render(request, 'login.html')

            # 检查 member 是否存在
            member, created = HKUMember.objects.get_or_create(
                member_id=member_id,
                defaults={'name': name}
            )

            # 若 member 存在但名字不一致，也更新名字
            if not created and member.name != name:
                member.name = name
                member.save()

            # 保存到 session
            request.session['member_id'] = member.member_id
            request.session['member_name'] = member.name
            request.session['role'] = 'member'

        elif role == 'owner':
            if not name:
                messages.error(request, "Please enter your name as Property Owner.")
                return render(request, 'login.html')

            owner, _ = PropertyOwner.objects.get_or_create(name=name)
            request.session['owner_id'] = owner.owner_id
            request.session['owner_name'] = owner.name
            request.session['role'] = 'owner'

            # 登录成功后跳转到 Owner 页面
            return redirect('owner_dashboard')

        elif role == 'specialist':
            if not name:
                messages.error(request, "Please enter your name as CEDARS Specialist.")
                return render(request, 'login.html')

            specialist, _ = CEDARSSpecialist.objects.get_or_create(name=name)
            request.session['specialist_id'] = specialist.specialist_id
            request.session['specialist_name'] = specialist.name
            request.session['role'] = 'specialist'

        else:
            messages.error(request, "Invalid role selected.")
            return render(request, 'login.html')            

        return redirect('browse_accommodations')

    return render(request, 'login.html')


def logout_member(request):
    # 清除 session 中的用户信息
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')



# def owner_dashboard(request):
#     accommodations = Accommodation.objects.all()

#     if request.method == 'POST' and 'delete_address' in request.POST:
#         address = request.POST.get('delete_address')
#         Accommodation.objects.filter(address=address).delete()

#     return render(request, 'owner_dashboard.html', {
#         'accommodations': accommodations
#     })

def owner_dashboard(request):
    # 取出当前登录的 owner_id
    owner_id = request.session.get('owner_id')
    if not owner_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')

    # 查询当前 owner
    try:
        owner = PropertyOwner.objects.get(owner_id=owner_id)
    except PropertyOwner.DoesNotExist:
        messages.error(request, "Owner not found.")
        return redirect('login')

    # 只获取该 owner 上传的房源
    accommodations = Accommodation.objects.filter(owner=owner)

    # 删除房源
    if request.method == 'POST' and 'delete_address' in request.POST:
        address = request.POST.get('delete_address')
        # 确保只能删除自己的房源
        Accommodation.objects.filter(address=address, owner=owner).delete()

    return render(request, 'owner_dashboard.html', {
        'accommodations': accommodations
    })








def add_accommodation(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        acc_type = request.POST.get('type')
        price = request.POST.get('price')
        distance = request.POST.get('distance')
        bedrooms = request.POST.get('bedrooms')
        beds = request.POST.get('beds')
        period = request.POST.get('period_of_availability') 

        # 从 session 获取当前登录的 owner_id
        owner_id = request.session.get('owner_id')
        if not owner_id:
            messages.error(request, "Session expired. Please log in again.")
            return redirect('login')

        # 查找该 owner 实例
        try:
            owner = PropertyOwner.objects.get(owner_id=owner_id)
        except PropertyOwner.DoesNotExist:
            messages.error(request, "Owner not found.")
            return redirect('login')

        # 创建新的 accommodation 并关联 owner
        Accommodation.objects.create(
            address=address,
            type=acc_type,
            price=price,
            distance=distance,
            number_of_bedrooms=bedrooms,
            number_of_beds=beds,
            period_of_availability=period,            
            owner=owner
        )

        messages.success(request, "Accommodation added successfully.")
        return redirect('owner_dashboard')

    return render(request, 'add_accommodation.html')