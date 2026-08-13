package main

import (
	"fmt"
	"math"
)

type Vertex struct{
	X, Y float64
}

// func <receiver> <name_func>() <type>{}
// its a value receiver
func (v Vertex) Abs() float64{
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

// its a pointer receiver
func (v*Vertex)Scale(f float64){
	v.X=v.X*f
	v.Y=v.Y*f
}

func main() {
	// here v is declared not used in above code
	v:=Vertex{3,4}
	v.Scale(10)
	fmt.Println(v.Abs())
}