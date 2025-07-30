"""Builder API implementation for multi-step workflows."""

from typing import Any, Dict, List, Optional

from nutrient_dws.file_handler import FileInput, prepare_file_for_upload, save_file_output


class BuildAPIWrapper:
    r"""Builder pattern implementation for chaining document operations.

    This class provides a fluent interface for building complex document
    processing workflows using the Nutrient Build API.

    Example:
        >>> client.build(input_file="document.pdf") \\
        ...     .add_step(tool="rotate-pages", options={"degrees": 90}) \\
        ...     .add_step(tool="ocr-pdf", options={"language": "en"}) \\
        ...     .add_step(tool="watermark-pdf", options={"text": "CONFIDENTIAL"}) \\
        ...     .execute(output_path="processed.pdf")
    """

    def __init__(self, client: Any, input_file: FileInput) -> None:
        """Initialize builder with client and input file.

        Args:
            client: NutrientClient instance.
            input_file: Input file to process.
        """
        self._client = client
        self._input_file = input_file
        self._parts: List[Dict[str, Any]] = [{"file": "file"}]  # Main file
        self._files: Dict[str, FileInput] = {"file": input_file}  # Track files
        self._actions: List[Dict[str, Any]] = []
        self._output_options: Dict[str, Any] = {}

    def _add_file_part(self, file: FileInput, name: str) -> None:
        """Add an additional file part for operations like merge.

        Args:
            file: File to add.
            name: Name for the file part.
        """
        self._parts.append({"file": name})
        self._files[name] = file

    def add_step(self, tool: str, options: Optional[Dict[str, Any]] = None) -> "BuildAPIWrapper":
        """Add a processing step to the workflow.

        Args:
            tool: Tool identifier (e.g., 'rotate-pages', 'ocr-pdf').
            options: Optional parameters for the tool.

        Returns:
            Self for method chaining.

        Example:
            >>> builder.add_step(tool="rotate-pages", options={"degrees": 180})
        """
        action = self._map_tool_to_action(tool, options or {})
        self._actions.append(action)
        return self

    def set_output_options(self, **options: Any) -> "BuildAPIWrapper":
        """Set output options for the final document.

        Args:
            **options: Output options (e.g., metadata, optimization).

        Returns:
            Self for method chaining.

        Example:
            >>> builder.set_output_options(
        ...     metadata={"title": "My Document", "author": "John Doe"},
        ...     optimize=True
        ... )
        """
        self._output_options.update(options)
        return self

    def execute(self, output_path: Optional[str] = None) -> Optional[bytes]:
        """Execute the workflow.

        Args:
            output_path: Optional path to save the output file.

        Returns:
            Processed file bytes, or None if output_path is provided.

        Raises:
            AuthenticationError: If API key is missing or invalid.
            APIError: For other API errors.
        """
        # Prepare the build instructions
        instructions = self._build_instructions()

        # Prepare files for upload
        files = {}
        for name, file in self._files.items():
            file_field, file_data = prepare_file_for_upload(file, name)
            files[file_field] = file_data

        # Make API request
        result = self._client._http_client.post(
            "/build",
            files=files,
            json_data=instructions,
        )

        # Handle output
        if output_path:
            save_file_output(result, output_path)
            return None
        else:
            return result  # type: ignore[no-any-return]

    def _build_instructions(self) -> Dict[str, Any]:
        """Build the instructions payload for the API.

        Returns:
            Instructions dictionary for the Build API.
        """
        instructions = {
            "parts": self._parts,
            "actions": self._actions,
        }

        # Add output options if specified
        if self._output_options:
            instructions["output"] = self._output_options  # type: ignore

        return instructions

    def _map_tool_to_action(self, tool: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Map tool name and options to Build API action format.

        Args:
            tool: Tool identifier.
            options: Tool options.

        Returns:
            Action dictionary for the Build API.
        """
        # Map tool names to action types
        tool_mapping = {
            "rotate-pages": "rotate",
            "ocr-pdf": "ocr",
            "watermark-pdf": "watermark",
            "flatten-annotations": "flatten",
            "apply-instant-json": "applyInstantJson",
            "apply-xfdf": "applyXfdf",
            "create-redactions": "createRedactions",
            "apply-redactions": "applyRedactions",
        }

        action_type = tool_mapping.get(tool, tool)

        # Build action dictionary
        action = {"type": action_type}

        # Handle special cases for different action types
        if action_type == "rotate":
            action["rotateBy"] = options.get("degrees", 0)
            if "page_indexes" in options:
                action["pageIndexes"] = options["page_indexes"]

        elif action_type == "ocr":
            if "language" in options:
                # Map common language codes to API format
                lang_map = {
                    "en": "english",
                    "de": "deu",
                    "eng": "eng",
                    "deu": "deu",
                    "german": "deu",
                }
                lang = options["language"]
                action["language"] = lang_map.get(lang, lang)

        elif action_type == "watermark":
            # Watermark requires width/height
            action["width"] = options.get("width", 200)  # Default width
            action["height"] = options.get("height", 100)  # Default height

            if "text" in options:
                action["text"] = options["text"]
            elif "image_url" in options:
                action["image"] = {"url": options["image_url"]}  # type: ignore
            else:
                # Default to text watermark if neither specified
                action["text"] = "WATERMARK"

            if "opacity" in options:
                action["opacity"] = options["opacity"]
            if "position" in options:
                action["position"] = options["position"]

        else:
            # For other actions, pass options directly
            action.update(options)

        return action

    def __str__(self) -> str:
        """String representation of the build workflow."""
        steps = [f"{action['type']}" for action in self._actions]
        return f"BuildAPIWrapper(steps={steps})"

    def __repr__(self) -> str:
        """Detailed representation of the build workflow."""
        return (
            f"BuildAPIWrapper("
            f"input_file={self._input_file!r}, "
            f"actions={self._actions!r}, "
            f"output_options={self._output_options!r})"
        )
