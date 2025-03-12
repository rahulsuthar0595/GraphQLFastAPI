from http import HTTPStatus

from starlette.responses import Response
from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse


class CustomGraphQLRouter(GraphQLRouter):

    def create_response(self, response_data: GraphQLHTTPResponse, sub_response: Response) -> Response:
        # NOTE: We can change the default status_code from 200 to any based on need.

        if (errors := response_data.get("errors")) and len(errors) >= 1:
            sub_response.status_code = HTTPStatus.BAD_REQUEST

        result = super().create_response(response_data=response_data, sub_response=sub_response)
        return result
