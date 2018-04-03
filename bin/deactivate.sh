#!/bin/bash
slave=$1
ssh ubuntu@$slave "cd $SPARK_HOME/sbin; ./stop-slave.sh"
