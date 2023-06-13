from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    id=models.AutoField(primary_key=True)
    city_name=models.CharField(max_length=122,default='')
    province=models.CharField(max_length=122)
    hotels=models.IntegerField(default=0)
    area=models.CharField(max_length=100)
    population=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    description= models.TextField(max_length=1000)
    long_description=models.TextField(max_length=1500)
    Image =models.ImageField(upload_to='pics')
    No_of_attrac_places= models.IntegerField(default=0)

    # def __str__(self):
    #     return self.city_name

class Tour_Type(models.Model):
    tour_type=models.CharField(max_length=100,primary_key=True)
    type_id=models.AutoField

    def __str__(self):
        return self.tour_type
    
class destination_seasons(models.Model):
    season_name=models.CharField(max_length=100,primary_key=True)
    id=models.AutoField

    def __str__(self):
        return self.season_name
    
class Tour_destinations(models.Model):
    id = models.AutoField(primary_key=True)
    destination_name=models.CharField(max_length=122,default='')
    province_name=models.CharField(max_length=100,default='')
    description= models.TextField(max_length=1000)
    long_description=models.TextField(max_length=2500)
    image =models.ImageField(upload_to='pics')
    tour_type=models.ForeignKey(Tour_Type,on_delete=models.CASCADE)
    season=models.ForeignKey(destination_seasons,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.destination_name


class Attraction_Places(models.Model):
    id = models.AutoField(primary_key=True)
    city_name=models.CharField(max_length=122,default='')
    Place_name=models.CharField(max_length=122)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    description= models.TextField(max_length=1000)
    long_description=models.TextField(max_length=1500)
    Image =models.ImageField(upload_to='pics')
    city_id=models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.Place_name


class Review_Rating(models.Model):
    attraction = models.ForeignKey(Attraction_Places, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    sentiment = models.FloatField(blank=True, null=True)

class Tour_Companies(models.Model):
    id = models.AutoField(primary_key=True)
    company_name=models.CharField(max_length=122,default='')
    address = models.TextField(max_length=100, blank=True)
    response_time=models.TextField(max_length=50, blank=True)
    group_size=models.TextField(max_length=50, blank=True)
    adventure_styles=models.TextField(max_length=80, blank=True)

class Tour_Packages(models.Model):
    id = models.AutoField(primary_key=True)
    package_name=models.CharField(max_length=122,default='')
    tour_length=models.TextField(max_length=100, blank=True)
    rupees=models.TextField(max_length=100, blank=True)
    destinations=models.TextField(max_length=150, blank=True)
    age=models.TextField(max_length=100, blank=True)
    tour_companies_id=models.ForeignKey(Tour_Companies, on_delete=models.CASCADE)

class Tour_Reviews(models.Model):
    tour = models.ForeignKey(Tour_Companies, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()

class City_Hotels(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_name=models.CharField(max_length=120,default='')
    city_name=models.CharField(max_length=120,default='')
    address=models.TextField(max_length=300, blank=True)
    start_price=models.TextField(max_length=80, blank=True)
    about=models.TextField(max_length=800)
    hotel_image=models.ImageField(upload_to='pics')
    city_id=models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel_name

   
    


# Create your models here.
