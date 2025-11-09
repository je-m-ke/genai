import pyautogui
import time

# Give yourself time to open Chrome manually
print("You have 5 seconds to open Chrome and focus the window...")
time.sleep(10)

# Type the Google URL and go there
pyautogui.write('https://www.google.com', interval=0.05)
pyautogui.press('enter')
time.sleep(3)

# Click on the search bar (approximate coordinates — adjust to your screen)
pyautogui.click(1007, 548)  # You may need to change these numbers

# Type the search query
pyautogui.write('election result', interval=0.05)
pyautogui.press('enter')
time.sleep(3)

# Click the first result (again, coordinates depend on your screen)
pyautogui.click(452, 369)  # Adjust as needed
