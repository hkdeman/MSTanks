#!/bin/bash

for i in `seq 1 10`;
do
	cp -r Server/ servers/Server$i
done

