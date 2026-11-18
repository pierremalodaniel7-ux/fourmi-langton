# make : compile tout ; make test : oracle (résultats connus, < 1 s)
SRC := $(wildcard *.c)
BIN := $(SRC:.c=)
CFLAGS := -O2 -w

all: $(BIN)
%: %.c ant.h
	gcc $(CFLAGS) -o $@ $< -lm

test: all
	@./bestiaire2 RL 3000000 0 0 0 | grep -q '"periode":104,"deplacement":\[-2,2\],"debut":9977' && echo "OK  RL seule : autoroute 104 dès 9 977" || echo "ÉCHEC RL seule"
	@./cyc 1000000 "0,0,H;40,0,G" | grep -q "periode 42716.*OUI" && echo "OK  R-08 : cycle 42 716" || echo "ÉCHEC R-08"
	@./cyc 1000 "0,0,H;-1,0,B" | grep -q "periode 16 .*OUI" && echo "OK  cycle 16" || echo "ÉCHEC cycle 16"
	@./tipmin 60 | grep -q "minimum = 11 cases" && echo "OK  R-20 : bout minimal 11" || echo "ÉCHEC R-20"
	@grep -v '^#' oracle.txt | while IFS= read -r l; do sit="$${l%% => *}"; att="$${l##* => }"; got=$$(./fourmi -T 4000000 "$$sit" | cut -d'|' -f4-5); [ "$$got" = "$$att" ] && echo "OK  fourmi $$sit -> $$got" || echo "ÉCHEC fourmi $$sit : $$got au lieu de $$att"; done
	@./fourmi -cert "RL|0,0,H|" | grep -q "CERT 9977 " && echo "OK  certificat : départ blanc DÉMONTRÉ dès 9 977" || echo "ÉCHEC certificat"
	@test "$$(./auto2 3000000 2>/dev/null | wc -l)" = 22 && echo "OK  R-16 : 22 collisions" || echo "ÉCHEC R-16"

clean:
	rm -f $(BIN)
.PHONY: all test clean
