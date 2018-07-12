import re
import time
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

class Inital_Comment(object):
    """Makes generating statistics about comments easier."""
    def __init__(self, comment_number, comment_author, account_creation_time, 
                 account_karma, comment_subreddit, comment_permalink, 
                 comment_id, comment_length):
        self.comment_number = comment_number
        self.comment_author = comment_author
        self.account_creation_time = account_creation_time
        self.account_karma = account_karma
        self.comment_subreddit = comment_subreddit
        self.comment_permalink = comment_permalink
        self.comment_id = comment_id
        self.comment_length = comment_length

class Final_Comment(object):
    """Makes generating statistics about comments easier."""
    def __init__(self, comment_number, comment_author, account_karma, 
                 comment_score, comment_num_replies, comment_permalink,
                 comment_id, comment_length):
        self.comment_number = comment_number
        self.comment_author = comment_author
        self.account_karma = account_karma
        self.comment_score = comment_score
        self.comment_num_replies = comment_num_replies
        self.comment_permalink = comment_permalink
        self.comment_id = comment_id
        self.comment_length = comment_length

def create_initial_comment_objects():
    """Goes through the initial comments and returns an array 
    of objects."""
    arr = [] # Stores objects
    for line in initial_file:
        row = line.split(",") # Get each
        
        # Set object variables for each object before adding it to the array
        comment_number, comment_author, account_creation_time, account_karma, \
        comment_subreddit, comment_permalink, comment_id, \
        comment_length = [i.strip('\n') for i in row]

        # Add the comment object to the array
        arr.append(Inital_Comment(comment_number, comment_author, \
                                  account_creation_time, account_karma, \
                                  comment_subreddit, comment_permalink, \
                                  comment_id, comment_length))
    return arr


def create_final_comment_objects():
    """Goes through the final comments and returns an array 
    of objects."""
    arr = [] # Stores objects
    for line in final_file:
        row = line.split(",")
        
        # Set object variables for each object before adding it to the array
        comment_number, comment_author, account_karma, comment_score, \
        comment_num_replies, comment_permalink, comment_id, \
        comment_length = [i.strip('\n') for i in row]
        
        # Add the comment object to the array
        arr.append(Final_Comment(comment_number, comment_author, account_karma, \
                                 comment_score, comment_num_replies, \
                                 comment_permalink, comment_id, comment_length))
    return arr

def get_deleted_comments(arr_final):
    """Takes a list of (final) Comment objects and 
    returns a list of deleted comment ID's."""
    deleted_comments = []

    # Get the ID's of deleted comments
    for comment in arr_final:
        if comment.comment_author == "Deleted/Removed":
            deleted_comments.append(comment.comment_id)

    return deleted_comments

def subreddit_data(arr_initial):
    """Takes in initial comment data and returns a dictionary sorted
    in descending order by number of comments made in each subreddit."""
    # Stores subreddits and number of comments made in them
    comments_per_subreddit = defaultdict(int)
    # Go through each comment, increment value of subreddit it was posted in
    for comment in arr_initial:
        comments_per_subreddit[comment.comment_subreddit] += 1

    # Sort the dictionary by value (number of comments) in descending order
    sorted_by_comments = sorted(comments_per_subreddit.items(), key=lambda x: int(x[1]), reverse=True)
    
    return sorted_by_comments

def account_age_data(arr_initial):
    """Takes in initial comment data and returns a tuple
    of the oldest account creation date as well as the average 
    account creation date (both in unix time)."""
    oldest_account_age = int(time.time()) # Assume oldest account created now
    all_account_ages = defaultdict(int)
    total_account_age = 0 # Stores sum of all account creation times (unix time)
    data_points = len(arr_initial) # Number of comments collected

    # Calculates oldest account
    for comment in arr_initial:
        # Add comments author and account creation date to dict
        all_account_ages[comment.comment_author] = comment.account_creation_time
        # If current author created their account before the oldest known,
        # then the current comment is the current oldest account
        if int(comment.account_creation_time) < int(oldest_account_age):
            oldest_account_age = comment.account_creation_time
        # Keep track of the sum of all creation times
        total_account_age += int(comment.account_creation_time)    

    average_creation = total_account_age // data_points
    sorted_account_ages = sorted(all_account_ages.items(), key=lambda x: int(x[1]))
    # Return both oldest account age and average creation time
    return (oldest_account_age, average_creation, sorted_account_ages)

