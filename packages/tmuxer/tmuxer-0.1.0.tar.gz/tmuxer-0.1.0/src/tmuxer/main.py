import random
import string
import re
import shlex
import atexit
from multiprocessing import shared_memory
import subprocess
import importlib.resources
import os


class TmuxSession:
    """Run shell commands inside *tmux* (preferred) or a local subprocess.

    In *tmux* mode each `run()` call:

    1. Opens a new window in the session.
    2. Emits a **START sentinel**, then the user’s command, then an **END sentinel**.
    3. Polls the default pane (0) until the END sentinel appears, then returns everything
       between the two markers.
    4. Kills the window on success; leaves it open if a timeout/error occurs.
    """

    # ------------------------------------------------------------------
    # Life-cycle
    # ------------------------------------------------------------------

    def __init__(
        self,
        *,
        max_capture_lines: int = 3000,
    ) -> None:
        self.max_capture_lines: int = max_capture_lines
        self.session: str = self.get_uid()
        self._ensure_tmux_session()

        self.shmw_path = str(importlib.resources.files("tmuxer").joinpath("shmw"))
        if not os.path.exists(self.shmw_path):
            raise FileNotFoundError

        atexit.register(self.close)

    # ------------------------------------------------------------------
    # Low-level helpers – tmux
    # ------------------------------------------------------------------

    def _ensure_tmux_session(self):
        """Ensure the tmux session exists; if not, create it detached."""
        session = self.session
        try:
            subprocess.run(
                ["tmux", "has-session", "-t", session],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            # Session does not exist, create it
            subprocess.run(f"tmux new-session -d -s {session}", shell=True, check=True)

    def close(self):
        subprocess.run(["tmux", "kill-session", "-t", self.session], check=True)

    def _tmux_new_window(self, target_session: str) -> str:
        """Create a new tmux window in the session and return its window id (e.g. 'sim:1')."""
        proc = subprocess.run(
            [
                "tmux",
                "new-window",
                "-d",
                "-t",
                target_session,
                "-P",
                "-F",
                "#{window_index}",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return proc.stdout.strip()

    def _tmux_kill_window(self, window_target: str) -> None:
        subprocess.run(
            [
                "tmux",
                "kill-window",
                "-t",
                window_target,
            ],
            check=True,
        )

    def _tmux_send(cmd: str, pane_target: str) -> None:
        subprocess.run(
            [
                "tmux",
                "send-keys",
                "-t",
                pane_target,
                cmd,
                "C-m",
            ],
            check=True,
        )

    def _tmux_capture(self, pane_target: str) -> str:
        proc = subprocess.run(
            [
                "tmux",
                "capture-pane",
                "-p",
                "-t",
                pane_target,
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return proc.stdout

    def _tmux_extract_output(self, sentinel: str) -> tuple[int, str]:
        shm = shared_memory.SharedMemory(name=sentinel, create=False)
        output = shm.buf.tobytes().decode("utf-8").rstrip("\x00")
        shm.close()
        shm.unlink()
        pattern = rf"{sentinel}_start_\d{{1,6}}_(.*?){sentinel}_end_(\d{{1,3}})_"
        match = re.search(pattern, output, re.DOTALL)
        return match.group(2), match.group(1).strip()

    def get_uid(self, length=30):
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))

    # ------------------------------------------------------------------
    # Core tmux runner
    # ------------------------------------------------------------------

    def run(self, cmd: str, attach: bool = False) -> str:
        sentinel = self.get_uid()

        wi = self._tmux_new_window(self.session)
        wt = f"{self.session}:{wi}"
        pt = f"{wt}.0"

        # Start pipe-pane first
        subprocess.run(
            f"tmux pipe-pane -t {pt} -o '{self.shmw_path} /{sentinel} 4096'", shell=True
        )

        if attach:
            cmd = (
                """echo %s_start_$$_; %s; echo %s_end_$?_; tmux wait-for -S %s; tmux detach-client"""
                % (sentinel, cmd, sentinel, sentinel)
            )
            cmd = shlex.quote(cmd)
            # NOTE: do not use fstring here.
            subprocess.run("tmux send-keys -t %s %s C-m" % (pt, cmd), shell=True)
            subprocess.run(f"tmux attach -t {pt}", shell=True)
        else:
            cmd = """echo %s_start_$$_; %s; echo %s_end_$?_; tmux wait-for -S %s""" % (
                sentinel,
                cmd,
                sentinel,
                sentinel,
            )
            cmd = shlex.quote(cmd)
            # NOTE: do not use fstring here.
            subprocess.run("tmux send-keys -t %s %s C-m" % (pt, cmd), shell=True)
            # Wait for the cmd to finish
            subprocess.run("tmux wait-for %s" % sentinel, shell=True, check=True)

        # Stop pipe-pane
        # NOTE: Always stop pipe-pane before extracting output
        subprocess.run(f"tmux pipe-pane -t {pt}", shell=True)

        # Extract output from the shared memory
        # NOTE: Make sure pipe-pane is stopped before extracting output
        # otherwise we get filenotfounderror, this happens on initial exection
        # with fresh install.
        rc, output = self._tmux_extract_output(sentinel)

        # Kill the window
        self._tmux_kill_window(wt)

        return int(rc), output
