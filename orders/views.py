from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Accommodation, HKUMember, Reservation
from .models import HKUMember
from django.contrib import messages


# 1. Browse + Filter + Sort accommodations
def browse_accommodations(request):

    accommodations = Accommodation.objects.all()

    acc_type = request.GET.get('type')
    max_price = request.GET.get('max_price')
    max_distance = request.GET.get('max_distance')
    sort_by = request.GET.get('sort_by')

    # ✅ 只有在参数不为空时才进行过滤
    if acc_type and acc_type.strip() != "":
        accommodations = accommodations.filter(type__icontains=acc_type)
    if max_price and max_price.strip() != "":
        accommodations = accommodations.filter(price__lte=max_price)
    if max_distance and max_distance.strip() != "":
        accommodations = accommodations.filter(distance__lte=max_distance)

    # ✅ 排序逻辑不变
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
            'max_price': max_price or '',
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
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        name = request.POST.get('name')

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

        return redirect('browse_accommodations')

    return render(request, 'login.html')


def logout_member(request):
    # 清除 session 中的用户信息
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')