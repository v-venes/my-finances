package internal

import (
	"github.com/gofiber/fiber/v3"
	"github.com/v-venes/my-finances/finances-api/internal/handlers"
)

type Server struct {
	instance *fiber.App
}

func NewServer() *Server {
	return &Server{
		instance: fiber.New(),
	}
}

func (s *Server) Setup() {
	s.setupRoutes()
}

func (s *Server) Run() {
	s.instance.Listen(":3000")
}

func (s *Server) setupRoutes() {
	transactionsRoutes := s.instance.Group("/transactions")
	transactionsHandlers := handlers.NewTransactionsHandlers()

	transactionsRoutes.Get("/", transactionsHandlers.GetAll)
}
