# Data
import pandas as pd
import numpy as np

# Graphics
import seaborn as sns ; sns.set()

# Machine learning - Preprocessing
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer

# Machine learning - Automatisation
from sklearn.pipeline import Pipeline
from sklearn import set_config

# Machine learning - Models
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.naive_bayes import ComplementNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

# Machine learning - Model selection
from sklearn.model_selection import train_test_split, GridSearchCV

# Machine learning - Metrics
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay, f1_score, fbeta_score, recall_score, fbeta_score, make_scorer, roc_curve, classification_report, mean_squared_error
from sklearn.preprocessing import LabelEncoder, RobustScaler, StandardScaler

# sql
from sqlalchemy import create_engine
from dotenv import load_dotenv

# others 
import os