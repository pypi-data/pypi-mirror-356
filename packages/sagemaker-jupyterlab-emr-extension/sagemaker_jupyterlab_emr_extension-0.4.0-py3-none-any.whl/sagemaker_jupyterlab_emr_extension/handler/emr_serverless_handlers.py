import json
import traceback
import botocore.credentials
import jsonschema
import botocore

from tornado import web
from jupyter_server.base.handlers import JupyterHandler
from jsonschema.exceptions import ValidationError
from sagemaker_jupyterlab_emr_extension._version import __version__ as ext_version

from sagemaker_jupyterlab_extension_common.logging.logging_utils import HandlerLogMixin

from sagemaker_jupyterlab_emr_extension.schema.emr_serverless_api_schema import (
    list_serverless_applications_request_schema,
    get_serverless_application_request_schema,
)
from sagemaker_jupyterlab_emr_extension.converter.emr_serverless_converters import (
    convert_list_serverless_applications_response,
    convert_get_serverless_application_response,
)
from sagemaker_jupyterlab_emr_extension.utils.logging_utils import (
    EmrErrorHandler,
)

from sagemaker_jupyterlab_emr_extension.client.emr_serverless_client import (
    get_emr_serverless_client,
)

from sagemaker_jupyterlab_emr_extension.handler.base_emr_handler import BaseEmrHandler


EXTENSION_NAME = "sagemaker_jupyterlab_emr_extension"
EXTENSION_VERSION = ext_version


class ListServerlessApplicationsHandler(BaseEmrHandler):
    """
    Response schema
    {
        applications: [ApplicationSummary]!
        errorMessage: String
    }
    """

    @web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json")
        try:
            body = self.get_json_body()
            jsonschema.validate(body, list_serverless_applications_request_schema)
            self.log.info(
                f"List applications request {body}",
                extra={"Component": "ListServerlessApplications"},
            )
            roleArn = body.pop("roleArn", None)
            response = await get_emr_serverless_client(
                roleArn=roleArn
            ).list_applications(**body)
            converted_resp = convert_list_serverless_applications_response(response)
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except web.HTTPError as error:
            await self._handle_http_error(error)
        except (
            botocore.exceptions.ParamValidationError,
            ValidationError,
        ) as error:
            await self._handle_validation_error(
                error, body, "ListServerlessApplications"
            )
        except botocore.exceptions.ClientError as error:
            await self._handle_client_error(error, "ListServerlessApplications")
        except botocore.exceptions.EndpointConnectionError as error:
            await self._handle_connection_error(error, "ListServerlessApplications")
        except botocore.exceptions.ConnectTimeoutError as error:
            helpful_context = (
                "Connection timed out. Looks like you do not have required networking setup to connect "
                "with EMR Serverless."
            )
            error_message = {
                "code": "ConnectTimeoutError",
                "errorMessage": f"{helpful_context} Error message: {str(error)}",
            }
            await self._handle_connection_timeout_error(
                error_message, "ListServerlessApplications"
            )
        except Exception as error:
            await self._handle_error(error, "ListServerlessApplications")


class GetServerlessApplicationHandler(BaseEmrHandler):
    """
    Response schema
    {
        application: Application
        errorMessage: String
    }
    """

    @web.authenticated
    async def post(self):
        self.set_header("Content-Type", "application/json")
        try:
            body = self.get_json_body()
            jsonschema.validate(body, get_serverless_application_request_schema)
            application_id = body["applicationId"]
            role_arn = body.pop("RoleArn", None)
            self.log.info(
                f"Get serverless application request {application_id}",
                extra={"Component": "GetServerlessApplication"},
            )
            response = await get_emr_serverless_client(
                roleArn=role_arn
            ).get_application(**body)
            self.log.info(
                f"Successfully got application for id {application_id}",
                extra={"Component": "GetServerlessApplication"},
            )
            converted_resp = convert_get_serverless_application_response(response)
            self.set_status(200)
            self.finish(json.dumps(converted_resp))
        except web.HTTPError as error:
            await self._handle_http_error(error)
        except (
            botocore.exceptions.ParamValidationError,
            ValidationError,
        ) as error:
            await self._handle_validation_error(error, body, "GetServerlessApplication")
        except botocore.exceptions.ClientError as error:
            await self._handle_client_error(error, "GetServerlessApplication")
        except botocore.exceptions.EndpointConnectionError as error:
            await self._handle_connection_error(error, "GetServerlessApplication")
        except Exception as error:
            await self._handle_error(error, "GetServerlessApplication")
