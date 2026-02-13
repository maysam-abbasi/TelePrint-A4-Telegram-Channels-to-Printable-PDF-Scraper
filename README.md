# TelePrint-A4 📄🚀

TelePrint-A4 is a Python-based automation tool designed to archive Telegram channel history into a print-ready PDF format. Unlike standard screenshots, this tool automatically scrolls through a channel, captures the window, and arranges the content into a **2x2 grid on standard A4 pages** to save paper and mimic a mobile reading experience.

## ✨ Features
* **Smart Window Detection:** Automatically locks onto the active Telegram window after a 5-second countdown.
* **Automatic Scrolling:** Captures a user-defined number of steps without manual intervention.
* **A4 Print Optimization:** Uses a "Fill & Crop" algorithm to fit 4 screenshots per page in a 2x2 grid, specifically formatted for A4 paper.
* **DPI Awareness:** Handles high-resolution/scaled Windows displays to ensure captures aren't blurry or misaligned.
* **Unique File Naming:** Automatically increments filenames (e.g., `Telegram_Channel_1.pdf`) so you never overwrite your data.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/maysam-abbasi/TelePrint-A4.git](https://github.com/maysam-abbasi/TelePrint-A4.git)
   cd TelePrint-A4

Install dependencies:

Bash
pip install pyautogui pillow pygetwindow
🚀 How to Use
Open your Telegram Desktop app and navigate to the desired channel.

Run the script: python main.py.

You have 5 seconds to click on the Telegram window to make it active.

The script will handle the rest! Your final PDF will be saved to a Telegram_Screenshots folder on your Desktop.

⚙️ Configuration
You can easily adjust the following variables in the script:

NUM_SCREENSHOTS: How many pages of content to capture.

SCROLL_AMOUNT: How much to scroll between captures.

SCROLL_DELAY: Seconds to wait for images to load after scrolling.
