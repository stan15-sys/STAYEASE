package com.takehome.stayease.service;

import com.takehome.stayease.dto.auth.LoginRequest;
import com.takehome.stayease.dto.auth.RegisterRequest;
import com.takehome.stayease.entity.User;

public interface UserService {
    User registeUser(RegisterRequest request);
    User authenticateUser(LoginRequest request);
}
