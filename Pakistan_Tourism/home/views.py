from django.shortcuts import render,HttpResponse,redirect
from .forms import ReviewForm,TourForm
from django.contrib.auth.models import User, auth
from .models import City,Attraction_Places,Review_Rating,Tour_Companies,Tour_Packages,Tour_Reviews,City_Hotels,Tour_destinations
import urllib.request
import json
import datetime
from django.contrib import messages
from nltk.sentiment import SentimentIntensityAnalyzer
from django.http import HttpResponseRedirect
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from django.db.models import Q
from django.db.models import Avg

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        print(query)
        
        province = City.objects.filter(Q(province__icontains=query))
        city = City.objects.filter(Q(city_name__icontains=query)).first()
        attractions = Attraction_Places.objects.filter(Q(Place_name__icontains=query)).first()
        dests = City.objects.all()
        
        
        context = {
            'city': city,
            'province': province,
            'attractions': attractions,
            'dests':dests
        }
        
        return render(request, 'destinations.html', context)
    else:
        return redirect('/destinations')


def about(request):
    dests = City.objects.all()
    return render(request,"about.html", {'dests': dests})

def index(request):
    dests = City.objects.all()
    return render(request,"index.html", {'dests': dests})

def index_u(request):
    return render(request,"index_u.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
         
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials...')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    url = request.META.get('HTTP_REFERER')
    return redirect(url) 
    # return redirect('/')

def destinations(request):
    dests = City.objects.all()
    context={
        'dests': dests
        }
    if request.user.is_authenticated:
        return render(request,"destinations.html" , context)
    else:
        return render(request,'login.html')


def destination_detail(request,id):
    desti = City.objects.all()
    hotels=City_Hotels.objects.filter(city_id=id)
    current_datetime = datetime.datetime.now() 
    dest=City.objects.filter(id=id).first()
    attraction = Attraction_Places.objects.filter(city_id=id)
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                        dest.city_name + '&units=metric&appid=36da7fb547d50d292016b3083158ea14').read()
        list_of_data = json.loads(source)

    
        data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ', '
                      + str(list_of_data['coord']['lat']),

        "temp": str(list_of_data['main']['temp']) + ' °C',
        "pressure": str(list_of_data['main']['pressure'])+ ' mb',
        "humidity": str(list_of_data['main']['humidity'])+ ' %',
        'main': str(list_of_data['weather'][0]['main']),
        'description': str(list_of_data['weather'][0]['description']),
        'icon': list_of_data['weather'][0]['icon'],
    }
        
    except :
         data= {
        "country_code": 'not found',
        "coordinate": 'not found',
        "temp": 'not found',
        "temprature": '2 °C',
        "pressure": '1022 mb',
        "humidity": '40 %',
        'main': 'Clear',
        'description': 'Periodic Clouds',
        'icon': 'not found',
        }
        

    context = {
        'hotels':hotels,
        'desti' : desti,
        'destination': dest,
        'atraction': attraction,
        'weather':   data, 
        'date' : current_datetime
    }
    if request.user.is_authenticated:
        return render(request, 'destination_detail.html',context)
    else:
        return render(request,'login.html')

def attractions(request,id):
    desti = City.objects.all()
    dest=City.objects.filter(id=id).first()
    attraction = Attraction_Places.objects.filter(city_id=id)

    context = {
        'desti' : desti,
        'destination': dest,
        'atraction': attraction
    }
    return render(request, 'attractions.html',context)

def attractions_detail(request,id):
    desti = City.objects.all()
    review=Review_Rating.objects.filter(attraction=id)

    # Retrieve overall_sentiment from the URL
    overall_sentiment = request.GET.get('overall_sentiment', '')

      # Calculate overall sentiment
    reviews = Review_Rating.objects.filter(attraction_id=id)
    overall_sentiments = calculate_overall_sentiment(reviews)

    attraction = Attraction_Places.objects.filter(id=id).first()

    context = {
        'desti' : desti,
        'atraction': attraction,
        'overall_sentiment': overall_sentiment,
        'overall_sentiments': overall_sentiments,
        'reviews':review
    }

    return render(request, 'attractions_detail.html', context)


def hotels(request,id):
    desti = City.objects.all()
    dest=City.objects.filter(id=id).first()
    city_hotel=City_Hotels.objects.filter(city_id=id)

    context = {
        'desti' : desti,
        'destination': dest,
        'hotel':city_hotel
    }

    return render(request, 'hotels.html', context)


