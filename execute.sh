#!/bin/bash

rm -rf logs

echo "=== child resources, dependencies, parent state, preview duration ==="

preview(){
    export LOGDIR=logs/${NUM_CHILD_RESOURCES}-${DO_PARENT}
    mkdir -p $LOGDIR
    echo -n "$NUM_CHILD_RESOURCES, $NUM_DEPENDENCIES, $DO_PARENT, "
    /bin/time --format="%e seconds" pulumi preview > ${LOGDIR}/${NUM_DEPENDENCIES}-deps.log

}

export DO_PARENT=false

echo "=== 0 child resources ==="
export NUM_CHILD_RESOURCES=0
export NUM_DEPENDENCIES=0
preview

for NUM_CHILD_RESOURCES in {100..1000..100};
do

    export NUM_CHILD_RESOURCES

    echo "=== ${NUM_CHILD_RESOURCES} child resources ==="

    for NUM_DEPENDENCIES in {0..1};
    do
        export NUM_DEPENDENCIES
        preview
    done

    for NUM_DEPENDENCIES in {10..20..10};
    do
        export NUM_DEPENDENCIES
        preview
    done

    for NUM_DEPENDENCIES in {50..100..50};
    do
        export NUM_DEPENDENCIES
        preview
    done

done
