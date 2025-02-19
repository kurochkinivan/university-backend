package entity

type User struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Phone    string `json:"phone"`
	Birthday string `json:"birthday"`
	Email    string `json:"email"`
	Username string `json:"username"`
}