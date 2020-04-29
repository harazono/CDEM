CXXFLAGS := -Wall -O0  -I htslib
CXX := $(HOME)/local/bin/g++
CC := $(HOME)/local/bin/gcc
#LDFLAGS := htslib
.PHONY: depend clean test biuld_test
SRCS := cdem.cpp

all: CDEM
CDEM: cdem.cpp htslib/hts.o htslib/sam.o htslib/hfile.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $^ $@


clean:
	-rm *.o

$(foreach SRC,$(SRCS),$(eval $(subst \,,$(shell $(CXX) -MM $(SRC)))))
