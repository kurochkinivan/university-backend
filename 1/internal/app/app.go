package app

import (
	"log"
	"net"
	"net/http"

	"github.com/kurochkinivan/university-backend-1/config"
	v1 "github.com/kurochkinivan/university-backend-1/internal/controller/http/v1"
	"github.com/kurochkinivan/university-backend-1/internal/usecase"
	"github.com/kurochkinivan/university-backend-1/internal/usecase/repository/local"
)

type App struct {
	cfg *config.Config
}

func NewApp(cfg *config.Config) *App {
	return &App{
		cfg: cfg,
	}
}

func (a *App) Start() error {
	storage := local.NewLocalStorage()
	repos := local.NewRepositories(storage)
	usecases := usecase.NewUseCases(repos)

	log.Println("creating router...")
	r := v1.NewRouter(usecases)

	log.Println("starting server...")
	addr := net.JoinHostPort(a.cfg.HTTP.Host, a.cfg.HTTP.Port)
	err := http.ListenAndServe(addr, r)
	if err != nil {
		log.Fatal(err)
	}

	return nil
}
