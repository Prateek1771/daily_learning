package main

import "fmt"

// range is used for iterating over data structures
func main(){
	nums :=[]int {6,7,8}

	for i:=0;i<len(nums);i++{
		fmt.Println(i, nums[i])
	}

	sum:=0

	for _, num :=range nums {
		sum = sum + num
		fmt.Println(num)
	}

	fmt.Println(sum)

}