def overall_karma_gain_data(arr_initial, arr_final):
    """Takes in starting and final comment data and returns
    the average overall author karma gain in the time between 
    the data collections."""
    total_start_karma = 0 # Total overall karma in initial data
    total_final_karma = 0 # Total overall karma in final data
    deleted_comments = get_deleted_comments(arr_final)
    # Data points = total initial data - total deleted data
    data_points = len(arr_initial) - len(deleted_comments)
    all_karma_gains = defaultdict(int)

    # Calculate deleted comment ID's and total overall karma in final data
    for comment in arr_final:
        # Only look at comments that weren't later deleted
        if comment.comment_id not in deleted_comments:
            all_karma_gains[comment.comment_author] = int(comment.account_karma)
            total_final_karma += int(comment.account_karma)

    # Calculate total overall karma in initial data            
    for comment in arr_initial:
        # Only look at comments that weren't later deleted
        if comment.comment_id not in deleted_comments:
            # Go through and subtract initial account karma for all accounts
            # To get the total karma gained
            all_karma_gains[comment.comment_author] -= int(comment.account_karma)
            # For the average, keep track of all initial karmas
            total_start_karma += int(comment.account_karma)

    sorted_karma_gains = sorted(all_karma_gains.items(), key=lambda x: int(x[1]), reverse=True)
    total_gain = total_final_karma - total_start_karma # Calculate karma gains
    average_gain = total_gain / data_points
    return (average_gain, sorted_karma_gains)

def average_comment_length(arr_initial):
    """ Takes in initial comment data and returns the
    average length (in characters) of the comments."""
    total_length = 0 # Sum of all comment lengths
    data_points = len(arr_initial) # Number of comments collected

    # Add each comment's length to total_length
    for comment in arr_initial:
        total_length += int(comment.comment_length)

    average_length = total_length / data_points
    return average_length

def score_gain_data(arr_final):
    """Takes in final comment data and returns a dict containing every 
    user's comment score gains and the average comment score since the 
    initial data was taken."""
    total_gain = 0 # Sum of all comment scores
    data_points = len(arr_final) # Number of comments (incl. deleted (= 0))
    all_score_gains = defaultdict(int)

    # Go through each comment to collect the sum of all comments scores
    for comment in arr_final:
        all_score_gains[comment.comment_author] = comment.comment_score
        total_gain += int(comment.comment_score)

    # Sort the dictionary by comment score
    sorted_score_gains = sorted(all_score_gains.items(), key=lambda x: int(x[1]), reverse=True)
    average_gain = total_gain / data_points
    return (average_gain, sorted_score_gains)

def average_number_replies(arr_final):
    """Takes in final comment data and returns the average number of 
    "top-level" replies of the comments."""
    total_replies = 0 # Sum of all replies
    deleted_comments = get_deleted_comments(arr_final) # Get ID of deleted comments
    data_points = len(arr_final) - len(deleted_comments) # All non-deleted comments

    for comment in arr_final:
        # If the comment wasn't deleted, add its number of replies to the total
        if comment.comment_id not in deleted_comments:
            total_replies += int(comment.comment_num_replies)

    average_replies = total_replies / data_points
    return average_replies

def deleted_comments_data(arr_initial, arr_final):
    """Takes in initial and final comment data and returns a dictionary
    Where the keys are the subreddits where comments were collected
    and the values are the number of deleted comments in that subreddit."""
    deleted_comments = get_deleted_comments(arr_final)
    # Stores number of comments deleted per subreddit
    deleted_comments_subreddits = defaultdict(int)

    # Go through each comment in initial data to check if it was deleted
    for comment in arr_initial:
        for deleted_comment_id in deleted_comments:
            # Check if the comment ID matches a deleted comment ID
            if comment.comment_id == deleted_comment_id:
                # If it does, increment the subreddit it came from
                deleted_comments_subreddits[comment.comment_subreddit] += 1
    
    # Get sorted dictionary based on number of deleted comments
    sorted_deleted_subreddits = sorted(deleted_comments_subreddits.items(), key=lambda x: int(x[1]), reverse=True)
    return (deleted_comments, sorted_deleted_subreddits)

