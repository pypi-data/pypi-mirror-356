"""Alternative timer using system commands for audio."""

import time
import os
import subprocess
import platform
from pathlib import Path
from typing import Optional


class PomodoroTimer:
    """A Pomodoro timer with sound notifications using system commands."""

    def __init__(self, sound_file: Optional[str] = None):
        """Initialize the timer.

        Args:
            sound_file: Path to custom sound file. If None, uses packaged default.
        """
        self.sound_file = sound_file or self._get_default_sound_file()

    def _get_default_sound_file(self) -> str:
        """Get the path to the packaged sound file."""
        current_dir = Path(__file__).parent
        sound_path = current_dir / "alarm_sounds" / "Gentle-wake-up-alarm-sound.mp3"
        return str(sound_path)

    def start(self, minutes: int) -> None:
        """Start the Pomodoro timer.

        Args:
            minutes: Duration of the timer in minutes.
        """
        if minutes <= 0:
            raise ValueError("Timer duration must be positive")

        seconds = minutes * 60
        print(f"🍅 Starting Pomodoro timer for {minutes} minutes.")
        print("Press Ctrl+C to cancel.")
        print()

        try:
            while seconds:
                mins, secs = divmod(seconds, 60)
                timer = f"{mins:02d}:{secs:02d}"
                print(f"\r⏰ Time left: {timer}", end="", flush=True)
                time.sleep(1)
                seconds -= 1

            print("\n🎉 Time's up! Great work!")
            self._play_alarm()

        except KeyboardInterrupt:
            print("\n❌ Timer cancelled.")

    def _play_alarm(self) -> None:
        """Play the alarm sound using system commands."""
        if not os.path.exists(self.sound_file):
            print(f"Warning: Sound file not found at {self.sound_file}")
            return

        system = platform.system().lower()
        
        try:
            if system == "linux":
                # Try different players in order of preference
                players = [
                    ["paplay", self.sound_file],           # PulseAudio
                    ["aplay", self.sound_file],            # ALSA
                    ["ffplay", "-nodisp", "-autoexit", self.sound_file],  # FFmpeg
                    ["mpg123", self.sound_file],           # mpg123
                    ["cvlc", "--play-and-exit", self.sound_file],  # VLC
                ]
                
                for player in players:
                    if subprocess.run(["which", player[0]], 
                                    capture_output=True).returncode == 0:
                        subprocess.run(player, capture_output=True)
                        return
                        
            elif system == "darwin":  # macOS
                subprocess.run(["afplay", self.sound_file])
                return
                
            elif system == "windows":
                subprocess.run(["powershell", "-c", 
                              f"(New-Object Media.SoundPlayer '{self.sound_file}').PlaySync()"])
                return
                
            print("No suitable audio player found")
            
        except Exception as e:
            print(f"Could not play sound: {e}")