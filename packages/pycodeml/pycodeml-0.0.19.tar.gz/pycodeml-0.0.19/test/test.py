

from sklearn.datasets import fetch_california_housing
data = fetch_california_housing()

import pandas as pd
df = pd.DataFrame(data.data,columns=data.feature_names)
df['MedHouseVal'] = data.target

from PyCodeml.regressor import RegressorTrainer
trainer = RegressorTrainer(df, 'MedHouseVal', data_sample_percent=50)
best_model = trainer.train_and_get_best_model()
trainer.save_best_model(path='model33333.pkl')