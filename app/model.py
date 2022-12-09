import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings
import pandas as pd


resources_dir = 'app/resources'


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    ml_model: LogisticRegression = pickle.load(open(resources_dir + '/model.pkl', 'rb'))
    scaler: StandardScaler = pickle.load(open(resources_dir + '/scaler.pkl', 'rb'))

columns = ['texture_mean', 'area_mean', 'concavity_mean', 'area_se',
           'concavity_se', 'fractal_dimension_se', 'smoothness_worst',
           'concavity_worst', 'symmetry_worst', 'fractal_dimension_worst']


def predict(data_dict: dict) -> int:
    transformed_data = dict_to_df(data_dict)
    [prediction] = ml_model.predict(transformed_data)
    return prediction


def dict_to_df(data_dict: dict) -> pd.DataFrame:
    """
    checks if data_dict has all necessary keys
    converts each value to list in order to create data frame
    scales the values
    :param data_dict: dict where keys are columns and values are int
    :return: data that is ready to be passed to LogisticRegression prediction
    """
    if sorted(data_dict.keys()) != sorted(columns):
        raise AttributeError()
    for k in data_dict.keys():
        data_dict[k] = [data_dict[k]]
    data = pd.DataFrame(data_dict, columns=columns)
    return scaler.transform(data)
