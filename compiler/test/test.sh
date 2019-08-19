EXPECTED="$(ls $1|grep expected)"
for expected in $EXPECTED
do
    actual="${expected/expected/actual}"
    cmd="./TextComparer.sh ${1}/$actual ${1}/$expected"
    echo $cmd
    eval $cmd
done
