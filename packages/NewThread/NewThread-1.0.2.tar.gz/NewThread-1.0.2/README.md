这个模块只要包括两个类： 

     一 ThreadEx：
   ThreadEx 类 继承了常用模块 threading 的 Thread  类
完整继承了Thread的6个参数： group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
新增了方法： 暂停线程 
           恢复线程
           强制停止线程
新增了： 线程状态属性       self.status
新增了： 系统级别线程id属性
        self.tid: 系统级别的id 这个 类创建的 对象
        python thread类对象，通常也称为 线程id 他是 thread操作的句柄对象。 这里我在执行thread对象时候执行获取了线程在系统里面的id
        然后通过系统api 根据 系统里面的线程id来控制线程的 暂停 停止 继续，结束 。这里对于默认的Thread 线程类的继承 

总结： 这个类适合 创建 操作 单个线程， 如果需要多个线程同时操作，可以使用 ThreadManage 类来实现更高级的功能。

    二 ThreadManage:
  调用 ThreadEx 类。 创建对象 创建对象时候每一次创建都会被记录线程id到ThreadManage的全局列表中， 后续使用这个列表对所有线程进行批量管理
可以批量停止全部线程，暂停全部线程，恢复全部线程运行。
这个类适合在需要管理多个线程时候使用

    pip 安装： 
"       pip install NewThread     "

    更新：
    1.01 版本做了部分更新。优化。增加了 停止单个线程的功能。
    1.02 版本新增了 清理 线程列表功能，防止线程列表 成员 在极端情况下会 一直增加
