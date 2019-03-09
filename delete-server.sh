#!/bin/bash
cd servers/
for i in `seq 1 10`;
do
        rm -r Server$i
done
cd ..
