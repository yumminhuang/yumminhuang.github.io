Title: 在 AWS Auto Scaling Group 中替换 Instance
Date: 2014-08-02 14:39
Modified: 2014-08-02 19:39
Category: Python
Tags: Python, Boto

这两周，我被分配的任务是实现[AWS](http://aws.amazon.com/)的[Auto Scaling](http://aws.amazon.com/autoscaling/)功能。多亏有了[Boto](https://github.com/boto/boto)， 很快就实现了创建Auto Scaling Group和添加Scaling Policy。但是有一个问题却花费了一些时间才顺利解决。

我们的团队每周四发布新的代码。为了确保服务不中断，更新代码的步骤如下：

1. 创建并配置（下载新发布的代码）多个新的Instance；
2. 依次关闭旧的Instance，每关闭一个Instance，就激活（运行代码）一个新的Instance来替代被关闭的Instance。

这样可以保证在AWS上运行的Instance依次得到更新，并且服务没有中断。

现在的问题是：使用了Auto Scaling之后，每次尝试改变Auto Scaling Group当中的Instance数目，都会激发Scaling Policy。比如我想关闭一个旧的Instance，这样Auto Scaling Group当中Instance的数量就会小于Desired Capacity，Auto Scaling Group就会新创建一个Instance， 而不是等我激活一个Instance去替代。

我想到的办法步骤如下：

1. 将Auto Scaling Group挂起（避免激发Scaling Policy）；
2. 按照以前的方法替换旧的Instance；
3. 将新创建的Instance添加到Auto Scaling Group。

因为AWS Auto Scaling的特性（比如Auto Scaling Group被挂起的时候不能够添加Instance，`desired_capacity`不能小于`min_size`），实现第三步并不容易。具体来说第三步又要分成下面几个步骤：

1. 将Auto Scaling Group的`desired_capacity`和`min_size`分别置为`0`（防止恢复Auto Scaling Group的时候自动创建Instance）；
2. 恢复Auto Scaling Group（结束挂起状态，然后才可以添加Instance）；
3. 添加Instance到Auto Scaling Group里；
4. 恢复Auto Scaling Group的`min_size`。

下面提供一份示例代码以供参考：

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
        setattr(as_group, "min_size", 1)
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
