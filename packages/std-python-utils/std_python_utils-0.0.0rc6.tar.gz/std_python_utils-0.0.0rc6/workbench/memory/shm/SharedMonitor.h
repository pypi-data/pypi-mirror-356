#ifndef SHAREDMONITOR_H
#define SHAREDMONITOR_H

#include <pthread.h>    // POSIX mutex and condition variables
#include <sys/mman.h>   // For shm_open(), mmap(), munmap(), shm_unlink()
#include <fcntl.h>      // For O_CREAT, O_RDWR
#include <unistd.h>     // For close(), ftruncate()

#define SHM_NAME "/shared_monitor"

struct SharedMonitor {
    pthread_mutex_t mutex;
    pthread_cond_t condition;
    int data;
    int waiting_count;  // Keeps track of waiting processes
};

class SharedMonitorManager {
private:
    int shm_fd;
    void* shm_ptr;

public:
    SharedMonitor* monitor;

    SharedMonitorManager();
    ~SharedMonitorManager();

    void wait();
    void signal();
    void broadcast(int count = -1);  // Wake up a specific number of processes
    int read();
    void write(int value);

    static SharedMonitorManager* create();
    static SharedMonitorManager* get();
    static void destroy();
};


#endif // SHAREDMONITOR_H
