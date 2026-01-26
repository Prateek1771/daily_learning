package main

import "fmt"

// constants can be declared outside the function
const age = 23

func main() {
	const age1 = 24

	// can declare multiple constants by grouping them:
	const (
		port = 5000
		host = "localhost"
	)

	fmt.Println(age)
	fmt.Println(age1)
	fmt.Println(port, host)
}