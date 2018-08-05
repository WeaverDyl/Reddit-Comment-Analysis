import praw
import time
import codecs
import re

initial_file = open('data/initial.csv', 'a+', encoding='utf-8') # Where to store initial comment info
initial_file.seek(0) # Move file pointer to beginning
final_file = open('data/final.csv', 'a+', encoding='utf-8') # Where to store final comment info
final_file.seek(0) # Move file pointer to beginning

comment_num = 1 # Used to represent the current comment being looked at (for run_initial)

def authenticate():
    """Logs in to Reddit through PRAW so data collection can start."""
    reddit = praw.Reddit('datacollector', user_agent="ENTER A USER AGENT HERE")
    return reddit
    
# INITIAL
def run_initial(reddit):
    """Takes a Reddit instance and prints a bunch of useful information to
    "initial_file". Skip any comments with issues."""
    COMMENTS_TO_GET = 10000 # How many comments we want total
    global comment_num
    print("RUNNING INITIAL")
    print("-------------------------- AWAKE -------------------------------")
    while comment_num < COMMENTS_TO_GET:
        for comment in reddit.subreddit('all').comments(limit=25):
            # Ensure we're only getting the number of comments the user wants
            # while comment_num <= COMMENTS_TO_GET:
            try:
                # Write the information to the initial file
                initial_file.write(f"{comment_num},{comment.author.name}," + 
                                    f"{str(int(reddit.redditor(comment.author.name).created_utc))}," + 
                                    f"{str(reddit.redditor(comment.author.name).link_karma + reddit.redditor(comment.author.name).comment_karma)}," + 
                                    f"{comment.subreddit.display_name},{comment.permalink}," + 
                                    f"{comment.id},{len(comment.body)}\n")
                print(comment_num) # Just so the user knows the current progress
                comment_num += 1
            except Exception as e:
                # If an error occurs, skip the comment and collect another one instead
                print(str(e))
                pass
        # After collecting 25 comments, sleep and flush the buffer
        print("-------------------------- ASLEEP -------------------------------")
        initial_file.flush()
        time.sleep(5)
    # If we finish early, just return
    print("INITIAL DONE")
    return


# FINAL
def get_ids():
    """Gets all of the comment ids from the initial file so
    the program can get the same comment information later."""
    ids = []
    for line in initial_file.readlines():
        row = line.split(',')
        ids.append(row[6]) # ID's are the 7th element (index 6)
    return ids

def run_final(reddit):
    """Takes a Reddit instance and prints a bunch of useful information to
    "final_file". If the comment was deleted, print as much information
    as possible, and fill the rest with placeholder info."""
    global comment_num
    print("RUNNING FINAL")
    ids = get_ids() # Get all of the initial comment ids
    for comment_id in ids:
        # Get the comment based on its id
        comment = reddit.comment(id=comment_id)
        try:
            comment.refresh() # Refresh the comment (fixes # of replies)
            # Write all of the information needed
            final_file.write(f"{comment_num}," +
                             f"{comment.author.name}," +
                             f"{str(reddit.redditor(comment.author.name).link_karma + reddit.redditor(comment.author.name).comment_karma)}," +
                             f"{comment.score},{len(comment.replies)},{comment.permalink}," +
                             f"{comment.id},{len(comment.body)}\n")
            print(comment_num) # Just so the user knows the current progress
            comment_num += 1
        except Exception as e:
            print(str(e))
            # If an exception occurs, the comment was probably deleted. We know the comment
            # number and the id, so print those. Assume a score of 0
            final_file.write(f"{comment_num},Deleted/Removed,Deleted/Removed,0,Deleted/Removed,Deleted/Removed," +
                             f"{comment.id},Deleted/Removed\n")
            print(comment_num)
            comment_num += 1 # Just so the user knows the current progress
    print("FINAL DONE")
    return

if __name__ == "__main__":
    reddit = authenticate()
    run_initial(reddit) # Comment out if getting final data
    #run_final(reddit) # Comment out if getting initial data