def companies(request):
    companies = Tour_Companies.objects.annotate(avg_rating=Avg('tour_reviews__rating')).order_by('-avg_rating')
    context = {
        'companies': companies
    }
    if request.user.is_authenticated:
        return render(request, 'tour_companies.html', context)
       
    else:
         return render(request,'login.html')
    

def tour_packages(request,id):
    dests = City.objects.all()
    company=Tour_Companies.objects.filter(id=id).first()
    review=Tour_Reviews.objects.filter(tour=id)
    packages=Tour_Packages.objects.filter(tour_companies_id=id)
    context = {
        'dests': dests,
        'packages': packages,
        'company': company,
        'reviews':review
    }

    return render(request,"company_packages.html", context)    
    
def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['confirm']       
      
        if password1==password2 and password1!="" and password2!="":
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken...")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken...")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, "User Created...")
                return redirect('login')
        else:
            messages.info(request, "Password not Matched...")
            return redirect('register')
           
    else:
        return render(request, 'register.html')


def tours_review(request, tour_companies_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Tour_Reviews.objects.get(username_id=request.user.id, tour_id=tour_companies_id)
            form = TourForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except Tour_Reviews.DoesNotExist:
            form = TourForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.tour_id = tour_companies_id
                data.username_id = request.user.id
                data.save()

                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
            

from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django.contrib import messages

def submit_review(request, attraction_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review_Rating.objects.get(username_id=request.user.id, attraction_id=attraction_id)
            review_count = reviews.count()
            form = ReviewForm(request.POST, instance=reviews)
            form.save()

            reviews = Review_Rating.objects.filter(attraction_id=attraction_id)
            percentages = calculate_overall_sentiment(reviews)
            print(percentages)
            chart_filename = plot_sentiment_pie_chart(percentages)
            print(chart_filename)
            messages.success(request, 'Thank you! Your review has been submitted.')

            # Update the URL with the 'overall_sentiment' parameter
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            query_params['overall_sentiment'] = chart_filename
            query_params['review_count'] = review_count
            updated_query = urlencode(query_params, doseq=True)
            updated_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                updated_query,
                parsed_url.fragment
            ))

            return redirect(updated_url)

        except Review_Rating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.attraction_id = attraction_id
                data.username_id = request.user.id
                data.save()

                reviews = Review_Rating.objects.filter(attraction_id=attraction_id)
                review_count = reviews.count()
                percentages = calculate_overall_sentiment(reviews)
                print(percentages)
                chart_filename = plot_sentiment_pie_chart(percentages)
                print(chart_filename)
                messages.success(request, 'Thank you! Your review has been submitted.')

                # Update the URL with the 'overall_sentiment' parameter
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                query_params['overall_sentiment'] = chart_filename
                query_params['review_count'] = review_count
                updated_query = urlencode(query_params, doseq=True)
                updated_url = urlunparse((
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    updated_query,
                    parsed_url.fragment
                ))

                return redirect(updated_url)
            else:
                messages.error(request, 'Invalid form submission.')
                return redirect(url)  # Redirect back to the previous URL with an error message

def calculate_overall_sentiment(reviews):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    total_compound_score = 0
    total_reviews = 0
    sentiment_counts = {'good': 0, 'bad': 0, 'unknown': 0}

    for review in reviews:
        review_text = review.review
        sentiment_scores = sentiment_analyzer.polarity_scores(review_text)
        total_compound_score += sentiment_scores['compound']
        total_reviews += 1

        # Increment the count for the corresponding sentiment category
        if sentiment_scores['compound'] >= 0.05:
            sentiment_counts['good'] += 1
        elif sentiment_scores['compound'] <= -0.05:
            sentiment_counts['bad'] += 1
        else:
            sentiment_counts['unknown'] += 1

    if total_reviews > 0:
        average_compound_score = total_compound_score / total_reviews

        # Calculate the percentages
        percentages = {k: v / total_reviews * 100 for k, v in sentiment_counts.items()}

        return percentages
    else:
        return {'good': 0, 'bad': 0, 'unknown': 0}

import os
import uuid
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def plot_sentiment_pie_chart(percentages):
    labels = list(percentages.keys())
    values = list(percentages.values())

    # Plotting the pie chart
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Generate a unique filename for the chart
    filename = f"chart_{uuid.uuid4().hex}.png"

    # Check if the chart file already exists
    existing_files = os.listdir(os.path.join('static', 'assets', 'images'))
    while filename in existing_files:
        filename = f"chart_{uuid.uuid4().hex}.png"

    # Save the pie chart to a file
    chart_path = os.path.join('static', 'assets', 'images', filename)
    plt.savefig(chart_path)
    plt.close()  # Close the figure to free up memory

    # Return the filename of the generated chart
    return filename



