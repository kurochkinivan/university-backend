package main

import (
	"html/template"
	"log"
	"net"
	"net/http"

	"github.com/kurochkinivan/backend-2/storage"
)

const (
	host = "0.0.0.0"
	port = "8080"
)

var (
	st           = storage.NewLocalStorage()
	productsTMPL = template.Must(template.ParseFiles("templates/index.html"))
	cartTMPL     = template.Must(template.ParseFiles("templates/cart.html"))
)

func main() {
	http.HandleFunc("GET /", homePage)
	http.HandleFunc("GET /cart", cartPage)

	err := http.ListenAndServe(net.JoinHostPort(host, port), nil)
	if err != nil {
		log.Fatal(err)
	}
}

func homePage(w http.ResponseWriter, r *http.Request) {
	err := productsTMPL.Execute(w, st)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func cartPage(w http.ResponseWriter, r *http.Request) {
	err := cartTMPL.Execute(w, st)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
