# Rules
Rules for generating the pattern.

## Methodology
Use the following methodology to generate the pattern:
1. Start point: X=-10, Y=60
2. Row generation: Create blocks moving diagonally (increasing X for each block in the row)
3. Row progression: After completing a row, move to next row by increasing Y by 80
4. Repeat: Continue this process until out of space (Y > 400 and X > 260)

Move any blocks starting at X=-10 and only have a single segment to the second layer.

Ensure the ID numbers are continuous across both layers.

## Datastructure
The data structure of the pattern is as follows:
```json
{
  "layers": [
    {
      "rows": [
        {
          "blocks": [
            {
              "id": 1,
              "x": -10,
              "y": 60,
              "segments": [
                {
                  "direction": "northeast",
                  "length": 170
                },
                {
                  "direction": "southeast",
                  "length": 113
                }
              ],
              "color": "purple"
            },
            {
              "id": 2,
              "x": 116,
              "y": 24,
              "segments": [
                {
                  "direction": "northeast",
                  "length": 113
                }
              ],
              "color": "cyan"
            }
          ]
        },
        {
          "blocks": [
            {
              "id": 3,
              "x": -10,
              "y": 140,
              "segments": [
                {
                  "direction": "southeast",
                  "length": 113
                },
                {
                  "direction": "northeast",
                  "length": 170
                }
              ],
              "color": "purple"
            }
          ]
        }
      ]
    },
    {
      "rows": [
        {
          "blocks": [
            {
              "id": 4,
              "x": -10,
              "y": 220,
              "segments": [
                {
                  "direction": "northeast",
                  "length": 452
                }
              ],
              "color": "cyan"
            }
          ]
        }
      ]
    }
  ]
}
```

## Rows
* The first row starts at X = -10 and Y = 60
* Rows are positioned on a 45 degree angle northeast
* Each subsequent row increases Y by 80
* Each row contains blocks that can contain multiple segments
* Each row must have at least 1 block and no more than 3 blocks
* The weighting for the number of blocks is:
  * 1 block - 40%
  * 2 blocks - 30%
  * 3 blocks - 30%

## General rules for blocks
* Each block must have a unique ID number for validation
* Blocks within each layer should be ordered first by Y position (ascending), then by X position (ascending) for readability
* Each block must have between 1 and 3 segments
* Each segment must be between 40 and 500 units long
* Each segment must be one of the following directions:
  * Northeast (45 degrees)
  * Southeast (315 degrees)
* Distributions for the direction of segments is:
  * Northeast - 70%
  * Southeast - 30%
* The color of each block must be purple (#B596C8) or cyan (#63C3DC)
* The color distribution is:
  * Purple - 60%
  * Cyan - 40%
* The weighting for the number of segments in each block is:
  * 1 segments - 30%
  * 2 segments - 50%
  * 3 segments - 20%
* Blocks must only have the lengths in multiples of 56 to ensure they
  align with the next row, e.g.
  * 56
  * 113
  * 170
  * 226
  * 282
  * 336
  * 452
  * 560
* The first two segments should never have a length greater than 170, the exception
  is if it is pointing northeast and the final segment then it should be 560.

## Positioning of blocks
* When X is -10, Y can only be:
  * 60
  * 140
  * 220
  * 300
  * 380
* Y can not be larger than 380 when X is -10
* If X increases by 50 then Y must decrease by 50 to keep the pattern on the diagonal
* Blocks can not be positioned at an X > 260 and Y > 400 or Y < 0
* Example: if a row has 2 blocks the first starting at X = -10 and Y = 180 then position of
  the second block must be on a diagonal line from the first block. So the second block
  would be at X = 50 and Y = 120, the increase in X is 60 and the decrease in Y is 60.
* When a block at -10 starts southeast the next block must start northeast and from the same X
  position but the Y position must be increased by 80 to align with the next row.
* The next block must be positioned to start after the first segment of the previous block to ensure 
  the pattern is continuous in the row.
* Given the following segment lengths the x and y positions change by the following values:
  * Length 56, X +46, Y -46
  * Length 113, X +85, Y -85
  * Length 170, X +126, Y -126
* If the Y on a block will be greater than 380 then set the Y at 404 and the X at 46, from this 
  point blocks will increase in distance on the X by 80.
* If the current Y is 404 or greater and the X is 206 or greater for the first block then stop
  generating blocks.

## Layers
* The pattern is made up of 2 layers
* Layer 1 contains blocks that should only have multiple segments
* Layer 2 contains blocks that only have a single segment