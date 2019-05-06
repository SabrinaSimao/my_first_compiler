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

'a = 0
'b = 10
'while a < b
'while a < 3
'print Fizz
'a = a + 1
'wend
'a = a + 1
'print Buzz
'wend