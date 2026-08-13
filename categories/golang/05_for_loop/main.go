package main

import "fmt"

func main() {
	// while loop
	i := 1

	for i <= 3 {
		fmt.Println(i)
		i = i+1
	}

	// for {
		//this is an infinite loop
	// }

	// classic for loop
	for i:=0; i<=3; i++ {
		// break --used to break
		if i == 2 {
			continue
		}
		fmt.Println(i)
	}

	// range
	for i:= range 11 {
		fmt.Print(i)
	}

}