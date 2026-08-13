package main

import "fmt"

type Vertex struct {
	Lat, Long float64
}

var m map[string]Vertex

func main() {
	// we use maps/hash maps to look for things as it has the complexity of o(1)
	m = make(map[string]Vertex)
	// make is used to initialize the values
	m["hello world"] = Vertex{
		40.2122, -74.32342,
	}
	fmt.Println(m["hello world"])
}