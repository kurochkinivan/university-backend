package local

type Repositories struct {
	UserRepository *UserRepository
}

func NewRepositories(storage *LocalStorage) *Repositories {
	userRepository := NewUserRepository(storage)
	return &Repositories{
		UserRepository: userRepository,
	}
}
