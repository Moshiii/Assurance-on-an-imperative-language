havoc m,n;
assume n>0;
p := 0;
x := 0;
while x < n
inv x<= n and p = x*m
do
{x := x + 1;p := p + m};
assert p = n*m




