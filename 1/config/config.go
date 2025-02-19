package config

import (
	"log"
	"os"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	HTTP struct {
		Host string `yaml:"host"`
		Port string `yaml:"port"`
	} `yaml:"http"`
}

func MustLoad() *Config {
	path := "../config/config.yaml"

	if _, err := os.Stat(path); os.IsNotExist(err) {
		log.Fatal(path, " does not exist")
	}

	cfg := &Config{}
	err := cleanenv.ReadConfig(path, cfg)
	if err != nil {
		log.Fatal("failed to read config, err: ", err)
	}

	return cfg
}
