# Reddit Comment Analysis

## About
This was much more of a curiosity project than anything else. I wanted to learn some more Python, as I haven't used the language for much in the past. I figured Python is the perfect language to write a Reddit bot in (because of [PRAW](https://praw.readthedocs.io/en/latest/), of course. I didn't want to make a bot that replies to comments (those are super annoying and overdone at this point), so I had to think of something else. I settled on a data collection bot that I can use to compile statistics based on comment patterns. It's not complicated (code-wise), but I made it in hoped that the results would be interesting.

My idea was to collect a bunch of Reddit comments on one day of the week, and then to collect any changes to those comments a day later (account karma gains, how many comments were deleted, etc...) and then collect a different set of comment data on a different day of the week and then repeat the process.

My data (the data provided in this repo) consists of 10,000 comments collected from [/r/all](https://www.reddit.com/r/all/) on Monday, 6/18, as well as any changes from those comments, which was collected on Tuesday, 6/19. I then collected 10,000 different comments on the following Saturday, 6/23, and collected the same data (with any differences) on Sunday, 6/24.

These are my results. It's worth noting that these results are definitely not super scientific or anything. This was purely just a learning experience.

In the future, I'd like to do a longer experiment, perhaps a week or two between collecting initial and final data. Both of the trials I ran with this lasted 24 hours, and it limited some of the results more than I expected.

## Setup
The only outside libraries you'll need to run this project yourself are [PRAW](https://praw.readthedocs.io/en/latest/), and [Matplotlib](https://matplotlib.org/). Both are available via pip.

Then you need to setup a script application on Reddit, and enter the login information in the `config.py` file. See instructions [here](https://praw.readthedocs.io/en/latest/getting_started/authentication.html). 

At the top of `bot.py`, add the relative path to your initial file and final file locations. `bot.py` should then run without issue.

In the middle of `data.py`, at the top of the `print_data_to_file` method, add a location where you would like some statistics printed. Then, at the bottom of `data.py`, in `main`, add the relative path to your initial file and final file locations. `data.py` should then run without issue.

Once those are setup, you're ready to collect data. You can set the subreddit as well as the number of comments you'd like to collect within `bot.py` Then, simply run `python bot.py` with the `run_initial(r)` method uncommented, and the `run_final(r)` method commented out. Once you have your data, run `bot.py` again with `run_initial(r)` commented out and `run_final(r)` uncommented. These method calls are made in `main`.

## Findings

### Initial Data
The full results are available in [`data/monday-tuesday/results.txt`](data/monday-tuesday/results.txt), but I will go over the basics here.

Relatively unsurprisingly, of the 10,000 comments I collected, the most, 517, in fact, came from [r/AskReddit](https://www.reddit.com/r/AskReddit/). See the chart below to see other top subreddits from my data.
![image](https://i.imgur.com/7SkM2Ep.png)

Overall, I collected comments from a staggering 2795 subreddits.

There were many interesting stats from the accounts that made the comments as well. The average account from the comments I collected was made on September 15th, 2015. The oldest account I collected was made on September 19th, 2005 (oddly similar dates compared with the average). The average account had 153 total karma.

In total, there were 401 deleted or removed comments. After 24 hours, the average comment had a score of just over 8, and the average number of replies was just over 0.5.
![image](https://i.imgur.com/p5cRaiA.png)

Again, to see more complete data, check the [`data/monday-tuesday/results.txt`](data/monday-tuesday/results.txt) file.

### Final Data
The full results are available in [`data/saturday-sunday/results.txt`](data/saturday-sunday/results.txt), but I will go over the basics here.

Again, as with the monday-tuesday results, most of the comments (by a wide margin), came from [r/AskReddit](https://www.reddit.com/r/AskReddit/). See the chart below to see other top subreddits.
![image](https://i.imgur.com/Dh2nMOQ.png)

This time around, I collected comments from 2818 subreddits, a number very similar to the previous 2795.

The oldest account I collected was made on September 13th, 2005, while the average account I collected data from was made on November 6th, 2015. The average account had 165 total karma.

In total, there were 399 deleted or removed comments. After 24 hours, the average comment had a score of just over 9, and the average number of replies was just over .5.
![image](https://i.imgur.com/emmRoOH.png)

Again, to see more complete data, check the [`data/saturday-sunday/results.txt`](data/saturday-sunday/results.txt) file.

### Overall Conclusions
After looking at the results, I would like to do multiple, longer length runs of this project. I am planning on doing multiple week long experiments and comparing those results. When I do these, I will attach the results to a new `README`, and hopefully the results will be a little more interesting.

One thing I noticed from the data is the popularity of certain subreddits during/after certain events have happened. There are examples of this in both the initial and final data sets, actually. 

In the initial data set, which has comments from Monday, June 18th, [r/hiphopheads](https://www.reddit.com/r/hiphopheads/) was the third most popular subreddit in [r/all](https://www.reddit.com/r/all/) with regards to number of comments. This can be attributed to the [murder of popular rapper XXXTentacion](https://en.wikipedia.org/wiki/Murder_of_XXXTentacion).

In the final data set, [r/soccer](https://www.reddit.com/r/soccer/) had the second most comments of any subreddit in [r/all](https://www.reddit.com/r/all/), and this can be attributed to the World Cup.

Overall, the data was very similar (much more so than I expected. [r/AskReddit](https://www.reddit.com/r/AskReddit/) was the most popular subreddit in both data sets, but that's about the only similarity I expected. Of the comments that I collected, the average age of the accounts from both data sets differed by only months, and the oldest account from both sets differed by only TWO days.

Everything else was very similar too. From the average account karma, to the average comment score after a day, to the average number of replies, I would have never expected all of these to be so close together.

Ultimately, this deserves to be looked further into with more trials, each of a longer period. And that's what I plan to do, as I've mentioned.

## LICENSE
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
