# Development Process

## Tools Used
- **uv**: For managing Python environments and dependencies via inline script metadata (PEP 723).
- **requests**: For downloading the raw IBTrACS CSV file.
- **pandas**: For parsing, filtering, and aggregating the large dataset.
- **matplotlib & cartopy**: For creating the map-based visualization and the interactive year slider.
- **Git & GitHub**: For version control and hosting the repository.
- **VS Code**: As the primary code editor.

## Use of AI Tools
I used an AI assistant (ChatGPT/Claude) as a debugging partner and technical tutor throughout this assignment. Its role was strictly to unblock technical hurdles and explain concepts, while I retained full control of the design and implementation. Specifically, AI was helpful in:
- **Environment Setup**: Troubleshooting the installation of `uv` on Windows and explaining the purpose of the inline `# /// script` dependency blocks.
- **Git Troubleshooting**: Diagnosing and resolving a major Git push rejection caused by the 109MB CSV file exceeding GitHub's 100MB limit. The AI guided me through `git rm --cached`, adding `.gitignore`, and using `git reset HEAD~1` to clean up the commit history.
- **Code Generation**: Providing boilerplate code for advanced libraries like `cartopy` (for the map background) and `LineCollection` (for mapping wind speed to colors). The AI also assisted in writing the interaction logic for the `Slider` widget.
- **Documentation**: Polishing the English wording and structure of this README and PROCESS.md.
*(Note: I ran every script, verified the outputs, and adapted all AI-generated code to my specific dataset and trimmed file size requirements.)*

## One Thing Kept: Trimming the dataset to 2000¨C2026
I kept the `trim_data.py` script that filters the raw IBTrACS data to only include storms from 2000 onwards. 
**Why?** 
Initially, the raw dataset was 109MB, which exceeded GitHub's 100MB file size limit and caused multiple push failures. By trimming it to 2000¨C2026, the file size dropped to ~30MB, making it Git-friendly. More importantly, it improved the visualization: pre-2000 data was sparse and inconsistent, making the map look messy. Focusing on the recent two decades provided a clearer, denser "corridor" of storm tracks while still telling a compelling story.

## One Thing Rejected: Using `ax.plot()` in a loop
I rejected the traditional `ax.plot()` approach for drawing each storm track individually.
**Why?**
While `ax.plot()` is the standard way to draw lines, looping over thousands of storms (each with dozens of points) made the script extremely slow and memory-intensive. Furthermore, it does not easily support mapping a continuous color gradient (wind speed) to each track segment. I switched to `LineCollection`, which allows me to draw all tracks in a single batch and map `WMO_WIND` values directly to a color scale (light blue to dark red). This made the script run significantly faster and gave the visualization the ability to highlight intense storms clearly.

## Interaction Design
When the user selects a specific year using the bottom slider, the interface highlights that year's storm tracks with a colour gradient mapped to wind speed, while fading all other years into a light grey background. This allows the user to see how intense storms in a particular year compare to the historical "corridor" of all storms.