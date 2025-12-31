package com.takehome.stayease.dto.hotel;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CreateHotelRequest {

    @NotBlank
    private String name;

    @NotBlank
    private String location;

    private String description;

    @NotNull
    private Integer availableRooms;
}
