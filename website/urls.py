from django.urls import path, include
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-review-test", views.add_review_test, name= "newReview"),
    path("podcasts", views.podcast_view, name="podcasts"),
    path("addPodcast", views.add_podcast, name="addPodcast"),
    path("addEpisode", views.add_episode, name="addEpisode"),
    path("profile/<int:user_id>", views.profile_view, name="profile"),
    path("lists", views.lists_view, name="lists"),
    path("makeList", views.make_list, name="makeList"),
    path("list/<int:list_id>", views.list_page_view, name="listPageView"),
    path("addListEpisode/<int:list_id>", views.add_list_episode, name="addListEpisode"),
    path("editList/<int:list_id>", views.edit_list, name="editList"),
    path("podcastPage/<int:podcast_id>", views.podcast_page, name="podcastPage"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:list_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/delete/<int:list_id>", views.watchlist_delete, name="watchlist_delete"),

    # DYNAMIC SELECTION PATHS
    path("get-episodes/<int:podcast_id>", views.get_episodes, name="getEpisodes"),
    
    # Follower/Following paths
    path("follow", views.follow, name="follow"),

    # Profile view paths
    path("reviews/<int:user_id>", views.load_profile_reviews, name="loadProfileReviews"),
    path("userlists/<int:user_id>", views.load_profile_lists, name="loadProfileLists"),
]