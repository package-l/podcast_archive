// JS mainly used to handle profile views, follows, and dealing with form updates/handling.

document.addEventListener('DOMContentLoaded', function() {

    // JS FOR PROFILE PAGE VIEW
    if (document.querySelector('#profile-view')) {
        console.log("triggered")
        let userId = document.querySelector(".theprofile").id.toString().charAt(0)

        document.querySelector('#review-view').style.display = 'block';
        document.querySelector('#watchlist-view').style.display = 'none';
        document.querySelector('#lists-view').style.display = 'none';

        // Adds event listeners to toggle profile view
        document.querySelector('#watchlist').addEventListener('click', () => load_watchlist(userId));
        document.querySelector('#lists').addEventListener('click', () => load_lists(userId));
        document.querySelector('#reviews').addEventListener('click', () => load_reviews(userId));

        // Add event listeners to follow button and calls follow function
        let followBtn = document.querySelector('.btnfollow');
        if (followBtn) {
            followBtn.addEventListener('click', function() {
                console.log(userId)
                follow(userId);
            })
        }
        
        load_reviews(userId);
    }

})


// CODE FOR DYNAMIC SELECTION FOR ADDING TO LIST
/* This is what allows user's to select a podcast in the Add Episode to the list page and have
 it return what episode options are available for selection based on the podcast selected. 
 Tutorials/information referenced is listed under Credits in the README.txt
*/

if (document.querySelector("#new-episode-list")) {
    podcastSelection = document.querySelector("#id_podcast");
    console.log(podcastSelection)
    if (podcastSelection) {
        podcastSelection.addEventListener('change', function() {
            console.log(podcastSelection)
            const podcastId = podcastSelection.value
            console.log(podcastId)
        
            fetch('/get-episodes/' + podcastId)
                .then(response => response.json())
                .then(result => {
                    let html_data = '<option value="">---------</option>'
                    const stringified_result = JSON.stringify(result)
                    const episodeObj = JSON.parse(stringified_result)
                    const episodes = episodeObj["episodes"]
                    episodes.forEach(episode => {
                        html_data += `<option value="${episode.episode_id}">${episode.title}</option>}`
                    })
                    document.querySelector("#id_episode").innerHTML = html_data;
                })
            
        })
    }
}

// CODE FOR DYNAMIC SELECTION FOR ADDING REVIEW
/* This is what allows user's to select a podcast in the Add Review page and have it return 
    what episode options are available for selection based on the podcast selected.
*/

if (document.querySelector("#new-review")) {
    podcastSelection = document.querySelector("#id_podcast");
    console.log(podcastSelection)
    if (podcastSelection) {
        podcastSelection.addEventListener('change', function() {
            console.log(podcastSelection)
            const podcastId = podcastSelection.value
            console.log(podcastId)
        
            fetch('/get-episodes/' + podcastId)
                .then(response => response.json())
                .then(result => {
                    let html_data = '<option value="">---------</option>'
                    const stringified_result = JSON.stringify(result)
                    const episodeObj = JSON.parse(stringified_result)
                    const episodes = episodeObj["episodes"]
                    episodes.forEach(episode => {
                        html_data += `<option value="${episode.episode_id}">${episode.title}</option>}`
                    })
                    document.querySelector("#id_episode").innerHTML = html_data;
                })
            
        })
    }
}


// CODE FOR PROFILE VIEW

// Updates follows and sends POST request to update follow count.
function follow(user_id) {

    let is_following = document.querySelector(".btnfollow").textContent;
    console.log(is_following)
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id,
            is_following: is_following,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        document.getElementById("followers").innerHTML = `${result.followerCnt}`;
        document.getElementById("following").innerHTML = `${result.followingCnt}`;
        document.querySelector(".btnfollow").innerHTML = `${result.is_following}`;
    })
}

function load_reviews(user_id) {
    document.querySelector('#review-view').style.display = 'block';
    document.querySelector('#watchlist-view').style.display = 'none';
    document.querySelector('#lists-view').style.display = 'none';

}

function load_watchlist(user_id) {
    document.querySelector('#review-view').style.display = 'none';
    document.querySelector('#watchlist-view').style.display = 'block';
    document.querySelector('#lists-view').style.display = 'none';

}

function load_lists(user_id) {
    document.querySelector('#review-view').style.display = 'none';
    document.querySelector('#watchlist-view').style.display = 'none';
    document.querySelector('#lists-view').style.display = 'block';


}