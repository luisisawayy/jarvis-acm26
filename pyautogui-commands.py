# opted to use keyboard shortcuts rather than coordinates
# to be more reliable across different screen sizes
# current version is Mac/Google Chrome specific

import pyautogui
import time
import subprocess

# 1. Emergency stop:
# Move your mouse to the TOP-LEFT corner of the screen to stop the program.
pyautogui.FAILSAFE = True

# 2. Adds a small pause after every PyAutoGUI action.
# This prevents commands from firing too fast.
pyautogui.PAUSE = 0.2

# 3. Cooldown so one gesture does not trigger 20 times.
last_action_time = 0
COOLDOWN = 1.0  # seconds


def safe_run_action(action_function):
    global last_action_time

    now = time.time()

    # Prevent repeated triggers
    if now - last_action_time < COOLDOWN:
        print("Action ignored because cooldown is active")
        return

    print("Running action in 1 second...")
    time.sleep(1)

    try:
        action_function()
        last_action_time = time.time()
    except pyautogui.FailSafeException:
        print("Failsafe triggered. Mouse moved to top-left corner.")
    except Exception as e:
        print("Something went wrong:", e)


# -------- list of actions ---------- #
# originally tried hotkeys, but didn't work
# used holding/releasing keys instead


# open new tab
def open_new_tab():
    pyautogui.keyDown("command")  # hold key down
    time.sleep(0.2)               # allow time for computer to process command
    pyautogui.press("t")          # press t
    time.sleep(0.2)
    pyautogui.keyUp("command")    # release command

    print("new tab opened\n")


# switch tab to the right
def switch_next_tab():
    pyautogui.keyDown("command")
    pyautogui.keyDown("option")
    time.sleep(0.2)

    pyautogui.press("right")
    time.sleep(0.2)

    pyautogui.keyUp("option")
    pyautogui.keyUp("command")

    print("switched tab to right\n")


# switch tab to the left
def switch_prev_tab():
    pyautogui.keyDown("command")
    pyautogui.keyDown("option")
    time.sleep(0.2)

    pyautogui.press("left")
    time.sleep(0.2)

    pyautogui.keyUp("option")
    pyautogui.keyUp("command")

    print("switched tab to the left\n")


# this implementation of close tab did not work for my mac
# might work for other systems

# # close current tab
# def close_current_tab():
#     pyautogui.keyDown("command")
#     time.sleep(0.2)
#     pyautogui.press("w")
#     time.sleep(0.2)
#     pyautogui.keyUp("command")

#     print("closed current tab\n")


# close current tab
# this version of close tab works for mac 
def close_current_tab():
    # PyAutoGUI Command + W was unreliable on some Macs,
    # so we use AppleScript to tell Google Chrome directly
    # to close the active tab in the front window.
    subprocess.run([
        "osascript",
        "-e",
        'tell application "Google Chrome" to close active tab of front window'
    ])

    print("closed current tab\n")



# press k for YouTube play/pause
# must be on YouTube with video/player focused already to work as intended
def pause_youtube():
    pyautogui.press("k")

    print("YouTube play/pause pressed\n")


# -------- test helper ---------- #

def test_action(action_name, action_function):
    print(f"Testing: {action_name}")
    print("Move mouse to top-left corner to emergency stop.")
    time.sleep(1)

    try:
        action_function()
    except pyautogui.FailSafeException:
        print("Failsafe triggered. Stopping tests.")
        return False
    except Exception as e:
        print("Something went wrong:", e)
        return False

    time.sleep(1.5)
    return True


# -------- test all pyautogui functions ---------- #

if __name__ == "__main__":
    print("Opening Google Chrome...")
    subprocess.run(["open", "-a", "Google Chrome"])
    time.sleep(2)

    print("Starting browser tests in 3 seconds.")
    print("Move mouse to top-left corner to emergency stop.")
    time.sleep(3)

    # Normal browser tests.
    # YouTube is NOT included here because the YouTube player must be focused.
    tests = [
        ("open new tab", open_new_tab),
        ("switch next tab", switch_next_tab),
        ("switch previous tab", switch_prev_tab),
        ("close current tab", close_current_tab),
    ]

    for action_name, action_function in tests:
        success = test_action(action_name, action_function)

        if not success:
            break

    print("Finished browser tests.")

    # -------- separate YouTube test ---------- #
    # Keep this separate because pressing "k" only works correctly
    # when a YouTube video/player is focused.
    #
    # To test YouTube:
    # 1. Change TEST_YOUTUBE to True
    # 2. Open a YouTube video
    # 3. Click on the video/player
    # 4. Run this file
    #
    # If YouTube is not focused, this may type "k" somewhere else.

    TEST_YOUTUBE = False

    if TEST_YOUTUBE:
        print("Separate YouTube test selected.")
        print("Open a YouTube video and click on the video/player.")
        print("Pressing k in 5 seconds...")
        time.sleep(5)

        pause_youtube()

# finish this after models are done
# -------- gesture mapping placeholder ---------- #

GESTURE_TO_ACTION = {
    "open_palm": open_new_tab,
    "swipe_right": switch_next_tab,
    "swipe_left": switch_prev_tab,
    "fist": close_current_tab,
    "peace_sign": pause_youtube,
}


def execute_command_from_gesture(predicted_gesture):
    # Connects a predicted gesture to its command.

    if predicted_gesture is None:
        print("No gesture detected")
        return

    predicted_gesture = predicted_gesture.strip().lower()
    action_function = GESTURE_TO_ACTION.get(predicted_gesture)

    if action_function is None:
        print(f"No command mapped for gesture: {predicted_gesture}")
        return

    print(f"Gesture detected: {predicted_gesture}")
    safe_run_action(action_function)


def get_predicted_gesture():
    # TODO: replace this with model prediction later.
    return None


def gesture_control_loop():
    # Runs gesture detection repeatedly.

    print("Starting gesture control loop.")
    print("Move mouse to top-left corner to emergency stop.")

    while True:
        predicted_gesture = get_predicted_gesture()
        execute_command_from_gesture(predicted_gesture)
        time.sleep(0.1)


def test_gesture_mapping():
    # Tests gesture commands without the model.

    test_gestures = [
        "open_palm",
        "swipe_right",
        "swipe_left",
        "fist",
        "peace_sign",
        "unknown_gesture",
    ]

    for gesture in test_gestures:
        print(f"\nTesting fake gesture: {gesture}")
        execute_command_from_gesture(gesture)
        time.sleep(1.5)
