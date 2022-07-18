from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Func
from .models import *
from .forms import *
from django.forms.models import modelformset_factory

# Create your views here.
def index(request):
    """ Renders index page and sends users, reviews, podcasts, and episodes context """
    return render(request, "website/index.html", {
        "users": User.objects.all(),
        "reviews": reversed(Review.objects.all()),
        "podcasts": Podcast.objects.all(),
        "episodes": Episode.objects.all(),
    })

def login_view(request):
    """ Handles Login page view """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")


def logout_view(request):
    """ Handles Logout view """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """ Handles account registration view """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "website/register.html")

# DYNAMIC SELECTIONS FOR PODCAST AND EPISODE FOR LIST/REVIEW FORM VIEWS
@login_required
def get_episodes(request, podcast_id):
    """ GET request for dynamic dropdown selections for List and Review forms. """

    if request.method == "GET":
        podcast = Podcast.objects.filter(podcast_id=podcast_id)

        episodes = list(Episode.objects.filter(podcast__in=podcast).values('episode_id', 'title'))
        return JsonResponse({
            "episodes": episodes
        })

# REVIEW PAGE FORM
@csrf_exempt
@login_required
def add_review_test(request):
    """ Renders/POSTs a new form to add review. """
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            form.save()
            print(form)
            return redirect('index')
        
    return render(request, "website/newReview.html", {
        "form": form,
    })


# PODCAST handling
@login_required
def podcast_view(request):
    """ Renders All Podcasts page view """
    podcasts = Podcast.objects.all();

    return render(request, "website/podcasts.html", {
        "podcasts": podcasts,
    })

@login_required
def add_podcast(request):
    """ Renders/POSTs a form for adding a new podcast to the database """
    form = PodcastForm()
    if request.method == 'POST':
        form = PodcastForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("podcasts"))
    return render(request, "website/addPodcast.html", {
        "form": form
    })

@login_required
def add_episode(request):
    """ Renders/POSTs a form for adding a new episode to the database """
    form = EpisodeForm()
    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("podcasts"))
    return render(request, "website/addEpisode.html", {
        "form": form
    })

@login_required
def podcast_page(request, podcast_id):
    """ Renders podcast view page for a single/specific podcast """
    podcast = Podcast.objects.get(podcast_id=podcast_id)

    episodes = Episode.objects.filter(podcast=podcast)

    podcastScore = Review.objects.filter(podcast=podcast).aggregate((Avg('score')))

    return render(request, "website/podcastPage.html", {
        "podcast": podcast,
        "episodes": episodes,
        "podcastScore": podcastScore
    })

# ALL LISTS PAGE
@login_required
def lists_view(request):
    """ Renders All Lists page view """
    lists = List.objects.all().order_by('-list_id')

    return render(request, "website/lists.html", {
        "lists": lists,
    })

# REQUESTED LIST PAGE
@login_required
def list_page_view(request, list_id):
    """ Renders list page view for a single/specific customized list """
    list = List.objects.get(list_id=list_id)
    listcontent = ListContent.objects.filter(custom_list=list)
    watchlist = request.user.is_authenticated and (list in request.user.watchlist.all())

    return render(request, "website/list.html", {
        "list": list,
        "listContent": listcontent,
        "watchlist": watchlist
    })

# CUSTOM LIST FORM

@login_required
def make_list(request):
    """ Renders/POSTs a form for adding a new custom list to the database """
    if request.method == "GET":
        form = ListForm()
    if request.method == "POST":
        print(request.POST)
        form = ListForm(request.POST)

        if form.is_valid(): # and formset.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            return redirect('lists')
    return render(request, "website/makeList.html", {
        "form": form,

    })

@login_required
def add_list_episode(request, list_id):
    """ Renders/POSTs a form for adding a new episode to a custom list """
    list = List.objects.get(list_id=list_id)
    form = ListContentForm()
    if request.method == "POST":
        form = ListContentForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.custom_list = list
            form.save()
            print(form)
            return redirect('lists')
    return render(request, 'website/addListEpisode.html', {
        "form": form,
    })

# EDIT LIST

@login_required
def edit_list(request, list_id):
    """ Renders/POSTs an edit/update form a customized list. Shows a prepopulated form. """
    instance = List.objects.get(list_id=list_id)
    print(instance)
    form = ListForm(request.POST)
    if request.method == "GET":
        form = ListForm(instance=instance)
    else:
        form = ListForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse("lists"))
    return render(request, 'website/editList.html', {
        "form": form,
    })

# PROFILE PAGE
@login_required
def profile_view(request, user_id):
    """ Renders profile page view """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")
    return render(request, "website/profile.html", {
        "watchlist": request.user.watchlist.all(),
        "lists": List.objects.filter(user=user),
        "reviews": Review.objects.filter(user=user),
        "user": user,
        "followers": Follow.objects.filter(following=user).count(), 
        "following": Follow.objects.filter(follower=user).count()
    })

@csrf_exempt
@login_required
def follow(request):
    """ Handles POST request when the follow button is clicked. """
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id", "")
        is_following = data.get("is_following", "")

        current_user = User.objects.get(id=request.user.id)
        other_user = User.objects.get(id=user_id)

        if Follow.objects.filter(follower=current_user, following=other_user).exists():
            Follow.objects.filter(follower=current_user, following=other_user).delete()
            is_following = "Follow"
        else:
            follow = Follow(follower=current_user, following=other_user)
            follow.save()
            is_following = "Unfollow"
        return JsonResponse({
            "is_following": is_following, 
            "followingCnt": Follow.objects.filter(follower=other_user).all().count(),
            "followerCnt": Follow.objects.filter(following=other_user).all().count()
        }, status=200)

    return JsonResponse({}, status=404)

@login_required
def load_profile_reviews(request, user_id):
    """ Returns a JSON response with user's reviews. Used for profile view. """
    try:
        user = User.objects.filter(id=user_id)
        reviews = list(Review.objects.filter(user__in=user).values('review_id', 'content', 'podcast', 'episode', 'score'))
    except Review.DoesNotExist:
        return JsonResponse({"error": "No reviews."})

    if request.method == "GET":
        return JsonResponse({
            "reviews": reviews
        })

@login_required
def load_profile_lists(request, user_id):
    """ Returns a JSON response with user's custom lists. Used for profile view. """
    try:
        user = User.objects.filter(id=user_id)
        lists = list(List.objects.filter(user__in=user))
        print(lists)
    except List.DoesNotExist:
        return JsonResponse({"error": "No lists."})

    if request.method == "GET":
        return JsonResponse({
            "lists": lists
        })

# FOLLOW/WATCH LISTS
@login_required
def watchlist(request):
    """ Returns a JSON response with lists the user has added to Watchlist. Used for profile view. """
    list = request.user.watchlist.all()
    return render(request, "website/profile.html", {
        "title": "Watchlist",
        "listings": list
    })

@login_required
def watchlist_add(request, list_id):
    """ Adds list to watchlist """
    if request.method == "POST":
        list = get_object_or_404(List, list_id=list_id)
        request.user.watchlist.add(list)
        return redirect(reverse("lists"))

@login_required
def watchlist_delete(request):
    """ Removes list from watchlist """
    if request.method == "POST":
        listing = get_object_or_404(List, pk=int(request.POST["list_id"]))
        request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("list", args=(list.id,)))


