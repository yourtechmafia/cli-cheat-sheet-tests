echo first > spaced.txt
echo first> tight.txt
for %%f in (spaced.txt tight.txt) do echo %%f: %%~zf bytes
