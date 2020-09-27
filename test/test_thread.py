from python_tools.thread.functions import at_new_thread
import pytest 

@pytest.mark.success
class TestThread:
    def test_at_new_thread(cls):
        import threading 
        main_id = threading.get_ident()
        @at_new_thread
        def what():
            # main thread id != new thread id 
            assert threading.get_ident() != main_id 

            # 2 ways of getting current id is the same
            assert threading.get_ident() == threading.current_thread().ident()