package main

import "fmt"

func main() {
	// if there any variables declared and not used it throws error, we need to use variables which are declared
	var name string = "prateek"
	var name1 = "prateek1"
	var isAdult = true // this is used to declare bool
	var age int = 23

	// short hand 
	name2 := "prateek2"

	// this method is uned when declared first and used later
	var name3 string

	name3 = "prateek3"

	fmt.Println(name)
	fmt.Println(name1)
	fmt.Println(isAdult)
	fmt.Println(age)
	fmt.Println(name2)
	fmt.Println(name3)
}