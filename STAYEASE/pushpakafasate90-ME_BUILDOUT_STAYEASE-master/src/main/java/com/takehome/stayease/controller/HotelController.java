package com.takehome.stayease.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;
import com.takehome.stayease.dto.hotel.CreateHotelRequest;
import com.takehome.stayease.dto.hotel.HotelResponse;
import com.takehome.stayease.dto.hotel.UpdateHotelRequest;
import com.takehome.stayease.entity.Hotel;
import com.takehome.stayease.service.HotelService;

@RestController
@RequestMapping("/api/hotels")
@RequiredArgsConstructor
public class HotelController {

    private final HotelService hotelService;
    private final ModelMapper modelMapper;

    @GetMapping
    public ResponseEntity<List<HotelResponse>> getAllHotels() {

        List<HotelResponse> response = hotelService.getAllHotels()
                .stream()
                .map(hotel -> modelMapper.map(hotel, HotelResponse.class))
                .collect(Collectors.toList());

        return ResponseEntity.ok(response);
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<HotelResponse> createHotel(
            @Valid @RequestBody CreateHotelRequest request) {

        Hotel hotel = hotelService.createHotel(request);
        HotelResponse response = modelMapper.map(hotel, HotelResponse.class);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @PutMapping("/{hotelId}")
    @PreAuthorize("hasRole('HOTEL_MANAGER')")
    public ResponseEntity<HotelResponse> updateHotel(
            @PathVariable Long hotelId,
            @Valid @RequestBody UpdateHotelRequest request) {

        Hotel hotel = hotelService.updateHotel(hotelId, request);
        HotelResponse response = modelMapper.map(hotel, HotelResponse.class);

        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{hotelId}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deleteHotel(@PathVariable Long hotelId) {

        hotelService.deleteHotel(hotelId);
        return ResponseEntity.noContent().build();
    }
}