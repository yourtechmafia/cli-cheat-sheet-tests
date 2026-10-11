GREETING="hello"
bash -c 'echo "child sees: [$GREETING]"'
export GREETING
bash -c 'echo "child sees: [$GREETING]"'
