package com.takehome.stayease.service.Impl;

import lombok.RequiredArgsConstructor;
import com.takehome.stayease.dto.auth.LoginRequest;
import com.takehome.stayease.dto.auth.RegisterRequest;
import com.takehome.stayease.entity.Role;
import com.takehome.stayease.entity.User;
import com.takehome.stayease.repository.UserRepository;
import com.takehome.stayease.service.UserService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService{

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User registeUser(RegisterRequest request) {

        if(userRepository.existsByEmail(request.getEmail())){
            throw new RuntimeException("User already exists");
        }

        Role role = Role.USER;

        if(request.getRole() != null){
            role = Role.valueOf(request.getRole());
        }

        User user = User.builder()
            .email(request.getEmail())
            .password(passwordEncoder.encode(request.getPassword()))
            .firstName(request.getFirstName())
            .lastName(request.getLastName())
            .role(role)
            .build();

        return userRepository.save(user);
    }

    @Override
    public User authenticateUser(LoginRequest request) {

        User user = userRepository.findByEmail(request.getEmail())
                    .orElseThrow(() -> new RuntimeException("Invalid credentials"));
        if(!passwordEncoder.matches(request.getPassword(), user.getPassword())){
            throw new RuntimeException("Invalid credentials");
        }

        return user;
    }
    
}
