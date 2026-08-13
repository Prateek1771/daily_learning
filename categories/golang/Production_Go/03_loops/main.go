package main

import (
	"fmt"
	"time"
)

func main() {

	// for loop
	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}

	fmt.Println("hello", sum)

	// while loop
	sum1 := 1
	for sum1 < 1000 {
		sum1 += sum1
	}
	fmt.Println(sum1)

	// infinite loop
	sum2 := 10
	for {
		if sum2 > 100 {
			break
		}
		sum2 += sum2
	}
	fmt.Println(sum2)

	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("good morning")
	case t.Hour() < 17:
		fmt.Println("good afternoon")
	case t.Hour() < 21:
		fmt.Println("evening")
	default:
		fmt.Println("night")
	}

	defer fmt.Println("world")
	fmt.Println("hello") // prints Hello world
	// defer calculates the values and stores in a stack where its shows the results after the executions of the main function

	fmt.Println("counting:")
	for i:=0;i<10;i++{
		defer fmt.Println(i)
	}
	fmt.Println("done")
}
