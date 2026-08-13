package main

import (
	"fmt"
	"strings"
)

type Vertex struct {
	x int
	y int
}

func main() {
	// pointers
	i, j := 43, 234
	p := &i         // point to i
	fmt.Println(*p) // read i through the pointer
	*p = 21         // set i through the pointer
	fmt.Println(i)  // see the new value of i

	p = &j         // point to j
	*p = *p / 37   // divide j through the pointer
	fmt.Println(j) // see the new value of j

	// struct
	V := Vertex{10, 20}
	fmt.Println(V.x)
	fmt.Println(V.y)

	// array - static typed
	var a [2]string
	// size is the part of array type
	a[0] = "hello"
	a[1] = "world"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	primes := [6]int{2, 3, 5, 7, 11, 13}
	fmt.Println(primes)

	// slice are reference types, dont have actual values
	var s []int = primes[1:4]
	fmt.Println(s)

	names := [4]string{
		"qwe",
		"asd",
		"zxc",
		"rty",
	}
	fmt.Println(names)
	a1 := names[0:2]
	b1 := names[1:3]
	fmt.Println(a1, b1)

	b1[0] = "xxx"
	fmt.Println(a1, b1)
	fmt.Println(names)

	q := []int{1, 2, 3, 4, 5, 6, 7, 8, 9}
	fmt.Println(q)

	s2 := []struct {
		i int
		b bool
	}{
		{2, true},
		{4, false},
		{6, true},
		{8, false},
		{1, true},
	}
	fmt.Println(s2)

	a2:=make([]int, 5)
	printSlice("a2",a2)

	b2:=make([]int, 0,5)
	printSlice("b2", b2) 
	
	c2:=b2[:2]
	printSlice("c2",c2)

	d2:=c2[2:5]
	printSlice("d2",d2)

	board:=[][]string{
		[]string{"_","_","_"},
		[]string{"_","_","_"},
		[]string{"_","_","_"},
	}
	board[0][0]="x"
	board[2][2]="0"
	board[1][2]="x"
	board[1][0]="0"
	board[0][2]="x"
	for i:=0;i<len(board);i++{
		fmt.Printf("%s\n", strings.Join(board[i]," "))
	}

	var s3[]int
	printSlice2(s3)

	// append works on nil slices
	s3 = append(s3, 0)
	printSlice2(s3)

	// the slice grows as needed
	s3=append(s3, 1)
	printSlice2(s3)

	// we can add more than 1 element at a time
	s3=append(s3, 2, 3, 4)
	printSlice2(s3)
	
}
 
func printSlice(s2 string, x []int){
	fmt.Printf("%s len=%d cap=%d %v\n",s2, len(x),cap(x),x)
}
func printSlice2(x []int){
	fmt.Printf("len=%d cap=%d %v\n", len(x),cap(x),x)
}