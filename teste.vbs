Sub Main()
dim fizz as integer
dim buzz as integer
dim fizzbuzz as integer
dim n as integer
dim tres as integer
dim cinco as integer

n = INPUT
Fizz = 7155
Buzz = 8055
FizzBuzz = 71558055

tres = (n - (n / 3 * 3))
cinco = (n - (n / 5 * 5))

if tres = 0 then
    if cinco = 0 then
        print FizzBuzz
    else
        print Fizz
    end if

else
    if tres = 0 then
        print Fizz
    else
        if cinco = 0 then
            print Buzz
        else
            print n
        end if
    end if
end if

end sub