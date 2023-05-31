# NO LONGER FUNCTIONING AS PUSHSHIFT API IS DEAD
I am looking into it, but it seems the only way forward will have to involve some other scraping API or there is no way forward. Top commenters earlier than March 2023 may still be generated for some subreddits using this data gathered by u/Watchful1: https://www.reddit.com/r/pushshift/comments/11ef9if. Will update this script appropriately after further research.
# Reddit Top Commenters Generator
Finds the redditors with the most upvotes (comments only, not submissions) within a certain timeframe.
No restrictions on time range, nor the amount of data gathered, but more time = more data = a very long runtime.
In particular, any post with many nested comments will take a very long time to process due to reddit's morechildren API.
When you run the file, it walks you through the input process.
Anyone looking to do more than get simple txt output results can easily modify the code; it's not complex at all.
