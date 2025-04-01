from django.db import models

# Property Owner model
class PropertyOwner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# CEDARS Specialist model
class CEDARSSpecialist(models.Model):
    specialist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Accommodation model
class Accommodation(models.Model):
    accommodation_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    period_of_availability = models.CharField(max_length=100)
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.FloatField()
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE, null=True, blank=True, related_name = 'accommodations')
    specialist = models.ForeignKey(CEDARSSpecialist, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_accommodations')

    def __str__(self):
        return f"{self.type} - {self.price} HKD"


# HKU Member model
class HKUMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Reservation model
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    reservation_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(HKUMember, on_delete=models.CASCADE, related_name='reservations')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Reservation {self.reservation_id} - {self.status}"


# Contract model
class Contract(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ('signed', 'Signed'),
        ('failed', 'Failed'),
    ]

    contract_id = models.AutoField(primary_key=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='contract')
    signed_date = models.DateTimeField(auto_now_add=True)
    contract_status = models.CharField(max_length=10, choices=CONTRACT_STATUS_CHOICES)

    def __str__(self):
        return f"Contract {self.contract_id} - {self.contract_status}"


# Optional: Rating model for multiple ratings per accommodation
class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(HKUMember, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating by {self.member.name} - {self.score}/5"
    

