from flask import Flask, redirect, url_for
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "Breast Cancer Prediction API",
    }
})


@app.route("/")
def hello():
    return redirect(url_for('health_check'))


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
