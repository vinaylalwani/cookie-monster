import os
import threading
import sys

messages = [
    "Give me a cookie",
    "COOKIES! COOKIES! COOKIES! COOKIES!",
    "I want a cookie!",
    "GIVE ME COOKIE!!",
    "I NEED a cookie!!!!!",
    "Please, just one cookie, I promise I'll go away!!",
    "YOU BAGBITER, KEEP YOUR ******* COOKIES!!",
]

times = [10, 20, 20, 30, 30, 30]

flipflop = True
counter = 0

class TimerManager:
    def __init__(self):
        self.timers = {}
        self.lock = threading.Lock()

    def alarm_call(self, delay_seconds, callback):
        t = threading.Timer(delay_seconds, callback)
        t.daemon = True
        with self.lock:
            self.timers[id(callback)] = t
        t.start()

    def reset_alarm_call(self, callback):
        with self.lock:
            t = self.timers.pop(id(callback), None)
            if t:
                t.cancel()

timer_manager = TimerManager()

def make_hungry():
    global flipflop
    flipflop = True
    print("\nCookie monster is hungry again! Type 'cookie' to feed him.")
    timer_manager.reset_alarm_call(callback)

def callback():
    global counter
    sys.stdout.write("\n" + messages[counter] + "\n")
    sys.stdout.flush()
    counter += 1
    if counter >= 2:
        os.fork()
    if counter >= len(messages):
        counter = 0
        threading.Timer(10, make_hungry).start()
        return
    timer_manager.alarm_call(times[counter - 1], callback)

def cookie_proc():
    global flipflop, counter
    timer_manager.reset_alarm_call(callback) 
    sys.stdout.write("yummy cookie... cookie monster is satisfied... for now...\n")
    sys.stdout.flush()
    counter = 0
    flipflop = False
    timer_manager.alarm_call(30, callback)  

def main():
    print("Type 'cookie' to feed the monster.")
    timer_manager.alarm_call(10, callback)
    try:
        while True:
            line = input("> ")
            cmd = line.strip().lower()
            if cmd == "cookie":
                cookie_proc()
            elif cmd == "fork you":
                sys.exit(0)
            elif cmd == "":
                continue
            else:
                print("Unknown command. Type 'cookie'.")
    except KeyboardInterrupt:
        print("\nExiting...")

    timer_manager.reset_alarm_call(callback)
    print("Goodbye.")

if __name__ == "__main__":
    main()