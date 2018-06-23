# Reddit Comment Analysis

## About
This was much more of a curiosity project than anything else. I wanted to learn some more Python, as I haven't used the language for much in the past. I figured Python is the perfect language to write a Reddit bot in (because of [PRAW](https://praw.readthedocs.io/en/latest/), of course. I didn't want to make a bot that replies to comments (those are super annoying and overdone at this point), so I had to think of something else. I settled on a data collection bot that I can use to compile statistics based on comment patterns. It's not complicated, but I made it in hoped that the results would be interesting.

My idea was to collect a bunch of Reddit comments on one day of the week, and then to collect any changes to those comments a day later (account karma gains, how many comments were deleted, etc...) and then collect a different set of comment data on a different day of the week and then repeat the process.

My data (the data provided in this repo) consists of 10,000 comments collected from [/r/all](https://www.reddit.com/r/all/) on Monday, 6/18, as well as any changes from those comments, which was collected on Tuesday, 6/19. I then collected 10,000 different comments on the following Saturday, 6/23, and collected the same data (with any differences) on Sunday, 6/24.

These are my results. It's worth noting that these results are definitely not super scientific or anything. This was purely just a learning experience.

In the future, I'd like to do a longer experiment, perhaps a week or two between collecting initial and final data. Both of the trials I ran with this lasted 24 hours, and it limited some of the results more than I expected.

## Setup
The only outside libraries you'll need to run this project yourself are [PRAW](https://praw.readthedocs.io/en/latest/), and [Matplotlib](https://matplotlib.org/). Both are available via pip.

Once those are setup, you're ready to collect data. You can set the subreddit as well as the number of comments you'd like to collect within `bot.py` Then, simply run `python bot.py`.

Make sure that if you run `bot.py` more than once, that you have copied the original files in some way, because `initial.csv` and `final.csv` will be overwritten upon any runs after the initial.

## Findings

### Initial Data
The full results are available in [results.txt](data/monday-tuesday/results.txt), but I will go over the basics here.

Relatively unsurprisingly, of the 10,000 comments I collected, the most, 517, in fact, came from [r/AskReddit](https://www.reddit.com/r/AskReddit/). See the chart below to see other top subreddits from my data.
![image](https://i.imgur.com/7SkM2Ep.png)

Overall, I collected comments from a staggering 2795 subreddits.

There were many interesting stats from the accounts that made the comments as well. The average account from the comments I collected was made on September 15th, 2015. The oldest account I collected was made on September 19th, 2005 (oddly similar dates compared with the average). The average account had 153 total karma.

In total, there were 401 deleted or removed comments. After 24 hours, the average comment had just over 8 upvotes, and the average number of replies was just over 0.5.

Again, to see more complete data, check the [results.txt](data/monday-tuesday/results.txt) file.

### Final Data
More to come soon

### Overall Conclusions
More to come soon

## LICENSE
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
