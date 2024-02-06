import pulumi
import pulumi_random as random

import os
import collections

DO_PARENT = os.environ["DO_PARENT"].upper() == "TRUE"
NUM_DEPENDENCIES = int(os.environ["NUM_DEPENDENCIES"])

STACK_SIZE = int(os.environ["STACK_SIZE"])
DEPENDING_RESOURCES = STACK_SIZE // 2
BASE_RESOURCES = STACK_SIZE - DEPENDING_RESOURCES

# Determine dependency mappings
depends_per_resource = NUM_DEPENDENCIES // DEPENDING_RESOURCES
leftover_depends = NUM_DEPENDENCIES % DEPENDING_RESOURCES

print("Per Resource:", depends_per_resource)
print("Leftover:", leftover_depends)
print("Parenting:", DO_PARENT, type(DO_PARENT))

if depends_per_resource > BASE_RESOURCES:
    pulumi.error(
        f"More dependencies requested per resource ({depends_per_resource}) "
        f"than we can support with {BASE_RESOURCES} parent resources"
    )
    exit(1)


parent_resources = []
for index in range(BASE_RESOURCES + depends_per_resource):
    last = random.RandomPassword(
        "base-" + str(index),
        length=1,
    )
    parent_resources.append(last)

dependencies_queue = collections.deque(parent_resources)

for index in range(0, DEPENDING_RESOURCES):
    num_depends = depends_per_resource

    # Spread leftovers among the resources
    if leftover_depends > 0:
        leftover_depends = leftover_depends - 1
        num_depends = num_depends + 1

    # rotating collection of resource dependencies from queue
    depends_on = [dependencies_queue[i] for i in range(num_depends)]
    dependencies_queue.rotate(num_depends)

    if DO_PARENT:
        parent: pulumi.Resource | None = parent_resources[index % 100]
    else:
        parent = pulumi.ROOT_STACK_RESOURCE

    last = random.RandomPassword(
        "depending-" + str(index),
        length=1,
        opts=pulumi.ResourceOptions(
            depends_on=parent_resources[0:depends_per_resource],
            parent=parent,
        ),
    )

    pulumi.debug(f"Num Dependencies = {len(depends_on)}", last)
