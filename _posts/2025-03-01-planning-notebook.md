---
layout: post
title: Planning radio networks, can you do better than my students?
date: 2025-03-01 08:57:00-0400
description: Follow through this basic radio planning notebook, and see if you can do better than my students.
tags: planning jupyter MRN
categories: teaching
giscus_comments: false
related_posts: false
---

In the context of mobile radio networks, radio planning means finding the optimal number and position of base stations to be installed in a given area. The optimality is evaluated against particular network objectives. The simplest objective one can imagine is to maximize the coverage in the given area, whatever that means, while being constrained to a monetary budget. 

Wireless networks are expensive both to deploy and operate. That's why radio planning is essential for operators. With a good network plan, they can get the most out of their often limited budget. 

I learned about radio planning during my M.Sc., but I kind of ignored it at that time. I discovered the beauty of it only during my first year of PhD when I finally started working on it practically. 

I wanted to bring the same experience to my students, so I wrote this jupyter notebook, where I guide them through a very simple network planning instance. Most of the code is used to prepare the data, namely the positions of base stations and users, as well as the propagation data. 

When the data is ready, one can finally solve the planning. That's easier said than done, as usual. Even the simplest planning we can imagine (like this one) is NP-Hard. Fortunately, a network plan can take hours or days to solve since it's an operation done once in a long while. 

We couldn't leave the lecture without seeing a solution, and I also wanted to give my students a little improvised challenge. So I wrote a pretty bad heuristic algorithm and left them 30 minutes to modify it. Whoever could modify it to increase the performance (in terms of increased coverage) would pass the challenge and get half a point. I also gave 1 point to the best-performing heuristic. 

I prepared a form where they could upload their solution, with a backend that evaluated each submission and updated a live leaderboard that I projected in the class during the challenge. When solutions started to come up on the leaderboard, I felt a mixture of satisfaction and relief; it was working! Not only did my students understand what network planning means, but they also found ways to improve my solution. 

After 30 minutes, 22 out of 28 participants could pass the challenge. Two of them who got the highest score managed to get a solution that was only 2 % worse than the optimal. I was pretty impressed. 

That challenge is close now, but that doesn't mean you can't still try. Can you do better than my students? You'll find the jupyter notebook here on this page. If not, you will still learn something about radio planning.

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/MRN_25_Radio_channel_and_planning_primer.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/blog.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
{% jupyter_notebook jupyter_path %}
{% else %}

<p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}

