package com.takehome.stayease.service;

import java.util.List;
import com.takehome.stayease.dto.hotel.CreateHotelRequest;
import com.takehome.stayease.dto.hotel.UpdateHotelRequest;
import com.takehome.stayease.entity.Hotel;

public interface HotelService {
    Hotel createHotel(CreateHotelRequest request);
    List<Hotel> getAllHotels();
    Hotel updateHotel(Long hotelId, UpdateHotelRequest request);
    void deleteHotel(Long hotelId);
}
