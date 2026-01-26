package main

import "fmt"

// numbered sequence of specific length and of same type
func main(){
	// it keeps all the initial values as 0
	var nums [4]int
	nums[0] = 10
	fmt.Println(len(nums))
	fmt.Println(nums[0])
	fmt.Println(nums)

	// keeps default values as false
	var vals [4]bool
	vals[1] = true
	fmt.Println(vals)

	// empty values will be printed
	var name [4]string
	name[0] = "prateek"
	fmt.Println(name) // [prateek   ]

	// to declare it in single line
	num := [3]int{10, 20, 40}
	fmt.Println(num)

	// 2d arrays
	num1:=[2][2]int{{1,2},{3,4}}
	fmt.Println(num1)


	// - fixed size, that is predictable
	// - memory optimization
	// - constant time access
}