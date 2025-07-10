package main

import "github.com/v-venes/my-finances/finances-api/internal"

func main() {
	server := internal.NewServer()

	server.Setup()

	server.Run()
}
