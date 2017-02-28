## Winner of "Best Hack to Reduce Online Harassment" at T9 Hacks Spring 2017.

## What is Empower?

Empower is an anonymous platform for women to rate and share their experiences in workplace. 
A news feed shows all the ratings and experiences shared recently. Users can select a specific company to pull up analytics on the ratings and reviews of that company. The reviews are all anonymous.

## Inspiration

A few days back,[Susan Fowler] (https://www.susanjfowler.com/blog/2017/2/19/reflecting-on-one-very-strange-year-at-uber) shared a horrifying experience regarding workplace harassment at Uber. Susan ended up quitting Uber. Who would have thought that Uber would have such a poor workplace environment for women?

Women would be greatly benefited by a platform where they could rate and share their workplace harassment experiences -- so that other women could benefit from that and not join a company which has a poor culture towards women.

## How we built it?

We had a flask server running in the backend which had a postgresql datastore. The front end was done using bootstrap. We used IBM Watson's tone analyzer to generate analytics and d3.js to generate the visualization.

The project is hosted on AWS.

## Running the project locally

1) Install Dependencies.
```
pip install -r requirements.txt
```
2) Create API keys for IBM Watson's tone analyzer and Alchemy API and update the respective variables.

3) Install Postgresql driver and create a new username and password. Update the config.properties with those credentials.

4) Run the create_db.py script to create the database initially.

5) Run application.py to run the main application and go to localhost:5000.


The site is hosted live at http://ec2-50-112-201-77.us-west-2.compute.amazonaws.com:5000/.
(PS: The site is down currently, but will be back online real soon!)
