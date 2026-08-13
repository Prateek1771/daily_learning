package main1

import "fmt"

type Vertex1 struct {
	x int // capatilize all these 
	y int
}

func main1() {
	v := Vertex1{1, 2}
	p := &v
	p.x = 1e9
	fmt.Println(v)
}