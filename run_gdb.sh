#!/bin/bash
gdb -q -ex "run" -ex "bt" -ex "quit" ./a.out &
GDB_PID=$!
sleep 1
kill -INT $GDB_PID
wait $GDB_PID
