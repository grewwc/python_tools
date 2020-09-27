package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:8000")
	if err != nil {
		fmt.Println(err)
	}
	for {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("text to send: ")
		input, err := reader.ReadString('\n')
		if err != nil {
			continue
		}

		tosend := input + "\n\n"
		fmt.Println("to send", tosend)
		fmt.Fprintf(conn, tosend)

		// listen for reply
		reader = bufio.NewReader(conn)
		received, err := reader.ReadString('\n')

		if err != nil {
			fmt.Println("err receiving", err)
			continue
		}

		fmt.Printf("received: %q\n", received)
	}
}
