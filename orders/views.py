from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Accommodation, HKUMember, Reservation

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
def accommodation_detail(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    return render(request, 'detail.html', {'accommodation': accommodation})

# 3. Reserve accommodation
def reserve_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)

    if request.method == 'POST':
        member = HKUMember.objects.get(pk=1)  # Assuming test member
        reservation = Reservation.objects.create(
            member=member,
            accommodation=accommodation,
            reservation_date=timezone.now(),
            status='confirmed',
            rating=None
        )
        return render(request, 'reserve_success.html', {'reservation': reservation})

    return render(request, 'reserve_confirm.html', {'accommodation': accommodation})