from flask import Flask, request, redirect
from flasgger import Swagger

from app import model, config

app = Flask(__name__)
swagger = Swagger(app, template=config.swagger_template, config=config.swagger_config)


@app.route("/predict")
def predict():
    """Prediction endpoint
    ---
    definitions:
        DiagnosticData:
            type: object
            properties:
                texture_mean:
                    type: number
                    example: 17.77
                area_mean:
                    type: number
                    example: 1326.0
                concavity_mean:
                    type: number
                    example: 0.0869
                area_se:
                    type: number
                    example: 74.08
                concavity_se:
                    type: number
                    example: 0.0186
                fractal_dimension_se:
                    type: number
                    example: 0.003532
                smoothness_worst:
                    type: number
                    example: 0.1238
                concavity_worst:
                    type: number
                    example: 0.2416
                symmetry_worst:
                    type: number
                    example: 0.275
                fractal_dimension_worst:
                    type: number
                    example: 0.08902
    parameters:
        - name: body
          in: body
          required: true
          schema:
              $ref: '#/definitions/DiagnosticData'

    responses:
        200:
            description:
                Prediction based on diagnostic data. 0 if benign, 1 if malignant
            schema:
                type: object
                properties:
                    prediction:
                        type: int
                        enum: [0, 1]
    """
    try:
        data = request.json
        result = model.predict(data)
    except AttributeError:
        return {
            'error': 'one or more important values missing from data'
        }, 422
    return {
        'prediction': result
    }


@app.route("/health")
def health_check():
    """Health Check Endpoint
    ---
    definitions:
        HealthStatus:
            type: object
            properties:
                status:
                    type: string
                    enum: ['available']
    responses:
        200:
            description:
                application status
            schema:
                $ref: '#/definitions/HealthStatus'
            examples:
                status: 'available'
    """
    return {
        'status': 'available'
    }


@app.route("/")
def main_page():
    return redirect('/docs')
