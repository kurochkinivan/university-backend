package local

import (
	"context"
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
	if _, ok := r.storage.users.Load(userID); !ok {
		return false
	}
	return true
}

func (r *UserRepository) GetAll(ctx context.Context) ([]*entity.User, error) {
	var users []*entity.User
	r.storage.users.Range(func(_, u any) bool {
		users = append(users, u.(*entity.User))
		return true
	})

	sort.Slice(users, func(i, j int) bool {
		return users[i].ID < users[j].ID
	})

	return users, nil
}

func (r *UserRepository) Create(ctx context.Context, user *entity.User) (*entity.User, error) {
	r.storage.lastID++
	user.ID = r.storage.lastID
	r.storage.users.Store(user.ID, user)
	return user, nil
}

func (r *UserRepository) Delete(ctx context.Context, userID int) error {
	if !r.Exists(ctx, userID) {
		return repository.ErrNotFound
	}

	r.storage.users.Delete(userID)
	return nil
}

func (r *UserRepository) Update(ctx context.Context, userID int, user *entity.User) (*entity.User, error) {
	if !r.Exists(ctx, userID) {
		return nil, repository.ErrNotFound
	}

	user.ID = userID
	r.storage.users.Store(userID, user)

	return user, nil
}

func (r *UserRepository) Patch(ctx context.Context, userID int, user *entity.User) (*entity.User, error) {
	exists := r.Exists(ctx, userID)
	if !exists {
		return nil, repository.ErrNotFound
	}

	u, _ := r.storage.users.Load(userID)
	curUser := u.(*entity.User)

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

	r.storage.users.Store(userID, curUser)

	return curUser, nil
}
