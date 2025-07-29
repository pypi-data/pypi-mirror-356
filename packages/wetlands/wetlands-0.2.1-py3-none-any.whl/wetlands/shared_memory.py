from multiprocessing import shared_memory
import numpy as np
from multiprocessing import resource_tracker

# Problem: we might want shared memory for other things than numpy, in which case we don't need numpy

def share_array(array: np.ndarray):
    # Create the shared memory
    shm = shared_memory.SharedMemory(create=True, size=array.nbytes)
    # Create a NumPy array backed by shared memory
    shared = np.ndarray(array.shape, dtype=array.dtype, buffer=shm.buf)
    # Copy the array into the shared memory
    shared[:] = array[:]
    # Return the shape, dtype and shared memory name to recreate the numpy array on the other side
    return array.shape, array.dtype, shm

def array_from_shared_memory(shape: tuple[int, ...], dtype: np.dtype, name: str):
    # Get the shared memory
    shm = shared_memory.SharedMemory(name=name)
    # Create a NumPy array backed by shared memory    
    return np.ndarray(shape, dtype=dtype, buffer=shm.buf), shm

def close_shared_memory(shm: shared_memory.SharedMemory):
    # Clean up the shared memory in this process
    shm.close()
    
def unregister(shm: shared_memory.SharedMemory):
    # Avoid resource_tracker warnings
    try:
        resource_tracker.unregister(shm._name, "shared_memory")  # type: ignore
    except Exception:
        pass  # Silently ignore if unregister fails

def release_shared_memory(shm: shared_memory.SharedMemory):
    # Clean up the shared memory in this process
    shm.close()
    # Free and release the shared memory block
    shm.unlink()
