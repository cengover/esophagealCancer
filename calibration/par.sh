#!/bin/sh
for j in 16 32 64 128
do
echo 'START '$j >> time.out
for i in `seq 1 3`
do
	start=`date +%s%N`
	python -m scoop --hosts=localhost -n $j optimization.py
	end=`date +%s%N`
	runtime=$((end-start))
	echo $(($runtime/1000000)) >> time.out
done
done
