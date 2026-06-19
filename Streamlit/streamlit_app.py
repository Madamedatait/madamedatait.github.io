import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "train.csv")
df=pd.read_csv("train.csv")
st.title("Projet de classification binaire Titanic")
st.sidebar.title("Sommaire")
pages=["Exploration", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)

if page==pages[0]:
    st.write("### Introduction")
    st.dataframe(df.head(10))
    st.write(df.shape)
    st.dataframe(df.describe())

    if st.checkbox("Afficher les NA"):
        st.dataframe(df.isna().sum())

if page==pages[1]:
    st.write("### DataVizualisation")

    fig=plt.figure()
    sns.countplot(x='Survived', data=df)
    st.pyplot(fig)

    fig=plt.figure()
    sns.countplot(x='Sex', data=df)
    plt.title("Repartition du genre des passagers")
    st.pyplot(fig)

    fig=plt.figure()
    sns.countplot(x= 'Pclass', data=df)
    plt.title("Repartition des classes des passagers")
    st.pyplot(fig)

    fig= sns.displot(x='Age', data=df)
    plt.title("Distribution de l'age des passagers")
    st.pyplot(fig)

    fig=plt.figure()
    sns.countplot(x='Survived', hue='Sex', data=df)
    st.pyplot(fig)

    fig= sns.catplot(x='Pclass', y='Survived', data=df, kind='point')
    st.pyplot(fig)

    fig=sns.lmplot(x='Age', y='Survived', hue="Pclass", data=df)
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.heatmap(df.select_dtypes(include=[np.number]).corr(), ax=ax)
    st.write(fig)

if page == pages[2]:
    st.write("### Modélisation")

    df = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)

    y = df['Survived']

    x_cat = df[['Pclass', 'Sex', 'Embarked']]
    x_num = df[['Age', 'Fare', 'SibSp', 'Parch']]

    for col in x_cat.columns:
        x_cat[col] = x_cat[col].fillna(x_cat[col].mode()[0])

    for col in x_num.columns:
        x_num[col] = x_num[col].fillna(x_num[col].median())

    x_cat_scaled = pd.get_dummies(x_cat, columns=x_cat.columns)

    x = pd.concat([x_cat_scaled, x_num], axis=1)

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    x_train[x_num.columns] = scaler.fit_transform(x_train[x_num.columns])
    x_test[x_num.columns] = scaler.transform(x_test[x_num.columns])

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix

    def prediction(classifier):

        if classifier == 'Random Forest':
            clf = RandomForestClassifier()

        elif classifier == 'SVC':
            clf = SVC()

        elif classifier == 'Logistic Regression':
            clf = LogisticRegression()

        clf.fit(x_train, y_train)

        return clf

    def scores(clf, choice):

        if choice == 'Accuracy':
            return clf.score(x_test, y_test)

        elif choice == 'Confusion matrix':
            return confusion_matrix(y_test, clf.predict(x_test))


    choix = ['Random Forest', 'SVC', 'Logistic Regression']

    option = st.selectbox('Choix du modèle', choix)

    st.write('Le modèle choisi est :', option)

    clf = prediction(option)

    display = st.radio('Que souhaitez-vous montrer ?', ('Accuracy', 'Confusion matrix'))

    if display == 'Accuracy':
        st.write(scores(clf, display))

    elif display == 'Confusion matrix':
        st.dataframe(scores(clf, display))
