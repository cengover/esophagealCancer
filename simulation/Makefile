# Compiler flags
ADEVS=/home/ozi/adevs-code
ABM=${PWD}
CFLAGS = -O3 -Wall -I${ADEVS}/include -I${ABM}
LIBS = \
	-lgsl \
	-lblas

# Best bet for GNU compiler
CXX = g++
OBJS = \
	   common.o \
	   TissueVolume.o \
		main.o

.SUFFIXES: .cpp
.cpp.o:
	${CXX} ${CFLAGS} ${OPTFLAG} -o $@ -c $<

objs: ${OBJS}
	${CXX} ${CFLAGS} ${OBJS} ${LIBS}

test: common.o
	${CXX} ${CFLAGS} test_common.cpp common.o ${LIBS}
	./a.out

clean:
	rm -f *.o a.out *csv*
