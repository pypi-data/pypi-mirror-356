#include "SharedMonitor.h"
#include <iostream>

SharedMonitorManager::SharedMonitorManager() {
    shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        std::cerr << "Error: shm_open failed\n";
        exit(1);
    }

    ftruncate(shm_fd, sizeof(SharedMonitor));

    shm_ptr = mmap(0, sizeof(SharedMonitor), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_ptr == MAP_FAILED) {
        std::cerr << "Error: mmap failed\n";
        exit(1);
    }

    monitor = static_cast<SharedMonitor*>(shm_ptr);

    pthread_mutexattr_t mutex_attr;
    pthread_condattr_t cond_attr;

    pthread_mutexattr_init(&mutex_attr);
    pthread_mutexattr_setpshared(&mutex_attr, PTHREAD_PROCESS_SHARED);

    pthread_condattr_init(&cond_attr);
    pthread_condattr_setpshared(&cond_attr, PTHREAD_PROCESS_SHARED);

    pthread_mutex_init(&monitor->mutex, &mutex_attr);
    pthread_cond_init(&monitor->condition, &cond_attr);

    monitor->data = 0;
    monitor->waiting_count = 0;
}

SharedMonitorManager::~SharedMonitorManager() {
    munmap(shm_ptr, sizeof(SharedMonitor));
    close(shm_fd);
}

void SharedMonitorManager::wait() {
    pthread_mutex_lock(&monitor->mutex);
    monitor->waiting_count++;
    pthread_cond_wait(&monitor->condition, &monitor->mutex);
    monitor->waiting_count--;
    pthread_mutex_unlock(&monitor->mutex);
}

void SharedMonitorManager::signal() {
    pthread_mutex_lock(&monitor->mutex);
    pthread_cond_signal(&monitor->condition);
    pthread_mutex_unlock(&monitor->mutex);
}

void SharedMonitorManager::broadcast(int count) {
    pthread_mutex_lock(&monitor->mutex);

    if (count == -1 || count >= monitor->waiting_count) {
        pthread_cond_broadcast(&monitor->condition);
    } else {
        for (int i = 0; i < count; ++i) {
            pthread_cond_signal(&monitor->condition);
        }
    }

    pthread_mutex_unlock(&monitor->mutex);
}

int SharedMonitorManager::read() {
    pthread_mutex_lock(&monitor->mutex);
    int value = monitor->data;
    pthread_mutex_unlock(&monitor->mutex);
    return value;
}

void SharedMonitorManager::write(int value) {
    pthread_mutex_lock(&monitor->mutex);
    monitor->data = value;
    pthread_mutex_unlock(&monitor->mutex);
}

SharedMonitorManager* SharedMonitorManager::create() {
    return new SharedMonitorManager();
}

SharedMonitorManager* SharedMonitorManager::get() {
    int shm_fd = shm_open(SHM_NAME, O_RDWR, 0666);
    if (shm_fd == -1) {
        std::cerr << "Error: shm_open failed\n";
        exit(1);
    }

    void* shm_ptr = mmap(0, sizeof(SharedMonitor), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_ptr == MAP_FAILED) {
        std::cerr << "Error: mmap failed\n";
        exit(1);
    }

    SharedMonitorManager* instance = new SharedMonitorManager();
    instance->monitor = static_cast<SharedMonitor*>(shm_ptr);
    return instance;
}

void SharedMonitorManager::destroy() {
    shm_unlink(SHM_NAME);
}
