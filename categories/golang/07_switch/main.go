package main

import (
	"fmt"
	"time"
)

func main() {
	// simple switch used when there are multiple cases to switch

	i:=10

	switch i {
	case 1: fmt.Println(1)
	case 2: fmt.Println(2) 
	case 3: fmt.Println(3) 
	case 4: fmt.Println(4) 
	case 5: fmt.Println(5) 
	// default: fmt.Println("other") // if not given default case it will work print nothing
	}
	
	// multiple condition switch
	switch time.Now().Weekday(){
	case time.Saturday, time.Sunday:
		fmt.Println("its weekend")
	default:
		fmt.Println("workday")
	}

	// type switch
	WhoAmI := func(i interface{}){
		switch t := i.(type) {
		case int: fmt.Println("int")
		case string: fmt.Println("str")
		case bool: fmt.Println("bool")
		default: fmt.Println("other", t)
	}
	}

	WhoAmI("hello")
	WhoAmI(10)
	WhoAmI(true)
}
