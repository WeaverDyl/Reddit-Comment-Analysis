import praw
import config
import time
import codecs
import re

initial_file = open('', 'a+', encoding='utf-8') # Where to store initial comment info
initial_file.seek(0) # Move file pointer to beginning
final_file = open('', 'a+', encoding='utf-8') # Where to store final comment info
final_file.seek(0) # Move file pointer to beginning

comment_num = 1 # Used to represent the current comment being looked at (for run_initial)
COMMENTS_TO_GET = 10000 # How many comments we want total

def login():
    r = praw.Reddit(username = config.username, 
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = config.user_agent)
    return r
    
    
# INITIAL
def run_initial(r):
    """
    Takes a Reddit instance and prints a bunch of useful information to
    "initial_file". Skip any comments with issues
    """
    global comment_num
    print("-------------------------- AWAKE -------------------------------")
    while comment_num < COMMENTS_TO_GET:
        for comment in r.subreddit('all').comments(limit=25):
            # Ensure we're only getting the number of comments the user wants
            # while comment_num <= COMMENTS_TO_GET:
            try:
                # Write the information to the initial file
                initial_file.write(f"{comment_num},{comment.author.name}," + 
                                    f"{str(int(r.redditor(comment.author.name).created_utc))}," + 
                                    f"{str(r.redditor(comment.author.name).link_karma + r.redditor(comment.author.name).comment_karma)}," + 
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
    print("done")
    return


# FINAL
def get_ids():
    """
    Gets all of the comment ids from the initial file so
    the program can get the same comment information later
    """
    ids = []
    for line in initial_file.readlines():
        row = line.split(',')
        ids.append(row[6]) # ID's are the 7th element (index 6)
    return ids

def run_final(r):
    """
    Takes a Reddit instance and prints a bunch of useful information to
    "final_file". If the comment was deleted, print as much information
    as possible, and fill the rest with placeholder info
    """
    global comment_num
    ids = get_ids() # Get all of the initial comment ids
    for comment_id in ids:

        # Get the comment based on its id
        comment = r.comment(id=comment_id)
        try:
            comment.refresh() # Refresh the comment (fixes # of replies)
            # Write all of the information needed
            final_file.write(f"{comment_num}," +
                             f"{comment.author.name}," +
                             f"{str(r.redditor(comment.author.name).link_karma + r.redditor(comment.author.name).comment_karma)}," +
                             f"{comment.score},{len(comment.replies)},{comment.permalink}," +
                             f"{comment.id},{len(comment.body)}\n")
            print(comment_num) # Just so the user knows the current progress
            comment_num += 1
        except Exception as e:
            print(str(e))
            # If an exception occurs, the comment was probably deleted. We know the comment
            # number and the id, so print those. Assume a score of 0
            final_file.write(f"{comment_num},0,0,0,Deleted/Removed,Deleted/Removed," +
                             f"{comment.id},Deleted/Removed\n")
            print(comment_num)
            comment_num += 1 # Just so the user knows the current progress

if __name__ == "__main__":
    r = login()
    #run_initial(r) # Comment out if getting final data
    run_final(r) # Comment out if getting initial data