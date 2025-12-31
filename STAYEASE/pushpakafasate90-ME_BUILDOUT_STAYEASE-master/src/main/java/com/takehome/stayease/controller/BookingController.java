package com.takehome.stayease.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import com.takehome.stayease.dto.booking.BookingResponse;
import com.takehome.stayease.dto.booking.CreateBookingRequest;
import com.takehome.stayease.entity.Booking;
import com.takehome.stayease.entity.User;
import com.takehome.stayease.security.CustomUserDetails;
import com.takehome.stayease.service.BookingService;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/bookings")
@RequiredArgsConstructor
public class BookingController {

    private final BookingService bookingService;
    private final ModelMapper modelMapper;

    @PostMapping("/{hotelId}")
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<BookingResponse> createBooking(@PathVariable Long hotelId,
            @Valid @RequestBody CreateBookingRequest request, Authentication authentication) {

        User user = ((CustomUserDetails) authentication.getPrincipal()).getUser();

        Booking booking = bookingService.createBooking(hotelId, request, user);

        BookingResponse response = new BookingResponse();
        // response.setBookingId(booking.getId());
        response.setBookingId(booking.getId());
        response.setHotelId(booking.getHotel().getId());
        response.setCheckInDate(booking.getCheckInDate());
        response.setCheckOutDate(booking.getCheckOutDate());

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{bookingId}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<BookingResponse> getBooking(@PathVariable Long bookingId) {

        Booking booking = bookingService.getBookingById(bookingId);

        BookingResponse response = new BookingResponse();
        response.setBookingId(booking.getId());
        response.setHotelId(booking.getHotel().getId());
        response.setCheckInDate(booking.getCheckInDate());
        response.setCheckOutDate(booking.getCheckOutDate());

        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{bookingId}")
    @PreAuthorize("hasRole('HOTEL_MANAGER')")
    public ResponseEntity<Void> cancelBooking(@PathVariable Long bookingId) {

        bookingService.cancelBooking(bookingId);
        return ResponseEntity.noContent().build();
    }
}
