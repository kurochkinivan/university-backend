package local

import (
	"context"
	"errors"
	"sort"

	"github.com/kurochkinivan/university-backend-1/internal/entity"
	"github.com/kurochkinivan/university-backend-1/internal/usecase/repository"
)

type UserRepository struct {
	storage *LocalStorage
}

func NewUserRepository(storage *LocalStorage) *UserRepository {
	return &UserRepository{
		storage: storage,
	}
}

func (r *UserRepository) Exists(ctx context.Context, userID int) bool {
	if _, ok := r.storage.users[userID]; !ok {
		return false
	}
	return true
}

func (r *UserRepository) GetAll(ctx context.Context) ([]*entity.User, error) {
	var users []*entity.User
	for _, u := range r.storage.users {
		users = append(users, u)
	}

	sort.Slice(users, func(i, j int) bool {
		return users[i].ID < users[j].ID
	})

	return users, nil
}

func (r *UserRepository) Create(ctx context.Context, user *entity.User) (*entity.User, error) {
	r.storage.lastID++
	user.ID = r.storage.lastID
	r.storage.users[user.ID] = user
	return user, nil
}

func (r *UserRepository) Delete(ctx context.Context, userID int) error {
	if _, ok := r.storage.users[userID]; !ok {
		return errors.New("user with provided ID was no found")
	}

	delete(r.storage.users, userID)
	return nil
}

func (r *UserRepository) Update(ctx context.Context, userID int, user *entity.User) (*entity.User, error) {
	if _, ok := r.storage.users[userID]; !ok {
		return nil, repository.ErrNotFound
	}

	user.ID = userID
	r.storage.users[userID] = user

	return r.storage.users[userID], nil
}

func (r *UserRepository) Patch(ctx context.Context, userID int, user *entity.User) (*entity.User, error) {
	exists := r.Exists(ctx, userID)
	if !exists {
		return nil, repository.ErrNotFound
	}

	curUser := r.storage.users[userID]
	if user.Name != "" {
		curUser.Name = user.Name
	}
	if user.Phone != "" {
		curUser.Phone = user.Phone
	}
	if user.Birthday != "" {
		curUser.Birthday = user.Birthday
	}
	if user.Email != "" {
		curUser.Email = user.Email
	}
	if user.Username != "" {
		curUser.Username = user.Username
	}

	r.storage.users[userID] = curUser

	return curUser, nil
}
