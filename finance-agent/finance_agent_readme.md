# Finance Headline Classifier

This project uses a local GAIA agent to classify finance headlines as **good**, **neutral**, or **bad**.

## Purpose

The reasoning of why I did this project is that I have a difficult time reading the news as a whole. I tend to always treat different news the wrong way, and it can be a struggle. This helps me solve that problem and makes it easier to understand. Also, I invest in the stock market, whether that's leaving money in an index fund or actively trading, so this tool could potentially help me make a decision on whether to buy, sell, or hold a trade. 

## What it does
- Accesses headlines from URL
- Sends each headline to the agent
- Prints the headline and the agent’s answer

## How to run
1. Open the project in VS Code
2. Make sure your GAIA environment is set up (activate virual enviornment, activate GAIA & Lemonade)
3. Run the agent script
4. Enter the URL to the headline you want to test

## Output
The script prints each selected headline and the agent’s answer in the terminal in one word: good, neutral, or bad.

## Errors
After reviewing the code, I realized that the clean_label() function returned anything the agent didn't know as neutral. Therefore, the neutral number could be inflated and can influence any other results. This has been updated so errors will return as "Unknown".

## What I Learned
From this project, I learned how to apply the basics of GAIA to make something that can be realistically used. I learned how to create virtual enviornments, Python formatting and classes, and how to set models for the agent to default to using. I also learned parsing, different encodings(utf-8, latin-1) and much more.

## What I Would Do Next
With this, I think it would be a good idea to replicate a Perplexity Task. I would have it automatically open up with my computer, pull the latest news from the internet, depict whether the news is good, bad, or neutral, and report back.

## Notes
- The agent returns one of three labels: **good**, **neutral**, or **bad**
- The sample size can be changed in the script
- This project is a baseline classifier, not a final model
