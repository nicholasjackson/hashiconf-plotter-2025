#!/usr/bin/env python3
import json
import random
import argparse

# Constants from the rules
SEGMENT_LENGTHS = [56, 113, 170]
COLORS = ["purple", "cyan"]
DIRECTIONS = ["northeast", "southeast"]

# Position changes for different segment lengths (from rules)
LENGTH_POSITION_CHANGES_NE = {
    56: (42, -42),
    113: (84, -84),
    170: (122, -122),
    226: (169, -169),
    282: (211, -211),
    336: (253, -253),
    452: (338, -338),
    560: (420, -420),
}

LENGTH_POSITION_CHANGES_SE = {
    56: (74, -74),
    113: (114, -114),
    170: (126, -126),
    226: (169, -169),
    282: (211, -211),
    336: (253, -253),
    452: (338, -338),
    560: (420, -420),
}

DIRECTIONS_WEIGHTS = {"northeast": 60, "southeast": 40}

BLOCK_WEIGHTINGS = {
    1: 40,
    2: 30,
    3: 30,
}

SEGMENT_WEIGHTINGS = {
    1: 20,
    2: 50,
    3: 30,
}

SEGMENT_LENGTHS_WEIGHTS = {
    56: 30,
    113: 40,
    170: 30,
}

COLORS_WEIGHTS = {"purple": 50, "cyan": 50}


def main():
    """Main function to generate and save the pattern."""
    parser = argparse.ArgumentParser(
        description="Generate pattern JSON according to rules"
    )
    parser.add_argument(
        "-o", "--output", default="pattern.json", help="Output JSON file"
    )
    parser.add_argument(
        "-s", "--seed", type=int, help="Random seed for reproducible patterns"
    )
    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Generate the pattern
    pattern = generate_pattern()

    # Save to file
    with open(args.output, "w") as f:
        json.dump(pattern, f, indent=2)

    # Count statistics
    total_blocks = 0
    purple_count = 0
    cyan_count = 0

    for layer in pattern["layers"]:
        for row in layer["rows"]:
            for block in row["blocks"]:
                total_blocks += 1
                if block["color"] == "purple":
                    purple_count += 1
                else:
                    cyan_count += 1

    print(f"Generated pattern saved to {args.output}")
    print(f"Total blocks: {total_blocks}")
    print(f"Purple blocks: {purple_count} ({purple_count / total_blocks * 100:.1f}%)")
    print(f"Cyan blocks: {cyan_count} ({cyan_count / total_blocks * 100:.1f}%)")
    print(f"Layers: {len(pattern['layers'])}")


def generate_pattern():
    """Generate the complete pattern according to the rules."""
    layer1_rows = []
    block_id_counter = 1

    # Starting position
    current_x = -10
    current_y = 60

    row_count = 0

    while True:
        print(f"Generating row {row_count} at position ({current_x}, {current_y})")

        # Generate blocks for this row
        blocks, block_id_counter = generate_row_blocks(
            current_x, current_y, block_id_counter
        )

        layer1_rows.append({"blocks": blocks})

        if current_y > 360 and current_x == -10:
            current_x = 52
            current_y = 400
        elif current_y == 400:
            current_x += 80
        else:
            current_y += 80

        if current_x > 260 and current_y > 360:
            break

        row_count += 1

    # Separate layers: extract rows with single blocks to layer 2
    layer1_final = []
    layer2_rows = []

    for row in layer1_rows:
        if len(row["blocks"]) == 1:
            # Single block row goes to layer 2
            layer2_rows.append(row)
        else:
            # Multi-block row stays in layer 1
            layer1_final.append(row)

    # Build final structure
    pattern = {"layers": []}

    # Add layer 1 if it has rows
    if layer1_final:
        pattern["layers"].append({"rows": layer1_final})

    # Add layer 2 if it has rows
    if layer2_rows:
        pattern["layers"].append({"rows": layer2_rows})

    # If no layers have content, ensure at least one empty layer
    if not pattern["layers"]:
        pattern["layers"].append({"rows": []})

    return pattern


