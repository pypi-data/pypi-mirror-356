# Copyright (c) 2024 Broadcom. All Rights Reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

from vmware.vapi.exception import BindingsException, CoreException


def raise_core_exception(msg_list):
    """
    Create and raise a CoreException from a list of messages

    :type msg_list: :class:`vmware.vapi.message.Message`
    :param msg_list: List of messages
    :raise: CoreException if msg list is not empty
    """
    exception = None
    if msg_list:
        for msg in reversed(msg_list):
            if exception:
                exception = CoreException(msg, cause=exception)
            else:
                exception = CoreException(msg)
    if exception is not None:
        raise exception  # pylint: disable-msg=E0702

def raise_bindings_exception(msg_list, data_value=None):
    """
    Create and raise a BindingsException from a list of messages
    and an optional DataValue.

    :type msg_list: :class:`vmware.vapi.message.Message`
    :param msg_list: List of messages
    :type  data_value: :class:`vmware.vapi.data.value.DataValue`, optional
    :param data_value: vAPI DataValue associated with the Exception

    :raise: BindingsException if msg list is not empty
    """
    exception = None
    if msg_list:
        for msg in reversed(msg_list):
            if exception:
                exception = BindingsException(msg, cause=exception, data_value=data_value)
            else:
                exception = BindingsException(msg, data_value=data_value)
    if exception is not None:
        raise exception  # pylint: disable-msg=E0702


class NameToTypeResolver(object):
    """
    Helper class that resolves a fully qualified canonical type name to a type
    descriptor. The type name can be a structure name or an error name.
    """
    def __init__(self, type_map):
        """
        Initialize NameToTypeResolver

        :type  type_map: :class:`dict` of :class:`str` and :class:`VapiStruct`
        :param type_map: Type map that contains the canonical names and the
            references to the binding classes for these types.
        """
        self._type_map = type_map

    def resolve(self, name):
        """
        Type name to be resolved
        """
        return self._type_map.get(name)
