#!/bin/sh

FILENAME="simulation_output"

python simulation.py > "$FILENAME"

function phase_output() {
  fail=`cat $FILENAME | grep $1 | grep fail | wc -l | xargs`
  success=`cat $FILENAME | grep $1 | grep got | wc -l | xargs`
  echo "$1, fail=$fail, success=$success"
}

for phase in warmup steady spike choke; do
  phase_output $phase
done
