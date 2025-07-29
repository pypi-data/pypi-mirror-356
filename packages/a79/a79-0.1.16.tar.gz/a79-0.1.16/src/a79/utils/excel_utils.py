from typing import Any, Optional

from common_py.model.retention_analysis_models import (
    ChartConfigData,
    RetentionChartingInputData,
    ToggleConfiguration,
    ToggleInfo,
    ToggleOption,
    ToggleSection,
    ToggleSelection,
)

__all__ = [
    "ChartConfigData",
    "RetentionChartingInputData",
    "ToggleConfiguration",
    "ToggleInfo",
    "ToggleOption",
    "ToggleSection",
    "ToggleSelection",
    "parse_control_panel_sheet",
    "get_toggle_configurations",
    "get_toggle_edit_operations",
]


def parse_control_panel_sheet(sheet_data: dict) -> list[ToggleInfo]:
    """
    Parse the control panel sheet data to extract toggle configurations.

    Args:
        sheet_data: Dictionary containing sheet data with cells array

    Returns:
        List of ToggleInfo objects representing each toggle section
    """
    toggles = []
    current_section: Optional[ToggleSection] = None
    current_options: list[ToggleOption] = []
    current_cell: Optional[str] = None

    # Create a dictionary for faster cell lookup by row/column
    cell_map = {}
    for cell in sheet_data["cells"]:
        if cell["value"] is None:
            continue
        cell_map[(cell["row"], cell["column"])] = cell["value"]["value"]

    # Get the maximum row to iterate through
    max_row = max(cell["row"] for cell in sheet_data["cells"])

    # Iterate through rows
    for row_idx in range(1, max_row + 1):
        # Get the first cell value in this row (if it exists)
        first_cell_value = cell_map.get((row_idx, 1))
        if first_cell_value is None:
            continue

        first_cell = str(first_cell_value).strip()

        # Check for section headers
        if any(section in first_cell for section in ToggleSection.__members__.values()):
            # If we were processing a previous section, add it to toggles

            if current_section and current_options and current_cell:
                # current_options has values like:
                # [
                #   '{"index":1,"value":"All","cell_row":14,"cell_col":3}',  -> selected option  # noqa: E501
                #   '{"index":1,"value":"All","cell_row":16,"cell_col":3}',
                #   '{"index":2,"value":"Greater than $200,000","cell_row":17,"cell_col":3}',  # noqa: E501
                #   '{"index":3,"value":"Greater than $100,000 up to $200,000","cell_row":18,"cell_col":3}',  # noqa: E501
                #   '{"index":4,"value":"Greater than $0 up to $100,000","cell_row":19,"cell_col":3}'  # noqa: E501
                #  ]
                # so we use the first option as the current chosen value for the toggle.
                # Rest are used as options to expose.

                toggles.append(
                    ToggleInfo(
                        section=current_section,
                        selection_cell=current_cell,
                        options=current_options[1:],
                        selection_cell_row=current_options[0].cell_row,
                        selection_cell_col=current_options[0].cell_col,
                    )
                )

            # Start new section
            current_section = ToggleSection(first_cell)
            current_options = []
            # Selection cell is typically in column C of the next row
            current_cell = f"C{row_idx + 4}"
            continue

        # Process option rows (they start with a number)
        if first_cell and first_cell.isdigit():
            option_index = int(first_cell)
            # Get the option value from column D (index 4)
            option_value = cell_map.get((row_idx, 2))
            option_value = str(option_value).strip()
            if option_value and option_value != "[ ]":
                current_options.append(
                    ToggleOption(
                        index=option_index,
                        value=option_value,
                        cell_row=row_idx + 2,
                        cell_col=3,
                    )
                )

    # Add the last section if exists
    if current_section and current_options and current_cell:  # Add check for current_cell
        toggles.append(
            ToggleInfo(
                section=current_section,
                selection_cell=current_cell,
                selection_cell_row=current_options[0].cell_row,
                selection_cell_col=current_options[0].cell_col,
                options=current_options[1:],
                selected_option_index=current_options[0].index,
            )
        )

    return toggles


def get_toggle_configurations(
    toggle_info: list[ToggleInfo], toggle_values: dict[str, str]
) -> dict[str, ToggleConfiguration]:
    """
    Create toggle configurations with selected values and available options.

    Args:
        toggle_info: List of toggle configurations
        toggle_values: Dictionary of toggle values from user input

    Returns:
        Dictionary mapping section names to their configurations
    """
    configurations = {}

    for toggle in toggle_info:
        section_name = toggle.section.replace(" Toggle", "").lower()
        selected_value = toggle_values.get(
            section_name, toggle.options[0].value if toggle.options else ""
        )

        configurations[section_name] = ToggleConfiguration(
            section=toggle.section,
            selected_value=selected_value,
            available_options=[opt.value for opt in toggle.options],
        )

    return configurations


def get_toggle_edit_operations(
    toggle_info: list[ToggleInfo], toggle_values: dict[str, str]
) -> list[dict[str, Any]]:
    """
    Generate Excel edit operations for each toggle based on selected values.

    Args:
        toggle_info: List of toggle configurations
        toggle_values: Dictionary of toggle values from user input

    Returns:
        List of edit operations with cell locations and values
    """
    edit_operations = []

    for toggle in toggle_info:
        # Get the selected value for this toggle
        section_name = toggle.section.replace(" Toggle", "").lower()
        selected_value = toggle_values.get(section_name)

        # Find the index of the selected value
        selected_index = 1  # Default to first option
        if selected_value:
            for option in toggle.options:
                if option.value.lower() == selected_value.lower():
                    selected_index = option.index
                    break

        # Create edit operation
        edit_operations.append(
            {
                "sheet_name": "Control Panel",
                "cell": toggle.selection_cell,
                "row": toggle.selection_cell_row,
                "column": toggle.selection_cell_col,
                "value": selected_index,
            }
        )

    return edit_operations
