EXPECTED="$(ls|grep expected)"
for expected in $EXPECTED
do
    actual="${expected/expected/actual}"
    cmd="./TextComparer.sh $actual $expected"
    echo $cmd
    eval $cmd
done
