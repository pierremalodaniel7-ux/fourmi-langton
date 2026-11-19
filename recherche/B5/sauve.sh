#!/bin/bash
# sauve.sh : archive les sous-arbres terminés (data/B5/jobs/*.res) dans recherche/B5/jobs.tar.gz (versionné)
D=$(cd $(dirname $0); pwd); J=$D/../../data/B5/jobs
(cd $J && ls *.res | tar -czf $D/jobs.tar.gz -T -); echo "$(tar -tzf $D/jobs.tar.gz | wc -l) sous-arbres sauvegardés"
