package local

import (
	"sync"

	"github.com/kurochkinivan/university-backend-1/internal/entity"
)

type LocalStorage struct {
	users  *sync.Map
	lastID int
}

func NewLocalStorage() *LocalStorage {
	m := &sync.Map{}
	m.Store(1, &entity.User{ID: 1, Name: "Ashley W. Walker", Phone: "317-769-0638", Birthday: "August 12, 1999", Email: "AshleyWWalker@dayrep.com", Username: "Joull1999"})
	m.Store(2, &entity.User{ID: 2, Name: "Martin M. Johnson", Phone: "301-962-1329", Birthday: "March 20, 1964", Email: "MartinMJohnson@teleworm.us", Username: "Youde1964"})
	m.Store(3, &entity.User{ID: 3, Name: "Justina D. Wallace", Phone: "914-819-0493", Birthday: "May 18, 1994", Email: "JustinaDWallace@rhyta.com", Username: "Donfe1994"})
	m.Store(4, &entity.User{ID: 4, Name: "Jason R. King", Phone: "608-562-1533", Birthday: "February 18, 1962", Email: "JasonRKing@dayrep.com", Username: "Ginusbact"})
	m.Store(5, &entity.User{ID: 5, Name: "Leroy T. Evans", Phone: "337-570-9574", Birthday: "January 7, 1946", Email: "LeroyTEvans@armyspy.com", Username: "Atiousaing"})

	return &LocalStorage{
		users:  m,
		lastID: 5,
	}
}
