from .connection import connect_to_region


class InstanceType(object):
    """ A minimal instance type wrapper. """

    connection = None
    instances = []  # list of instances of this type

    def __init__(self, ami_id, key_name, security_groups, instance_type,
                 region_name):
        self.ami_id = ami_id
        self.key_name = key_name
        self.security_groups = security_groups
        self.instance_type = instance_type
        self.region_name = region_name
        self.conn = connect_to_region(self.region_name)

    @property
    def states(self):
        """ Return the status of each instances from this type. """
        return [] if not self.instances else [i.update() for i in self.instances]

    def launch(self, count=1):
        """ Launch new instance based on AMI with id `ami_id`. """
        reservation = self.conn.run_instances(
            self.ami_id,
            max_count=count,
            key_name=self.key_name,
            security_groups=self.security_groups,
            instance_type=self.instance_type
        )
        self.instances = reservation.instances
        return self.instances

    def terminate(self):
        """ Terminates all instances from this type. """
        if self.instances:
            for instance in self.instances:
                instance.terminate()
