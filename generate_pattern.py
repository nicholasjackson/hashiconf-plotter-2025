#!/usr/bin/env python3
from typing import Dict
import svgwrite
import math
import json
import argparse

width = 300
height = 416
angles = {"northeast": math.radians(45), "southeast": math.radians(315)}
colors = {"purple": "#B596C8", "cyan": "#63C3DC", "white": "#FFFFFF"}
pipe_width = 6


def create_pattern(data_file: str) -> Dict:
    """
    Create an SVG with a single chevron starting from southwest corner,
    going northeast then turning southeast.

    Args:
        width: Width of the SVG canvas
        height: Height of the SVG canvas

    Returns:
        Dictionary with 3 SVGs for each color and combined
    """

    color1 = svgwrite.Drawing(size=(width, height))
    color2 = svgwrite.Drawing(size=(width, height))
    combined = svgwrite.Drawing(size=(width, height))

    # Create SVG drawing
    color1 = svgwrite.Drawing(size=(width, height))
    color2 = svgwrite.Drawing(size=(width, height))
    combined = svgwrite.Drawing(size=(width, height))

    # Add white background
    color1.add(color1.rect(insert=(0, 0), size=(width, height), fill="white"))
    color2.add(color2.rect(insert=(0, 0), size=(width, height), fill="white"))
    combined.add(combined.rect(insert=(0, 0), size=(width, height), fill="white"))

    # Load the data from JSON file
    with open(data_file, "r") as file:
        data = json.load(file)

    # Store block information for ID drawing later
    block_ids = []

    for layer in data["layers"]:
        # Handle both old format (direct blocks) and new format (rows with blocks)
        if "rows" in layer:
            # New format with rows (logical grouping)
            for row in layer["rows"]:
                for block in row["blocks"]:
                    # Get block ID if it exists
                    block_id = block.get("id", None)
                    block_x = block["x"]
                    block_y = block["y"]

                    # Store block info for later ID drawing
                    if block_id is not None:
                        block_ids.append(
                            {
                                "id": block_id,
                                "x": block_x,
                                "y": block_y,
                                "color": block["color"],
                            }
                        )

                    drawpipe_group(
                        combined,
                        block_x,
                        block_y,
                        block["segments"],
                        block["color"],
                    )

                    if block["color"] == "purple":
                        drawpipe_group(
                            color1,
                            block_x,
                            block_y,
                            block["segments"],
                            block["color"],
                        )
                    elif block["color"] == "cyan":
                        drawpipe_group(
                            color2,
                            block_x,
                            block_y,
                            block["segments"],
                            block["color"],
                        )
        else:
            # Old format with direct blocks (for backward compatibility)
            for block in layer["blocks"]:
                # Get block ID if it exists
                block_id = block.get("id", None)

                # Store block info for later ID drawing
                if block_id is not None:
                    block_ids.append(
                        {
                            "id": block_id,
                            "x": block["x"],
                            "y": block["y"],
                            "color": block["color"],
                        }
                    )

                drawpipe_group(
                    combined,
                    block["x"],
                    block["y"],
                    block["segments"],
                    block["color"],
                )

                if block["color"] == "purple":
                    drawpipe_group(
                        color1,
                        block["x"],
                        block["y"],
                        block["segments"],
                        block["color"],
                    )
                elif block["color"] == "cyan":
                    drawpipe_group(
                        color2,
                        block["x"],
                        block["y"],
                        block["segments"],
                        block["color"],
                    )

    # Add white border as the last element
    add_border(color1, width, height)
    add_border(color2, width, height)
    add_border(combined, width, height)

    # Add grid overlay (comment out to disable)
    add_grid(color1, width, height)
    add_grid(color2, width, height)
    add_grid(combined, width, height)

    # Draw IDs last so they appear on top of everything
    # Track used positions to avoid overlaps
    used_positions = {}

    for block_info in block_ids:
        # Calculate base position
        x, y = block_info["x"], block_info["y"]
        base_x = 10 if x < 0 else x
        base_y = 400 if y > 400 else y

        # Find available position near the base position
        text_x, text_y = find_available_position(used_positions, base_x, base_y)
        used_positions[(text_x, text_y)] = block_info["id"]

        draw_block_id_at_position(
            combined, text_x, text_y, block_info["id"], block_info["color"]
        )
        if block_info["color"] == "purple":
            draw_block_id_at_position(
                color1, text_x, text_y, block_info["id"], block_info["color"]
            )
        elif block_info["color"] == "cyan":
            draw_block_id_at_position(
                color2, text_x, text_y, block_info["id"], block_info["color"]
            )

    return {
        "color1": color1.tostring(),
        "color2": color2.tostring(),
        "combined": combined.tostring(),
    }


def drawpipe_group(dwg, x, y, segments, color):
    last_positions = []
    pipes = 7

    # Calculate perpendicular direction for alignment (direction + 90°)
    draw_color = colors[color]

    for i in range(pipes):
        drawpipe(
            dwg,
            x,
            y,
            segments,
            i,
            draw_color,
        )

        # Alternate between white and the specified color
        if draw_color != colors["white"]:
            draw_color = colors["white"]
        else:
            draw_color = colors[color]

    return last_positions


