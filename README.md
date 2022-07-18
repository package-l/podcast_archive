# Project: Pod Archive

Pod Archive is a website dedicated to allowing people to create an account to review, rate,
and make customized lists of podcast episodes they are interested in. The goal of the website is to
function as a podcast episode centric website to organize and rate information similar to Letterboxd
or IMDB.

File details: 

Main page views accessed through navigation:
    - index.html (Home)
    - podcasts.html (Podcasts page)
    - lists.html (All lists page)
    - profile.html (User's profile page)
Other page views:
    - login.html
    - podcastPage.html
    - list.html
    - register.html
    - layout.html
Form pages:
    - makeList.html
    - newReview.html
    - editList.html
    - addPodcast.html
    - addEpisode.html

More specific information on each of the files is in the comments of each file. 

Technologies used: Python, Django, JavaScript, CSS, HTML

## Installation

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## How to use

- Register/sign in to see/utilize all the website's features.
- The Home page shows recently reviewed podcast episodes.
- The Podcast page shows all the podcasts that have been added to the website. From there you can click
     on each podcast listed to go to the selected podcast's page, where you can see what the podcast's
     information and what podcast episodes have been added to the site. 
- The Lists page shows all the public customized lists that have been added to the site. From there you
    can click on the lists and be taken to the list page to see information about the list and what
    episodes have been added to the list. Clicking Edit List on the list page will take you to a 
    pre-populated form where you can edit the list information.
- Add Review page lets you add a review to the the site.
- Profile pages can be accessed by clicking on any username. On the profile page you can see how many
    followers a user has and how many users the user is following. Clicking through buttons Reviews, Lists,
    and Watchlist will show you what reviews the user has written, what lists they have made, and what 
    lists they have followed. 

## Credits
When working through the project, I consulted these tutorials:
    - Tutorial for Date Input styling used in Add Episode form: https://www.youtube.com/watch?v=I2-JYxnSiB0
    - Tutorial for add multiple formset: https://www.youtube.com/watch?v=Tg6Ft_ZV19M
    - Formset tutorial: https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript.html