def province(request,province_name):
    province=City.objects.filter(province=province_name)
    context={
        'province':province
    }
    return render(request, 'province.html',context)

def forts(request):
    forts=Tour_destinations.objects.filter(tour_type='Forts')
    context={
        'forts':forts,
    }
    if request.user.is_authenticated:
         return render(request, 'forts.html',context)
       
    else:
         return render(request,'login.html')
    

def mountains(request):
    mountains=Tour_destinations.objects.filter(tour_type='Mountains')
    context={
        'mountains':mountains,
    }
    if request.user.is_authenticated:
         return render(request, 'mountains.html',context)
    else:
         return render(request,'login.html')
    

def valleys(request):
    valleys=Tour_destinations.objects.filter(tour_type='VALLEYS')
    context={
        'valleys':valleys,
    }
    if request.user.is_authenticated:
         return render(request, 'valleys.html',context)
       
    else:
         return render(request,'login.html')
   

def hill(request):
    hill=Tour_destinations.objects.filter(tour_type='HILL STATION')
    context={
        'hill':hill,
    }
    if request.user.is_authenticated:
        return render(request, 'hill_station.html',context)
       
    else:
         return render(request,'login.html')

def walking(request):
    walking=Tour_destinations.objects.filter(tour_type='walking')
    context={
        'walking':walking,
    }
    if request.user.is_authenticated:
        return render(request, 'walking.html',context)
       
    else:
         return render(request,'login.html')
    
    
def tour_destination(request):
    if request.user.is_authenticated:
        return render(request,'tour_destination.html')
       
    else:
         return render(request,'login.html')
    
def punjab(request):
    punjab=Tour_destinations.objects.filter(province_name='Punjab')
    context={
        'punjab':punjab,
    }
    return render(request,'punjab.html', context)

def sindh(request):
    sindh=Tour_destinations.objects.filter(province_name='Sindh')
    context={
        'sindh':sindh,
    }
    return render(request,'sindh.html', context) 

def kpk(request):
    kpk=Tour_destinations.objects.filter(province_name='KPK')
    context={
        'kpk':kpk,
    }
    return render(request,'kpk.html', context) 

def balochistan(request):
    balochistan=Tour_destinations.objects.filter(province_name='Balochistan')
    context={
        'balochistan':balochistan,
    }
    return render(request,'balochistan.html', context) 


def season(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and 'btn' in request.GET:
            user_keyword = request.GET['date']
            today = datetime.datetime.strptime(user_keyword, "%Y-%m-%d").date()
            
            spring = datetime.date(today.year, 3, 20)
            summer = datetime.date(today.year, 6, 20)
            fall = datetime.date(today.year, 9, 22)
            winter = datetime.date(today.year, 12, 21)

            city_season = 'winter'
            if spring <= today < summer:
                city_season = 'spring'
            elif summer <= today < fall:
                city_season = 'summer'
            elif fall <= today < winter:
                city_season = 'fall'

            season= Tour_destinations.objects.filter(season=city_season)

            context = {
                'season': season,
            }
            return render(request, 'season.html', context)
        else:
            return render(request, 'season.html')
    else:
         return render(request,'login.html')
    
         
def view(request,id):
    tour_destinations= Tour_destinations.objects.filter(id=id)
    context = {
        'tour_destination': tour_destinations
    }
    return render(request,"view.html" , context)


def hotels_view(request):
    if request.user.is_authenticated:
        return render(request,'hotels_view.html')
       
    else:
         return render(request,'login.html')
    

def hotel1(request):
    return render(request,'hotel1.html')

def hotel2(request):
    return render(request,'hotel2.html')

def hotel3(request):
    return render(request,'hotel3.html')

def hotel4(request):
    return render(request,'hotel4.html')
    
def searching(request):
    query = request.GET.get('query')
    rows =Tour_destinations.objects.filter(destination_name__icontains=query) | Tour_destinations.objects.filter(province_name__icontains=query)
    attractions = Attraction_Places.objects.filter(Q(Place_name__icontains=query))
    context = {'rows': rows,
               'attractions':attractions
               }
    return render(request, 'searching.html', context)

def gilgit(request):
    url = request.META.get('HTTP_REFERER')
    return redirect(url) 