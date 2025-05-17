package usecase

import (
	"context"
	"errors"
	"fmt"

	"github.com/kurochkinivan/university-backend-1/internal/entity"
	"github.com/kurochkinivan/university-backend-1/internal/usecase/repository"
)

type UserRepository interface {
	GetAll(ctx context.Context) ([]*entity.User, error)
	Create(ctx context.Context, user *entity.User) (*entity.User, error)
	Delete(ctx context.Context, userID int) error
	Update(ctx context.Context, userID int, user *entity.User) (*entity.User, error)
	Patch(ctx context.Context, userID int, user *entity.User) (*entity.User, error)
}

type UserUseCase struct {
	repo UserRepository
}

func NewUserUseCase(u UserRepository) *UserUseCase {
	return &UserUseCase{
		repo: u,
	}
}

func (u *UserUseCase) GetAll(ctx context.Context) ([]*entity.User, error) {
	users, err := u.repo.GetAll(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get users, err: %w", err)
	}

	return users, nil
}

func (u *UserUseCase) Create(ctx context.Context, user *entity.User) (*entity.User, error) {
	user, err := u.repo.Create(ctx, user)
	if err != nil {
		return nil, fmt.Errorf("failed to create user: %w", err)
	}

	return user, nil
}

func (u *UserUseCase) Delete(ctx context.Context, userID int) error {
	err := u.repo.Delete(ctx, userID)
	if err != nil {
		return fmt.Errorf("failed to delete user: %w", err)
	}

	return nil
}

func (u *UserUseCase) Update(ctx context.Context, userID int, user *entity.User) (*entity.User, error) {
	user, err := u.repo.Update(ctx, userID, user)
	if err == nil {
		return user, nil
	}

	if errors.Is(err, repository.ErrNotFound) {
		user, err := u.repo.Create(ctx, user)
		if err != nil {
			return nil, fmt.Errorf("failed to create user, err: %w", err)
		}
		return user, nil
	}

	return nil, fmt.Errorf("failed to update user: %w", err)
}

func (u UserUseCase) Patch(ctx context.Context, userID int, user *entity.User) (*entity.User, error) {
	user, err := u.repo.Patch(ctx, userID, user)
	if err != nil {
		return nil, fmt.Errorf("failed to patch user, err: %v", err)
	}
	
	return user, nil
}