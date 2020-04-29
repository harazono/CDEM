DEPENDS  := .depend.mk
#CXXFLAGS := -g -Wall -O0 -DNDEBUG -std=c++11 -fopenmp -lgomp -I /home/harazono/R10-3BaseCallEval/CDEM/htslib/
CXXFLAGS := -g -Wall -O0 -std=c++11 -fopenmp -lgomp -include $(DEPENDS) -I /home/harazono/R10-3BaseCallEval/CDEM/htslib
GTESTFLAGS := -lgtest -lpthread
SOURCES := cdem.cpp
CXX := $(HOME)/local/bin/g++

.PHONY: depend clean test build_test

all: CDEM

CDEM: cdem.o
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	-rm *.o

