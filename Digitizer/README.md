# LinePilot Digitizer 2.17 — User Guide

## What is this?

**LinePilot Digitizer** turns a *picture of a graph* into *numbers you can use*. You give it an image of a chart (a screenshot, a scan, a figure from a paper), and it reads the curve off the picture and hands you back a **spreadsheet-friendly table of data points** (a CSV file) plus an **overlay image** that shows you exactly which points it detected, drawn on top of your original graph. That way you can check its work at a glance.

There are **two ways to use it**:

- **The click-and-go app** — a normal program for **Windows** and **macOS**. Double-click and follow the on-screen steps. No coding, nothing to install. **This is what most people want.**
- **The command line** — a one-line typed command for people who like terminals or want to process images quickly. This needs Python and the source files (see [Using the command line](#using-the-command-line)).

If you just want your data out, head to the [Quick start](#quick-start).

> **New to all this?** Don't worry about the technical words yet. Just follow [Quick start](#quick-start) and then [Using the app](#using-the-app-step-by-step) — every button is explained as you go. You can ignore the entire command-line half of this guide.


### Find the instructions for your computer

| | **Windows** | **Mac** |
| --- | --- | --- |
| Download and open the app | [On Windows](#on-windows) | [On a Mac](#on-a-mac) |
| The first-launch security warning | [SmartScreen: *Run anyway*](#the-first-run-windows-warning-expected) | [Gatekeeper: *Open Anyway*](#the-first-run-mac-warning-expected) |
| Install Python to use the command line | [On Windows](#on-windows-1) | [On a Mac](#on-a-mac-1) |
| Open a terminal | [On Windows](#open-a-terminal-in-the-digitizer-folder) | [On a Mac](#open-a-terminal-in-the-digitizer-folder) |
| Build the app yourself | [Starter command (Windows)](#starter-command-windows) | [Starter command (macOS)](#starter-command-macos) |
| Something went wrong | [Opening the app on Windows](#opening-the-app-on-windows) | [Opening the app on a Mac](#opening-the-app-on-a-mac) |

Every command-line example shows the Windows and the Mac command one after the other — start with [Windows and Mac at a glance](#windows-and-mac-at-a-glance) and [Your first run, step by step](#your-first-run-step-by-step).

---

## Quick start

1. **Download the app for your computer** from the **[latest release](https://github.com/RayanA07/LinePilot/releases/latest)** — scroll to the heading **Assets**:
   - **Windows:** `Digitizer.exe`
   - **Mac:** `Digitizer-macOS-AppleSilicon.zip` (M1–M4 Macs) or `Digitizer-macOS-Intel.zip` (Intel Macs)

   (Exact clicks for each, with what the pages look like: [On Windows](#on-windows) · [On a Mac](#on-a-mac).)
2. **Open it.** Windows: double-click `Digitizer.exe`. Mac: double-click the zip, then double-click `Digitizer.app`. (*Double-click* means quickly press the mouse button twice in a row on the icon.) The very first time, your computer shows a security warning — that's expected; here is what to click on [Windows](#the-first-run-windows-warning-expected) and on a [Mac](#the-first-run-mac-warning-expected).
3. In the app, work top to bottom: **Import** your graph image → set the **curve color** → run **Axis Detection** → run **Calibration** → **Place Points** → **Export** to CSV.

That's the whole flow. **Don't worry if those words mean nothing yet** — each one is explained, with exactly what to click, in [Using the app](#using-the-app-step-by-step) below. The app looks and works the same on Windows and Mac.

---

## Download & install (no Python needed)

You do **not** need Python, and you do **not** need to install anything. The OCR engine (the part that reads the axis numbers) is already built into the app, on both Windows and Mac.

| | **Windows** 10 / 11 (64-bit) | **Mac** — macOS 15 Sequoia or later |
| --- | --- | --- |
| **File to download** | `Digitizer.exe` | `Digitizer-macOS-AppleSilicon.zip` or `Digitizer-macOS-Intel.zip` |
| **Direct link** | [Digitizer.exe](https://github.com/RayanA07/LinePilot/releases/latest/download/Digitizer.exe) | [Apple Silicon](https://github.com/RayanA07/LinePilot/releases/latest/download/Digitizer-macOS-AppleSilicon.zip) · [Intel](https://github.com/RayanA07/LinePilot/releases/latest/download/Digitizer-macOS-Intel.zip) |
| **First-run warning** | SmartScreen → [what to click](#the-first-run-windows-warning-expected) | Gatekeeper → [what to click](#the-first-run-mac-warning-expected) |

### On Windows

#### Step 1 — Open the Releases page

Go to <https://github.com/RayanA07/LinePilot/releases/latest>.

This is a GitHub *release page*. It shows a title and a description at the top. **Scroll down** past the description until you see a grey heading called **Assets** with a small triangle next to it. If the list under it looks collapsed, click the word **Assets** to open it.

#### Step 2 — Download the program

In the **Assets** list, click the file named **`Digitizer.exe`**. (Ignore the green **Source code (zip)** and **Source code (tar.gz)** links — you do not need those, and ignore the `macOS` zips, which are for Macs.)

Your browser will **download** the file rather than open it. Edge or Chrome may warn that the file is "not commonly downloaded" and offer **Keep** or **Discard** — choose **Keep** (then **Keep anyway** if it asks again). If you accidentally chose Discard, nothing is harmed — just click `Digitizer.exe` again and choose Keep.

> *Optional:* if you also want the accuracy-checking tool, download **`AccuracyTester.exe`** the same way — see the [last section](#accuracy-tester-optional).

#### Step 3 — Find the downloaded file

The file lands in your **Downloads** folder. To get there: open **File Explorer** (the yellow folder icon on the taskbar, or press the **Windows key + E**), then click **Downloads** in the left-hand list.

You can leave it there, or drag it somewhere easy to find like your **Desktop**. There is nothing to "install" — the `.exe` *is* the program.

#### Step 4 — Launch it

**Double-click `Digitizer.exe`** (quickly press the left mouse button twice in a row on its icon) to open the app.

#### The first-run Windows warning (expected)

The first time you run it, Windows SmartScreen may show a blue box that says **"Windows protected your PC."** This is **not** a virus warning. It appears because the file is not "code-signed" (a paid certificate the author hasn't bought), and Windows is cautious about any program it hasn't seen before.

To run it:

1. The box at first shows only a **Don't run** button — **do not click that.** Instead, click the small **More info** text in the middle of the box.
2. A **Run anyway** button now appears. Click it.

*(If you accidentally clicked **Don't run**, nothing bad happened — just double-click `Digitizer.exe` again and try the steps above.)*

You'll only need to do this once. If double-clicking does **nothing at all** — no window and no warning — see [Troubleshooting](#troubleshooting) (*Smart App Control*).

### On a Mac

#### Step 1 — Check which kind of Mac you have

Click the **Apple menu** (the Apple logo in the top-left corner of the screen) → **About This Mac**.

- If it says **Chip: Apple M1** (or M2, M3, M4…), you have an **Apple Silicon** Mac.
- If it says **Processor: …Intel…**, you have an **Intel** Mac.

The app needs **macOS 15 Sequoia or later** (the same window shows your macOS version). The exact minimum for each download is printed at the top of the release page; on Sequoia, install the latest updates first (**System Settings → General → Software Update**).

#### Step 2 — Download the program

Go to <https://github.com/RayanA07/LinePilot/releases/latest>, scroll down to the grey **Assets** heading (click it if the list is collapsed), and click:

- **`Digitizer-macOS-AppleSilicon.zip`** for an Apple Silicon Mac, or
- **`Digitizer-macOS-Intel.zip`** for an Intel Mac.

(Ignore **Source code**, and ignore the `.exe` files — those are for Windows.)

> *Optional:* the accuracy-checking tool is **`AccuracyTester-macOS-AppleSilicon.zip`** / **`AccuracyTester-macOS-Intel.zip`** — see the [last section](#accuracy-tester-optional).

#### Step 3 — Unzip it

Open your **Downloads** folder (in the Dock, or in **Finder → Downloads**) and **double-click the zip**. macOS unpacks it into **`Digitizer.app`** right next to it.

There is nothing to "install" — `Digitizer.app` *is* the program. You can drag it into your **Applications** folder so it shows up in Launchpad, or leave it where it is.

#### Step 4 — Launch it

**Double-click `Digitizer.app`** to open the app.

#### The first-run Mac warning (expected)

The first time you open it, macOS shows a box saying it **could not verify** that *"Digitizer" is free of malware*. This is **not** a virus warning. It appears because the app isn't "notarized" (a check that needs a paid Apple Developer account the authors haven't bought), and macOS is cautious about any app downloaded from the internet.

To open it:

1. Click **Done** in that box (not *Move to Trash*).
2. Open **System Settings** (Apple menu → System Settings) → **Privacy & Security**.
3. Scroll down to the message *"Digitizer" was blocked to protect your Mac* and click **Open Anyway**. Confirm with your password or Touch ID, then click **Open Anyway** once more.

You'll only need to do this once; after that it opens with a normal double-click.

> If macOS says the app **"is damaged and can't be opened"**, the download's quarantine flag is stuck. Open **Terminal** (press **⌘ + Space**, type *Terminal*, press Return), paste the line below (change the path if the app isn't in Applications), press Return, and open the app again:
>
> ```bash
> xattr -dr com.apple.quarantine /Applications/Digitizer.app
> ```
>
> If macOS says **"You can't use this version of the application with this version of macOS"**, your Mac is older than the download supports — update macOS, or [run from source](#run-from-source-for-developers), which works on older versions too.

---

## Using the app (step by step)

When the app opens you'll see your future graph in the big main area, a floating **Cursor Zoom** panel in the top-right corner, and a **status bar** along the bottom. A few things to know up front:

- **The status bar is the thin strip along the very bottom edge of the window.** It shows a short message after every action — **watch it.** It confirms success or tells you why something didn't work. At the start it reads *"Load an image to begin."*
- **Cursor Zoom** is just a magnifying glass — it shows an enlarged view of whatever is under your mouse so you can click precisely. It's a helper only; it has nothing to do with exporting.
- **Import, Tools, Advanced, and Export are buttons along the top of the window.** Clicking one opens a small menu of choices. Throughout this guide, "open the **Tools** button → **Pick Color**" means: click **Tools** at the top, then click **Pick Color** in the menu that drops down.

Follow these steps in order. **On a Mac** everything works the same; the only differences are that undo is **⌘Z** instead of **Ctrl+Z**, and dialogs look like normal Mac dialogs.

### 1. Load your graph image

Click the **Import** button (top-left), then choose:

- **Import Image** — to pick a file from your computer (PNG, JPG, JPEG, BMP, TIF/TIFF), or
- **Paste Image** — to use a screenshot you've already copied to the clipboard.

Your chart appears in the main area. The app automatically guesses your curve's color and shows it as the first colored square in the **Selected color** row at the bottom of the window.

### 2. Confirm or set the curve color

Look at the auto-picked color square in the **Selected color** row (the strip of colored squares near the bottom).

- If it already matches your data line, **keep it** — you're done with this step.
- To set it yourself: open the **Tools** button, click **Pick Color** (your cursor becomes a crosshair), then click directly on the curve in the image. The color square updates, and Pick Color turns itself off.

> **Tracing more than one curve?** Click the small green **`+`** square in the Selected color row to add another color slot, select it, then use Pick Color again for that line. (Most people only have one curve and can skip this.)

### 3. Read the axis numbers automatically

Open the **Advanced** button → **Axis Scale Detection** submenu → click **Run Axis Detection**.

The app uses OCR (text recognition) to read the numbers printed along your axes and automatically fills in the four boxes in the **Min-Max Coordinates** panel: **X min, X max, Y min, Y max**. The same submenu also displays the detected values for reference.

### 4. Check and fix the axis numbers

Look at the four **Min-Max Coordinates** boxes. OCR is good but not perfect, so **always sanity-check them.** If any value is missing or misread, just **type the correct number into the box** yourself.

> These four values are required. Export will not run until all four boxes contain valid numbers.

### 5. Calibrate the plot box

This tells the app exactly where your plotted area sits in the image. Open **Tools → Calibration**, then choose one:

- **Coordinate-Mediated Calibration** *(recommended — easiest)* — run **Axis Detection** first (step 3), because this option uses those detected axis positions. It automatically snaps a **dashed green box** onto your plot area. **If you ran step 3, use this and you can skip manual calibration entirely.**
- **Manual Calibration** *(by hand)* — you click four ticks **directly on your chart image**. A **large green step-by-step banner** appears above the image and walks you through each click in order: **X MIN** (smallest X), **X MAX** (largest X), **Y MIN** (smallest Y), **Y MAX** (largest Y), telling you exactly which point to click at each step. You are clicking *locations on the picture*, not typing numbers. The points don't have to be in textbook positions — the box is built correctly from wherever you click, as long as **X MIN is left of X MAX** and **Y MIN is below Y MAX**.

Either way, you'll end up with a **dashed green box** (a rectangle drawn with a dashed green outline) marking the plotted region.

> If you pick Coordinate-Mediated Calibration without running Axis Detection first, the status bar will say *"Run Axis Scale Detection first."*

### 6. Adjust the box if needed (optional)

If the dashed green box edges don't line up exactly with your axes, hover over an edge until the cursor becomes a **resize arrow**, then **drag** it into place. The app remembers your adjusted box for export.

### 7. Extract the data points

Open **Tools → Place Points → Run**.

The app scans the image for your chosen color and overlays the detected points on the curve. The **status bar tells you how many points were placed.**

> **Stray text or a legend getting picked up as data?** Use the optional **Masking** tools first. Under **Advanced → Masking** you can blank out words, numbers, or a legend, or hand-draw mask rectangles (Manual Mask Mode), so they aren't mistaken for your curve. Do this *before* Place Points. There's also a **Clear Masks** option to undo them.

### 8. Choose which colors to export (only for multiple curves)

If you traced more than one curve: open the **Export** button → **Colors to Export** submenu, and tick the color slots you want (or choose **Active Color Only** / **All Configured Colors**). **With a single curve this is already handled for you** — skip it.

### 9. Export your data

Open the **Export** button and choose:

- **Export CSV → Raw values** — a plain text spreadsheet file that opens in Excel, Google Sheets, Python, etc.
- **Export Excel → Raw values** — a real Excel `.xlsx` workbook.

A standard **Save** dialog appears (**Save As** on Windows). **Note which folder is shown at the top** (Downloads or Desktop are easy choices so you can find it again), keep the suggested name **`digitized_points.csv`**, and click **Save**.

**That's it — you now have a spreadsheet of your graph's data.** To open it, go to the folder you just saved into and **double-click the CSV file**; it opens in Excel by default (Numbers on a Mac, if Excel isn't installed), where you'll see your X and Y columns.

### Where your files go

Exports go **wherever you choose in the Save dialog** — they are not forced into a fixed folder, so make a note of the location you pick. The app suggests the filename **`digitized_points.csv`** (or **`digitized_points.xlsx`** for Excel) and forces the correct extension.

Each row in the file is one detected point, with these columns:

| Column | Meaning |
| --- | --- |
| `color_slot` | which color slot the point belongs to (1 for a single curve) |
| `color_r`, `color_g`, `color_b` | the curve's color (0–255 each) |
| `x`, `y` | the real-world data values |
| `x_px`, `y_px` | the original pixel position in the image |

The CSV is saved as UTF-8, with one header row followed by one row per point.

> **Excel export needs a helper library** (`openpyxl`). In the prebuilt app it's already included. If you're running from source and it's missing, the status bar will say so and nothing is saved — use CSV instead, or install it (see [Run from source](#run-from-source-for-developers)).

### Two things that block export (and how the app tells you)

Export will **quietly refuse** and show a status message unless **both** of these are true:

1. **The four Min-Max Coordinate boxes contain valid numbers** — otherwise you'll see *"Export requires X/Y min/max values."*
2. **A calibration has been run** (the dashed green box exists) — otherwise you'll see *"Export requires calibration."*

If either message appears, glance at the status bar, go back, and finish that step.

### Log-scale axes (optional)

Most plots are linear, so leave this alone for a normal graph — but if your graph uses a **logarithmic** X or Y axis, turn it on with the small **log** toggle buttons that sit just to the **right of the Min-Max Coordinates boxes** (one on the X-min/X-max row, one on the Y-min/Y-max row):

- Click the **log** button beside the X boxes and/or the one beside the Y boxes. It turns **green** when it's on.
- Calibrate and enter the axis min/max **as the real numbers printed on the axis** (e.g. `1` and `1000`), exactly as you would for a linear plot.
- On export, that axis is interpolated in log space, so the values come out correct for a log scale. Leave the buttons off (grey) for normal linear axes.

> A log axis needs **positive** min/max values (you can't take the log of zero or a negative number). If a value is zero or negative, export will tell you instead of producing wrong numbers.

### Tips for the best results

- A **clean, distinctly-colored curve** works best. Point extraction matches your selected color within a tolerance and takes the vertical midpoint of matching pixels in each column.
- **Loading a new image resets everything** — points, color slots, calibration, and the coordinate boxes. Finish one image before loading the next.
- If **Axis Detection** ever says Tesseract OCR isn't available, just **type the four axis values in by hand** (step 4) — everything else still works.
- Stuck on an error? **Advanced → Error Log** opens a window of recent errors.

---

# For developers

> **Using the click-and-go app? You can stop here.** Everything below is the optional command-line and build-from-source material for people comfortable with a terminal. If you just want your data, you're already done — see [Troubleshooting](#troubleshooting) if anything went wrong.

## Using the command line

> **Important:** The command line runs from the **source files with Python installed** — see [Run from source](#run-from-source-for-developers). The prebuilt **`Digitizer.exe` / `Digitizer.app` is the click-and-go app only**: it always opens the graphical window and ignores any command-line options. If you want to type commands, you need the source code and Python, not the downloaded app.

Every command on this page is shown twice: once for **Windows** (PowerShell) and once for **Mac** (Terminal). The options are identical on both; only the word that starts Python and the way paths are written differ.

### Windows and Mac at a glance

| | **Windows** | **Mac** |
| --- | --- | --- |
| Where you type commands | **PowerShell** / Windows Terminal | **Terminal** (Applications → Utilities, or **⌘ + Space**, type *Terminal*) |
| Open it in the `Digitizer` folder | right-click inside the folder → **Open in Terminal** | right-click the folder → **New Terminal at Folder** |
| Before your first command | nothing | `source .venv/bin/activate` (the [virtual environment](#on-a-mac-1)) |
| Start Python with | `py` | `python3` (or `python` once the virtual environment is active) |
| A path to an image | `"C:\Users\You\Pictures\graph.png"` | `~/Pictures/graph.png` |
| Default output folder | `C:\Users\You\Downloads` | `~/Downloads` (`/Users/you/Downloads`) |
| Open the output folder | `explorer $HOME\Downloads` | `open ~/Downloads` |
| Built-in help | `py digitizer.py --help` | `python3 digitizer.py --help` |

### Open a terminal in the Digitizer folder

**On Windows**

1. Open the folder that contains the Digitizer source files in **File Explorer**.
2. **Right-click an empty area** inside the folder.
3. Choose **Open in Terminal** (or **Open PowerShell window here**).

A blue/black window opens, already pointed at the right folder. Type your commands there.

**On a Mac**

1. In **Finder**, find the `Digitizer` folder inside the source code.
2. **Right-click** (or Control-click) the folder and choose **New Terminal at Folder**. *(Not in the menu? Turn it on once in System Settings → Keyboard → Keyboard Shortcuts → Services → Files and Folders. Or open Terminal and type `cd ` — with a space — then drag the `Digitizer` folder onto the Terminal window and press Return.)*
3. Activate the virtual environment from [Run from source](#on-a-mac-1):

   ```bash
   source .venv/bin/activate
   ```

   The prompt now starts with `(.venv)`. You need to do this once each time you open a new Terminal window.

> The examples below use the placeholder image name **`graph.png`**. Substitute the real name of your own image file. The image must be either in the folder the terminal is pointed at, or in your **Downloads** folder, or you must give its full path (in quotes on Windows if it contains spaces; on a Mac, drag the image file onto the Terminal window to paste its full path).

### Your first run, step by step

The source code includes a real Raman spectrum, so you can try the command line before using your own image. From a terminal in the `Digitizer` folder:

**Windows** (PowerShell)

```powershell
py digitizer.py ..\docs\assets\demo\example_raman.png
explorer $HOME\Downloads
```

**Mac** (Terminal, with `(.venv)` showing)

```bash
python3 digitizer.py ../docs/assets/demo/example_raman.png
open ~/Downloads
```

The first command prints:

```text
Success. Output -> /Users/you/Downloads
    example_raman_digitized_points.csv
    example_raman_digitized_overlay.png
```

(on Windows the folder reads `C:\Users\You\Downloads`). The second command opens that folder: double-click the **CSV** to see the numbers in Excel or Numbers, and open the **overlay PNG** to check that the purple dots sit on the curve. To see what it worked out along the way, add `--verbose 1`:

```text
Digitized successfully.
    color (r,g,b)  : 125, 0, 255
    pixel coords   : x_min=(162, 775) x_max=(1077, 775) y_min=(116, 764) y_max=(116, 22)
    tick -> values : x_min=400.0 x_max=1800.0 y_min=2000.0 y_max=14000.0  (OCR)
    OCR confidence : 96.0%
    num points     : 916
```

That's the whole loop. Now swap in your own image.

### The simplest command

Give it an image. That's it:

**Windows**

```powershell
py digitizer.py graph.png
```

**Mac**

```bash
python3 digitizer.py graph.png
```

With nothing else, the app automatically:

1. **detects the curve color**,
2. **detects the axes and tick positions** with OCR (so it reads X min / X max / Y min / Y max straight off the image), and
3. **writes a CSV of data points plus an overlay PNG** to your **Downloads** folder.

A bare filename like `graph.png` is looked up first in the current folder, then in your Downloads folder — so the one-liner works as long as the image is in either place. By default it stays quiet: it prints just a success line and the output folder. Add **`--verbose 1`** to see the full detail — the color, pixel coordinates, the OCR readings, the point count, and the **OCR confidence score** (see [Seeing more detail](#seeing-more-detail---verbose)).

> Two other spellings do exactly the same thing: `digitizer_2_11.py cli graph.png` and `digitizer_2_11.py digitize graph.png` (started with `py` on Windows, `python3` on a Mac).

### Options

Add any of these to the command for more control. They are the same on Windows and Mac:

| Option (aliases) | What it does | Default |
| --- | --- | --- |
| `pic_path` *(positional)* | Path to the image. A bare filename is searched in the current folder, then Downloads. Either this **or** `--pic-dir` is required. | none (required) |
| `--pic-dir` | Another way to give the image path. If both are given, `--pic-dir` wins. | none |
| `--color R,G,B` | Curve color, e.g. `255,0,0` (each part 0–255). Also accepts `[r,g,b]`. **Must match your curve's actual color**, or the run finds no points. | auto-detected |
| `--axis-values` *(`--axis`)* | Axis numbers as `xmin,xmax,ymin,ymax`. X min must differ from X max, and Y min from Y max. | read by OCR |
| `--ticks` *(`--tick-setting`, `--tick-coordinates`)* | Four tick pixel points in `x_min,x_max,y_min,y_max` order, e.g. `[10,200],[500,200],[10,200],[10,20]`. | found by OCR |
| `--log-x` | Read the X axis in base-10 **log** space (X min/max must be positive). Mirrors the GUI's **log** toggle. | off (linear) |
| `--log-y` | Read the Y axis in base-10 **log** space (Y min/max must be positive). Mirrors the GUI's **log** toggle. | off (linear) |
| `--output-dir` *(`--out`, `-o`)* | Folder to save into. Created if it doesn't exist. | your Downloads folder |
| `--verbose N` *(`-v`)* | How much to print. `1` (or a bare `-v` / `--verbose`) shows the color, pixel coords, tick→OCR values, point count, and OCR confidence, and writes a `<image>_log.txt`. `0` prints only success + the output folder. | `0` (quiet) |
| `--json` | Print the result details as JSON instead of plain text. | off |
| `-h` / `--help` | Show the usage help and exit. | — |
| `--normalize-y` *(optional extra)* | Adds an extra `y_norm` column (Y rescaled to 0–1 over the axis range). Leave it off for normal use. | off |
| `--limit-to-calibration` *(optional extra)* | Export **only** points inside the calibration box. **Off by default** (since 2.14): if OCR reads an extreme tick slightly short, the box would otherwise clip real data off the ends of the curve. | off |
| `--no-limit-to-calibration` *(optional extra)* | Also export points outside the calibration box. This is **already the default**; the flag is kept so older scripts keep working. | (the default) |

### The "fill-in-the-blank" template and function-call style

If you'd like a copy-and-edit reference, run:

**Windows**

```powershell
py digitizer.py template
```

**Mac**

```bash
python3 digitizer.py template
```

This **prints a fill-in-the-blank line** (it does **not** digitize anything). It shows a minimal example, a full example listing every option, and a short legend explaining each value — already written for the computer you run it on.

You can then run that **function-call form** — one quoted line. In PowerShell and in the Mac Terminal alike, wrap the whole `digitizer_cli(...)` call in **single quotes** so the inner double quotes survive. *(On a Mac this is required: without the single quotes the shell itself rejects the brackets with* `no matches found` *or* `unknown file attribute`*.)*

**Minimal example** (just the image; everything else auto-detected). This is the form to copy first:

**Windows**

```powershell
py digitizer.py 'digitizer_cli(pic_dir="graph.png")'
```

**Mac**

```bash
python3 digitizer.py 'digitizer_cli(pic_dir="graph.png")'
```

**Full example** — the `color`, `axis_values`, and `tick_setting` values below are **placeholders you must edit to match your own chart.** A leftover `color=(255,0,0)` (red) on a non-red curve finds no points and exits with *"produced no points."* Either delete the options you don't need (so those values auto-detect) or replace them with your real values:

**Windows**

```powershell
py digitizer.py 'digitizer_cli(pic_dir="graph.png", color=(255,0,0), axis_values=(0,10,0,100), tick_setting=([10,200],[500,200],[10,200],[10,20]), log_x=False, log_y=False, output_dir="C:/Users/You/Downloads/out", verbose=1, json=False, normalize_y=False, limit_to_calibration=False)'
```

**Mac**

```bash
python3 digitizer.py 'digitizer_cli(pic_dir="graph.png", color=(255,0,0), axis_values=(0,10,0,100), tick_setting=([10,200],[500,200],[10,200],[10,20]), log_x=False, log_y=False, output_dir="~/Downloads/out", verbose=1, json=False, normalize_y=False, limit_to_calibration=False)'
```

(`~` means your home folder; it works inside the quotes too.)

The values you can put inside `digitizer_cli(...)`:

| Name (aliases) | What it is | Default |
| --- | --- | --- |
| `pic_dir` *(`pic_path`, `plot_location`, `image`, `image_path`)* | **Required.** The image path; a bare filename is looked up in the current folder, then Downloads. | none (required) |
| `color` *(`rgb`, `color_rgb`)* | Curve color as `(R,G,B)` or `"255,0,0"`. Blank = auto-detect. Must match your curve's real color. | auto-detected |
| `tick_setting` *(`ticks`, `tick_coordinates`, `tick_coordinate`)* | Four tick pixel points in `x_min,x_max,y_min,y_max` order. Blank = OCR. | OCR-detected |
| `axis_values` *(`axis`, `bounds`)* | Axis numbers as `(xmin,xmax,ymin,ymax)`. Blank = OCR. | OCR-detected |
| `log_x` *(`logx`, `x_log`)* | `True` reads the X axis in base-10 log space (X min/max must be positive). | False |
| `log_y` *(`logy`, `y_log`)* | `True` reads the Y axis in base-10 log space (Y min/max must be positive). | False |
| `output_dir` *(`out_dir`, `out`)* | Folder to save into. Blank = Downloads. | Downloads |
| `verbose` *(`v`)* | `1` prints full detail and writes a `<image>_log.txt`; `0` stays quiet. | `0` |
| `json` *(`as_json`, `print_json`)* | `True` prints full details as JSON. **Only accepted in this function-call form** (the flag version is `--json`). | False |
| `normalize_y` *(`normalize`)* — *optional extra* | `True` adds the `y_norm` (0–1) column. Leave off for normal use. | False |
| `limit_to_calibration` *(`limit`)* — *optional extra* | `True` keeps only points inside the calibration window. | False |

Arguments can be **positional** in the order `pic_dir, color, tick_setting, axis_values, output_dir`, or by **name** using any alias above. Empty positions are allowed and fall back to defaults, and the words `none` / `null` / blank are treated as "auto".

### Worked examples

Auto-detect everything (color and axes), save to Downloads — **the safest example to copy as-is**:

**Windows**

```powershell
py digitizer.py graph.png
```

**Mac**

```bash
python3 digitizer.py graph.png
```

Set the axis values yourself but still auto-detect the color:

**Windows**

```powershell
py digitizer.py graph.png --axis 0,10,0,100
```

**Mac**

```bash
python3 digitizer.py graph.png --axis 0,10,0,100
```

Force a specific curve color — **change `130,5,255` to your curve's real R,G,B**; a color that doesn't match the curve produces no points:

**Windows**

```powershell
py digitizer.py graph.png --color 130,5,255 --axis 0,10,0,100
```

**Mac**

```bash
python3 digitizer.py graph.png --color 130,5,255 --axis 0,10,0,100
```

Use a full path, choose an output folder, and read the Y axis on a **log scale**:

**Windows**

```powershell
py digitizer.py "C:\path\to\graph.png" --out "C:\path\to\out" --log-y
```

**Mac**

```bash
python3 digitizer.py ~/path/to/graph.png --out ~/path/to/out --log-y
```

See everything the run worked out — color, pixel coordinates, the tick→OCR values, point count, and the **OCR confidence score** — and drop a `log.txt` alongside the output:

**Windows**

```powershell
py digitizer.py graph.png --verbose 1
```

**Mac**

```bash
python3 digitizer.py graph.png --verbose 1
```

> **Tip:** There's also an interactive wizard that asks for each field one at a time. Start it with `py digitizer_2_11.py interactive` on Windows or `python3 digitizer_2_11.py interactive` on a Mac (`wizard` works too).

### A whole folder at once (batch mode)

Put your chart images in one folder and point `digitizer_batch_cli.py` at it. Every image is digitized; a file that fails (not a plot, unreadable axes) is recorded in the report and never stops the run.

**Windows**

```powershell
py digitizer_batch_cli.py "C:\Users\You\Downloads\charts" --out "C:\Users\You\Downloads\charts_digitized"
```

**Mac**

```bash
python3 digitizer_batch_cli.py ~/Downloads/charts --out ~/Downloads/charts_digitized
```

It prints one line per image (`[1/2] a.png ... ok (916 points, 0.7s)`) and a summary, and writes `digitized_csvs/`, `digitized_overlays/`, `batch_report.csv` and `batch_report.json` into the output folder (into the image folder itself if you leave out `--out`). The same `--color`, `--axis`, `--log-x`, `--log-y` and `--verbose` options apply, to every image. Run it with `--help` for the full list.

### Seeing more detail (`--verbose`)

By default the command line is **quiet** — it just confirms success and tells you the output folder. When you want to see (or keep a record of) exactly what the tool did, raise the verbosity:

**Windows**

```powershell
py digitizer.py graph.png --verbose 1
```

**Mac**

```bash
python3 digitizer.py graph.png --verbose 1
```

At level `1` it prints, and the run also writes a `<image>_log.txt`, the following:

- **color (r,g,b)** — the curve color it used.
- **pixel coords** — where the four axis ticks sit in the image, in pixels.
- **tick → values** — the four axis numbers (X min, X max, Y min, Y max) the tool used, and whether it read them automatically or you typed them in.
- **OCR confidence** — how sure the built-in number-reader (Tesseract) was about the axis numbers it read off your image, as a percentage. A low number is a hint to double-check the numbers, or to type them in yourself with `--axis`. Shows **n/a** only when you supply *both* the axis values **and** the tick pixel coordinates yourself (so no reading is done); if you pass `--axis` but let the tick positions auto-detect, the reader still runs and a percentage is shown.
- **num points** — how many data points were extracted.
- **elapsed (s)** — how long the run took, in seconds.

Level `0` (the default) stays quiet; you can also write just `--verbose` or `-v` as shorthand for level `1`.

### Output files

Every run writes two files (named after your image), plus a third at `--verbose 1`:

- **`<imageName>_digitized_points.csv`** — the table of digitized points.
- **`<imageName>_digitized_overlay.png`** — a copy of your image with the calibration box, the OCR axis-detection rectangles, and the detected points drawn on top (in the inverse of the curve color, so they stand out).
- **`<imageName>_log.txt`** — *(only with `--verbose 1`)* a plain-text record of the run: time, color, pixel coords, tick→OCR values, point count, OCR confidence, and the output paths.

The CSV columns:

| Column | Meaning |
| --- | --- |
| `color_slot` | 1-based color slot number (1 for a single-color run). |
| `color_r` | Red component (0–255) of the curve color. |
| `color_g` | Green component (0–255) of the curve color. |
| `color_b` | Blue component (0–255) of the curve color. |
| `x` | Digitized X value in data coordinates (rounded to 6 decimals). |
| `y` | Digitized Y value in data coordinates (rounded to 6 decimals). |
| `x_px` | Raw X pixel position in the image. |
| `y_px` | Raw Y pixel position in the image. |
| `y_norm` | *Only when `--normalize-y` is on.* Y rescaled to 0–1 over the axis range; appended as the last column (rounded to 6 decimals). |

---

## Run from source (for developers)

The source code is the same on every platform: **<https://github.com/RayanA07/LinePilot>**. Download it with the green **Code → Download ZIP** button (then unzip it), or clone it with git. You also need **Python 3** and, for the OCR features, the **Tesseract** program (the downloaded apps bundle it; running from source does not).

### On Windows

1. Install **Python 3** from <https://python.org> — tick *"Add python.exe to PATH"* during setup — and **Tesseract** from the [UB Mannheim installer](https://github.com/UB-Mannheim/tesseract/wiki).
2. Get the code and install the libraries ([open a terminal](#open-a-terminal-in-the-digitizer-folder) in the `Digitizer` folder):

   ```powershell
   git clone https://github.com/RayanA07/LinePilot.git
   cd LinePilot\Digitizer
   py -m pip install -r requirements.txt
   ```

3. Launch the graphical app:

   ```powershell
   py digitizer_2_11.py
   ```

### On a Mac

1. Install **[Homebrew](https://brew.sh)** if `brew --version` doesn't work yet (paste the one-line command from brew.sh into Terminal, then close and reopen Terminal), then install Python and Tesseract:

   ```bash
   brew install python tesseract
   ```

2. Get the code and install the libraries in a private **virtual environment** — Homebrew's Python refuses system-wide `pip install` (*"externally-managed-environment"*):

   ```bash
   git clone https://github.com/RayanA07/LinePilot.git
   cd LinePilot/Digitizer
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -r requirements.txt
   ```

   Next time, just `cd` into the folder and run `source .venv/bin/activate` again.

3. Launch the graphical app:

   ```bash
   python3 digitizer_2_11.py
   ```

The command-line interface ([above](#using-the-command-line)) runs from this same source setup on both platforms.

The dependencies are: `PyInstaller` (for building the apps), `PyQt6` (the window), `numpy`, `pillow` (image handling), `pytesseract` (OCR), and `openpyxl` (Excel export).

---

## Build pipeline — turning the code into an app

The project is plain Python (a PyQt6 GUI plus a small CLI). There are three "shapes" you can run it as, and the conversion is the same idea each time — **[PyInstaller](https://pyinstaller.org)** bundles the Python interpreter, this code, and the dependencies into one self-contained program described by a `.spec` file:

| Target | What it is | How it's made |
| --- | --- | --- |
| **CLI** | `py digitizer.py …` / `python3 digitizer.py …` | No build needed — it runs straight from the source files with Python (see [Run from source](#run-from-source-for-developers)). |
| **Windows `.exe`** | a one-file `Digitizer.exe` you double-click | PyInstaller reads `digitizer.spec`, bundles the GUI entry `digitizer_desktop.py` **and** the Tesseract OCR runtime in `vendor\tesseract`, and writes `dist\Digitizer.exe`. |
| **macOS `.app`** | a `Digitizer.app` bundle, zipped for download | PyInstaller reads `digitizer_macos.spec`, bundles the same entry **and** a self-contained Tesseract copied from Homebrew into `vendor/tesseract`, and writes `dist/Digitizer.app`. |

Windows and macOS share all of the code; the few things that must differ (the undo key shown in hints, where Tesseract is looked for, the log folder, the example commands in `--help`) live in **`platform_info.py`**.

### Starter command (Windows)

One-click: double-click **`build.cmd`** in this folder. (It just runs the PowerShell build with the execution policy unblocked, then keeps the window open so you can read the result.)

Or from a terminal in this folder:

```powershell
py -m pip install -r requirements.txt
.\build_windows.ps1
```

Either way the result is **`dist\Digitizer.exe`** — a windowed, one-file app you can double-click. The **Tesseract OCR runtime** under `vendor\tesseract` is **bundled into the exe**, so OCR features (axis-value detection and the text/number/legend masking tools) work without anyone needing a separate Tesseract install.

### Starter command (macOS)

With Homebrew installed, from the repository folder:

```bash
brew install tesseract dylibbundler
bash Digitizer/build_macos.sh
```

The result is **`dist/Digitizer.app`** plus a ready-to-share zip, `dist/Digitizer-macOS-AppleSilicon.zip` (or `-Intel.zip`, matching the Mac that built it). The script copies a self-contained Tesseract (binary, libraries and English language data) into `vendor/tesseract`, records the lowest macOS the app can run on in its `Info.plist`, and signs the app so it can launch. The app runs on the **same chip** as the Mac that built it and on **that Mac's macOS version or newer**, because the bundled Tesseract comes from Homebrew, which compiles for the build machine (`python3 tools/macho_minos.py dist/Digitizer.app --report` shows which file sets the limit).

### Releases

You normally don't build by hand: every push to GitHub is built and tested by **[`release.yml`](../.github/workflows/release.yml)** on Windows and on Apple Silicon and Intel Macs, and creating a `v*` tag publishes all six downloads in one release with one set of notes. Each build is checked on a clean machine before it is attached — see [TESTING.md](../TESTING.md).

---

## Troubleshooting

### Opening the app on Windows

**"Windows protected your PC" when I open the .exe.**
Expected on the first run — the file just isn't code-signed. Click the small **More info** text, then **Run anyway**. (Full explanation in [Download & install](#the-first-run-windows-warning-expected).)

**Double-clicking `Digitizer.exe` does nothing at all — no window, no warning.**
**Smart App Control** (on by default on new Windows 11 installs) is silently blocking unsigned programs. [Run from source](#run-from-source-for-developers) instead; that path is not blocked. Turning Smart App Control off is a one-way door, so prefer running from source.

**I can't find `Digitizer.exe` after downloading it.**
It's in your **Downloads** folder. Open **File Explorer** (the yellow folder icon on the taskbar, or **Windows key + E**) and click **Downloads** on the left.

**"`py` is not recognized" in the terminal.**
Python isn't installed (or wasn't added to your PATH). Install it from <https://python.org> and make sure to tick **"Add python.exe to PATH"** during setup. Then open a fresh terminal and try again. (Reminder: the command line needs Python; the `.exe` does not.)

### Opening the app on a Mac

**"Apple could not verify 'Digitizer' is free of malware" when I open the app.**
Expected on the first launch — the app just isn't notarized. Click **Done**, then **System Settings → Privacy & Security → Open Anyway**. (Full explanation in [Download & install](#the-first-run-mac-warning-expected).)

**"Digitizer is damaged and can't be opened."**
The download's quarantine flag is stuck. In **Terminal** run `xattr -dr com.apple.quarantine /Applications/Digitizer.app` (adjust the path if the app isn't in Applications), then open it again.

**"You can't use this version of the application with this version of macOS."**
Your Mac is older than this download supports (the minimum is on the release page). Update macOS, or [run from source](#on-a-mac-1), which works on older versions.

**I downloaded the wrong zip (Apple Silicon vs Intel).**
An Intel Mac can't open the Apple Silicon build. Check **Apple menu → About This Mac** and download the matching zip. (Apple Silicon Macs can usually run the Intel build too, but the Apple Silicon one is faster.)

**I can't find `Digitizer.app` after downloading.**
Double-click the downloaded zip in **Finder → Downloads**; `Digitizer.app` appears next to it. Safari sometimes unzips automatically, so the app may already be there.

**`python3: command not found`, or `pip install` fails with "externally-managed-environment".**
Install Python with `brew install python`, open a new Terminal window, and use the [virtual environment](#on-a-mac-1) — Homebrew's Python refuses system-wide installs.

**`zsh: no matches found` or `zsh: unknown file attribute` when using the `digitizer_cli(...)` form.**
Keep the single quotes around the whole `'digitizer_cli(...)'` call — the Mac shell treats unquoted brackets as file patterns.

### Using the app and the command line

**It picked the wrong curve color.**
- *In the app:* use **Tools → Pick Color** and click your curve (step 2).
- *On the command line:* pass it yourself, e.g. `--color 130,5,255` (flags) or `color=(130,5,255)` (function-call form) — using your curve's real R,G,B.

**The command line says "produced no points" / exits without a CSV.**
The color it's matching doesn't match your curve. If you passed `--color` (or `color=`), the values are wrong — fix them, or drop the option entirely to let it auto-detect. The placeholder `255,0,0` (red) in the template will fail on any non-red plot.

**The axis numbers came out wrong.**
OCR can misread numbers. Always check them.
- *In the app:* type the correct value into the **Min-Max Coordinates** box.
- *On the command line:* give them with `--axis xmin,xmax,ymin,ymax` (flags) or `axis_values=(xmin,xmax,ymin,ymax)` (function-call form). Run with `--verbose 1` to see the **OCR confidence score** — a low number is a strong hint that you should type the axis values in yourself with `--axis`.

**"Image file not found" on the command line.**
Put the image in your **Downloads** folder or in the folder the terminal is pointed at (a bare filename is searched in both), or pass the **full path in quotes**, e.g. `py digitizer.py "C:\Users\You\Pictures\graph.png"` on Windows or `python3 digitizer.py ~/Pictures/graph.png` on a Mac.

**OCR says "Tesseract OCR executable not found" (running from source).**
The downloaded apps bundle Tesseract; source code doesn't. Windows: install it from the [UB Mannheim installer](https://github.com/UB-Mannheim/tesseract/wiki). Mac: `brew install tesseract`, then open a new Terminal window. To point at a specific copy, set `TESSERACT_CMD` to its full path.

**Export does nothing in the app.**
Check the status bar (the thin strip at the bottom). You need **all four Min-Max Coordinate boxes filled** *and* **a calibration run** (the dashed green box). Finish whichever is missing, then export again.

**Where did my files go?**
- *In the app:* wherever you chose in the **Save** dialog.
- *On the command line:* your **Downloads** folder by default, or the folder you set with `--out` / `output_dir=`.

**Where is the error log?**
Open it in the app with **Advanced → Error Log**. On disk it's in `%LOCALAPPDATA%\DataDigitizer\<version>\logs` on Windows (paste that into File Explorer's address bar) and `~/Library/Application Support/DataDigitizer/<version>/logs` on a Mac (Finder → **Go → Go to Folder…**).

---

## Folder contents

```text
digitizer.py        # CLI / function-call launcher
digitizer_2_11.py   # GUI + CLI dispatch and runtime path setup
digitizer_desktop.py# GUI-only entry used by the PyInstaller build
digitizer_cli.py    # Terminal CLI
digitizer_api.py    # Programmatic API (digitize_image)
function.py         # Thin re-export of digitize_image
UI.py               # Main window and GUI workflows
ImageTray.py        # Canvas rendering and interaction
PointPlacer.py      # Color-based point extraction + interpolation
AxisReader.py       # OCR axis detection
Calibration.py      # Calibration strategies
Masking.py          # OCR / manual masking helpers
ErrorLogger.py      # Error logging utilities
platform_info.py    # What differs between Windows, macOS and Linux
digitizer.spec      # PyInstaller spec — Windows (Digitizer.exe)
build.cmd           # One-click Windows build (runs build_windows.ps1)
build_windows.ps1   # Windows build script
digitizer_macos.spec        # PyInstaller spec — macOS (Digitizer.app)
build_macos.sh              # macOS build script (zip ready to share)
vendor_tesseract_macos.sh   # Copies a self-contained Tesseract from Homebrew
make_macos_icons.py         # Makes the macOS icon from the Windows .ico
requirements.txt    # Python dependencies
version.json        # App name + version (the single source of every version string)
assets/             # Application icons
vendor/tesseract/   # Bundled Tesseract OCR runtime (created by the build; not in git)
```

---

## Accuracy Tester (optional)

This is a **separate, optional** tool. It's completely independent of the main Digitizer — you don't need it to get your data out.

**What it does:** it measures how faithfully a digitized curve reproduces a reference curve. You load **two CSV files** — an *original* reference and a *digitized* one — and it lines them up on a common X grid and reports accuracy numbers (MAE, RMSE, R-squared, bias, MAPE/sMAPE/WAPE, and more) alongside diagnostic plots: the curve overlay, residuals, absolute error, and zoomable outliers. It cleans messy data (drops non-numeric rows, collapses duplicate X values), can filter by color slot, and can optionally optimize a constant X-shift before comparing. Results can be exported to a comparison CSV.

**Run the app (no Python needed):** download it from the **[latest release](https://github.com/RayanA07/LinePilot/releases/latest)** like the Digitizer —
- **Windows:** double-click **`AccuracyTester.exe`** — a windowed, one-file app, no install or console needed.
- **Mac:** double-click **`AccuracyTester-macOS-AppleSilicon.zip`** (or `-Intel.zip`), then open **`AccuracyTester.app`**; the first launch needs the same [Open Anyway](#the-first-run-mac-warning-expected) step.

**Run from source** (in the `AccuracyTester` folder):

**Windows**

```powershell
py -m pip install -r requirements.txt
py accuracytester_desktop.py
```

**Mac** — Homebrew's Python needs `python-tk` for this tool's window:

```bash
brew install python-tk
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 accuracytester_desktop.py
```

---

*Runtime logs are written to `%LOCALAPPDATA%\DataDigitizer\2.17\logs` on Windows and `~/Library/Application Support/DataDigitizer/2.17/logs` on a Mac (you can also view them in-app via **Advanced → Error Log**).*
