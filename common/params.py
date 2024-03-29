#!/usr/bin/env python3
# this file is part of openpilot
"""ROS has a parameter server, we have files.

  The parameter store is a persistent key value store, implemented as a directory with a writer lock.
  On Android, we store params under params_dir = /data/params. The writer lock is a file
  "<params_dir>/.lock" taken using flock(), and data is stored in a directory symlinked to by
  "<params_dir>/d".

  Each key, value pair is stored as a file with named <key> with contents <value>, located in
    <params_dir>/d/<key>

  Readers of a single key can just open("<params_dir>/d/<key>") and read the file contents.
  Readers who want a consistent snapshot of multiple keys should take the lock.

  Writers should take the lock before modifying anything. Writers should also leave the DB in a
  consistent state after a crash. The implementation below does this by copying all params to a temp
  directory <params_dir>/<tmp>, then atomically symlinking <params_dir>/<d> to <params_dir>/<tmp>
  before deleting the old <params_dir>/<d> directory.

  Writers that only modify a single key can simply take the lock, then swap the corresponding value
  file in place without messing with <params_dir>/d.
  """

import time
import os
import errno
import shutil
import fcntl
import tempfile
import threading
from enum import Enum, auto
import common.constants as co
from common.keys import keys, TxType, keys_by_Type
from factory_settings.params import factory_settings
from pprint import PrettyPrinter
pPrint = PrettyPrinter(indent=1).pprint

def mkdirs_exists_ok(path):
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

class UnknownKeyName(Exception):
  pass

def fsync_dir(path):
  fd = os.open(path, os.O_RDONLY)
  try:
    os.fsync(fd)
  finally:
    os.close(fd)


class FileLock():
  def __init__(self, path, create):
    self._path = path
    self._create = create
    self._fd = None

  def acquire(self):
    self._fd = os.open(self._path, os.O_CREAT if self._create else 0)
    fcntl.flock(self._fd, fcntl.LOCK_EX)

  def release(self):
    if self._fd is not None:
      os.close(self._fd)
      self._fd = None


class DBAccessor():
  def __init__(self, path):
    self._path = path
    self._vals = None

  def keys(self):
    self._check_entered()
    return self._vals.keys()

  def get(self, key):
    self._check_entered()

    if self._vals is None:
      return None

    try:
      return self._vals[key]
    except KeyError:
      return None

  def _get_lock(self, create):
    lock = FileLock(os.path.join(self._path, ".lock"), create)
    lock.acquire()
    return lock

  def _read_values_locked(self):
    """Callers should hold a lock while calling this method."""
    vals = {}
    try:
      data_path = self._data_path()
      keys = os.listdir(data_path)
      for key in keys:
        with open(os.path.join(data_path, key), "rb") as f:
          vals[key] = f.read()
    except (OSError, IOError) as e:
      # Either the DB hasn't been created yet, or somebody wrote a bug and left the DB in an
      # inconsistent state. Either way, return empty.
      if e.errno == errno.ENOENT:
        return {}

    return vals

  def _data_path(self):
    return os.path.join(self._path, "d")

  def _check_entered(self):
    if self._vals is None:
      raise Exception("Must call __enter__ before using DB")


class DBReader(DBAccessor):
  def __enter__(self):
    try:
      lock = self._get_lock(False)
    except OSError as e:
      # Do not create lock if it does not exist.
      if e.errno == errno.ENOENT:
        self._vals = {}
        return self

    try:
      # Read everything.
      self._vals = self._read_values_locked()
      return self
    finally:
      lock.release()

  def __exit__(self, exc_type, exc_value, traceback):
    pass


