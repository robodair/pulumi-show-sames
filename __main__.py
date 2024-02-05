import pulumi
import pulumi_random as random

import os

NUM_CHILD_RESOURCES = int(os.environ["NUM_CHILD_RESOURCES"])
DO_PARENT = os.environ.get("DO_PARENT", False)
NUM_DEPENDENCIES = int(os.environ["NUM_DEPENDENCIES"])

print(
    "NUM_CHILD_RESOURCES=",
    NUM_CHILD_RESOURCES,
    "NUM_DEPENDENCIES=",
    NUM_DEPENDENCIES,
    "DO_PARENT=",
    DO_PARENT,
)

parent_resources = []
for name in range(100):
    last = random.RandomPassword(
        "parent-" + str(name),
        length=20,
    )
    parent_resources.append(last)

depends_on = parent_resources[0:NUM_DEPENDENCIES]

for name in range(NUM_CHILD_RESOURCES):
    if DO_PARENT:
        parent: pulumi.Resource | None = parent_resources[name % 100]
    else:
        parent = pulumi.ROOT_STACK_RESOURCE

    last = random.RandomPassword(
        "child-" + str(name),
        length=20,
        opts=pulumi.ResourceOptions(
            depends_on=depends_on,
            parent=parent,
        ),
    )
    depends_on.append(last)
