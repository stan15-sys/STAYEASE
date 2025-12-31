package com.takehome.stayease.dto.booking;

import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import java.time.LocalDate;

@Getter
@Setter
public class CreateBookingRequest {
    @NotNull
    @Future
    private LocalDate checkInDate;
    @NotNull
    private LocalDate checkOutDate;
}
