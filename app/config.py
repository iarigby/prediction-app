import os

from flasgger import Swagger

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config["specs_route"] = "/docs"

script_name = os.environ.get('SCRIPT_NAME')
if script_name is None:
    swagger_config["basePath"] = script_name
else:
    swagger_config["basePath"] = "/api"

swagger_template = {
    "info": {
        "title": "Breast Cancer Prediction API",
    }
}
