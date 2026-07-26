from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def train_models(df):

    # Last column is the target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {

        "Logistic Regression": LogisticRegression(max_iter=1000),

        "Decision Tree": DecisionTreeClassifier(random_state=42),

        "Random Forest": RandomForestClassifier(random_state=42),

        "KNN": KNeighborsClassifier(),

        "SVM": SVC()

    }

    results = {}

    best_model = ""
    best_accuracy = 0

    for name, model in models.items():

        model.fit(X_train, y_train)

        prediction = model.predict(X_test)

        accuracy = accuracy_score(y_test, prediction) * 100

        accuracy = round(accuracy, 2)

        results[name] = accuracy

        if accuracy > best_accuracy:

            best_accuracy = accuracy
            best_model = name

    return best_model, best_accuracy, results