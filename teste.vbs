Function test(a as integer, c as integer) as integer
    print a

    Dim b as integer
    b = a * 5

    if b < c then
        test = b
    else
        test = a
    end if

End Function

Sub main()
    ' hello world
    Dim top as integer
    top = input
    print test(top, 100)
End Sub