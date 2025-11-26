# Simple inotify

Very thin inotify(7) wrapper for Linux.

+ Pure Python, depends on *ctypes* in standard library, no other dependencies
+ Simply group and expose the underlying syscall, Linux specific
+ Only simple event parsing, no complex event model or worker thread
+ No recursive watching support, the same as the underlying syscall
+ Supports non-blocking mode and get the fd, to be polled in your event loop


## Example

```python

from simple_inotify import *

observer = Inotify()
wd = ovserver.add_watch("/tmp")
while True:
	events = observer.read()
	for ev in events:
		print(ev)

```


## API reference

The import module name is **simple_inotify**

Please refer to inotify(7) for details


### inotify_event

inotify_event = namedtuple("inotify_event", ("wd", "mask", "cookie", "len", "name"))


### class Inotify

Inotify class thar wraps inotify functions.


**__init__(self, flags = 0)**

Initializer, calling *inotify_init1(2)* with *flags* and holds the returned fd.
Available flags are *IN_CLOEXEC* and *IN_NONBLOCK*.


**close(self)**

Calling *close(2)* on the inotify fd.


**fileno(self)**

Gets the underlying inotify fd, could be used to poll(2) elsewhere.


**add_watch(self, path, /, mask = IN_ALL_EVENTS)**

Calling *inotify_add_watch(2)* to register a new watch item, returns the watch descriptor.


**rm_watch(self, wd)**

Calling *inotify_rm_watch(2)* with given *wd* to unregister a watch.


**get(self, wd)**

Gets the path used to register the watch *wd*, returns *None* if not known.


**read(self)**

Calling *read(2)* on the inotify fd and parse the results. Returns a list of *inotify_event*.
If the *IN_NONBLOCK* flag is set, returns an empty list if there is no new data.


### constants

+ IN_ACCESS
+ IN_MODIFY
+ IN_ATTRIB
+ IN_CLOSE_WRITE
+ IN_CLOSE_NOWRITE
+ IN_OPEN
+ IN_MOVED_FROM
+ IN_MOVED_TO
+ IN_CREATE
+ IN_DELETE
+ IN_DELETE_SELF
+ IN_MOVE_SELF
+ IN_UNMOUNT
+ IN_Q_OVERFLOW
+ IN_IGNORED
+ IN_CLOSE
+ IN_MOVE
+ IN_ONLYDIR
+ IN_DONT_FOLLOW
+ IN_EXCL_UNLINK
+ IN_MASK_CREATE
+ IN_MASK_ADD
+ IN_ISDIR
+ IN_ONESHOT
+ IN_ALL_EVENTS
+ IN_CLOEXEC
+ IN_NONBLOCK


## Reference

+ [inotify(7)](https://linux.die.net/man/7/inotify)

