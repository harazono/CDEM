CXXFLAGS := -Wall -O0  -I htslib
CXX := $(HOME)/local/bin/g++
CC := $(HOME)/local/bin/gcc
.PHONY: depend clean test biuld_test
SRCS := cdem.cpp
$(foreach SRC,$(SRCS),$(eval $(subst \,,$(shell $(CXX) -MM $(SRC)))))


all: CDEM

CDEM: cdem.cpp htslib/hts.o htslib/sam.o htslib/hfile.o
	$(CXX) $(CXXFLAGS) -o $@


clean:
	-rm *.o

