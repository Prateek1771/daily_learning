package main

import (
	"fmt" // contains everything related to strings
	"math"
	"math/rand"
) 

func add(x int, y int) int {
	return (x+y)
}

// can return multiple values but need to declare the type
func swap(x string, y string) (string, string) {
	return y, x
}

// try to ignore writing this format, heard to read and if large function hard to debug values
func split(sum int)(x,y int){
	x=sum *4/9
	y=sum-x
	return
}

var greet string
var c, python, java bool
var react, next int

func main() {
	fmt.Println("hello") // hello
	fmt.Println("Printing", rand.Intn(10)) // Printing 8
	fmt.Println("Pi", math.Pi) // Pi 3.141592653589793
	fmt.Println(add(10,20)) // 30
	fmt.Println(swap("10","20")) // 20 10
	fmt.Println(split(67)) // 29 38
	fmt.Println(greet) // nothing
	fmt.Println(c, python, java) // false false false
	fmt.Println(react, next) // 0 0

	i:=10 // only acceable inside a function
	fmt.Println(i) // 10
}