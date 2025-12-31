package com.takehome.stayease.service.Impl;

import lombok.RequiredArgsConstructor;
import java.time.LocalDate;
import com.takehome.stayease.dto.booking.CreateBookingRequest;
import com.takehome.stayease.entity.Booking;
import com.takehome.stayease.entity.Hotel;
import com.takehome.stayease.entity.User;
import com.takehome.stayease.repository.BookingRepository;
import com.takehome.stayease.repository.HotelRepository;
import com.takehome.stayease.service.BookingService;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class BookingServiceImpl implements BookingService {

    private final BookingRepository bookingRepository;
    private final HotelRepository hotelRepository;

    @Override
    public Booking createBooking(Long hotelId, CreateBookingRequest request, User user) {

        Hotel hotel = hotelRepository.findById(hotelId)
                .orElseThrow(() -> new RuntimeException("Hotel not found"));

        if (hotel.getAvailableRooms() <= 0) {
            throw new RuntimeException("No rooms available");
        }

        LocalDate checkIn = request.getCheckInDate();
        LocalDate checkOut = request.getCheckOutDate();

        if (!checkOut.isAfter(checkIn)) {
            throw new RuntimeException("Check-out date must be after check-in date");
        }

        hotel.setAvailableRooms(hotel.getAvailableRooms() - 1);
        hotelRepository.save(hotel);

        Booking booking = Booking.builder().hotel(hotel).user(user).checkInDate(checkIn)
                .checkOutDate(checkOut).build();

        return bookingRepository.save(booking);
    }

    @Override
    public Booking getBookingById(Long BookingId) {
        return bookingRepository.findById(BookingId)
                .orElseThrow(() -> new RuntimeException("Booking not found"));
    }

    @Override
    public void cancelBooking(Long bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new RuntimeException("Booking not found"));

        Hotel hotel = booking.getHotel();
        hotel.setAvailableRooms(hotel.getAvailableRooms() + 1);
        hotelRepository.save(hotel);

        bookingRepository.delete(booking);
    }

}