def print_data_to_file(arr_initial, arr_final):
    """Prints a bunch of raw data to a file, as well as some compiled
    statistics."""
    results_file = open('data/results.txt', 'w')
    
    # Returns sorted dictionaries of format ('subreddit' : num comments)
    subreddit_stats = subreddit_data(arr_initial)
    # Returns a 3-tuple of (oldest account age, average account age, all accounts ages)
    account_age_stats = account_age_data(arr_initial)
    # Returns average post + comment karms gained between initial and final data
    karma_gain_stats = overall_karma_gain_data(arr_initial, arr_final)
    # Returns the average comment length
    comment_length_stats = average_comment_length(arr_initial)
    # Returns a 2-tuple containing all score gains by user and the average score gain between initial/final data
    comment_score_stats = score_gain_data(arr_final)
    # Returns the average number of replies
    comment_reply_stats = average_number_replies(arr_final)
    # Returns a 2-tuple of (list of deleted comment ids, dict of subreddit deletion multiplicity)
    deleted_comments_stats = deleted_comments_data(arr_initial, arr_final)

    # Write basics to file (# subreddits, oldest account, avg account, etc)
    results_file.write("FAST FACTS FROM DATA:\n")
    results_file.write("\tSubreddit Stats:\n")
    results_file.write(f"\t\tMost popular subreddit: '{subreddit_stats[0][0]}' with {subreddit_stats[0][1]} comments\n")
    results_file.write(f"\t\tComments collected from {len(subreddit_stats)} subreddits total\n\n")

    results_file.write("\tAccount Statistics:\n")
    oldest_account_date = time.strftime('%m/%d/%Y', time.gmtime(int(account_age_stats[0])))
    average_account_date = time.strftime('%m/%d/%Y', time.gmtime(int(account_age_stats[1])))
    results_file.write(f"\t\tOldest account created on {oldest_account_date}\n")
    results_file.write(f"\t\tAverage account created on {average_account_date}\n")
    results_file.write(f"\t\tAverage overall (comment + post) karma gained: {karma_gain_stats[0]}\n\n")

    results_file.write("\tComment Data:\n")
    results_file.write(f"\t\tAverage comment length: {comment_length_stats} characters\n")
    results_file.write(f"\t\tAverage comment score: {comment_score_stats[0]} points\n")
    results_file.write(f"\t\tAverage number of comment replies: {comment_reply_stats}\n")
    results_file.write(f"\t\tThere were {len(deleted_comments_stats[0])} deleted or removed comments\n\n")
    
    results_file.write("FULL(ER) STATS FROM DATA:\n")
    results_file.write("\tOldest Accounts (From Collected Data):\n")
    # Print 50 oldest accounts (can be increased)
    for k,v in account_age_stats[2][0:50]:
        v = time.strftime('%m/%d/%Y', time.gmtime(int(v)))
        results_file.write(f"\t\t'{k}' Created their account on: {v}\n")
    results_file.write('\n')

    results_file.write("\tHighest Overall Karma Gains (From Collected Data):\n")
    for k,v in karma_gain_stats[1][0:25]:
        results_file.write(f"\t\t'{k}' gained: {v} overall karma\n")
    results_file.write('\n')

    results_file.write("\tHighest Upvoted Comments (From Collected Data):\n")
    # Print 25 most upvoted comments to file
    for k,v in comment_score_stats[1][0:25]:
        results_file.write(f"\t\t'{k}' had a comment with: {v} upvotes\n")
    results_file.write('\n')

    results_file.write("\tMost Commented Subreddits (From Collected Data):\n")
    # Print 25 subreddits with most comments
    for k,v in subreddit_stats[0:25]:
        results_file.write(f"\t\t'{k}' had {v} comments\n")
    results_file.write('\n')

    results_file.write("\tSubreddits With Most Deleted Comments (From Collected Data):\n")
    # Print 10 subreddits with most deleted comments
    for k,v in deleted_comments_stats[1][0:10]:
        results_file.write(f"\t\t'{k}' had {v} deleted comments\n")
    results_file.write('\n')

def subreddit_comments_chart(arr_initial, arr_final):
    """Generates a chart based on which subreddits had the most comments."""
    subreddit_info = subreddit_data(arr_initial)
    
    # Show plot of subreddits with the most comments
    plot_points = dict(subreddit_info[0:10])
    keys = list(plot_points.keys())
    values = list(plot_points.values())
    plt.title("Most Commented-in Subreddits", fontsize=20)
    plt.bar(keys, values, align='center')
    plt.xlabel('Subreddit', fontsize=20, labelpad=20)
    plt.ylabel("Number of Comments", fontsize=20,labelpad=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    # Puts number of comments above bar
    for a,b in zip(keys, values):
        plt.text(a, b, str(b), fontsize=20, horizontalalignment='center')
    plt.show()

def deleted_comments_chart(arr_initial, arr_final):
    """Generates a chart based on which subreddits had the most deleted
    comments."""
    deleted_comments_info = deleted_comments_data(arr_initial, arr_final)
    
    # Show plot of subreddits with the most comments
    plot_points = dict(deleted_comments_info[1][0:10])
    keys = list(plot_points.keys())
    values = list(plot_points.values())
    plt.title("Subreddits With Most Deleted Comments", fontsize=20)
    plt.bar(keys, values, align='center')
    plt.xlabel('Subreddit', fontsize=20, labelpad=20)
    plt.ylabel("Number of Deleted Comments", fontsize=20,labelpad=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    # Puts number of deleted comments above bar
    for a,b in zip(keys, values):
        plt.text(a, b, str(b), fontsize=20, horizontalalignment='center')
    plt.show()

if __name__ == '__main__':
    initial_file = open('data/final.csv', 'a+', encoding='utf-8') # Store initial comment info
    initial_file.seek(0) # Move file pointer to beginning
    final_file = open('data/final.csv', 'a+', encoding='utf-8') # Store final comment info
    final_file.seek(0) # Move file pointer to beginning

    initial_objs = create_initial_comment_objects() # get Initial Comment objects
    final_objs = create_final_comment_objects() # get Final Comment objects

    # Start collecting data!
    subreddit_data(initial_objs)
    account_age_data(initial_objs)
    average_comment_length(initial_objs)
    average_number_replies(final_objs)
    score_gain_data(final_objs)
    overall_karma_gain_data(initial_objs, final_objs)
    deleted_comments_data(initial_objs, final_objs)

    # Print data to file!
    print_data_to_file(initial_objs, final_objs)

    # Make plots!
    subreddit_comments_chart(initial_objs, final_objs)
    deleted_comments_chart(initial_objs, final_objs)

    # Close files
    initial_file.close()
    final_file.close()