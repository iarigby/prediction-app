from flasgger import Swagger

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config["specs_route"] = "/docs"

swagger_template = {
    "info": {
        "title": "Breast Cancer Prediction API",
    }
}
