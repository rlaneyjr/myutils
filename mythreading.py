"""Utility module for Threading using Python3"""
import threading


class MultiThreadUtility:
    """Utility class for multi threaded operations."""

    @staticmethod
    def get_current_thread_identity():
        """Get current thread Unique Identity."""
        current_thread_id = threading.get_ident()
        return current_thread_id()

    @staticmethod
    def get_no_of_active_threads():
        """Get the total no. of active threads."""
        get_no_of_threads = threading.active_count()
        return get_no_of_threads()

    @staticmethod
    def get_thread_name():
        """Get Current Thread Name."""
        current_thread_name = threading.currentThread().getName()
        return current_thread_name()
