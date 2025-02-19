package usecase

import "github.com/kurochkinivan/university-backend-1/internal/usecase/repository/local"

type UseCases struct {
	UserUseCase *UserUseCase
}

func NewUseCases(repos *local.Repositories) *UseCases {
	userUseCase := NewUserUseCase(repos.UserRepository)
	return &UseCases{
		UserUseCase: userUseCase,
	}
}
