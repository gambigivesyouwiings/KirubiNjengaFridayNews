## EXCLUSIVE CONTENT WEBSITE
----------------------------

# Introduction
This is the codebase for the web-app: http://fridaynews.pythonanywhere.com/
Designed by: Victor Mugambi Kimathi
The go-to site for exclusive content for loyal fans.


Background & context
At a time of tens of social media apps that attract billions of users on their platforms, far outstripping traditional media, content creation has become big business.

So when a couple of my friends, who are upcoming content creators, asked if I could make an interactive web-app for them where they can share exclusive content with their loyal fans, I was excited to put some of the skills I learnt on ALX and other learning sites like Udemy to the test.

The team
Victor Mugambi Kimathi - currently the only team member, will take care of all front and backend tasks.

Technologies 
Flask
Bootstrap
Jinja
Postgresql
PythonAnywhere.org

Trade-offs: Postgresql vs Sqlite

Postgresql is more adjustable and works better with flask-migrate compared with Sqlite. This is because by design sqlite doesn’t really support ALTER statements, meaning we’ll get problems down the road when scaling the project and the need to expand the database structure arises.

Trade-offs: PythonAnywhere vs Other hosting services

For most hosting sites like SmarterAsp or Hostinger, while they claim to support python, it seems to be more of a side priority as most of their services are tailored for WordPress sites which make up more than 40% of internet websites as of 2023.

PythonAnywhere really is, well, working from anywhere as they provide bash consoles to work with plus readily support 3.X, which are all welcome. It is also cheaper than, say, AWS cloud services as their web developer offer starts at 5$ a month, which supports one web-app. They also have a free tier with full functionality which is good when you’re trying out a hosting service for the first time before committing real money.

  

Challenge Statement
The challenge here is making a fully functioning and interactive web app that is responsive on Desktop and mobile size view ports.

It is ideal for content creators looking to build their own brand by providing a professional website where subscribers can view exclusive content before they post on their main channels.

To be clear, the project is not meant to be another social media site. More of a subscriber-only access portal.

Risks
Technical risks
A key technical risk is the scalability of the site. Since I’m using Flask, which is a lightweight web framework compared to big-hitters like Django, it would be interesting to see how the site handles, say, 10,000 visitors a day. This scalability could be mitigated by adding the number of web-workers to handle requests.

Non-technical risks

A non-technical risk is the monetary aspect as quality web hosting for a big site is not cheap. A way to mitigate this in the future is to add a paid tier to the site, as well as adding advertiser functionality to the site.

#Infrastructure
Deployment is to a version control service like github, from where the codebase can be accessed by making pull requests from the PythonAnywhere Bash consoles.

App data is populated by special admin-only routes where videos and images can be uploaded using WTForms.


Existing Solutions
A private account on any major social media site like Instagram or Twitter (X??). However, this would deny some control on the site like advertising decisions and user privacy.


## Related projects:
I also design web-apps as a gig on Fiver. You can check that out here: https://www.fiverr.com/s/1ozAdp
