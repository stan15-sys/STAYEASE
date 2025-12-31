package com.takehome.stayease.service;

import com.takehome.stayease.dto.booking.CreateBookingRequest;
import com.takehome.stayease.entity.Booking;
import com.takehome.stayease.entity.User;

public interface BookingService {
    Booking createBooking(Long hotelId, CreateBookingRequest request, User user);
    Booking getBookingById(Long BookingId);
    void cancelBooking(Long bookingId);
}
