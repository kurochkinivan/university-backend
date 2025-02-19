package v1

import (
	"net/http"

	"github.com/julienschmidt/httprouter"
	"github.com/kurochkinivan/university-backend-1/internal/usecase"
)

type Handler interface {
	Register(r *httprouter.Router)
}

func NewRouter(useCases *usecase.UseCases) http.Handler {
	r := httprouter.New()

	userHandler := NewUserHandler(useCases.UserUseCase)
	userHandler.Register(r)

	return r
}