class DBWriter(DBAccessor):
  def __init__(self, path):
    super(DBWriter, self).__init__(path)
    self._lock = None
    self._prev_umask = None

  def put(self, key, value):
    self._vals[key] = value

  def delete(self, key):
    self._vals.pop(key, None)

  def __enter__(self):
    mkdirs_exists_ok(self._path)

    # Make sure we can write and that permissions are correct.
    self._prev_umask = os.umask(0)

    try:
      os.chmod(self._path, 0o777)
      self._lock = self._get_lock(True)
      self._vals = self._read_values_locked()
    except Exception:
      os.umask(self._prev_umask)
      self._prev_umask = None
      raise

    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self._check_entered()

    try:
      # data_path refers to the externally used path to the params. It is a symlink.
      # old_data_path is the path currently pointed to by data_path.
      # tempdir_path is a path where the new params will go, which the new data path will point to.
      # new_data_path is a temporary symlink that will atomically overwrite data_path.
      #
      # The current situation is:
      #   data_path -> old_data_path
      # We're going to write params data to tempdir_path
      #   tempdir_path -> params data
      # Then point new_data_path to tempdir_path
      #   new_data_path -> tempdir_path
      # Then atomically overwrite data_path with new_data_path
      #   data_path -> tempdir_path
      old_data_path = None
      new_data_path = None
      tempdir_path = tempfile.mkdtemp(prefix=".tmp", dir=self._path)

      try:
        # Write back all keys.
        os.chmod(tempdir_path, 0o777)
        for k, v in self._vals.items():
          with open(os.path.join(tempdir_path, k), "wb") as f:
            f.write(v)
            f.flush()
            os.fsync(f.fileno())
        fsync_dir(tempdir_path)

        data_path = self._data_path()
        try:
          old_data_path = os.path.join(self._path, os.readlink(data_path))
        except (OSError, IOError):
          # NOTE(mgraczyk): If other DB implementations have bugs, this could cause
          #             copies to be left behind, but we still want to overwrite.
          pass

        new_data_path = "{}.link".format(tempdir_path)
        os.symlink(os.path.basename(tempdir_path), new_data_path)
        os.rename(new_data_path, data_path)
        fsync_dir(self._path)
      finally:
        # If the rename worked, we can delete the old data. Otherwise delete the new one.
        success = new_data_path is not None and os.path.exists(data_path) and (
          os.readlink(data_path) == os.path.basename(tempdir_path))

        if success:
          if old_data_path is not None:
            shutil.rmtree(old_data_path)
        else:
          shutil.rmtree(tempdir_path)

        # Regardless of what happened above, there should be no link at new_data_path.
        if new_data_path is not None and os.path.islink(new_data_path):
          os.remove(new_data_path)
    finally:
      os.umask(self._prev_umask)
      self._prev_umask = None

      # Always release the lock.
      self._lock.release()
      self._lock = None


def read_db(params_path, key):
  path = "%s/d/%s" % (params_path, key)
  try:
    with open(path, "rb") as f:
      return f.read()
  except IOError:
    return None


def write_db(params_path, key, value):
  if isinstance(value, str):
    value = value.encode('utf8')

  prev_umask = os.umask(0)
  lock = FileLock(params_path + "/.lock", True)
  lock.acquire()

  try:
    tmp_path = tempfile.NamedTemporaryFile(mode="wb", prefix=".tmp", dir=params_path, delete=False)
    with tmp_path as f:
      f.write(value)
      f.flush()
      os.fsync(f.fileno())
    os.chmod(tmp_path.name, 0o666)

    path = "%s/d/%s" % (params_path, key)
    os.rename(tmp_path.name, path)
    fsync_dir(os.path.dirname(path))
  finally:
    os.umask(prev_umask)
    lock.release()

class Params():
  def __init__(self, db=co.PARAMS):
    self.db = db
    self.keys = keys
    # create the database if it doesn't exist...
    if not os.path.exists(self.db + "/d"):
      with self.transaction(write=True):
        pass

  def clear_all(self):
    shutil.rmtree(self.db, ignore_errors=True)
    with self.transaction(write=True):
      pass

  def transaction(self, write=False):
    if write:
      return DBWriter(self.db)
    else:
      return DBReader(self.db)

  def _clear_keys_with_type(self, tx_type):
    with self.transaction(write=True) as txn:
      for key in self.keys:
        if tx_type in self.keys[key]:
          txn.delete(key)
  
  def get_list_of_keys_with_type(self, tx_type):
    result = []
    #print(f"\n\n\n tx_type {tx_type.value}")
    for key in self.keys:
      #print(f"key {key} - keys[key] {keys[key]}")
      if tx_type.value in self.keys[key]:
        result.append(key)
        #pPrint(result)
    return result

  def get_list_of_all_keys(self):
    result=[]
    for key in self.keys:
      result.append(key)
    return result

  def delete(self, key):
    with self.transaction(write=True) as txn:
      txn.delete(key)

  def get(self, key, block=False, encoding='utf-8'):
    if key not in keys:
      raise UnknownKeyName(key)

    while 1:
      ret = read_db(self.db, key)
      if not block or ret is not None:
        break
      # is polling really the best we can do?
      time.sleep(0.05)

    if ret is not None and encoding is not None:
      ret = ret.decode(encoding)
    #print(f"key: {key} -- ret: {ret}")
    return ret

  def get_filtered(self, key, block=False, encoding='utf-8'):
    if key not in keys:
      raise UnknownKeyName(key)

    while 1:
      ret = read_db(self.db, key)
      if not block or ret is not None:
        break
      # is polling really the best we can do?
      time.sleep(0.05)

    if ret is not None and encoding is not None:
      ret = ret.decode(encoding)

    if ret is None:
      ret = "not defined"

    return ret

  def put(self, key, dat):
    """
    Warning: This function blocks until the param is written to disk!
    In very rare cases this can take over a second, and your code will hang.

    Use the put_nonblocking helper function in time sensitive code, but
    in general try to avoid writing params as much as possible.
    """
    if type(dat) == bool:
      if dat:
        dat="1"
      else:
        dat="0"

    if key not in self.keys:
      raise UnknownKeyName(key)
    #print(f"put -- key {key}; value {dat}; type of value: {type(dat)}")
    write_db(self.db, key, dat)

  def add_rfid_card_code_to_keys(self, rfid_card_code):
    self.keys[rfid_card_code]= [TxType.RFID_CARD_CODE]



