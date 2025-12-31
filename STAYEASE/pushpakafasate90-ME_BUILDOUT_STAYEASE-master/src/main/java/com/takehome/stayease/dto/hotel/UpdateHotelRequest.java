package com.takehome.stayease.dto.hotel;

import jakarta.validation.constraints.Min;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UpdateHotelRequest {
    private String name;
    private String location;
    private String description;
    @Min(0)
    private Integer availableRooms;
}
