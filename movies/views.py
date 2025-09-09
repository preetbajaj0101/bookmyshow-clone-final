from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def movie_list(request):
    search_query=request.GET.get('search')
    if search_query:
        movies=Movie.objects.filter(name__icontains=search_query)
    else:
        movies=Movie.objects.all()
    return render(request,'movies/movie_list.html',{'movies':movies})

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})



# movies/views.py (Corrected version)

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    # FIX 1: Rename variable to singular 'theater' for clarity
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)
    if request.method == 'POST':
        selected_Seats = request.POST.getlist('seats')
        error_seats = []
        if not selected_Seats:
            # FIX 2: Use correct variable 'theater' and a clear key
            return render(request, "movies/seat_selection.html", {'theater': theater, "seats": seats, 'error': "No seat selected"})
        for seat_id in selected_Seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats:
            # FIX 3: Improve the error message formatting
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            # FIX 4: Pass the correct 'theater' object and the generated error_message
            return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats, 'error': error_message})
        return redirect('profile')
    # FIX 5: Use the consistent 'theater' variable here as well
    return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})

