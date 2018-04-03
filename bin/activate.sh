#!/bin/bash
slave=$1
ssh ubuntu@$slave "cd $SPARK_HOME/sbin; ./start-slave.sh spark://43.240.97.180:7077"
