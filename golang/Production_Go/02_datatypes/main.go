package main

import (
	"fmt"
	"math"
	"math/cmplx"
)

var (
	ToBe   bool       = false
	MaxInt uint       = 1<<64-1
	z      complex128 = cmplx.Sqrt(-5 + 12i)
)

func main() {
	fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe) //Type: bool Value: false
	fmt.Printf("Type: %T Value: %v\n", MaxInt, MaxInt) //Type: uint Value: 18446744073709551615
	fmt.Printf("Type: %T Value: %v\n", z, z) //Type: complex128 Value: (2+3i)

	var i int
	var f float32
	var b bool
	var s string
	fmt.Printf("%v %v %v %v\n", i, f, b, s)

	var x, y int = 3, 5
	var f1 float64 = math.Sqrt(float64(x*x+y*y))
	var z uint = uint(f1)
	fmt.Println(x, y, z)

	v := 45
	fmt.Printf("v is of type %T\n", v)

	
}