# Excalidraw icon libraries

Moved from `../SKILL.md` for progressive disclosure. Use this reference only when the activated workflow needs the detailed material below.

## Icon Libraries (Optional Enhancement)

For specialized diagrams (e.g., AWS/GCP/Azure architecture diagrams), you can use pre-made icon libraries from Excalidraw. This provides professional, standardized icons instead of basic shapes.

### When User Requests Icons

**If user asks for AWS/cloud architecture diagrams or mentions wanting to use specific icons: **

1. **Check if library exists **: Look for `libraries/<library-name>/reference.md`
2. **If library exists **: Proceed to use icons (see AI Assistant Workflow below)
3. **If library does NOT exist **: Respond with setup instructions:

   ```
   To use [AWS/GCP/Azure/etc.] architecture icons, please follow these steps:

   1. Visit https://libraries.excalidraw.com/
   2. Search for "[AWS Architecture Icons/etc.]" and download the .excalidrawlib file
   3. Create directory: skills/excalidraw-diagram-generator/libraries/[icon-set-name]/
   4. Place the downloaded file in that directory
   5. Run the splitter script:
      python skills/excalidraw-diagram-generator/scripts/split-excalidraw-library.py skills/excalidraw-diagram-generator/libraries/[icon-set-name]/

   This will split the library into individual icon files for efficient use.
   After setup is complete, I can create your diagram using the actual AWS/cloud icons.

   Alternatively, I can create the diagram now using simple shapes (rectangles, ellipses)
   which you can later replace with icons manually in Excalidraw.
   ```

### User Setup Instructions (Detailed)

**Step 1: Create Library Directory **
```bash
mkdir -p skills/excalidraw-diagram-generator/libraries/aws-architecture-icons
```

**Step 2: Download Library **
- Visit: https://libraries.excalidraw.com/
- Search for your desired icon set (e.g., "AWS Architecture Icons")
- Click download to get the `.excalidrawlib` file
- Example categories (availability varies; confirm on the site):
   - Cloud service icons
   - UI/Material icons
   - Flowchart symbols

**Step 3: Place Library File **
- Rename the downloaded file to match the directory name (e.g., `aws-architecture-icons.excalidrawlib`)
- Move it to the directory created in Step 1

**Step 4: Run Splitter Script **
```bash
python skills/excalidraw-diagram-generator/scripts/split-excalidraw-library.py skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
```

**Step 5: Verify Setup **
After running the script, verify the following structure exists:
```
skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
  aws-architecture-icons.excalidrawlib  (original)
  reference.md                          (generated - icon lookup table)
  icons/                                (generated - individual icon files)
    API-Gateway.json
    CloudFront.json
    EC2.json
    Lambda.json
    RDS.json
    S3.json
    ...
```

### AI Assistant Workflow

**When icon libraries are available in `libraries/`: **

**RECOMMENDED APPROACH: Use Python Scripts (Efficient & Reliable) **

The repository includes Python scripts that handle icon integration automatically:

1. **Create base diagram structure **:
   - Create `.excalidraw` file with basic layout (title, boxes, regions)
   - This establishes the canvas and overall structure

2. **Add icons using Python script **:
   ```bash
   python skills/excalidraw-diagram-generator/scripts/add-icon-to-diagram.py \
     <diagram-path> <icon-name> <x> <y> [--label "Text"] [--library-path PATH]
   ```
   - Edit via `.excalidraw.edit` is enabled by default to avoid overwrite issues; pass `--no-use-edit-suffix` to disable.

   **Examples **:
   ```bash
   # Add EC2 icon at position (400, 300) with label
   python scripts/add-icon-to-diagram.py diagram.excalidraw EC2 400 300 --label "Web Server"

   # Add VPC icon at position (200, 150)
   python scripts/add-icon-to-diagram.py diagram.excalidraw VPC 200 150

   # Add icon from different library
   python scripts/add-icon-to-diagram.py diagram.excalidraw Compute-Engine 500 200 \
     --library-path libraries/gcp-icons --label "API Server"
   ```

3. **Add connecting arrows **:
   ```bash
   python skills/excalidraw-diagram-generator/scripts/add-arrow.py \
     <diagram-path> <from-x> <from-y> <to-x> <to-y> [--label "Text"] [--style solid|dashed|dotted] [--color HEX]
   ```
   - Edit via `.excalidraw.edit` is enabled by default to avoid overwrite issues; pass `--no-use-edit-suffix` to disable.

   **Examples **:
   ```bash
   # Simple arrow from (300, 250) to (500, 300)
   python scripts/add-arrow.py diagram.excalidraw 300 250 500 300

   # Arrow with label
   python scripts/add-arrow.py diagram.excalidraw 300 250 500 300 --label "HTTPS"

   # Dashed arrow with custom color
   python scripts/add-arrow.py diagram.excalidraw 400 350 600 400 --style dashed --color "#7950f2"
   ```

4. **Workflow summary **:
   ```bash
   # Step 1: Create base diagram with title and structure
   # (Create .excalidraw file with initial elements)

   # Step 2: Add icons with labels
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw "Internet-gateway" 200 150 --label "Internet Gateway"
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw VPC 250 250
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw ELB 350 300 --label "Load Balancer"
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw EC2 450 350 --label "EC2 Instance"
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw RDS 550 400 --label "Database"

   # Step 3: Add connecting arrows
   python scripts/add-arrow.py my-diagram.excalidraw 250 200 300 250  # Internet → VPC
   python scripts/add-arrow.py my-diagram.excalidraw 300 300 400 300  # VPC → ELB
   python scripts/add-arrow.py my-diagram.excalidraw 400 330 500 350  # ELB → EC2
   python scripts/add-arrow.py my-diagram.excalidraw 500 380 600 400  # EC2 → RDS
   ```

