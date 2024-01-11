import matplotlib as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

df = pd.read_csv("Loan_Data.csv")
X = df.values[:, 1:7]
y = df.values[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

dtree = DecisionTreeClassifier(max_depth=4)
dtree = dtree.fit(X_train, y_train)
tree.plot_tree(dtree, fontsize=10, feature_names=list(df.columns[1:7]))
# plt.pyplot.show()
y_pred_en = dtree.predict(X_test)
print(("Accuracy is"), accuracy_score(y_test, y_pred_en) * 100)


def expected_loss(customer_data):
    predict = dtree.predict([customer_data])
    print("Prediction of default is ", predict)
    return predict * customer_data[1] * 0.9

n = 18
test_point = df.values[n, 1:7]
print("Default actual is ", df.values[n, 7])
print(expected_loss(test_point))
