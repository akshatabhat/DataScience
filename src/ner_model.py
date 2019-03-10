import sys
from tqdm import tqdm
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn import metrics
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2

sys.path.append('../utils')

import letterFeatures, posFeatures

import nltk
nltk.download('averaged_perceptron_tagger')
	
def generate_features(data):
	print("---------- Generating features ---------- ")
	X = []
	for index, row in tqdm(data.iterrows()):
		features = []

		#print("row : ", row)
		
		# Generate Letter Fetures

		features.append(letterFeatures.firstLetterCapital(row))
		features.append(letterFeatures.allCapitals(row))
		#features.append(letterFeatures.allLower(row))
		features.append(letterFeatures.isFirstLetterAlphabet(row))
		#features.append(letterFeatures.containsDigits(row))
		features.append(letterFeatures.stringLen(row))
		features.append(letterFeatures.numWords(row))
		features.append(letterFeatures.isFirstLetterofAnyWordCapital(row))
		features.append(letterFeatures.doesTheStringContainQuotes(row))
		features.append(letterFeatures.isItPrecededByThe(row))
		features.append(letterFeatures.numberOfVowels(row))
		features.append(letterFeatures.nextWordISsaid(row))
		features.append(letterFeatures.isItPrecededByIn(row))
		features.append(letterFeatures.isFirstLetterofEveryWordCapital(row))
		# POS Tagging Features

		features += posFeatures.posCounts(row)
		features += posFeatures.posCountsNGram(row) # 1-gram

		X.append(features)

		
	X = np.asarray(X)
	print("Total number of features : ", X.shape[1], "\n")

	return X

def feature_selection(X, Y, method):
	print("---------- Performing feature selection using", method, " ---------- ", )
	if method == 'threshold':
		sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
		X = sel.fit_transform(X)
	elif method == 'select-k-best':
		sel = SelectKBest(score_func=chi2, k=130)
		X = sel.fit_transform(X, Y)

	print("Number of features selected : ", X.shape[1], "\n")
	return X

def create_grid_for_CV():
	# Number of trees in random forest
	n_estimators = [int(x) for x in np.linspace(start = 10, stop = 1000, num = 50)]
	# Number of features to consider at every split
	max_features = ['auto', 'sqrt']
	# Maximum number of levels in tree
	max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
	max_depth.append(None)
	# Minimum number of samples required to split a node
	min_samples_split = [2, 5, 10]
	# Minimum number of samples required at each leaf node
	min_samples_leaf = [1, 2, 4]
	# Method of selecting samples for training each tree
	bootstrap = [True, False]
	# Create the random grid
	random_grid = {'n_estimators': n_estimators,
	               'max_features': max_features,
	               'max_depth': max_depth,
	               'min_samples_split': min_samples_split,
	               'min_samples_leaf': min_samples_leaf,
	               'bootstrap': bootstrap}
	
	return random_grid
	
def training(X_train, Y_train, method, random_grid):
	print("---------- Building model ----------")

	if method == "Logistic Regression":
		model = LogisticRegression(C=1e5, solver='lbfgs')
		model.fit(X_train, Y_train)
	elif method == "Support Vector Machine":
		model = SVC(gamma='scale')
		model.fit(X_train, Y_train) 
	elif method == "Decision Tree Classifier":
		model = DecisionTreeClassifier()
		model.fit(X_train, Y_train)
	elif method == "Random Forest":
		model = RandomForestClassifier(random_state = 42)
		#model.fit(X_train, Y_train)
		rf_random = RandomizedSearchCV(estimator = model, param_distributions = random_grid, n_iter = 2, cv = 3, verbose=2, random_state=42, n_jobs = -1)
		rf_random.fit(X_train, Y_train)
		print(rf_random.best_params_)
		print(rf_random.cv_results_)
		model = rf_random
	else:
		print("Incorrect Input")
	return model

def evaluate_model(X_test, Y_test, model):
	Y_pred = model.predict(X_test)

	false_neg_idx = np.where((Y_test==1) & (Y_pred==0)) # False Negative

	false_pos_idx = np.where((Y_pred==1) & (Y_test==0)) # False Positive


	accuracy = metrics.accuracy_score(Y_test, Y_pred)
	precision = metrics.precision_score(Y_test, Y_pred) # tp/(tp+fp)
	recall = metrics.recall_score(Y_test, Y_pred) # tp/(tp+fn)
	f1_score = metrics.f1_score(Y_test, Y_pred)
	print("accuracy : ", accuracy)  
	print("Precision : ", precision)
	print("Recall : ", recall)
	print("f1-score : ", f1_score)
	print("")
	return false_pos_idx, false_neg_idx

def build_ner_model(data_train, data_test, method):
	print("----------",method,"----------")
	print("---------- Training Phase ----------")


	# Generate feature matrix
	X_train = generate_features(data_train)
	Y_train = data_train['labels'].astype(int)
	print("Class Distribution of training data : ", np.unique(Y_train, return_counts = True)), "\n"

	# Feature Selection 
	# X_train = feature_selection(X_train, Y, 'select-k-best')

	# Creating Grid for CV
	random_grid = create_grid_for_CV()

	# Training model
	model = training(X_train, Y_train, method, random_grid)

	# Evaluating the model with training data

	print("---------- Evaluation performance on training data ----------")

	false_pos_idx, false_neg_idx = evaluate_model(X_train, Y_train, model)
	#data_train.iloc[false_pos_idx[0], :].reset_index().to_pickle('../result/'+method+'_false_pos_train.pkl')
	#data_train.iloc[false_neg_idx[0], :].reset_index().to_pickle('../result/'+method+'_false_neg_train.pkl')

	print("---------- Testing Phase ----------")
	# Evaluting the model
	X_test = generate_features(data_test)
	Y_test = data_test['labels'].astype(int)
	print("---------- Evaluation performance on test data ----------")
	print("Class Distribution of test data : ", np.unique(Y_test, return_counts = True), "\n")

	false_pos_idx, false_neg_idx = evaluate_model(X_test, Y_test, model)
	#data_test.iloc[false_pos_idx[0], :].reset_index().to_pickle('../result/'+method+'_false_pos.pkl')
	#data_test.iloc[false_neg_idx[0], :].reset_index().to_pickle('../result/'+method+'_false_neg.pkl')



