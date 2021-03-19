# Quizgo

Quizgo is a web app developed with Django. The idea of this app is to create a fun quiz game, similar to other quiz games such as Trivia Crack, using Django as the framework.
The game is simple in design and easy to play.

### Website Link
[https://quizgo.herokuapp.com/](https://quizgo.herokuapp.com/)

### How to Play

To start off, simply create an account using the sign up button on the top right. Once you've done so, you can log in.
From the home page, you have the choices of clicking the play button; which will present you with any random questions from the database to answer, choosing a specific category; which will only give you questions from that specific category, and choosing one of the challenge modes, which depending on which you choose, will give you x amount of questions and if you get them all right, you will get bonus points.

As you complete more questions and earn more points, you will earn different badges depending on the milestone you've reached. These badges will show up on your profile page. You can view all of the possible badges by clicking on the "All Badges" link near the top right of the page.

You also have the ability to view the leaderboard and compare your score with the current top 10 players. From here, you can also click on user's names to go to their profile. There, you can view their stats and also send them a friend request. Once said user accepts the friend request, they are added to your friends list and you can choose to send them messages.

### Technical Brief

Quizgo has been developed with Django, a web framework that uses Python. It is currently hosted on Heroku, and uses a PostgreSQL database. Most of the Django views in the
project are Class-Based, although the views that handle Questions and friending other users are Function-Based views. The user model is an AbstractUser, with most of their
data being stored as digits or strings. Achievement tracking stores a string of ID's to a user, then pulls that string later and converts it into a list of strings for usage.
Badges, Streaks, and Challenge Progression are all checked within the Question view, hence why it is so long.
