package handlers

import "github.com/gofiber/fiber/v3"

type TransactionsHandlers struct{}

func NewTransactionsHandlers() *TransactionsHandlers {
	return &TransactionsHandlers{}
}

func (t *TransactionsHandlers) GetAll(c fiber.Ctx) error {

	return nil
}