class Log():
  def __init__(self, db=co.LOG):
    self.params = Params()
    self.db = db

    self.keys = {} # every key (0,1,2,...) is a line of log 
    for i in range(co.MAX_NUMBER_OF_LOG_ENTRIES+1):
      self.keys[str(i)]=[TxType.LOG]
    self.keys["index"] = [TxType.LOG]

    # create the database if it doesn't exist...
    if not os.path.exists(self.db + "/d"):
      with self.transaction(write=True):
        pass

    if self.get("index") is not None:
      self.set_index(int(self.get("index")))
    else:
      self.set_index(0) # where the next entry comes

  def previous_index(self, i):
    previous_index = i-1
    if previous_index <0:
      previous_index = co.MAX_NUMBER_OF_LOG_ENTRIES
    return previous_index
  
  def get_next_index(self, index):
    next_index = index+1
    if next_index>co.MAX_NUMBER_OF_LOG_ENTRIES:
      next_index = 0
    return next_index

  def get_whole_log(self, begin):
    end = self.previous_index(begin)
    return self.get_inc_log(begin, end)

  def sanitize_index(self,i):
    i = int(i)
    if i<0: i=0
    if i>co.MAX_NUMBER_OF_LOG_ENTRIES: i = co.MAX_NUMBER_OF_LOG_ENTRIES
    return i

  def get_inc_log(self, begin, end):
    begin = self.sanitize_index(begin)
    end   = self.sanitize_index(end)
    if begin == end: return ''
    incremental_log =""
    index = begin
    entry = self.get(str(index))
    incremental_log = entry + '\n' + incremental_log
    index = self.get_next_index(index)
    stop_mark = self.previous_index(end)
    while index != stop_mark:
      entry = self.get(str(index))
      incremental_log = entry + '\n' + incremental_log
      index = self.get_next_index(index)
    return incremental_log    

  def next_index(self):
    next_index = self.index+1
    if next_index>co.MAX_NUMBER_OF_LOG_ENTRIES:
      next_index = 0
    self.set_index(next_index)

  def set_index(self, i):
    self.index = i
    write_db(self.db, "index", str(i))
    print(f"set index: {i}")

  def clear_all(self):
    shutil.rmtree(self.db, ignore_errors=True)
    with self.transaction(write=True):
      pass

  def transaction(self, write=False):
    if write:
      return DBWriter(self.db)
    else:
      return DBReader(self.db)

  def _clear_keys_with_type(self, tx_type):
    with self.transaction(write=True) as txn:
      for key in self.keys:
        if tx_type in self.keys[key]:
          txn.delete(key)
  
  def get_list_of_keys_with_type(self, tx_type):
    result = []
    for key in self.keys:
      if tx_type in self.keys[key]:
        result.append(key)
    return result

  def get_list_of_all_keys(self):
    result=[]
    for key in self.keys:
      result.append(key)
    return result

  def delete(self, key):
    with self.transaction(write=True) as txn:
      txn.delete(key)

  def get(self, key, block=False, encoding='utf-8'):
    if key not in self.keys:
      raise UnknownKeyName(key)

    while 1:
      ret = read_db(self.db, key)
      if not block or ret is not None:
        break
      # is polling really the best we can do?
      time.sleep(0.05)

    if ret is not None and encoding is not None:
      ret = ret.decode(encoding)
    #print(f"key: {key} -- ret: {ret}")
    return ret

  def put(self, dat):
    """
    Warning: This function blocks until the param is written to disk!
    In very rare cases this can take over a second, and your code will hang.

    Use the put_nonblocking helper function in time sensitive code, but
    in general try to avoid writing params as much as possible.
    """
    key = self.get("index", block=True)
    self.index = int(key)
    if key not in self.keys:
      raise UnknownKeyName(key)
    #print(f"put -- key {key}; value {dat}; type of value: {type(dat)}")
    write_db(self.db, key, dat)
    self.next_index()



def put_nonblocking(key, val):
  def f(key, val):
    params = Params()
    params.put(key, val)

  t = threading.Thread(target=f, args=(key, val))
  t.start()
  return t

