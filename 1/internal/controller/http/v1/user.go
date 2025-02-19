package v1

import (
	"context"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"net/http"
	"strconv"

	"github.com/julienschmidt/httprouter"
	"github.com/kurochkinivan/university-backend-1/internal/entity"
)

type UserUseCase interface {
	GetAll(ctx context.Context) ([]*entity.User, error)
	Create(ctx context.Context, user *entity.User) (*entity.User, error)
	Delete(ctx context.Context, userID int) error
	Update(ctx context.Context, userID int, user *entity.User) (*entity.User, error)
}

type UserHandler struct {
	u UserUseCase
}

func NewUserHandler(u UserUseCase) Handler {
	return &UserHandler{
		u: u,
	}
}

func (c *UserHandler) Register(r *httprouter.Router) {
	r.GET("/v1/users-query", c.getUsersQuery)
	r.GET("/v1/users-header", c.getUsersHeader)
	r.POST("/v1/users", c.createUser)
	r.DELETE("/v1/users/:id", c.deleteUser)
	r.PUT("/v1/users/:id", c.updateUser)
}

type (
	getUsersResponse struct {
		Users []*entity.User `json:"users"`
		Total int            `json:"total"`
	}
)

func mapUsersToGetUsersResp(users []*entity.User) getUsersResponse {
	return getUsersResponse{
		Users: users,
		Total: len(users),
	}
}

func (c *UserHandler) getUsersQuery(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	users, err := c.u.GetAll(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	format := r.URL.Query().Get("format")
	var resp []byte
	switch format {
	case "json", "":
		resp, err = json.Marshal(mapUsersToGetUsersResp(users))
	case "xml":
		resp, err = xml.Marshal(mapUsersToGetUsersResp(users))
	default:
		err = fmt.Errorf("unknown format: %s", format)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err != nil {
		http.Error(w, fmt.Sprintf("failed to serialize resp, err: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", fmt.Sprintf("application/%s", format))
	w.Write(resp)
}

func (c *UserHandler) getUsersHeader(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	users, err := c.u.GetAll(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	accept := r.Header.Get("Accept")
	var resp []byte
	switch accept {
	case "application/json":
		resp, err = json.Marshal(mapUsersToGetUsersResp(users))
	case "application/xml":
		resp, err = xml.Marshal(mapUsersToGetUsersResp(users))
	default:
		err = fmt.Errorf("unknown header accept: %s", accept)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err != nil {
		http.Error(w, fmt.Sprintf("failed to serialize resp, err: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", accept)
	w.Write(resp)
}

type (
	createUserRequest struct {
		Name     string `json:"name"`
		Phone    string `json:"phone"`
		Birthday string `json:"birthday"`
		Email    string `json:"email"`
		Username string `json:"username"`
	}

	createUserResponse struct {
		ID       int    `json:"id"`
		Name     string `json:"name"`
		Phone    string `json:"phone"`
		Birthday string `json:"birthday"`
		Email    string `json:"email"`
		Username string `json:"username"`
	}
)

func mapCreateUserReqToUser(req createUserRequest) *entity.User {
	return &entity.User{
		Name:     req.Name,
		Phone:    req.Phone,
		Birthday: req.Birthday,
		Email:    req.Email,
		Username: req.Username,
	}
}

func mapUserToCreateUserResp(user *entity.User) createUserResponse {
	return createUserResponse{
		ID:       user.ID,
		Name:     user.Name,
		Phone:    user.Phone,
		Birthday: user.Birthday,
		Email:    user.Email,
		Username: user.Username,
	}
}

func (c *UserHandler) createUser(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	var req createUserRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to deserialize data, err: %v", err), http.StatusBadRequest)
	}
	defer r.Body.Close()

	user, err := c.u.Create(r.Context(), mapCreateUserReqToUser(req))
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to create user, err: %v", err), http.StatusInternalServerError)
		return
	}

	resp, err := json.Marshal(mapUserToCreateUserResp(user))
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to serialize data, err: %v", err), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Header().Set("Content-Type", "application/json")
	w.Write(resp)
}

func (c *UserHandler) deleteUser(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	userID, err := strconv.Atoi(p.ByName("id"))
	if err != nil {
		http.Error(w, "invalid user id, must be a numeric value", http.StatusBadRequest)
		return
	}

	err = c.u.Delete(r.Context(), userID)
	if err != nil {
		http.Error(w, fmt.Sprintf("faield to delete user, err: %v", err), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

type (
	updateUserRequest struct {
		Name     string `json:"name"`
		Phone    string `json:"phone"`
		Birthday string `json:"birthday"`
		Email    string `json:"email"`
		Username string `json:"username"`
	}
)

func mapUpdateUserReqToUser(req updateUserRequest) *entity.User {
	return &entity.User{
		Name:     req.Name,
		Phone:    req.Phone,
		Birthday: req.Birthday,
		Email:    req.Email,
		Username: req.Username,
	}
}

func (c *UserHandler) updateUser(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	w.Header().Set("Content-Type", "application/json")

	userID, err := strconv.Atoi(p.ByName("id"))
	if err != nil {
		http.Error(w, "invalid user id, must be a numeric value", http.StatusBadRequest)
		return
	}

	var req updateUserRequest
	err = json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "failed to desirialize data", http.StatusBadRequest)
		return
	}

	user, err := c.u.Update(r.Context(), userID, mapUpdateUserReqToUser(req))
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to update user, err: %v", err), http.StatusInternalServerError)
		return
	}

	resp, err := json.Marshal(user)
	if err != nil {
		http.Error(w, fmt.Sprintf("failed to serialize data, err: %v", err), http.StatusInternalServerError)
		return
	}

	w.Write(resp)
}
