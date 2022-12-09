from app import model
import pytest


def test_malignant_prediction():
	values = [17.77, 1326.0, 0.0869, 74.08, 0.0186, 0.003532, 0.1238, 0.2416, 0.275, 0.08902]
	data = create_data_dict(values)
	assert model.predict(data) == 1


def test_benign_prediction():
	values = [14.36, 566.3, 0.06664, 23.56, 0.02387, 0.0023, 0.144, 0.239, 0.2977, 0.07259]
	data = create_data_dict(values)
	assert model.predict(data) == 0


def test_attribute_checking():
	values = [14.36, 566.3, 0.06664, 23.56, 0.02387, 0.0023, 0.144, 0.239, 0.2977, 0.07259]
	data = create_data_dict(values)
	del data[model.columns[0]]
	with pytest.raises(AttributeError):
		model.predict(data)


def create_data_dict(data):
	return {model.columns[i]: data[i] for i in range(len(model.columns))}
