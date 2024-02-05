#!/bin/bash

rm -rf logs

echo "stack size, dependencies per child, preview duration"

preview(){
    export LOGDIR=logs/${NUM_CHILD_RESOURCES}-${DO_PARENT}
    mkdir -p $LOGDIR
    echo -n "$NUM_CHILD_RESOURCES, $NUM_DEPENDENCIES, "
    /bin/time --format="%e" pulumi preview > ${LOGDIR}/${NUM_DEPENDENCIES}-deps.log

}

export DO_PARENT=false

for NUM_CHILD_RESOURCES in {0..1000..100};
do

    export NUM_CHILD_RESOURCES
    echo "=== stack size: 100 base + $NUM_CHILD_RESOURCES children ==="

    for NUM_DEPENDENCIES in {0..20};
    do
        export NUM_DEPENDENCIES
        preview
    done

done
