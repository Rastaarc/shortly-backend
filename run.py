from api import create_app
from flask_cors import CORS
from api.config import DevelopmentConfig, ProductionConfig
from api.socketio import socketio
from api.utilities.constants import API_ROUTE, APP_NAME, APP_CREATOR, APP_DESCRIPTION
from flask_graphql import GraphQLView
from api.graphql.schema import schema

#app = create_app(DevelopmentConfig)
app = create_app(ProductionConfig)  # production

cors = CORS(app, resources={r'{}*'.format(API_ROUTE): {'origin': '*'}})


@app.route("/")
def home():
    return {"AppName": APP_NAME,
            "Creator": APP_CREATOR,
            "Description": APP_DESCRIPTION
            }


app.add_url_rule(
    API_ROUTE, view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,

    )
)

if __name__ == "__main__":
    socketio.run(app)
