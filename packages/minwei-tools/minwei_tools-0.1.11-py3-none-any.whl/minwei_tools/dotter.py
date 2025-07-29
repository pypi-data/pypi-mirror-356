# A dotter while I'm thinking
from typing import Optional

import colorama as cm
import itertools
import threading
import time
import sys

piano = ['▉▁▁▁▁▁', '▉▉▂▁▁▁', '▉▉▉▃▁▁', '▉▉▉▉▅▁', 
         '▉▉▉▉▉▇', '▉▉▉▉▉▉', '▉▉▉▉▇▅', '▉▉▉▆▃▁', 
         '▉▉▅▃▁▁', '▉▇▃▁▁▁', '▇▃▁▁▁▁', '▃▁▁▁▁▁', 
         '▁▁▁▁▁▁', '▁▁▁▁▁▉', '▁▁▁▁▃▉', '▁▁▁▃▅▉', 
         '▁▁▃▅▇▉', '▁▃▅▇▉▉', '▃▅▉▉▉▉', '▅▉▉▉▉▉',
         '▇▉▉▉▉▉', '▉▉▉▉▉▉', '▇▉▉▉▉▉', '▅▉▉▉▉▉', 
         '▃▅▉▉▉▉', '▁▃▅▉▉▉', '▁▁▃▅▉▉', '▁▁▁▃▅▉',
         '▁▁▁▁▃▅', '▁▁▁▁▁▃', '▁▁▁▁▁▁', '▁▁▁▁▁▁', 
         '▁▁▃▁▁▁', '▁▃▅▃▁▁', '▁▅▉▅▁▁', '▃▉▉▉▃▁', 
         '▅▉▁▉▅▃', '▇▃▁▃▇▅', '▉▁▁▁▉▇', '▉▅▃▁▃▅', 
         '▇▉▅▃▅▇', '▅▉▇▅▇▉', '▃▇▉▇▉▅', '▁▅▇▉▇▃', 
         '▁▃▅▇▅▁', '▁▁▃▅▃▁', '▁▁▁▃▁▁', '▁▁▁▁▁▁',
        ]

slash = ["\\","|","/", "-"]

class Dotter:
    # A dotter while I'm thinking
    def __init__(self, message: str = "Thinking", delay: float = 0.5, 
                 cycle: list[str] = ["", ".", ". .", ". . ."], 
                 show_timer: bool = False) -> None:
        
        self.spinner          : itertools.cycle            = itertools.cycle(cycle)
        self.show_timer       : bool                       = show_timer
        self.message          : str                        = message
        self.delay            : float                      = delay
        self.dotter_thread    : Optional[threading.Thread] = None
        self.start_time       : Optional[float]            = None
        self.running          : bool                       = False
        self.inserted_messages: list[str]                 = []  # Store inserted messages
        self.max_inserted_line = 0

    def format_elapsed(self, elapsed: float) -> str:
        if elapsed < 300:
            return f"{elapsed:.1f}s"
        else:
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            return f"{mins}m{secs:02d}s"
        
    def dot(self):
        self.start_time = time.time()
        while self.running:
            elapsed = time.time() - self.start_time
            text  = f"{self.message} {next(self.spinner)}"
            
            if self.show_timer:
                timer_str = f"[{self.format_elapsed(elapsed)}]"
                text = timer_str + ' ' + text
                
            sys.stdout.write(f"\r{text}\n")
            for msg in self.inserted_messages:
                sys.stdout.write(f"    {cm.Style.DIM}{msg}{cm.Style.RESET_ALL}\n")
            sys.stdout.flush()
            time.sleep(self.delay)
            self.max_inserted_line = max(self.max_inserted_line, len(self.inserted_messages))
            lines_to_clear = 1 + self.max_inserted_line
            for _ in range(lines_to_clear):
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the entire line
            sys.stdout.flush()
      
    def update_message(self, new_message, delay=0.1):
        time.sleep(delay)
        sys.stdout.write(
            f"\r{' ' * (len(self.message) + 20)}\r"
        )  # Clear the current message
        sys.stdout.flush()
        self.message = new_message
        self.delay = delay  # Update the delay if needed
        
    def insert_message(self, new_message: str, max_str : int = 5, prefix = "=>"):
        self.inserted_messages.append(prefix + " " + new_message)
        while len(self.inserted_messages) > max_str:
            self.inserted_messages.pop(0)
        
    def __enter__(self):
        self.running = True
        self.dotter_thread = threading.Thread(target=self.dot)
        self.dotter_thread.start()
        return self

    def __exit__(self, *args) -> None:
        self.running = False
        if self.dotter_thread is not None:
            self.dotter_thread.join()
        self.max_inserted_line = max(self.max_inserted_line, len(self.inserted_messages))
        lines_to_clear = 1 + self.max_inserted_line
        for _ in range(lines_to_clear):
            sys.stdout.write("\033[F")  # Move cursor up one line
            sys.stdout.write("\033[K")  # Clear the entire line
        sys.stdout.flush()

if __name__ == "__main__":
    from time import sleep
    import colorama as cm
    import asyncio

    with Dotter(message="[*] Grabing player log", cycle=slash, delay=0.2, show_timer=0) as d:
        d.insert_message("This is a test message 1")
        sleep(1)
        d.insert_message("This is a test message 2")
        sleep(1)
        d.insert_message("This is a test message 3")
        sleep(1)
        d.update_message("[*] Player log grabbed", delay=0.1)
        sleep(1)
        d.insert_message("This is a test message 4")
        sleep(1)
        d.insert_message("This is a test message 5")
        sleep(1)        
        d.insert_message("This is a test message 6")
        for i in range(7, 80):
            d.insert_message(f"This is another message {i}", max_str = 10, prefix = "*")
            sleep(0.05)
        for i in range(80, 250):
            d.insert_message(f"This is another message {i}", max_str = 20, prefix = f"🚀{cm.Style.RESET_ALL}{cm.Style.BRIGHT}")
            sleep(0.01)       
        for i in range(250, 500):
            d.insert_message(f"This is another message {i}", max_str = 5, prefix = f"{cm.Style.RESET_ALL}{cm.Style.BRIGHT}🚀{cm.Style.RESET_ALL}{cm.Style.DIM}")
            sleep(0.01)            
            