# Copyright (c) 2015-2024 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

class CoreException(Exception):
    """
    This exception is raised by various components of the vAPI runtime
    infrastructure to indicate failures in that infrastructure.

    Server-side the exception is caught by specific components and an
    internal_server_error is reported to the client that invoked the
    request.  Client-side the exception may be raised for certain failures
    before a request was sent to the server or after the response was
    received from the server.  Similarly, server-side the exception may
    be raised for failures that occur when a provider implementation
    invokes the vAPI runtime.

    This exception is not part of the vAPI message protocol, and it must
    never be raised by provider implementations.

    :type messages: generator of :class:`vmware.vapi.message.Message`
    :ivar messages: Generator of error messages describing why the Exception
                    was raised
    """

    def __init__(self, message, cause=None):
        """
        Initialize CoreException

        :type  message: :class:`vmware.vapi.message.Message`
        :param message: Description regarding why the Exception was raised
        :type  cause: :class:`Exception`, optional
        :param cause: Exception that led to this Exception
        """
        Exception.__init__(self, str(message))
        self._message = message
        self._cause = cause

    @property
    def messages(self):
        """
        :rtype: generator of :class:`vmware.vapi.message.Message`
        :return: Generator of error messages describing why the Exception
                 was raised
        """
        e = self
        while e:
            try:
                yield e._message  # pylint: disable=W0212
                e = e._cause      # pylint: disable=W0212
            except AttributeError:
                e = None

    # This method is primarily for use in tests
    def __eq__(self, other):
        return (isinstance(other, CoreException) and
                (list(self.messages) == list(other.messages)))

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        result = Exception.__str__(self)
        if self._cause is not None:
            cause_class = self._cause.__class__
            cause_class_name = '%s.%s' % (cause_class.__module__,
                                          cause_class.__name__)
            result = '%s, \n\tCaused by: %s: %s' % (result,
                                                    cause_class_name,
                                                    str(self._cause))
        return result

    def __hash__(self):
        return str(self).__hash__()


class BindingsException(CoreException):
    """
    Thrown in cases of communication protocol errors related to the vAPI
    protocol errors.
    """

    def __init__(self, message, cause=None, data_value=None):
        """
        Initialize BindingsException

        :type  message: :class:`vmware.vapi.message.Message`
        :param message: Description regarding why the Exception was raised
        :type  cause: :class:`Exception`, optional
        :param cause: Exception that led to this Exception
        :type  data_value: :class:`vmware.vapi.data.value.DataValue`, optional
        :param data_value: vAPI DataValue associated with the Exception
        """
        CoreException.__init__(self, message, cause)
        self._data_value = data_value

    @property
    def data_value(self):
        """
        :rtype :class:`vmware.vapi.data.value.DataValue`
        :return: vAPI DataValue associated with the Exception

        """
        return self._data_value

    @data_value.setter
    def data_value(self, data_value):
        """
        :type  data_value: :class:`vmware.vapi.data.value.DataValue`
        :param data_value: vAPI DataValue associated with the Exception
        """
        self._data_value = data_value

    @classmethod
    def from_core_exception(cls, core_exception):
        """
        Factory method creating a BindingsException from a supplied
        CoreException.

        :type  core_exception: :class:`vmware.vapi.exception.CoreException``
        :param core_exception: a CoreException from which the BindingsException
                               is created
        """
        return BindingsException(core_exception._message, core_exception._cause)

    def __eq__(self, other):
        return ((isinstance(other, BindingsException) and
                (list(self.messages) == list(other.messages))) and
                self.data_value == other.data_value)


class HttpProtocolException(CoreException):
    """
    Thrown by the client when HTTP response validation fails.
    """

    def __init__(self, message, cause=None, http_response=None):
        """
        Initialize HttpProtocolException

        :type  message: :class:`vmware.vapi.message.Message`
        :param message: Description regarding why the Exception was raised
        :type  cause: :class:`Exception`, optional
        :param cause: Exception that led to this Exception
        :type  http_response: :class:`vmware.vapi.protocol.client.http_lib.HTTPResponse`, optional
        :param http_response: HTTPResponse associated with the Exception
        """
        CoreException.__init__(self, message, cause)
        self._http_response = http_response

    @property
    def http_response(self):
        """
        :rtype :class:`vmware.vapi.protocol.client.http_lib.HTTPResponse`
        :return: HTTPResponse associated with the Exception

        """
        return self._http_response

    @http_response.setter
    def http_response(self, http_response):
        """
        :type  http_response: :class:`vmware.vapi.protocol.client.http_lib.HTTPResponse`, optional
        :param http_response: HTTPResponse associated with the Exception
        """
        self._http_response = http_response

    def __eq__(self, other):
        return ((isinstance(other, HttpProtocolException) and
                (list(self.messages) == list(other.messages))) and
                self.http_response == other.http_response)