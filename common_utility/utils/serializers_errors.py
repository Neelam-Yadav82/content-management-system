def serializer_error(serializer_error):
    """
    Extract all error messages from a serializer error dictionary.
    """
    error_messages = []
    for error_text in serializer_error.keys():
        error_messages.extend(serializer_error.get(error_text))
    return error_messages


# def serializer_error(serializer_error):
#     """
#     Extract the first error message from a serializer error dictionary.
#     """
#     error_keys = serializer_error.keys()
#     error_message = ""
#     for error_text in error_keys:
#         error_message += serializer_error.get(error_text)[0]
#         break
#     return error_message
