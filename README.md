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
   git clone [https://github.com/YOUR_USERNAME/TelePrint-A4.git](https://github.com/YOUR_USERNAME/TelePrint-A4.git)
   cd TelePrint-A4
