
import subprocess
import time
from pathlib import Path

import requests


class LLMManager:
    def __init__(
        self,
        model="Qwen/Qwen3-1.7B-GGUF:Q8_0",
        port=8082,
        startup_timeout=180,
        n_gpu_layers=99,
        ctx_size=16384,
        parallel=1,
        flash_attn="on",
        reasoning="off"
    ):
        self.model = model
        self.port = port
        self.startup_timeout = startup_timeout
        self.n_gpu_layers = n_gpu_layers
        self.ctx_size = ctx_size
        self.parallel = parallel
        self.flash_attn = flash_attn
        self.reasoning = reasoning

        self.base_url = f"http://127.0.0.1:{port}"

        self.process = None
        self.log_file = None
        self.started_by_us = False

        self.project_root = Path(__file__).resolve().parent.parent
        self.log_path = self.project_root / "llama-server.log"
        
    def get_status(self):
        """Return the current LLM server status."""

        if self.is_running():
            return "running"

        if self.started_by_us and self.process:
            if self.process.poll() is not None:
                return "crashed"

        return "unavailable"

    def is_running(self):
        """Check whether a llama-server is responding."""

        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=2
            )

            return response.status_code == 200

        except requests.RequestException:
            return False

    def start(self):
        """
        Start llama-server if it is not already running.
        Wait until its health endpoint responds.
        """

        if self.is_running():
            print("LLM server is already running.")
            return True

        command = [
            "llama-server",
            "-hf", self.model,
            "--port", str(self.port),
            "-ngl", str(self.n_gpu_layers),
            "-c", str(self.ctx_size),
            "-np", str(self.parallel),
            "--flash-attn", self.flash_attn,
            "--reasoning", self.reasoning
        ]

        try:
            print("Starting VoxMate LLM server...")

            self.log_file = open(
                self.log_path,
                "a",
                encoding="utf-8"
            )

            self.process = subprocess.Popen(
                command,
                cwd=self.project_root,
                stdin=subprocess.DEVNULL,
                stdout=self.log_file,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            self.started_by_us = True

        except FileNotFoundError:
            self._close_log()
            raise RuntimeError(
                "llama-server was not found. "
                "Make sure it is installed and available in PATH."
            )

        except Exception:
            self._close_log()
            raise

        start_time = time.time()

        while time.time() - start_time < self.startup_timeout:

            if self.process.poll() is not None:
                self._close_log()
                raise RuntimeError(
                    "llama-server stopped unexpectedly. "
                    f"Check the log file: {self.log_path}"
                )

            if self.is_running():
                print("LLM server is ready.")
                return True

            time.sleep(1)

        self.stop()

        raise TimeoutError(
            "LLM server did not become ready in time. "
            f"Check the log file: {self.log_path}"
        )

    def stop(self):
        """
        Stop only the server process started by this manager.
        Never terminate an externally started server.
        """

        if not self.started_by_us:
            print("Leaving externally started LLM server untouched.")
            return

        if self.process and self.process.poll() is None:
            print("Stopping VoxMate LLM server...")

            self.process.terminate()

            try:
                self.process.wait(timeout=10)

            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self.process = None
        self.started_by_us = False

        self._close_log()

    def _close_log(self):
        if self.log_file:
            self.log_file.close()
            self.log_file = None
