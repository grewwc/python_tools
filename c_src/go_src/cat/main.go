package main

import (
	"errW"
	"fmt"
	"io"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stdout, `cat "filename"`)
		return
	}

	fname := os.Args[1]
	f, err := os.Open(fname)
	errW.Fatalln(err)
	io.Copy(os.Stdout, f)
}
