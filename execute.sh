#!/bin/bash

# rm -rf logs

echo "stack size, dependencies per child, preview duration"

preview(){
    export LOGDIR=logs/${STACK_SIZE}-${DO_PARENT}
    mkdir -p $LOGDIR
    echo -n "$STACK_SIZE, $NUM_DEPENDENCIES, "
    /bin/time --format="%e" pulumi preview > ${LOGDIR}/${NUM_DEPENDENCIES}-deps.log

}

# export DO_PARENT=false

# for STACK_SIZE in {500..3000..500};
# do
#     export STACK_SIZE
#     for NUM_DEPENDENCIES in {0..3000..500};
#     do
#         export NUM_DEPENDENCIES
#         preview
#     done
# done

export DO_PARENT=true

for STACK_SIZE in {500..3000..500};
do
    export STACK_SIZE
    for NUM_DEPENDENCIES in {0..3000..500};
    do
        export NUM_DEPENDENCIES
        preview
    done
done
