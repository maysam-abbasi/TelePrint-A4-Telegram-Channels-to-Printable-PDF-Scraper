# TelePrint-A4 📄🚀

TelePrint-A4 is a Python-based automation tool designed to archive Telegram channel or group history into a print-ready PDF format. Unlike standard screenshots, this tool automatically scrolls through a channel, captures the window, and arranges the content into a **2x2 grid on standard A4 pages** to save paper and mimic a mobile reading experience.

## ✨ Features
* **Smart Window Detection:** Automatically locks onto the active Telegram window after a 5-second countdown.
* **Automatic Scrolling:** Captures a user-defined number of steps without manual intervention.
* **A4 Print Optimization:** Uses a "Fill & Crop" algorithm to fit 4 screenshots per page in a 2x2 grid, specifically formatted for A4 paper.
* **DPI Awareness:** Handles high-resolution/scaled Windows displays to ensure captures aren't blurry or misaligned.
* **Unique File Naming:** Automatically increments filenames (e.g., `Telegram_Channel_1.pdf`) so you never overwrite your data.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/maysam-abbasi/TelePrint-A4-Telegram-Channels-to-Printable-PDF-Scraper.git
   cd TelePrint-A4-Telegram-Channels-to-Printable-PDF-Scraper

2. **Install dependencies:**
   ```bash
   pip install pyautogui pillow pygetwindow

   
## 🚀 How to Use
1. Open your Telegram Desktop app and navigate to the desired channel.

2. Run the script: python main.py.

3. You have 5 seconds to click on the Telegram window to make it active.

4. The script will handle the rest! Your final PDF will be saved to a Telegram_Screenshots folder on your Desktop.

## ⚙️ Configuration
You can customize the script by adjusting these variables at the top of the main.py file:

NUM_SCREENSHOTS: 10 — Total number of images to capture.

SCROLL_AMOUNT: -14 — How many "clicks" to scroll per step (Negative = Down).

SCROLL_DELAY: 1.0 — Seconds to wait for content to load/render after scrolling.
