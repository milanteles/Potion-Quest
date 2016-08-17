EXENAME  = jsonToBin.exe
JSONLIB  = cJSON/libcjson.a

CFLAGS   = -IcJSON -ggdb -std=c11

SRCFILES = $(shell find . -maxdepth 1 -type f -name '*.c')
OBJFILES = $(patsubst %.c,%.o,$(SRCFILES))

all: $(EXENAME) 

%.o: %.c
	cc -c $(CFLAGS) -o $@ $<

$(EXENAME): $(OBJFILES) $(JSONLIB)
	cc -o $(EXENAME) $(OBJFILES) $(JSONLIB) -lm

$(JSONLIB):
	make -C cJSON install

clean:
	rm -f ./*.o
	rm -f $(EXENAME)
	make -C cJSON clean