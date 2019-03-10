#!/bin/bash

for i in `seq 1 5`;
do
	./servers/Server$i/Server.x86_64 &
done
