# Finance Headline Classifier

This project uses a local GAIA agent to classify finance headlines as **good**, **neutral**, or **bad**.

## What it does
- Reads finance headlines from a text file
- Randomly selects a sample of headlines
- Sends each headline to the agent
- Prints the headline and the agent’s answer
- Saves the results to a CSV file

## How to run
1. Open the project in VS Code
2. Make sure your GAIA environment is set up (activate virual enviornment, activate GAIA & Lemonade)
3. Run the agent script
4. Enter the path to your text file containing the headlines
5. Enter how many headlines you want to sample

## Output
The script prints each selected headline and the agent’s answer in the terminal. It also saves a CSV file with the headline and answer for each sampled line.

## Notes
- The agent returns one of three labels: **good**, **neutral**, or **bad**
- The sample size can be changed in the script
- This project is a baseline classifier, not a final model