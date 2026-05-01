from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count, Min, Max
from .models import Title
from .forms import TitleForm
from django.db import transaction #technically django alr uses transations but making more explicit

# LANDING PAGE
def landing_page(request):
    rating_count = Title.objects.count()

    return render(request, 'landing.html', {
        'rating_count': rating_count
    })

# MAIN LIST + ADD + FILTER
@transaction.atomic
def title_list(request):
    titles = Title.objects.all()

    # FILTER VALUES
    title_query = request.GET.get("title")
    year_query = request.GET.get("year")
    min_rating = request.GET.get("min_rating")
    type_query = request.GET.get("type")

    filtering = False

    if title_query:
        titles = titles.filter(name__icontains=title_query)
        filtering = True

    if year_query:
        titles = titles.filter(release_year=year_query)
        filtering = True

    if min_rating:
        titles = titles.filter(rating__gte=min_rating)
        filtering = True

    if type_query:
        titles = titles.filter(type=type_query)
        filtering = True

    # ADD TITLE
    if request.method == "POST":
        form = TitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("title_list")
    else:
        form = TitleForm()

    context = {
        "titles": titles,
        "form": form,
        "filtering": filtering,
        "title_query": title_query,
        "year_query": year_query,
        "min_rating": min_rating,
        "type_query": type_query,
    }

    return render(request, "title_list.html", context)


# EDIT
@transaction.atomic
def edit_title(request, pk):
    title = get_object_or_404(Title, pk=pk)

    if request.method == "POST":
        form = TitleForm(request.POST, instance=title)
        if form.is_valid():
            form.save()
            return redirect("title_list")
    else:
        form = TitleForm(instance=title)

    return render(request, "edit_title.html", {"form": form})


# DELETE
@transaction.atomic
def delete_title(request, pk):
    title = get_object_or_404(Title, pk=pk)
    title.delete()
    return redirect("title_list")

# REPORT
def report_view(request):
    titles = Title.objects.all()

    type_choices = Title._meta.get_field('type').choices

    title_query = request.GET.get('title')
    year_query = request.GET.get('year')
    min_rating_query = request.GET.get('min_rating')
    type_query = request.GET.get('type')

    #filters heeeeeeree
    if title_query:
        titles = titles.filter(name__icontains=title_query) #safely binds user input as a parameter to prevent injections

    if year_query:
        titles = titles.filter(release_year=year_query)

    if min_rating_query:
        titles = titles.filter(rating__gte=min_rating_query)

    if type_query and type_query != "all":      #clean type filtering!!
        titles = titles.filter(type=type_query)

    stats = titles.aggregate(
        total_titles=Count('id'),
        average_rating=Avg('rating'),
        oldest_release=Min('release_year'),
        newest_release=Max('release_year')
    )

    total_movies = titles.filter(type='movie').count()
    total_shows = titles.filter(type='show').count()

    context = {
    'titles': titles,
    'stats': stats,
    'total_movies': total_movies,
    'total_shows': total_shows,
    'type_query': type_query,
     'type_choices': type_choices,
}

    return render(request, 'report.html', context)