def generate_row_blocks(start_x, start_y, block_id_counter):
    """Generate blocks for a single row."""
    blocks = []

    # Determine number of blocks in this row
    num_blocks = weighted_choice(BLOCK_WEIGHTINGS)

    current_x = start_x
    current_y = start_y

    for i in range(num_blocks):
        direction = weighted_choice(DIRECTIONS_WEIGHTS)

        # Override the direction tp set to northeast only
        ## if the previous block was northeast
        ## or this is the only block in the row
        if num_blocks == 1 or (
            i > 0 and blocks[i - 1]["segments"][0]["direction"] == "northeast"
        ):
            direction = "northeast"

        # Determine number of segments
        num_segments = weighted_choice(SEGMENT_WEIGHTINGS)

        # If we only have one block in the row, it must have a single segment
        if num_blocks == 1:
            num_segments = 1

        # Check if this is the last block in the row
        # We handle the length of the last blocks segments differently
        if i == num_blocks - 1:
            is_last_block = True
        else:
            is_last_block = False

        # Generate the block
        block = generate_block(block_id_counter, direction, num_segments, is_last_block)

        # Set the start position
        if i > 0 and blocks[i - 1]["segments"][0]["direction"] == "northeast":
            if block["segments"][0]["direction"] == "northeast":
                x_adjust = 0
                y_adjust = 0

                # Adjust gap if the previous block had a single segment
                # As there is no corner
                if len(blocks[i - 1]["segments"]) == 1:
                    x_adjust = -4
                    y_adjust = +4

                prev_len = blocks[i - 1]["segments"][0]["length"]
                current_x += LENGTH_POSITION_CHANGES_NE[prev_len][0] + x_adjust
                current_y += LENGTH_POSITION_CHANGES_NE[prev_len][1] + y_adjust
            else:  # southeast
                prev_len = blocks[i - 1]["segments"][0]["length"]
                current_x += LENGTH_POSITION_CHANGES_SE[prev_len][0]
                current_y += LENGTH_POSITION_CHANGES_SE[prev_len][1]
        elif i > 0 and blocks[i - 1]["segments"][0]["direction"] == "southeast":
            if block["segments"][0]["direction"] == "northeast":
                prev_len = blocks[i - 1]["segments"][0]["length"]
                current_x += 4
                current_y += -4
            else:  # southeast
                prev_len = blocks[i - 1]["segments"][0]["length"]
                current_x += 40
                current_y += -40

        block["x"] = current_x
        block["y"] = current_y
        blocks.append(block)
        block_id_counter += 1

    return blocks, block_id_counter


def generate_block(block_id, direction, num_segments, is_last_block=False):
    """Generate a single block."""

    # Determine color
    color = weighted_choice(COLORS_WEIGHTS)

    # Generate segments
    print(
        f"  Generating block {block_id} with direction {direction}, num_segments {num_segments}, is_last_block={is_last_block}, color {color}"
    )
    segments = generate_segments(num_segments, direction, is_last_block)

    return {"id": block_id, "segments": segments, "color": color}


def generate_segments(num_segments, direction, is_last_block=False):
    """Generate segments for a block."""
    segments = []

    for i in range(num_segments):
        segment_length = weighted_choice(SEGMENT_LENGTHS_WEIGHTS)

        # If the last segment of the last block and direction is northeast, force to 560 length
        if is_last_block and i == num_segments - 1 and direction == "northeast":
            segment_length = 560

        print(
            f"    Generating {i} segment, is_last_block {is_last_block}, direction {direction}, length {segment_length}"
        )

        segments.append({"direction": direction, "length": segment_length})

        # Alternate direction for next segment
        if direction == "northeast":
            direction = "southeast"
        else:
            direction = "northeast"

    return segments


def weighted_choice(weights):
    """Make a weighted random choice."""
    return random.choices(list(weights.keys()), weights=list(weights.values()))[0]


if __name__ == "__main__":
    main()
