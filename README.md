# emotion_detector
Machine learning model to predict emotions throught text

# Table of Contents

1. [Objective](#Objective)
2. [Ml_algo](#Ml_algo)
3. [Backend](#Backend)
4. [Frontend](#Frontend)



## Objective
I want to create an app where user can write his/her diary and analyze thier emotions with the help of sentiment analysis algorithm.

## Ml_algo
-I have developed emotion detection model using TFIDF  vectorization method .
 used word2vec and doc 2 vec too but  got more accuracy with TFIDF vectorizer.

TFIDF  vectorizer is easy to use method 
https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76

Removed  stop words  using NLTK  and cleaned text before vectorizing the text.
Used Random forest classification as it is good at large data sets.

## Backend
I’ve used Flask  to develop the  web app. And chose SQLITE as database connecting method as  I’m restricting maximum no of users .
Created Two tables login and diary for data storage  and created triggers to keep both tables in sync

## Frontend
I’ve created js file along with html to run various functions within the page .


Below figure is the working  design of this app

![HLD for emotion detector](https://user-images.githubusercontent.com/73159496/202917105-93d1f227-7fc2-40a8-9cdd-b3285dd39a26.jpg)


When user enters the home page of the app, they can go to different links(home.html)

![image](https://user-images.githubusercontent.com/73159496/202916989-85d2fc89-a8c4-4d78-b5e1-df0fe1aa8321.png)

 
User can go to login page to either login or register and login to the profile page .
Here login.html calls  login python func (app.py)for authentication 

![image](https://user-images.githubusercontent.com/73159496/202917010-20b4249a-ac28-4cb0-b5bc-721cfd8677d0.png)




User can add , edit , delete notes in their diary and app creates the  feelings pie chart 
Updates the user data through app.py in database.db


![image](https://user-images.githubusercontent.com/73159496/202917018-ff0221c2-50d6-4524-8ab7-93ae19c17787.png)


Check out my app at 
https://know-thyself.onrender.com/


