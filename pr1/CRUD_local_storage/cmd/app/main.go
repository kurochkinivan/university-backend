package main

import (
	"log"

	"github.com/kurochkinivan/university-backend-1/internal/app"
	"github.com/kurochkinivan/university-backend-1/config"
)

func main() {
	log.Println("reading config...")
	cfg := config.MustLoad()

	log.Println("creating app...")
	a := app.NewApp(cfg)
	a.Start()
}