def drawpipe(dwg, x, y, segments, pipe, color):
    """Draw a pipe shape with two segments and rounded joint."""

    offset_angle = angles[segments[0]["direction"]] + math.radians(90)

    # Calculate offset position along perpendicular direction
    start_x = x - (pipe * pipe_width) * math.cos(offset_angle)
    start_y = y + (pipe * pipe_width) * math.sin(offset_angle)

    points = [(start_x, start_y)]

    # First segment using direction_1
    for i, segment in enumerate(segments):
        length = segment["length"]
        angle = angles[segment["direction"]]
        offset = 0

        # For the first segment, offset in the positive direction
        # For the last segment, reverse the offset direction
        # For all other segments, no offset
        if i == 0 and len(segments) == 1:
            offset = 0
        elif i == 0 and len(segments) > 1:
            offset = pipe * pipe_width
        elif i == len(segments) - 1:
            offset = -(pipe * pipe_width)

        # Calculate end point of the segment
        if segment["direction"] == "southeast":
            end_x = points[i][0] + (length + offset) * math.cos(angle)
            end_y = points[i][1] - (length + offset) * math.sin(angle)
        else:
            end_x = points[i][0] + (length - offset) * math.cos(angle)
            end_y = points[i][1] - (length - offset) * math.sin(angle)

        points.append((end_x, end_y))

    # Build parameters dictionary
    polyline_params = {
        "points": points,
        "stroke": color,
        "stroke_width": pipe_width,
        "fill": "none",
    }

    # Only add stroke_linejoin if we have a second segment
    if len(segments) > 1:
        polyline_params["stroke_linejoin"] = "round"
        polyline_params["stroke_linecap"] = "square"

    dwg.add(dwg.polyline(**polyline_params))


def add_border(dwg, width, height, border_width=20, color="white"):
    """Add a border around the entire SVG."""
    dwg.add(
        dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill="none",
            stroke=color,
            stroke_width=border_width,
        )
    )


def find_available_position(used_positions, base_x, base_y):
    """Find an available position near the base position to avoid overlaps."""
    # Try the base position first
    if (base_x, base_y) not in used_positions:
        return base_x, base_y

    # Try positions in a spiral pattern around the base
    offset = 25  # Distance between overlapping IDs
    for attempt in range(1, 5):  # Try up to 4 alternative positions
        for dx, dy in [(offset, 0), (0, offset), (-offset, 0), (0, -offset)]:
            new_x = base_x + dx * attempt
            new_y = base_y + dy * attempt

            # Keep within bounds
            if 0 <= new_x <= width and 0 <= new_y <= height:
                if (new_x, new_y) not in used_positions:
                    return new_x, new_y

    # Fallback: return base position (will overlap)
    return base_x, base_y


def draw_block_id_at_position(dwg, text_x, text_y, block_id, color):
    """Draw the block ID at the specified position."""
    # Get the color hex value
    border_color = colors[color]

    # Add white background circle for better visibility
    dwg.add(
        dwg.circle(
            center=(text_x, text_y),
            r=10,
            fill="white",
            stroke=border_color,
            stroke_width=2,
            opacity=0.9,
        )
    )

    # Add the ID text
    dwg.add(
        dwg.text(
            str(block_id),
            insert=(text_x, text_y + 3),  # Slight vertical adjustment for centering
            font_size="10",
            font_weight="bold",
            fill="black",
            text_anchor="middle",
        )
    )


def add_grid(dwg, width, height, spacing=20):
    """Add coordinate grid and markers to the SVG for debugging/positioning."""
    # Add coordinate markers and grid lines every spacing pixels
    for x in range(0, width + 1, spacing):
        # Add vertical grid line
        dwg.add(
            dwg.line(
                start=(x, 0),
                end=(x, height),
                stroke="red",
                stroke_width=0.5,
                opacity=0.3,
            )
        )
        # Add x coordinate text
        dwg.add(dwg.text(str(x), insert=(x, 15), font_size="8", fill="red"))

    for y in range(0, height + 1, spacing):
        # Add horizontal grid line
        dwg.add(
            dwg.line(
                start=(0, y),
                end=(width, y),
                stroke="red",
                stroke_width=0.5,
                opacity=0.3,
            )
        )
        # Add y coordinate text
        dwg.add(dwg.text(str(y), insert=(5, y), font_size="8", fill="red"))


def main():
    """Generate and save the SVG pattern."""
    parser = argparse.ArgumentParser(description="Generate SVG patterns from JSON data")
    parser.add_argument("--data-file", required=True, help="Path to the JSON data file")
    args = parser.parse_args()

    svg_content = create_pattern(args.data_file)

    with open("pattern_combined.svg", "w") as f:
        f.write(svg_content["combined"])
    with open("pattern_color1.svg", "w") as f:
        f.write(svg_content["color1"])
    with open("pattern_color2.svg", "w") as f:
        f.write(svg_content["color2"])

    print(f"Generated SVG patterns from {args.data_file}")


if __name__ == "__main__":
    main()
