import inspect
import threading
import ctypes
import time
from ctypes import wintypes
import os

from path import best_realpath

# Windows API 定义
THREAD_SUSPEND_RESUME = 0x0002
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

OpenThread = kernel32.OpenThread
OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenThread.restype = wintypes.HANDLE

SuspendThread = kernel32.SuspendThread
SuspendThread.argtypes = [wintypes.HANDLE]
SuspendThread.restype = wintypes.DWORD

ResumeThread = kernel32.ResumeThread
ResumeThread.argtypes = [wintypes.HANDLE]
ResumeThread.restype = wintypes.DWORD

CloseHandle = kernel32.CloseHandle


class ThreadEx(threading.Thread):
    def __init__(self, target=None, args=(), start=True, is_daemon=True, kwargs=None, group=None,  name=None, daemon=None):
        """
             self.tid: 系统级别的id 这个 类创建的 对象
                 python thread类对象，通常也称为 线程id 他是 thread操作的句柄对象。 这里我在执行thread对象时候执行获取了线程在系统里面的id
                 然后通过系统api 根据 系统里面的线程id来控制线程的 暂停 停止 继续，结束 。这里对于默认的Thread 线程类的继承 完全继承了6个初始化对象
                 的参数： group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
            通过 self.status  记录线程的状态。
            这个类适合 创建 操作 单个线程， 如果需要多个线程同时操作，可以使用 ThreadManage 类来实现更高级的功能。
        """
        if os.name != 'nt':
            raise NotImplementedError("当前仅支持 Windows 平台")

        self.status = ''
        self.target_function = target
        self.tid = None
        super().__init__(target=self.__target_function, args=args, kwargs=kwargs, group=group, name=name, daemon=daemon)
        # 守护线程。默认True
        if start and is_daemon:
            self.setDaemon(True)
        # 启动线程 默认True
        if start:
            self.start()
            self.status = 'running'
        # 如果不想直接启动线程，也可以仅创建一个线程对象，返回 被继承后的 Thread 对象， 拥有全部Thread原本方法和属性 和新增的方法。

    def suspend(self):
        """ 调用系统api 暂停线程"""
        try:
            h_thread = OpenThread(THREAD_SUSPEND_RESUME, False, self.tid)
            if h_thread:
                SuspendThread(h_thread)
                CloseHandle(h_thread)
            self.status = "suspended"
        except Exception as e:
            pass

    def resume(self):
        """ 调用系统api 恢复线程"""
        try:
            h_thread = OpenThread(THREAD_SUSPEND_RESUME, False, self.tid)
            if h_thread:
                ResumeThread(h_thread)
                CloseHandle(h_thread)
            self.status = "resumed"
        except Exception as e:
            pass

    def stop(self, message=''):
        """ 强制停止线程 返回布尔值 和 错误信息"""
        try:
            self._async_raise(self.tid, SystemExit)
            if message:
                print(f'{message}停止线程成功')
            self.status = 'stopped'
            return True, ""
        except Exception as e:
            print(e)
            return  False, e

    def __target_function(self, *args, **kwargs):
        """
            里用__target_function 调用 target_function 在调用之前这样不需要修改 原版的 thread库，可以再调用之前。
            # 准确获取到系统级的 线程id
            这里完全复刻了 子类的 参数传递。
        """
        try:
            self.tid = ctypes.windll.kernel32.GetCurrentThreadId()
            self.target_function(*args, **kwargs)
        except SystemExit:
            # print("线程被强制停止，执行清理...")
            pass
        finally:
            self.status = 'stopped'

    def _async_raise(self,tid, exc_type):
        """ 尝试根据线程 id 强制停止 线程 返回布尔值 是否成功"""
        try:
            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exc_type):
                exc_type = type(exc_type)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
            return True
        except Exception as e:
            return False


class ThreadManage:
    """
        调用 包含更多功能的 ThreadEx 类。 创建对象 线程， 并记录线程
        这个类适合在需要管理多个线程时候使用, 可以停止全部线程，暂停全部线程，恢复全部线程运行，
    """
    _lock = threading.Lock()
    thread_list = []  # 全局线程列表

    def __init__(self):
        pass

    @classmethod
    def create_thread(cls, target, is_daemon=True, start=True, args=(), kwargs=None, group=None,  name=None, daemon=None):
        cls.cleanup()
        with cls._lock:
            thread_id = ThreadEx(target=target, start=start, is_daemon=is_daemon, args=args,
                                kwargs=kwargs, group=group, name=name, daemon=daemon)
            ThreadManage.thread_list.append(thread_id)  # 添加到全局列表
            return thread_id

    @classmethod
    def suspend_all(cls):
        """ 暂停全部线程 进入休眠状态"""
        cls.cleanup()
        for t in cls.thread_list:
            t.suspend()

    @classmethod
    def resume_all(cls):
        """ 恢复全部线程 从休眠状态中"""
        cls.cleanup()
        for t in cls.thread_list:
            t.resume()

    @classmethod
    def stop_all(cls):
        cls.cleanup()
        """ 强制停止 全部线程"""
        for index in range(len(cls.thread_list)-1, -1, -1):
            if cls.thread_list[index].stop():
                cls.thread_list.pop(index)

    @classmethod
    def stop(cls, t):
        cls.cleanup()
        index_ = -1
        for index in range(len(cls.thread_list)):
            if cls.thread_list[index] == t:
                index_ = index
                break
        if t.stop():
            cls.thread_list.pop(index_)

    @classmethod
    def cleanup(cls):
        cls.thread_list = [t for t in cls.thread_list if t.status != 'stopped']

def test_worker(startwith):
    count = 0
    for ii in range(600):
        print(f"{startwith} 运行: {count}")
        count += 1
        time.sleep(1)
    time.sleep(1)
    print("运行结束")


if __name__ == '__main__':
    t = ThreadManage.create_thread(target=test_worker, args=('子线程 1',))
    t2 = ThreadManage.create_thread(target=test_worker, args= ('子线程 2', ))
    # print(f't.tid={t.tid}')
    time.sleep(3)
    print("暂停线程 1")
    # ThreadManage.suspend_all()  # 暂停

    ThreadManage.stop(t)
    # time.sleep(3)
    # print("恢复线程")
    # # t.resume()   # 恢复
    #
    # time.sleep(3)
    # t.stop()
    count = 0
    while True:
        print(f"主线程： Running: {count}")
        count += 1
        time.sleep(1)

