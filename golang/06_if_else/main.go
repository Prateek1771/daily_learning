package main

import "fmt"

func main() {
	age := 18

	if age>18 {
		fmt.Println("adult")
	} else if age == 18 {
		fmt.Println("adult-18")
	} else {
		fmt.Println("not adult")
	}

	var role = "user"
	var hasPermission = true

	if role == "admin" || hasPermission {
		fmt.Println("yes")
	}

	if role == "admin" && hasPermission {
		fmt.Println("yes")
	} else {
		fmt.Println("no")
	}

	// can declare values inside if else
	if age:=16; age>=18{
		fmt.Println("adult",age)
	} else if age>=16{
		fmt.Println("age is:", age)
	} else {
		fmt.Println("child")
	}

	// go does not has ternary operator, u willl have to use if else

}