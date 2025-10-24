import os
import time
import signal
import subprocess

from mctl.core.constants import SERVERS_PATH


class ServerManager:

    def __init__(self, server_name: str):
        self.server_name = server_name
        self.server_path = SERVERS_PATH / server_name
        self.jar_path = self.server_path / "server.jar"
        self.pid_file = self.server_path / "pid"
        self.log_file = self.server_path/ "logs" / "latest.log"

    def _is_running(self) -> bool:
        if not self.pid_file.exists():
            return False
        try:
            pid = int(self.pid_file.read_text().strip())
            os.kill(pid, 0)
            return True
        except (ValueError, ProcessLookupError, PermissionError):
            return False

    def start(self) -> None:
        """
        Starts a server, save pid into a text file and verify if it's running.
        :return:
        """
        if not self.jar_path.exists():
            print("Server does not exist")
            return

        if self._is_running():
            print(f"Server '{self.server_name}' is already running")
            return

        self.log_file.parent.mkdir(exist_ok=True)

        cmd = ["java", "-Xmx2G", "-Xms1G", "-jar", str(self.jar_path), "nogui"]
        process = subprocess.Popen(
            cmd,
            cwd=self.server_path,
            stdout=open(self.log_file, "a"),
            stderr=subprocess.STDOUT,
        )
        self.pid_file.write_text(str(process.pid))
        print(f"Started server '{self.server_name}' (PID {process.pid})")

        # --- Safeguard: wait up to 10 seconds ---
        success = False
        for _ in range(20):  # check every 0.5s → ~10 seconds
            time.sleep(0.5)
            if process.poll() is not None:
                print("Server process exited prematurely.")
                print(f"Check log file at '{self.log_file}'")
                self.pid_file.unlink(missing_ok=True)
                return
            try:
                # Look for "Done" in the latest log content
                if self.log_file.exists():
                    log_text = self.log_file.read_text(errors="ignore")
                    if "Done (" in log_text:
                        success = True
                        break
            except Exception:
                pass

        if success:
            print(f"✅ Server '{self.server_name}' started successfully.")
        else:
            print(f"⚠️ Server '{self.server_name}' did not report 'Done' after 10s.")
            print(f"Check logs at: {self.log_file}")

    def stop(self) -> None:
        """
        Stopping a server based on the pid saved in a text file.
        :return: None
        """
        if not self._is_running():
            print(f"Server '{self.server_name}' is not running.")
            return

        pid = int(self.pid_file.read_text().strip())

        try:
            os.kill(pid, signal.SIGTERM)
            os.remove(self.pid_file)
            print(f"Server '{self.server_name}' stopped.")
        except ProcessLookupError:
            print("Process not found — removing stale pid file.")
            self.pid_file.unlink(missing_ok=True)
