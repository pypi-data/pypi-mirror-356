"""Security-related mutators for defanging and refanging URLs and indicators."""

from typing import Any, Dict

from .base import BaseMutator, append_to_result


class RefangMutator(BaseMutator):
    """
    Mutator that refangs (un-defangs) URLs and indicators.

    This mutator reverses common defanging patterns to make URLs and
    indicators clickable/active again. It handles various defanging patterns:
    - hXXp:// -> http://
    - hXXps:// -> https://
    - [.]  -> .
    - [.] -> .
    - [:]  -> :
    - [:] -> :
    - fXp:// -> ftp://
    - [at] -> @
    - [@] -> @

    Parameters:
        field: Optional field to store the refanged value
    """

    def apply(self, field_name: str, record: Dict[str, Any], value: Any) -> Any:
        """Apply the refang transformation."""
        append_field = self.params.get("field")

        # Handle different input types
        refanged_value: Any
        if value is None:
            refanged_value = None
        elif isinstance(value, str):
            refanged_value = self._refang_string(value)
        elif isinstance(value, list):
            # Refang each string in the list
            refanged_value = []
            for item in value:
                if isinstance(item, str):
                    refanged_value.append(self._refang_string(item))
                else:
                    refanged_value.append(item)
        elif isinstance(value, (int, float, bool)):
            # Convert to string, refang, then return
            refanged_value = self._refang_string(str(value))
        else:
            # For other types, return as-is
            refanged_value = value

        # If append_field is specified, add to record and return original value
        if append_field:
            append_to_result(record, append_field, refanged_value)
            return value
        else:
            # Return the refanged value directly
            return refanged_value

    def _refang_string(self, s: str) -> str:
        """Refang a single string."""
        result = s

        # Apply replacements in specific order to handle spaces properly
        # First handle patterns with spaces
        result = result.replace(" [.] ", ".")
        result = result.replace(" [dot] ", ".")
        result = result.replace(" [at] ", "@")
        result = result.replace(" [:] ", ":")

        # Protocol defanging (various cases)
        result = result.replace("hxxp://", "http://")
        result = result.replace("hXXp://", "http://")
        result = result.replace("HxXp://", "http://")
        result = result.replace("HxxP://", "http://")
        result = result.replace("HXXP://", "http://")
        result = result.replace("hxxps://", "https://")
        result = result.replace("hXXps://", "https://")
        result = result.replace("HXXPS://", "https://")
        result = result.replace("fxp://", "ftp://")
        result = result.replace("fXp://", "ftp://")
        result = result.replace("FXP://", "ftp://")

        # Dot defanging
        result = result.replace("[.]", ".")
        result = result.replace("(.)", ".")
        result = result.replace("{.}", ".")
        result = result.replace("[dot]", ".")
        result = result.replace("(dot)", ".")
        result = result.replace("{dot}", ".")

        # Colon defanging
        result = result.replace("[:]", ":")
        result = result.replace("(:)", ":")
        result = result.replace("{:}", ":")

        # At symbol defanging
        result = result.replace("[at]", "@")
        result = result.replace("(at)", "@")
        result = result.replace("{at}", "@")
        result = result.replace("[@]", "@")
        result = result.replace("(@)", "@")
        result = result.replace("{@}", "@")

        # Slash defanging
        result = result.replace("[/]", "/")
        result = result.replace("(/)", "/")
        result = result.replace("{/}", "/")

        return result


class DefangMutator(BaseMutator):
    """
    Mutator that defangs URLs and indicators to make them unclickable.

    This mutator applies common defanging patterns to URLs and indicators
    to prevent accidental clicks or automatic processing:
    - http:// -> hXXp://
    - https:// -> hXXps://
    - . -> [.]
    - : -> [:]
    - @ -> [at]
    - ftp:// -> fXp://

    Parameters:
        field: Optional field to store the defanged value
    """

    def apply(self, field_name: str, record: Dict[str, Any], value: Any) -> Any:
        """Apply the defang transformation."""
        append_field = self.params.get("field")

        # Handle different input types
        defanged_value: Any
        if value is None:
            defanged_value = None
        elif isinstance(value, str):
            defanged_value = self._defang_string(value)
        elif isinstance(value, list):
            # Defang each string in the list
            defanged_value = []
            for item in value:
                if isinstance(item, str):
                    defanged_value.append(self._defang_string(item))
                else:
                    defanged_value.append(item)
        elif isinstance(value, (int, float, bool)):
            # Convert to string, defang, then return
            defanged_value = self._defang_string(str(value))
        else:
            # For other types, return as-is
            defanged_value = value

        # If append_field is specified, add to record and return original value
        if append_field:
            append_to_result(record, append_field, defanged_value)
            return value
        else:
            # Return the defanged value directly
            return defanged_value

    def _defang_string(self, s: str) -> str:
        """Defang a single string."""
        # Apply defanging patterns
        result = s

        # Protocol defanging (do these first to avoid double-defanging)
        result = result.replace("https://", "hXXps://")
        result = result.replace("http://", "hXXp://")
        result = result.replace("ftp://", "fXp://")
        result = result.replace("HTTPS://", "HXXPS://")
        result = result.replace("HTTP://", "HXXP://")
        result = result.replace("FTP://", "FXP://")

        # Now defang dots, but not in the protocol part we just defanged
        # Split by whitespace to handle individual tokens
        tokens = result.split()
        defanged_tokens = []

        for token in tokens:
            # Check if this is a URL (has protocol)
            has_protocol = any(
                token.startswith(p)
                for p in [
                    "hXXp://",
                    "hXXps://",
                    "fXp://",
                    "HXXP://",
                    "HXXPS://",
                    "FXP://",
                    "hxxp://",
                    "hxxps://",
                    "fxp://",  # Already defanged variations
                ]
            )

            if has_protocol and "://" in token:
                # For URLs, defang only the domain part
                protocol, rest = token.split("://", 1)
                # Only defang if not already defanged
                if "[.]" not in rest and "[at]" not in rest:
                    # Defang dots in domain/path
                    rest = rest.replace(".", "[.]")
                    # Defang @ if present (for URLs with auth)
                    rest = rest.replace("@", "[at]")
                    # Defang colons in port numbers
                    # Only defang colon if it's followed by numbers (port)
                    import re

                    rest = re.sub(r":(\d+)", r"[:]\1", rest)
                defanged_tokens.append(f"{protocol}://{rest}")
            else:
                # For non-URL tokens, defang dots and @ symbols
                # But avoid double-defanging
                if "[.]" not in token and "[at]" not in token:
                    defanged = token.replace(".", "[.]")
                    defanged = defanged.replace("@", "[at]")
                    defanged_tokens.append(defanged)
                else:
                    # Already defanged, leave as-is
                    defanged_tokens.append(token)

        return " ".join(defanged_tokens)
