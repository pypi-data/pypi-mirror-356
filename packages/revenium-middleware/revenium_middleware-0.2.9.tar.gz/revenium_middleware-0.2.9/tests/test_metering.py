import pytest
import logging
import asyncio
from unittest.mock import patch, AsyncMock

from revenium_middleware.metering import (
    active_threads,
    shutdown_event,
    handle_exit,
    run_async_in_thread
)


class TestMetering:
    @pytest.fixture
    def reset_state(self):
        """Fixture to reset global state before each test."""
        # Clear any active threads
        active_threads.clear()
        shutdown_event.clear()
        yield
        # Cleanup: make sure threads get stopped
        handle_exit()

    def test_run_async_in_thread_when_shutdown(self, reset_state, caplog):
        """If shutdown_event is set, run_async_in_thread should log a warning and return None."""
        shutdown_event.set()
        with caplog.at_level(logging.WARNING):
            thread = run_async_in_thread(asyncio.sleep(0.01))
            assert thread is None
            assert "Not starting new metering thread during shutdown" in caplog.text

    def test_run_async_in_thread_normal(self, reset_state):
        """Check that run_async_in_thread starts a thread and runs the coroutine."""
        coro_mock = AsyncMock()
        thread = run_async_in_thread(coro_mock)
        assert thread is not None
        thread.join(timeout=1.0)
        # Ensure the thread is removed from active_threads once done
        assert thread not in active_threads

    def test_metering_thread_error_handling(self, reset_state, caplog):
        """Ensure MeteringThread logs a warning if an exception occurs."""

        async def fail_coro():
            raise ValueError("Test error")

        with caplog.at_level(logging.WARNING):
            thread = run_async_in_thread(fail_coro())
            thread.join(timeout=1.0)
            assert "Error in metering thread: Test error" in caplog.text

    @patch("signal.signal")
    def test_handle_exit(self, mock_signal, reset_state, caplog):
        """handle_exit should set the shutdown_event and wait for threads to complete."""

        # Create a long-running coroutine
        async def long_run():
            await asyncio.sleep(0.2)

        thread = run_async_in_thread(long_run())
        assert thread is not None
        with caplog.at_level(logging.INFO):
            handle_exit()
            assert shutdown_event.is_set()
            # Thread should have been joined
            assert "Shutdown initiated" in caplog.text
            assert "Shutdown complete" in caplog.text
