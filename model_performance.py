"""
This code will display the results of the model
"""
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score


# Define the threshold of what probability > threshold is considered true
THRESHOLD = 0.5

empty = pd.read_csv("./outputs/batch_predictions_empty.csv")
rat = pd.read_csv("./outputs/batch_predictions_rat.csv")

# histogram to see how the model is performing
empty = pd.read_csv("./outputs/batch_predictions_empty.csv")
sns.histplot(empty['prediction'])
rat = pd.read_csv("./outputs/batch_predictions_rat.csv")
sns.histplot(rat['prediction'])

empty["actual"] = 0
rat["actual"] = 1

empty["prediction"] = empty["prediction"].apply(lambda x: 1 if x > THRESHOLD else 0)
rat["prediction"] = rat["prediction"].apply(lambda x: 1 if x > THRESHOLD else 0)

result = pd.concat([empty, rat])

cm = pd.crosstab(result['actual'], result['prediction'], rownames=['Actual'], colnames=['Predicted'])
print(cm)

print(accuracy_score(result['actual'], result['prediction']))
print(f1_score(result['actual'], result['prediction']))
print(recall_score(result['actual'], result['prediction']))
print(precision_score(result['actual'], result['prediction']))