**Benefits of Python Script Approach **:
- **No token consumption **: Icon JSON data (200-1000 lines each) never enters AI context
- **Accurate transformations **: Coordinate calculations handled deterministically
- **ID management **: Automatic UUID generation prevents conflicts
- **Reliable **: No risk of coordinate miscalculation or ID collision
- **Fast **: Direct file manipulation, no parsing overhead
- **Reusable **: Works with any Excalidraw library you provide

**ALTERNATIVE: Manual Icon Integration (Not Recommended) **

Only use this if Python scripts are unavailable:

1. **Check for libraries **:
   ```
   List directory: skills/excalidraw-diagram-generator/libraries/
   Look for subdirectories containing reference.md files
   ```

2. **Read reference.md **:
   ```
   Open: libraries/<library-name>/reference.md
   This is lightweight (typically <300 lines) and lists all available icons
   ```

3. **Find relevant icons **:
   ```
   Search the reference.md table for icon names matching diagram needs
   Example: For AWS diagram with EC2, S3, Lambda → Find "EC2", "S3", "Lambda" in table
   ```

4. **Load specific icon data ** (WARNING: Large files):
   ```
   Read ONLY the needed icon files:
   - libraries/aws-architecture-icons/icons/EC2.json (200-300 lines)
   - libraries/aws-architecture-icons/icons/S3.json (200-300 lines)
   - libraries/aws-architecture-icons/icons/Lambda.json (200-300 lines)
   Note: Each icon file is 200-1000 lines - this consumes significant tokens
   ```

5. **Extract and transform elements **:
   ```
   Each icon JSON contains an "elements" array
   Calculate bounding box (min_x, min_y, max_x, max_y)
   Apply offset to all x/y coordinates
   Generate new unique IDs for all elements
   Update groupIds references
   Copy transformed elements into your diagram
   ```

6. **Position icons and add connections **:
   ```
   Adjust x/y coordinates to position icons correctly in the diagram
   Update IDs to ensure uniqueness across diagram
   Add connecting arrows and labels as needed
   ```

**Manual Integration Challenges **:
- High token consumption (200-1000 lines per icon × number of icons)
- Complex coordinate transformation calculations
- Risk of ID collision if not handled carefully
- Time-consuming for diagrams with many icons

### Example: Creating AWS Diagram with Icons

**Request **: "Create an AWS architecture diagram with Internet Gateway, VPC, ELB, EC2, and RDS"

**Recommended Workflow (using Python scripts) **:
**Request **: "Create an AWS architecture diagram with Internet Gateway, VPC, ELB, EC2, and RDS"

**Recommended Workflow (using Python scripts) **:

```bash
# Step 1: Create base diagram file with title
# Create my-aws-diagram.excalidraw with basic structure (title, etc.)

# Step 2: Check icon availability
# Read: libraries/aws-architecture-icons/reference.md
# Confirm icons exist: Internet-gateway, VPC, ELB, EC2, RDS

# Step 3: Add icons with Python script
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw "Internet-gateway" 150 100 --label "Internet Gateway"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw VPC 200 200
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw ELB 350 250 --label "Load Balancer"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw EC2 500 300 --label "Web Server"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw RDS 650 350 --label "Database"

# Step 4: Add connecting arrows
python scripts/add-arrow.py my-aws-diagram.excalidraw 200 150 250 200  # Internet → VPC
python scripts/add-arrow.py my-aws-diagram.excalidraw 265 230 350 250  # VPC → ELB
python scripts/add-arrow.py my-aws-diagram.excalidraw 415 280 500 300  # ELB → EC2
python scripts/add-arrow.py my-aws-diagram.excalidraw 565 330 650 350 --label "SQL" --style dashed

# Result: Complete diagram with professional AWS icons, labels, and connections
```

**Benefits **:
- No manual coordinate calculation
- No token consumption for icon data
- Deterministic, reliable results
- Easy to iterate and adjust positions

**Alternative Workflow (manual, if scripts unavailable) **:
1. Check: `libraries/aws-architecture-icons/reference.md` exists → Yes
2. Read reference.md → Find entries for Internet-gateway, VPC, ELB, EC2, RDS
3. Load:
   - `icons/Internet-gateway.json` (298 lines)
   - `icons/VPC.json` (550 lines)
   - `icons/ELB.json` (363 lines)
   - `icons/EC2.json` (231 lines)
   - `icons/RDS.json` (similar size)
   **Total: ~2000+ lines of JSON to process **
4. Extract elements from each JSON
5. Calculate bounding boxes and offsets for each icon
6. Transform all coordinates (x, y) for positioning
7. Generate unique IDs for all elements
8. Add arrows showing data flow
9. Add text labels
10. Generate final `.excalidraw` file

**Challenges with manual approach **:
- High token consumption (~2000-5000 lines)
- Complex coordinate math
- Risk of ID conflicts

### Supported Icon Libraries (Examples — verify availability)

- This workflow works with any valid `.excalidrawlib` file you provide.
- Examples of library categories you may find on https://libraries.excalidraw.com/:
   - Cloud service icons
   - Kubernetes / infrastructure icons
   - UI / Material icons
   - Flowchart / diagram symbols
   - Network diagram icons
- Availability and naming can change; verify exact library names on the site before use.

### Fallback: No Icons Available

**If no icon libraries are set up: **
- Create diagrams using basic shapes (rectangles, ellipses, arrows)
- Use color coding and text labels to distinguish components
- Inform user they can add icons later or set up libraries for future diagrams
- The diagram will still be functional and clear, just less visually polished

