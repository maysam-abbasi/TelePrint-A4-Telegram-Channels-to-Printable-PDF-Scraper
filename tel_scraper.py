import os
import sys
import time
import glob
import ctypes

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────
NUM_SCREENSHOTS = 10
SCROLL_AMOUNT = -14
SCROLL_DELAY = 1.0
INITIAL_DELAY = 5
OVERLAP_CROP_TOP = 50
OVERLAP_CROP_BOTTOM = 50
OUTPUT_FOLDER_NAME = "Telegram_Screenshots"
OUTPUT_PDF_NAME = "Telegram_Channel.pdf"

# ──────────────────────────────────────────────
# 1. DPI AWARENESS FIX (Crucial for Windows)
# ──────────────────────────────────────────────
try:
    if sys.platform == "win32":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")


def setup_output_folder():
    desktop = get_desktop_path()
    output_dir = os.path.join(desktop, OUTPUT_FOLDER_NAME)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def capture_screenshot(output_dir, index, region=None):
    import pyautogui
    filename = os.path.join(output_dir, f"screenshot_{index:04d}.png")

    # Force region to integers if it exists
    if region:
        region = tuple(map(int, region))
        screenshot = pyautogui.screenshot(region=region)
    else:
        screenshot = pyautogui.screenshot()

    screenshot.save(filename)
    return filename


def scroll_down():
    import pyautogui
    # Increasing scroll multiplier for Windows apps
    pyautogui.scroll(SCROLL_AMOUNT * 100)


def crop_overlaps(output_dir):
    from PIL import Image
    if OVERLAP_CROP_TOP == 0 and OVERLAP_CROP_BOTTOM == 0:
        return

    print("[*] Processing images to remove overlap...")
    files = sorted(glob.glob(os.path.join(output_dir, "screenshot_*.png")))

    for i, filepath in enumerate(files):
        try:
            img = Image.open(filepath)
            w, h = img.size
            top = OVERLAP_CROP_TOP if i > 0 else 0
            bottom = OVERLAP_CROP_BOTTOM if i < len(files) - 1 else 0

            if top + bottom < h:
                cropped = img.crop((0, top, w, h - bottom))
                cropped.save(filepath)
        except Exception as e:
            print(f"[!] Error cropping {filepath}: {e}")


def get_unique_filename(directory, filename):
    """
    Checks if a file exists. If it does, adds a number (1, 2, 3...) to the end
    until a unique name is found.
    """
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    # Keep looping until we find a filename that doesn't exist yet
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1

    return new_filename


def create_pdf(output_dir):
    """
    Compiles screenshots into an A4 PDF with a 2x2 grid.
    USES 'ASPECT FILL': Zooms images to fill the quadrant completely,
    cropping excess edges to eliminate whitespace.
    """
    from PIL import Image, ImageOps

    # A4 Dimensions at 300 DPI
    A4_WIDTH = 2480
    A4_HEIGHT = 3508

    # Quadrant Dimensions
    Q_WIDTH = A4_WIDTH // 2
    Q_HEIGHT = A4_HEIGHT // 2

    # 2x2 Grid Positions (Top-Right, Top-Left, Bottom-Right, Bottom-Left)
    POSITIONS = [
        (Q_WIDTH, 0),  # 1
        (0, 0),  # 2
        (Q_WIDTH, Q_HEIGHT),  # 3
        (0, Q_HEIGHT)  # 4
    ]

    desktop = get_desktop_path()
    save_location = os.path.join(desktop, OUTPUT_FOLDER_NAME)
    unique_pdf_name = get_unique_filename(save_location, OUTPUT_PDF_NAME)
    pdf_path = os.path.join(save_location, unique_pdf_name)

    files = sorted(glob.glob(os.path.join(output_dir, "screenshot_*.png")))
    if not files:
        return None

    print(f"[*] Formatting {len(files)} screenshots (Fill & Crop mode)...")

    images = []
    for f in files:
        try:
            img = Image.open(f).convert("RGB")
            images.append(img)
        except Exception:
            pass

    if not images:
        return None

    pdf_pages = []

    # Loop through chunks of 4
    for i in range(0, len(images), 4):
        chunk = images[i: i + 4]

        # Create blank A4 page
        a4_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))

        for idx, img in enumerate(chunk):
            if idx >= 4: break  # Safety check

            # Target position
            target_x, target_y = POSITIONS[idx]

            # --- INTELLIGENT FILL LOGIC ---
            # 1. Calculate aspect ratios
            target_aspect = Q_WIDTH / Q_HEIGHT
            img_aspect = img.width / img.height

            if img_aspect > target_aspect:
                # Image is WIDER than the quadrant -> Scale by height, crop sides
                scale_factor = Q_HEIGHT / img.height
                new_w = int(img.width * scale_factor)
                new_h = Q_HEIGHT
            else:
                # Image is TALLER than the quadrant -> Scale by width, crop top/bottom
                scale_factor = Q_WIDTH / img.width
                new_w = Q_WIDTH
                new_h = int(img.height * scale_factor)

            # 2. Resize
            img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # 3. Center Crop
            # We want to keep the center of the image
            left = (new_w - Q_WIDTH) // 2
            top = (new_h - Q_HEIGHT) // 2
            right = left + Q_WIDTH
            bottom = top + Q_HEIGHT

            img_cropped = img_resized.crop((left, top, right, bottom))

            # 4. Paste into quadrant
            a4_page.paste(img_cropped, (target_x, target_y))

        pdf_pages.append(a4_page)

    if pdf_pages:
        pdf_pages[0].save(
            pdf_path,
            "PDF",
            resolution=300.0,
            save_all=True,
            append_images=pdf_pages[1:]
        )
        print(f"[+] PDF Saved: {pdf_path}")
        return pdf_path

    return None


# ──────────────────────────────────────────────
# MAIN EXECUTION
# ──────────────────────────────────────────────
def main():
    import pygetwindow as gw

    print("=" * 50)
    print("  Telegram Screenshot Tool (Active Window Mode)")
    print("=" * 50)

    output_dir = setup_output_folder()

    # 1. COUNTDOWN & LOCK TARGET
    print(f"\n[*] Please click the TELEGRAM window to focus it.")
    print(f"[*] Locking onto active window in {INITIAL_DELAY} seconds...")

    for i in range(INITIAL_DELAY, 0, -1):
        print(f"    {i}...")
        time.sleep(1)

    # 2. GET ACTIVE WINDOW
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            region = (active_window.left, active_window.top, active_window.width, active_window.height)
            print(f"[+] Locked onto window: '{active_window.title}'")
            print(f"    Region: {region}")
        else:
            print("[!] Could not detect active window. Using Full Screen.")
            region = None
    except Exception as e:
        print(f"[!] Error detecting window: {e}")
        region = None

    print("    Starting capture now!\n")

    # 3. CAPTURE LOOP
    for i in range(NUM_SCREENSHOTS):
        filepath = capture_screenshot(output_dir, i, region=region)
        print(f"  [{i + 1}/{NUM_SCREENSHOTS}] Saved {os.path.basename(filepath)}")

        if i < NUM_SCREENSHOTS - 1:
            scroll_down()
            time.sleep(SCROLL_DELAY)

    # 4. FINISH
    crop_overlaps(output_dir)
    create_pdf(output_dir)
    print("\n[+] Done.")


if __name__ == "__main__":
    main()