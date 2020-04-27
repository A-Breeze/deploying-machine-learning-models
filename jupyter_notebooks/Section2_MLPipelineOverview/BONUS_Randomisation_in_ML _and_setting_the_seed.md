## Reproducibility in Machine Learning

Reproducibility in machine learning modeling is an important problem faced by data scientists and companies seeking to put machine learning models into production. Reproducibility means that given the same inputs, we should obtain exactly the same outputs. And this is for both our research and our production environment. In other words, our research models and our deployed models should produce the same score for the same input.

There are tremendous costs to irreproducible machine learning models including:

- Financial costs
- Time costs (lost time)
- Reputational costs
- Compliance costs
- Regulatory costs

The problems with reproducibility can arise in any and all of the machine learning building pipeline steps:

- Data gathering
- Feature extraction and feature engineering
- Feature selection
- Model building
- Data scoring

This is because all these steps involve elements of randomness. For example, if gathering data with SQL, there is an element of randomness when retrieving the rows from the database. During feature engineering, if we replace missing information by a random extraction of non-missing observations, we are introducing another layer of randomness. Machine learning models and feature selection algorithms involve randomness during model fitting. Think for example Random Forests; there is an element of randomness to select the features at each split, as well as to bootrstrap a sample of the dataset to fit each tree. For neural networks there is an element of randomness to initialise the network weights.

In a future section, we will show you how to tackle reproducibility between research and deployment pipelines.

For this section, please go ahead and get familiar with randomness in computer science and machine learning by visiting the following resources:

- [Why do we need randomness?](https://www.kdnuggets.com/2017/06/surprising-complexity-randomness.html)
- [Embrace Randomness in Machine Learning](https://machinelearningmastery.com/randomness-in-machine-learning/)
- [Random Number Generators for ML in python](https://machinelearningmastery.com/introduction-to-random-number-generators-for-machine-learning/)
