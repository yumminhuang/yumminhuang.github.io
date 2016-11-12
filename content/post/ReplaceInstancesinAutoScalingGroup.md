+++
title      = "在 AWS AutoScaling Group 中替换 Instance"
categories = ["DevOps"]
tags       = ["DevOps", "Python", "Boto", "AWS"]
date       = "2014-08-02"
+++

这两周，我被分配的任务是实现 [AWS](http://aws.amazon.com/) 的 [Auto Scaling](http://aws.amazon.com/autoscaling/)功能。多亏有了 [Boto](https://github.com/boto/boto)， 很快就实现了创建 Auto Scaling Group 和添加 Scaling Policy。但是有一个问题却花费了一些时间才顺利解决。
<!--more-->


我们的团队每周四发布新的代码。为了确保服务不中断，更新代码的步骤如下：

1. 创建并配置（下载新发布的代码）多个新的 Instance；
2. 依次关闭旧的 Instance，每关闭一个 Instance，就激活（运行代码）一个新的 Instance 来替代被关闭的 Instance。

这样可以保证在 AWS 上运行的 Instance 依次得到更新，并且服务没有中断。

现在的问题是：使用了 Auto Scaling 之后，每次尝试改变 Auto Scaling Group 当中的 Instance 数目，都会激发 Scaling Policy。比如我想关闭一个旧的 Instance，这样 Auto Scaling Group 当中 Instance 的数量就会小于 Desired Capacity，Auto Scaling Group 就会新创建一个 Instance， 而不是等我激活一个 Instance 去替代。

我想到的办法步骤如下：

1. 将 Auto Scaling Group 挂起（避免激发 Scaling Policy）；
2. 按照以前的方法替换旧的 Instance；
3. 将新创建的 Instance 添加到 Auto Scaling Group。

因为 AWS Auto Scaling 的特性（比如 Auto Scaling Group 被挂起的时候不能够添加 Instance，`desired_capacity` 不能小于 `min_size`），实现第三步并不容易。具体来说第三步又要分成下面几个步骤：

1. 将 Auto Scaling Group 的 `desired_capacity` 和 `min_size` 分别置为 `0`（防止恢复 Auto Scaling Group 的时候自动创建 Instance）；
2. 恢复 Auto Scaling Group（结束挂起状态，然后才可以添加 Instance）；
3. 添加 Instance 到 Auto Scaling Group 里；
4. 恢复 Auto Scaling Group 的 `min_size`。

下面提供一份示例代码以供参考：

```
#!python
import sys
import time

from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.connection import EC2Connection

AUTO_SCALING_GROUP = "test_auto_scaling_group"
NEW_INSTANCES = ["i-4acb0666", "i-4acbqa9"]
CHECK_INTERVAL = 5


def suspend(as_conn):
    """
    Suspend auto scaling group
    """
    as_conn.suspend_processes(AUTO_SCALING_GROUP)
    print "Suspend Done\n"


def resume(as_conn):
    """
    Resume auto scaling group
    """
    as_conn.resume_processes(AUTO_SCALING_GROUP)
    print "Resume Done\n"


def get_instance_by_id(ec2conn, inst_id):
    """
    Get instance by its id
    """
    ...
    pass

def deactivate_instance(inst):
    """
    Deactivate instance
    """
    ...
    pass


def delete_instances(as_conn, ec2conn):
    """
    Delete instances in auto scaling group
    """
    as_group = as_conn.get_all_groups(names=[AUTO_SCALING_GROUP])[0]
    instances = [get_instance_by_id(ec2conn, i.instance_id) for i in as_group.instances]
    for instance in instances:
        if instance.state != "terminated":
            print "*** Terminate Instance %s" % instance.id
            deactivate_instance(instance)
    # All instances should be terminated
    while any([inst.update() != "terminated" for inst in instances]):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(CHECK_INTERVAL)
    print ".\nDelete Done\n"


def attach_instances(as_conn):
    """
    Attach instances into auto scaling group
    """
    while True and NEW_INSTANCES:
        as_group = as_conn.get_all_groups(names=[AUTO_SCALING_GROUP])[0]
        if len(as_group.instances) == 0:
            as_conn.attach_instances(AUTO_SCALING_GROUP, NEW_INSTANCES)
            print "Attach Done\n"
            return
        else:
            print "There are instances still in the group"
            time.sleep(CHECK_INTERVAL)


def set_capacity(as_conn):
    """
    Set desired capacity and minimum size as 0
    """
    as_group = as_conn.get_all_groups(names=[AUTO_SCALING_GROUP])[0]
    as_group.min_size = 0
    as_group.desired_capacity = 0
    as_group.update()
    print "Set Capacity Done\n"


def resume_capacity(as_conn):
    """
    Resume minimum size as the original value
    """
    as_group = as_conn.get_all_groups(names=[AUTO_SCALING_GROUP])[0]
    setattr(as_group,"min_size", 1)
    as_group.update()
    print "Resume Capacity Done\n"


def main():
    as_conn = AutoScaleConnection()
    ec2conn = EC2Connection()

    print "Suspend Auto Scaling Group"
    suspend(as_conn)

    print "Delete Instances"
    delete_instances(as_conn, ec2conn)

    print "Set Capacity"
    set_capacity(as_conn)

    print "Resume Auto Scaling Group"
    resume(as_conn)

    print "Attach Instances"
    attach_instances(as_conn)

    print "Resume Capacity"
    resume_capacity(as_conn)


if __name__ == "__main__":
    main()
```
