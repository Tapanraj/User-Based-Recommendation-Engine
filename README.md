# User-Based-Recommendation-Engine
This repository displays code for a user based recommendation engine that recommends movies to a user based on what other users have rated a movie. 


Collaborative Filtering is a technique used in recommendation systems by automatically recommending a user based on the information received from other users. 
This is called collaborative as recommendations are based on the peer ratings. 
The approach I used is memory based. That means I find similarity between the users and then recommend a particlar user, the products (movies here) based on the closest match. 

The UserBasedFiltering.py contains a class that gives the recommendations by finding k similar users. It contains subclasses which calculates pearson correlation between 2 users to find closest users and recommend based on k nearest neighbors. 

The CollaborativeFilteringUBF.py contains the movies and its ratings data for the users and calls the class from UserBasedFiltering.py to  provide recommendations.

