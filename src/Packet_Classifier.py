import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
from sklearn.inspection import permutation_importance
from load_data import load_data
from build_flows import build_flows
from extract_features import extract_features
from write_output import write_output

class Classifiers():
    def __init__(self,data,features=None):
 
        data = shuffle(data, random_state=42)

        if features is None:
            features = ['packet_count','total_bytes','duration',
                  'packet_size_cv','packet_size_std','bytes_ratio_asymmetry','throughput','burstiness', 'iat_mean']
            self.features = features
        else :
            self.features = features
        
        print("Training with features: ",self.features)

        number_of_features = len(self.features)

        X = data[self.features]
        
        y = data['Label']

        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify  = y, random_state = 42)
    
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        self.training_data = X_train
        self.training_labels = y_train
        self.testing_data = X_test
        self.testing_labels = y_test
        self.num = number_of_features
        self.outputs = []
        self.output2 = []

    def classifyNearestNeighbors(self):
     
        clf = KNeighborsClassifier()
        
        neighbors = list(range(1, 20, 2))
        leaf_size = list(range(5, 31, 5))   

        self.param_grid = {"n_neighbors":neighbors, "leaf_size": leaf_size}
        self.name = "Nearest Neighbors"

        return self.test_clf(clf)
    
    def classifyLogisticRegression(self): 

        clf = LogisticRegression(max_iter=1000, class_weight="balanced")
        
        C = [0.1, 0.5, 1, 5, 10, 50, 100]

        self.param_grid = {"C":C}
        self.name = "Logistic Regression"

        return self.test_clf(clf)
    
    def classifyDecisionTree(self):
        
        clf = DecisionTreeClassifier(class_weight="balanced",random_state=42)
        
        max_depth = list(range(1,51,1))
        min_samples = list(range(2,11,1))

        self.param_grid = {"max_depth":max_depth, "min_samples_split":min_samples}
        self.name = "Decision Tree"

        return self.test_clf(clf)
    
    def classifyRandomForest(self):

        clf = RandomForestClassifier(class_weight="balanced",random_state=42)
        
        max_depth = list(range(1,6,1))
        min_samples = list(range(2,11,1))

        self.param_grid = {"max_depth":max_depth,  "min_samples_split":min_samples}
        self.name = "Random Forest"
    
        return self.test_clf(clf)
    
    def classifyAdaBoost(self):

        clf = AdaBoostClassifier()
        
        num_estimators = list(range(1,80,10))
        
        self.param_grid = {"n_estimators" :num_estimators}
        self.name = "AdaBoost"

        return self.test_clf(clf)
    
    def test_clf(self, clf, classifier_name=''):

        grid_search = GridSearchCV(estimator=clf, param_grid=self.param_grid, scoring='accuracy', cv=5)
        grid_search.fit(self.training_data, self.training_labels)

        training_accuracy = grid_search.best_score_
    
        best_model = grid_search.best_estimator_

        testing_accuracy = (best_model.predict(self.testing_data) == self.testing_labels).mean()

        conf_matrix = confusion_matrix(self.testing_labels, best_model.predict(self.testing_data))
        print("Confusion Matrix for", self.name ,"with",self.num,"Features:")
        print(conf_matrix)
        self.outputs.append(f"{self.name},{training_accuracy:.3f},{testing_accuracy:.3f}") 
      
        labels = ["Browsing", "Streaming", "File Download"]

        cm_df = pd.DataFrame(conf_matrix, index=labels, columns=labels)
        cm_df.to_csv(f"{self.name} Confusion Matrix with {self.num} Features.csv")

        if self.num > 6:
            return self.compute_permutation(best_model)

    def compute_permutation(self, best_model):
        perm_importance = permutation_importance(best_model, self.testing_data, self.testing_labels, n_repeats=10, random_state=42)

        perm_importance_df = pd.DataFrame({'Feature': self.features, 'Importance': perm_importance.importances_mean})
        perm_importance_df = perm_importance_df.sort_values(by='Importance', ascending=False)
        ranked_features = perm_importance_df['Feature'].tolist()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=perm_importance_df)
        plt.title(f"Permutation Feature Importance in {self.name} with {self.num} features")
        plt.savefig(f"{self.name}_importance.png")
        plt.show()
        plt.close()
        
        self.ranked_features = ranked_features[:6]
       
      
def call_models(models):
    models.classifyNearestNeighbors()
    models.classifyLogisticRegression()
    models.classifyDecisionTree()
    models.classifyRandomForest()
    models.classifyAdaBoost()
    write_output(flow_df, models) 

if __name__ == "__main__":

    df = load_data()

    flow_df = build_flows(df)
    flow_df = extract_features(flow_df)

    models = Classifiers(flow_df)
    call_models(models)
  
    reduced_models = Classifiers(flow_df, models.ranked_features)
    call_models(reduced_models)

  