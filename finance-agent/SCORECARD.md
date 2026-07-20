# SCORECARD

## Project
Finance headline classifier

## Goal
Build a local GAIA agent that classifies finance headlines as good, neutral, or bad.

## Test setup
- Input file: Financial PhraseBank's "Sentences_66Agree"
- Sample size: 150 random headlines
- Model: GAIA local model
- Labels: good, neutral, bad

## Results
- Accuracy: 0.893/1

## Confusion matrix summary
- Most common mix-up: neutral predicted as good
- Other mistakes: good predicted as neutral

## Notes
- The agent works best on clear headlines.
- Ambiguous headlines are harder to classify.
- This is a baseline project, not a final model.
