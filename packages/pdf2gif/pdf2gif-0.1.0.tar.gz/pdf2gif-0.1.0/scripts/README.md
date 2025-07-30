# Windows "Send to" Integration

This directory contains scripts to add pdf2gif to the Windows "Send to" menu for easy PDF to GIF conversion.

## Files

### Main Script
- `pdf2gif-converter.bat` - Batch file that activates conda environment and runs pdf2gif

### Setup Scripts
- `setup-send-to-menu.bat` - Batch script to create a shortcut in the "Send to" folder
- `remove-send-to-menu.bat` - Batch script to remove the shortcut from the "Send to" folder

## Prerequisites

1. **Conda/Miniconda installed** - Make sure you have conda installed and a conda environment with pdf2gif
2. **pdf2gif installed** - Install pdf2gif in your conda environment: `pip install pdf2gif`


## Setup Instructions

### Method 1: Automated Setup (Recommended)

1. **Edit the batch file**: Open `pdf2gif-converter.bat` and replace `bio11` with your actual conda environment name

2. **Run the setup script**:
   - Double-click `setup-send-to-menu.bat`
   - Or right-click and select "Run"

### Method 2: Manual Setup

1. **Edit the batch file**: Open `pdf2gif-converter.bat` and replace `bio11` with your actual conda environment name

2. **Create a shortcut**:
   - Right-click on `pdf2gif-converter.bat`
   - Select "Create shortcut"
   - Rename the shortcut to "Convert to GIF"
   - Copy the shortcut to your "Send to" folder

3. **Find your "Send to" folder**:
   - Press `Win + R`, type `shell:sendto`, and press Enter
   - Or navigate to: `%APPDATA%\Microsoft\Windows\SendTo`

## Usage

### Converting PDFs to GIF

1. **Right-click on a PDF file** in Windows Explorer
2. **Hover over "Send to"** in the context menu
3. **Click "Convert to GIF"** (or whatever you named the shortcut)
4. The PDF will be converted to GIF in the same folder

### Converting Multiple PDFs

1. **Select multiple PDF files** (hold Ctrl while clicking)
2. **Right-click** on any selected file
3. **Hover over "Send to"** and click "Convert to GIF"
4. Each PDF will be converted to its own GIF file

## Removal

### Method 1: Automated Removal
- Double-click `remove-send-to-menu.bat`

### Method 2: Manual Removal
1. Press `Win + R`, type `shell:sendto`, and press Enter
2. Delete the "Convert to GIF" shortcut (or whatever you named it)

## Customization

You can customize the batch file to use different pdf2gif parameters:

```batch
REM Example: Use custom frame delay and first slide multiplier
pdf2gif "%pdf_file%" --frame-delay 200 --first-slide-multiplier 5
```

You can also create multiple shortcuts with different settings:
- "Convert to GIF (Fast)" - with `--frame-delay 100`
- "Convert to GIF (Slow)" - with `--frame-delay 500`
- "Convert to GIF (High Quality)" - with `--first-slide-multiplier 10`

## Troubleshooting

### "Conda is not recognized"
- Make sure conda is in your system PATH
- Try using the full path to conda in the batch file

### "pdf2gif is not recognized"
- Ensure pdf2gif is installed in your conda environment
- Verify the environment name in the batch file

### "Send to" option doesn't appear
- Make sure the shortcut is in the correct "Send to" folder
- Try refreshing Windows Explorer (F5)
- Check that the shortcut points to the correct batch file

### Batch file doesn't work
- Test the batch file directly by double-clicking it
- Make sure the conda environment name is correct
- Check that pdf2gif is installed in the specified environment

## Advantages of "Send to" Method

- **No administrator privileges required**
- **No registry modifications**
- **Easy to set up and remove**
- **Works with multiple file selection**
- **Can create multiple shortcuts with different settings**
- **Safer than registry modifications**
- **User-specific (doesn't affect other users on the same computer)**

## Finding Your "Send to" Folder

The "Send to" folder is typically located at:
- `%APPDATA%\Microsoft\Windows\SendTo`
- Or `C:\Users\[YourUsername]\AppData\Roaming\Microsoft\Windows\SendTo`

You can quickly open it by:
1. Press `Win + R`
2. Type `shell:sendto`
3. Press Enter 