package main

import (
	"fmt"
	"maps"
)

// map => hash, object, dict
func main(){
	// create map
	m := make(map[string]string)

	// setting an element
	m["name"]="prateek"
	m["area"]="backend"

	// get an element
	fmt.Println(m["name"],m["area"])
	fmt.Println(m["phone"]) // if key value doesnot exists in map then it returns 0 value

	m1:=make(map[string]int)
	m1["phone"] = 9606861693
	m1["price"] = 960
	fmt.Println(m1["phone"])
	fmt.Println(m1["age"]) // 0
	fmt.Println(len(m1))
	fmt.Println(m1) //map[phone:9606861693 price:960]
	
	delete(m1, "price")
	fmt.Println(m1) // map[phone:9606861693]

	// to delete a map
	clear(m)
	fmt.Println(m) //map[]

	m2:=map[string]int{"price":40, "phones":3}
	fmt.Println(m2)
	
	v, ok := m2["price"]
	fmt.Println(v) // 40
	if ok {
		fmt.Println("all ok")
	} else {
		fmt.Println("not ok")
	}

	m3 :=map[string]int{"price":40, "phones":30}
	m4 :=map[string]int{"price":40, "phones":30}
	fmt.Println(maps.Equal(m3,m4))
} 