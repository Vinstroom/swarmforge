import typing as t
from src.swarmforge.message_bus import MessageBus

class MessageBusInputValidator:
    """
    Validator for input data related to MessageBus.
    """

    @staticmethod
    def validate_message(message: t.Union[str, bytes]) -> None:
        """
        Validate that a message is either a string or bytes.

        Raises:
            TypeError: If the message is neither a string nor bytes.
        """
        if not isinstance(message, (str, bytes)):
            raise TypeError("Message must be either a string or bytes")

    @staticmethod
    def validate_recipients(recipients: t.iterable) -> None:
        """
        Validate that recipients are a non-empty iterable of strings.

        Raises:
            TypeError: If recipients are not a non-empty iterable of strings.
            ValueError: If any recipient is not a string.
        """
        if not recipients or not all(isinstance(recipient, str) for recipient in recipients):
            raise ValueError("Recipients must be a non-empty iterable of strings")

    @staticmethod
    def validate_options(options: t.Optional[t.Mapping[str, t.Any]] = None) -> None:
        """
        Validate that options are a mapping of strings to any type.

        Raises:
            TypeError: If options are not a mapping or if keys are not strings.
        """
        if options is not None and not isinstance(options, t.Mapping) or not all(
            isinstance(k, str) for k in options.keys()
        ):
            raise TypeError("Options must be a mapping of strings to any type")

    @staticmethod
    def validate_send_message_input(message_bus: MessageBus, message: str, recipients: t.iterable, options: t.Optional[t.Mapping[str, t.Any]] = None) -> None:
        """
        Validate input for sending a message.

        Raises:
            TypeError or ValueError for invalid input.
        """
        MessageBusInputValidator.validate_message(message)
        MessageBusInputValidator.validate_recipients(recipients)
        MessageBusInputValidator.validate_options(options)
