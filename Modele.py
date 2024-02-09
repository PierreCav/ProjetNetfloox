from imports import *

load_dotenv('BDD_URL.env')
BDD_URL = os.environ['BDD_URL']
engine = create_engine(BDD_URL)
SQL = 'SELECT "averageRating", "startYear", "runtimeMinutes" from principal.title_basics join principal.title_ratings on principal.title_basics."tconst" = principal.title_ratings."tconst"  limit 50000;'
data = pd.read_sql(SQL, engine)
numcat = 5

# PreProcessing
for column in ["averageRating", "startYear", "runtimeMinutes"]:
    data[column].fillna(data[column].mean(), inplace=True)

# Features
X = data[['startYear','runtimeMinutes']]
# Target
y = data['averageRating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

pred = model.predict(X_test_scaled)
accure = mean_squared_error(y_test, pred)
print('accuracy:', accure)







""" 

preparation = ColumnTransformer(
    transformers=[
        ('data_num', RobustScaler(), ["startYear","runtimeMinutes"])
])

# Pipeline
pipel = Pipeline(steps=[
                        ('vector/Scale', preparation),
                        ('modelisation', LinearRegression())
                        ])

params = {
    'modelisation': [LogisticRegression(), KNeighborsClassifier(), DecisionTreeClassifier(), LinearRegression()],
}

scorer = {'accuracy': 'accuracy', 'recall': make_scorer(recall_score, pos_label="note")}

searchCV = GridSearchCV(pipel, params, scoring=scorer, refit='recall')

searchCV.fit(X_train,y_train)
y_pred = searchCV.predict(X_test)

print("Score training:", searchCV.best_score_)
print("Score recall test:", accuracy_score(y_pred, y_test, pos_label="note"))
print("Le modèle de ML utilisé c'est le", searchCV.best_params_['modelisation'])

engine.dispose() """