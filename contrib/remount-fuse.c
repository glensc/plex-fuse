//
// https://stackoverflow.com/questions/28302178/how-can-i-add-a-volume-to-an-existing-docker-container/77944759#77944759
//
// $ gcc remount-fuse.c -o remount-fuse
//
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sched.h>
#include <fcntl.h>
#include <unistd.h>

#include <linux/mount.h>

#include <errno.h>
#include <sys/syscall.h>

int main(int argc, char **argv)
{
    if (argc < 3) {
        printf("usage: ./a.out pid src_dir dst_dir\n");
        return 0;
    }

    char *pid = argv[1];
    char *src_dir = argv[2];
    char *dst_dir = argv[3];

    int fd_mnt;
    fd_mnt = syscall(__NR_open_tree, 
        -EBADF, src_dir, OPEN_TREE_CLONE);

    if (fd_mnt < 0) {
        perror("open_tree failed");
        return 1;
    }

    char mount_namespace[1000];
    snprintf(mount_namespace, 1000, "/proc/%s/ns/mnt", pid);
    int fd_mntns = open(mount_namespace, O_RDONLY);

    if (fd_mntns < 0) {
        printf("open /proc/%s/ns/mnt failed: %s", pid, strerror(errno));
        return 1;
    }

    setns(fd_mntns, 0);

    int ret = syscall(__NR_move_mount, 
        fd_mnt, "", -EBADF, dst_dir, MOVE_MOUNT_F_EMPTY_PATH );

    if (ret < 0) {
        perror("move_mount failed");
        return 1;
    }

    printf("mounted %s to %s of namespace %s\n", src_dir, dst_dir, mount_namespace);
    return 0;
}
