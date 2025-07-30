"""Code formatter for content parsing."""

import logging
from typing import Any

from markdown_it.token import Token

from markdowndeck.models import Element

# ElementFactory will be injected via __init__ from BaseFormatter
from markdowndeck.parser.content.formatters.base import BaseFormatter

logger = logging.getLogger(__name__)


class CodeFormatter(BaseFormatter):
    """Formatter for code block elements."""

    def can_handle(self, token: Token, leading_tokens: list[Token]) -> bool:
        """Check if this formatter can handle the given token."""
        return token.type == "fence"

    def process(
        self,
        tokens: list[Token],
        start_index: int,
        section_directives: dict[str, Any],
        element_specific_directives: dict[str, Any] | None = None,
        **kwargs,
    ) -> tuple[list[Element], int]:
        """Create a code element from a fence token.

        TASK 3.1: Updated to return list[Element] instead of Element | None.
        """
        # Merge section and element-specific directives
        merged_directives = self.merge_directives(
            section_directives, element_specific_directives
        )

        token = tokens[start_index]
        if token.type != "fence":
            logger.warning(
                f"CodeFormatter received non-fence token: {token.type} at index {start_index}"
            )
            return [], start_index  # Should not happen if can_handle is correct

        code_content = token.content
        language = token.info.strip() if token.info else "text"

        element = self.element_factory.create_code_element(
            code=code_content, language=language, directives=merged_directives.copy()
        )
        logger.debug(
            f"Created code element (lang: {language}) from token index {start_index}"
        )

        # Fence token is self-contained, so the next token is at start_index + 1
        return [element], start_index
