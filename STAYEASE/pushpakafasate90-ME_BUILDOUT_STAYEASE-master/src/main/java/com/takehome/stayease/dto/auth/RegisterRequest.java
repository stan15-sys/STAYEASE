package com.takehome.stayease.dto.auth;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class RegisterRequest {
    @Email
    @NotBlank
    private String email;
    @NotBlank
    @Pattern(
        regexp = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&]).{8,}$",
        message = "Password must be at least 8 characters, contain uppercase, lowercase, number, and special character"
    )
    private String password;
    @NotBlank
    private String firstName;
    @NotBlank
    private String lastName;
    private String role;
}
