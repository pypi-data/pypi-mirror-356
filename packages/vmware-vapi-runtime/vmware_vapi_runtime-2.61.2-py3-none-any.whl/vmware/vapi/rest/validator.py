# Copyright (c) 2024 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

from vmware.vapi.exception import HttpProtocolException
from vmware.vapi.lib.constants import JSON_CONTENT_TYPE


class HttpResponseValidator:
    """
    Utility which helps with the validation of a REST API response.
    """

    # This is a safety guard to avoid excessive memory allocations and
    # flooding log files with large error messages
    MAX_BODY_LENGTH_IN_ERROR = 4096

    @staticmethod
    def validate_content_type(http_response):
        """
        Validates the 'Content-Type' header of the given HTTP response does not exist
        or is JSON. Otherwise, a CoreException is raised.
        """
        content_type =  http_response.get_content_type()
        if content_type is None:
            return

        # Mime-types should be case-insensitive
        content_type = content_type.lower()

        if HttpResponseValidator._is_mime_type_json(content_type):
            return

        raise HttpResponseValidator._build_error(http_response,
                                                 content_type)

    @staticmethod
    def _is_mime_type_json(mime_type):
        if JSON_CONTENT_TYPE in mime_type:
            return True
        return mime_type.startswith("application/") and mime_type.endswith("+json")

    @staticmethod
    def _is_mime_type_xml(mime_type):
        if "application/xml" in mime_type:
            return True
        return mime_type.startswith("application/") and mime_type.endswith("+xml")

    @staticmethod
    def _is_mime_type_printable(mime_type):
        return (mime_type.startswith("text/") or
                HttpResponseValidator._is_mime_type_json(mime_type) or
                HttpResponseValidator._is_mime_type_xml(mime_type))

    @staticmethod
    def _response_body_to_message(body):
        # Body is always utf-8 encoded string
        if body and HttpResponseValidator.MAX_BODY_LENGTH_IN_ERROR < len(body):
            return body[:HttpResponseValidator.MAX_BODY_LENGTH_IN_ERROR]
        return body

    @staticmethod
    def _build_error(response, mime_type):
        message = ("HTTP response with status code {0} has unsupported content-type '{1}'".
                   format(response.status, mime_type))
        if response.body and HttpResponseValidator._is_mime_type_printable(mime_type):
            message = message + ": " + HttpResponseValidator._response_body_to_message(response.body)
        return HttpProtocolException(message, http_response=response)
