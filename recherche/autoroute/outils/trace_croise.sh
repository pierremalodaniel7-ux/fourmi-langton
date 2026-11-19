#!/bin/bash
# trace_croise.sh P A0 A1 B0 B1 ROT : a,b, direction finale, pas certifié (ou NONCERT)
D=$(dirname $0); L=$(mktemp); C=$(mktemp)
python3 $D/trace_croise.py "$@" 2>$L >$C
$D/../../../src/fourmi -T 8000000 -cert -lot < $C \
 | sed -E 's/^.*CERT ([0-9]+) .*104,(-?[0-9]+),(-?[0-9]+),.*fin (.*)$/(\2,\3) \1 fin \4/; t; s/^RL[^|]*\|[^|]*\|/NONCERT /' | paste $L - ; rm $L $C
