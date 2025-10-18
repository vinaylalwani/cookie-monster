import threading
import sys
import os


messages = [
    "Give me a cookie",
    "COOKIES! COOKIES! COOKIES! COOKIES!",
    "I want a cookie!",
    "GIVE ME COOKIE!!",
    "I ^RNEED^B a cookie!!!!!",
    "Please, just ^Rone^B cookie, I promise I'll go away!!",
    "YOU BAGBITER, ^RKEEP^B YOUR ******* COOKIES!!",
]

flipflop = False
counter = 1

times = [10, 20, 20, 30, 30, 30]


class TimerManager:
    def __init__(self):
        self.timers = {}
        self.lock = threading.Lock()

    def alarm_call(self, delay_seconds, callback):
        with self.lock:
            self.reset_alarm_call(callback)
            t = threading.Timer(delay_seconds, callback)
            t.daemon = True
            self.timers[id(callback)] = t
            t.start()

    def reset_alarm_call(self, callback):
        with self.lock:
            t = self.timers.pop(id(callback), None)
            if t:
                t.cancel()

timer_manager = TimerManager()


def callback():
    global counter, flipflop
    idx = counter - 1
    sys.stdout.write("\n" + messages[idx])
    sys.stdout.flush()

    if counter == 7:
        flipflop = False
        timer_manager.reset_alarm_call(callback)
        counter = 1
        return

    timer_manager.reset_alarm_call(callback)
    if 1 <= counter <= len(times):
        timer_manager.alarm_call(times[counter - 1], callback)
        counter += 1
    else:
        flipflop = False
        timer_manager.reset_alarm_call(callback)
        counter = 1


def cookie_proc():
    global flipflop, counter
    if not flipflop:
        timer_manager.alarm_call(10, callback)
    else:
        timer_manager.reset_alarm_call(callback)
        sys.stdout.write("yummy cookie... cookie monster is satisfied... for now...")
        sys.stdout.flush()
        counter = 1
    flipflop = not flipflop


def main():
    print("Type 'cookie' to feed the monster.")
    try:
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            cmd = line.strip().lower()
            if cmd == "cookie":
                cookie_proc()
                os.fork()
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
