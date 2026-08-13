//  need to learn slices in depth

package main

import (
	"fmt"
	"slices"
)

// most used construct in go
// + useful methods

func main() {
	// uninitialize slice is nil
	var nums []int
	fmt.Print(nums == nil)
	fmt.Println(len(nums))

	// can declare minimum number of values
	var numbers = make([]int, 2)
	fmt.Println(numbers==nil) //in slices the values cannot be nil
	fmt.Println(numbers)
	fmt.Println(cap(numbers))

	var num1 = make([]int,2,5)
	// var var_name = make([]int, minimum, maximum_known_size(this automatically resizes as per values))
	// slice adds values dynamically
	num1 = append(num1, 1) // [0 0 1]
	num1 = append(num1, 2) // [0 0 1 2]
	num1 = append(num1, 3) // [0 0 1 2 3]
	num1 = append(num1, 4) // [0 0 1 2 3 4]
	num1 = append(num1, 6) // [0 0 1 2 3 4 6]
	num1 = append(num1, 7) // [0 0 1 2 3 4 6 7]
	num1 = append(num1, 8) // [0 0 1 2 3 4 6 7 8]
	num1 = append(num1, 9) // [0 0 1 2 3 4 6 7 8 9]
	num1 = append(num1, 10) // [0 0 1 2 3 4 6 7 8 9 10]
	num1 = append(num1, 11) // [0 0 1 2 3 4 6 7 8 9 10 11]
	num1 = append(num1, 12) // [0 0 1 2 3 4 6 7 8 9 10 11 12]
	fmt.Println(num1)
	fmt.Println(cap(num1)) // 5 -> 10 -> 20 this when moves abote the initial value it scales up by itself

	var num2 = make([]int, 0, 5) // initally takes as 0 to keep the values
	num2 = append(num2, 1)
	num2 = append(num2, 2)
	num2 = append(num2, 3)
	num2[0] = 10
	fmt.Println(num2) // [10 2 3]
	fmt.Println(len(num2))
	fmt.Println(cap(num2))

	// shorthand to create slice
	num3:=[]int{}
	fmt.Println(num3)
	fmt.Println(cap(num3))
	fmt.Println(len(num3))

	var num4 = make([]int, 0, 5)
	num4 = append(num4, 2)
	num2 = make([]int, len(num4))
	num4 = append(num2, 2)
	// copy function
	copy (num2, num4)
	fmt.Println(num4, num2)

	// slice operator
	var num5 = []int{1,2,3}
	fmt.Println(num5[0:2]) // [1 2]
	fmt.Println(num5[2:3]) // [3]
	fmt.Println(num5[:3]) // [1 2 3]
	fmt.Println(num5[:]) // [1 2 3]
	fmt.Println(num5[2:]) // [3]

	// slice package
	var num6 = []int{1,2,3}
	var num7 = []int{1,2,3}
	var num8 = []int{1,2,4}
	fmt.Println(slices.Equal(num6, num7)) // true
	fmt.Println(slices.Equal(num7, num8)) // false
	fmt.Println(slices.Equal(num7, num7)) // true

	// 2d slices
	var num9 = [][]int{{1,2,3},{1,2,3}}
	fmt.Println(num9)
}