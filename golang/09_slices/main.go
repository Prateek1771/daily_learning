package main

import "fmt"

// most used construct in go
// + useful methods

func main() {
	// uninitialize slice is nil
	var nums []int
	fmt.Print(nums == nil)
	fmt.Println(len(nums))
}