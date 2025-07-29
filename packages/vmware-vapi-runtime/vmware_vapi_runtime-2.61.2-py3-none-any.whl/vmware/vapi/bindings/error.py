# Copyright (c) 2015-2024 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

"""
Error classes and factory
"""

from vmware.vapi.bindings.struct import VapiStruct


class VapiError(VapiStruct, Exception):
    """
    Representation of VMODL Error in python language bindings
    """
    def __init__(self, error_value=None):
        """
        Initialize VapiError

        :type  error_value: :class:`vmware.vapi.data.value.ErrorValue` or
            :class:`None`
        :param error_value: ErrorValue to be used for VapiError
        """
        VapiStruct.__init__(self, struct_value=error_value)
        Exception.__init__(self)
        self._status_code = 0

    def get_error_value(self):
        """
        Returns the corresponding ErrorValue for the VapiError class

        :rtype: :class:`vmware.vapi.data.value.ErrorValue`
        :return: ErrorValue for this VapiError
        """
        return self.get_struct_value()

    def get_status_code(self):
        """
        Returns the HTTP response status code of the error.

        Available only for REST API calls, otherwise returns zero.

        :rtype: :class:`int`
        :return: HTTP response status code
        """
        return self._status_code

    def set_status_code(self, status_code):
        """
        Sets the HTTP response status code of the error.

        :type status_code: :class:`int`
        :param status_code:  HTTP response status code
        """
        self._status_code = status_code


class UnresolvedError(VapiError):
    """
    VapiError which represents a VMODL2 error that was reported but couldn't
    be resolved
    """
    pass


class ThrowsClauseElement:
    """
    Represents one element of the `throws` clause of an API operation.
    """

    def __init__(self, error_type, status_codes):
        self._error_type = error_type
        self._status_codes = status_codes

    @property
    def error_type(self):
        """
        Returns the data type of the current element of the `throws`
        clause.

        :rtype: :class:`vmware.vapi.bindings.type.ErrorType`
        :return: The associated ErrorType (may be wrapped in ReferenceType)
        """
        return self._error_type

    @property
    def status_codes(self):
        """
        Returns the HTTP status codes which are applicable to this element of the
        `throws` clause.

        If empty, all status codes are applicable to this element.

        :rtype: :class:`list` of :class:`int`
        :return: HTTP status codes
        """
        return self._status_codes


class ThrowsClauseDef:
    """
    The API bindings representation of the `throws` clause of an API
    operation.
    """

    def __init__(self, throws_clause_elements):
        self._throws_clause_elements = throws_clause_elements

    @property
    def throws_clause_elements(self):
        """
        :rtype: :class:`list` of :class:`vmware.vapi.bindings.error.ThrowsClauseElement`
        :return: List of ThrowsClauseElement objects
        """
        return self._throws_clause_elements


class ThrowsClauseBuilder:
    """
    Builds the API bindings representation of the `throws` clause of an
    API operation.
    """

    def __init__(self):
        self.throws_clause_elements = []

    def add(self, error_type, status_codes):
        self.throws_clause_elements.append(ThrowsClauseElement(error_type, status_codes))
        return self

    def build(self):
        return ThrowsClauseDef(self.throws_clause_elements)
