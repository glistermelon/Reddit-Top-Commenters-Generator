# Reddit Top Commenters Generator
Finds the redditors with the most upvotes (comments only, not submissions) within a certain timeframe.
No restrictions on time range, nor the amount of data gathered, but more time = more data = a very long runtime.
In particular, any post with many nested comments will take a very long time to process due to reddit's morechildren API.
When you run the file, it walks you through the input process.
Anyone looking to do more than get simple txt output results can easily modify the code; it's not complex at all.

### Fixed thanks to [Arctic Shift by Arthur Heitmann](https://github.com/ArthurHeitmann/arctic_shift).
Note that if that api is down, this won't work. I am working on a different script that does not have this problem.